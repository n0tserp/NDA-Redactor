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

[![Run NDA Redactor](https://img.shields.io/badge/Run%20Demo-NOW-brightgreen?style=for-the-badge&logo=python)](https://github.com/codespaces/new?repo=n0tserp/NDA-Redactor&ref=main&machine=basicLinux)

Click above → GitHub boots a free Linux box → run `python nda_redactor.py your_file.docx` and watch it fly!
---

## 🧰 Requirements
- Python 3.9+
- `python-docx`
- `PyPDF2`

Install dependencies:
```bash
pip install python-docx PyPDF2
