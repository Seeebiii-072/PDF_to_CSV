# 📄 PDF_to_CSV (Employee Data Extraction using OCR)

## 🚀 Overview
PDF_to_CSV is an OCR-based Python project that extracts structured employee information from image-based PDF files (scanned documents or screenshots) and converts it into a clean CSV format.

It extracts:
- 👤 Full Name  
- 💼 Job Title  
- 🏢 Organization  

---

## 🧠 How It Works (Technique)
We used a **layout-aware OCR pipeline**:

1. PDF pages are converted into images using `pdf2image`
2. OCR extracts text + positional data using `pytesseract`
3. Text is grouped using (x, y) coordinates
4. Rule-based parsing extracts structured fields:
   - Full Name
   - Job Title
   - Organization
5. Final cleaned output is saved into CSV format

---

## ⚙️ Features
- PDF to image conversion
- OCR-based text extraction
- Position-based row reconstruction
- Noise handling & cleaning
- CSV export (structured output)

---

## 📚 Libraries Used
- pytesseract  
- pdf2image  
- OpenCV (cv2)  
- NumPy  
- re (regex)  
- tqdm  

---

## 📂 Output Format

| Full Name | Job Title | Organization |
|-----------|----------|--------------|
| John Doe  | Engineer | ABC Corp     |

---

## ▶️ How to Run

```bash
python extract.py --pdf input.pdf --output output.csv
