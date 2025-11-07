# 🕵️ NDA Redactor — Automated Document Sanitizer

## Overview
**NDA Redactor** is a Python utility that automatically removes sensitive information from NDA documents in `.docx` and `.pdf` formats.  
It identifies and redacts **names, dates, fees, emails, and phone numbers**, while logging file hashes to ensure tamper-proof integrity.

---

## ✨ Features
- 🔒 Regex-based detection and replacement of:
  - Dates (MM/DD/YYYY, YYYY-MM-DD, textual, and European formats)
  - Fees and currency references ($, €, USD, dollars, euros)
  - Emails and phone numbers (U.S. + international)
  - Client names (custom list input)
- 🧠 Accent- and apostrophe-insensitive redaction
- 🧾 SHA-256 hashing for before/after integrity comparison
- 📊 Console summary of all redactions performed
- 💡 Simple CLI: works by drag-and-dropping a file into your terminal

[![Try it FREE ⚡](https://img.shields.io/badge/Try%20it%20FREE%20in%20browser-00bf63?style=for-the-badge&logo=github)](https://git.new/n0tserp/NDA-Redactor)
---

## 🧰 Requirements
- Python 3.9+
- `python-docx`
- `PyPDF2`

Install dependencies:
```bash
pip install python-docx PyPDF2
