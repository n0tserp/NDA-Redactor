import os
import re
import hashlib
import unicodedata
from collections import Counter
from docx import Document
import PyPDF2

# --- FILE HASHING ---
def compute_hash(file_path):
    sha256 = hashlib.sha256()
    with open(file_path, 'rb') as f:
        while chunk := f.read(4096):
            sha256.update(chunk)
    return sha256.hexdigest()

# --- TEXT EXTRACTION ---
def extract_from_docx(file_path):
    doc = Document(file_path)
    full_text = [para.text for para in doc.paragraphs]
    return '\n'.join(full_text)

def extract_from_pdf(file_path):
    full_text = []
    with open(file_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            full_text.append(page.extract_text())
    return '\n'.join(full_text)

# --- REDACTION ENGINE ---
def redact_text(text, client_names):
    """
    Redacts sensitive information such as dates, fees, emails, phone numbers,
    and client names from the provided text.
    Automatically normalizes accented characters and apostrophes for robust matching.
    """

    # Normalize accents and apostrophes
    def normalize(s):
        s = unicodedata.normalize('NFD', s)
        s = ''.join(c for c in s if unicodedata.category(c) != 'Mn')
        s = s.replace("’", "'").replace("‘", "'")
        return s

    normalized_text = normalize(text)

    # Regex patterns
    date_pattern = (
        r'\b\d{1,2}/\d{1,2}/\d{4}\b|'              # 12/06/2025
        r'\b\d{4}-\d{1,2}-\d{1,2}\b|'              # 2025-12-06
        r'\b\d{1,2}/\d{1,2}/\d{2}\b|'              # 12/06/25
        r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{1,2}, \d{4}\b|'  # Dec 6, 2025
        r'\b\d{1,2} (?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{4}\b'    # 6 Dec 2025
    )

    fee_pattern = (
        r'(?:\$|€|\bUSD\b|\bdollars\b|\beuros\b)\s*\d+(?:,\d{3})*(?:\.\d{2})?'
        r'|\d+(?:,\d{3})*(?:\.\d{2})?\s*(?:USD|dollars|euros)'
        r'|\b\d+\.?\d*%?\s*(?:of|fee|deposit|retainer|cap|bonus|payment|profit)'
    )

    email_pattern = r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}'

    phone_pattern = (
        r'(?:(?:\+?\d{1,3}[-.\s]?)?'               # +1, +44
        r'(?:\(?\d{3}\)?[-.\s]?)?'                 # (305), 305-
        r'\d{3}[-.\s]?\d{4})'                      # 555-0199
    )

    # Redact patterns
    normalized_text = re.sub(date_pattern, '[REDACTED_DATE]', normalized_text, flags=re.IGNORECASE)
    normalized_text = re.sub(fee_pattern, '[REDACTED_FEE]', normalized_text, flags=re.IGNORECASE)
    normalized_text = re.sub(email_pattern, '[REDACTED_EMAIL]', normalized_text, flags=re.IGNORECASE)
    normalized_text = re.sub(phone_pattern, '[REDACTED_PHONE]', normalized_text, flags=re.IGNORECASE)

    # Redact client names (accent- and apostrophe-insensitive)
    normalized_names = [normalize(n).lower() for n in client_names]
    tokens = re.findall(r'\b[\w\'’]+\b', normalized_text)
    for token in set(tokens):
        if normalize(token).lower() in normalized_names:
            normalized_text = re.sub(rf'\b{re.escape(token)}\b', '[REDACTED_NAME]', normalized_text, flags=re.IGNORECASE)

    return normalized_text

# --- SUMMARY / AUDIT LOG ---
def summarize_redactions(redacted_text):
    """
    Counts how many redactions of each type occurred and prints a summary.
    """
    tags = re.findall(r'\[REDACTED_[A-Z]+\]', redacted_text)
    counts = Counter(tags)
    print("\n--- REDACTION SUMMARY ---")
    if not counts:
        print("No redactions were made.")
    else:
        for tag, count in counts.items():
            print(f"{tag}: {count}")
    print("--------------------------\n")

# --- MAIN PROGRAM ---
def main():
    file_path = input("Enter the full path to the NDA file (drag-and-drop into terminal): ").strip()
    
    if not os.path.exists(file_path):
        print("File not found! Try again.")
        return

    client_names_input = input("Enter client names to redact (comma-separated, e.g., Acme Corp,John Doe): ")
    client_names = [name.strip() for name in client_names_input.split(',') if name.strip()]

    # Extract text
    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.docx':
        original_text = extract_from_docx(file_path)
    elif ext == '.pdf':
        original_text = extract_from_pdf(file_path)
    else:
        print("Unsupported file type! Only .docx or .pdf.")
        return

    # Redact and output
    redacted_text = redact_text(original_text, client_names)
    output_path = os.path.join(os.path.dirname(file_path), 'redacted_nda.txt')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(redacted_text)
    print(f"Redacted file saved to: {output_path}")

    # Redaction summary
    summarize_redactions(redacted_text)

    # Hash logging
    original_hash = compute_hash(file_path)
    redacted_hash = compute_hash(output_path)
    log_content = f"Original Hash: {original_hash}\nRedacted Hash: {redacted_hash}\n"
    log_path = 'hashes.log'
    with open(log_path, 'a', encoding='utf-8') as log:
        log.write(log_content)
    print(f"Hashes logged to {log_path}. Compare to verify tamper-free redaction.")

if __name__ == "__main__":
    main()

