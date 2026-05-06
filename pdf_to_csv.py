# """
# ====================================================================
#    PRODUCTION AI PDF EMPLOYEE EXTRACTION PIPELINE (ENTERPRISE VERSION)
# ====================================================================
# """

# import os
# import re
# import csv
# import cv2
# import pytesseract
# import numpy as np
# from pdf2image import convert_from_path
# import argparse
# from tqdm import tqdm
# from difflib import SequenceMatcher


# # ========================= CONFIG =========================
# TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
# POPPLER_PATH = r"C:\Users\Haseeb Ishtiaq\Downloads\poppler-26.02.0\Library\bin"

# pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH


# # ========================= MODULE 1: PDF ENGINE =========================
# def pdf_to_images(pdf_path, dpi=300):
#     return convert_from_path(
#         pdf_path,
#         dpi=dpi,
#         poppler_path=POPPLER_PATH
#     )


# # ========================= MODULE 2: IMAGE PREPROCESSING =========================
# def preprocess_image(pil_img):
#     img = np.array(pil_img)

#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#     gray = cv2.bilateralFilter(gray, 9, 75, 75)

#     thresh = cv2.adaptiveThreshold(
#         gray, 255,
#         cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
#         cv2.THRESH_BINARY,
#         31, 2
#     )

#     return thresh


# # ========================= MODULE 3: OCR =========================
# def run_ocr(image):
#     config = r'--oem 3 --psm 6'
#     return pytesseract.image_to_string(image, config=config)


# # ========================= MODULE 4: CLEANING =========================
# def is_noise(line):
#     noise_keywords = [
#         "laserfiche", "attendees", "home", "contact",
#         "search", "filter", "sort", "exhibition", "logo"
#     ]

#     l = line.lower()

#     if any(k in l for k in noise_keywords):
#         return True

#     if len(line.strip()) < 2:
#         return True

#     return False


# def clean_text(text):
#     lines = text.split("\n")
#     cleaned = []

#     for line in lines:
#         line = line.strip()

#         if is_noise(line):
#             continue

#         line = re.sub(r"^\d+\s+", "", line)
#         line = re.sub(r"[^\w\s,.-]", "", line)

#         if len(line) > 2:
#             cleaned.append(line)

#     return cleaned


# # ========================= MODULE 5: SMART DETECTION =========================
# def is_name(text):
#     if len(text) < 2:
#         return False

#     if any(char.isdigit() for char in text):
#         return False

#     words = text.split()

#     # FIX: allow realistic names
#     if len(words) > 6:
#         return False

#     return True


# def is_job(text):
#     keywords = [
#         "engineer", "developer", "manager", "analyst",
#         "designer", "lead", "architect", "consultant",
#         "administrator", "director", "specialist",
#         "coordinator", "supervisor"
#     ]
#     return any(k in text.lower() for k in keywords)


# def is_org(text):
#     keywords = [
#         "inc", "ltd", "systems", "solutions",
#         "technologies", "company", "university",
#         "city", "college", "group", "services",
#         "school", "hospital"
#     ]
#     return any(k in text.lower() for k in keywords)


# # ========================= MODULE 6: ENTERPRISE PARSER (FIXED CORE) =========================
# def parse_records(lines):
#     records = []
#     i = 0

#     while i < len(lines):

#         name = lines[i].strip()
#         job = ""
#         org = ""

#         # skip invalid noise
#         if not is_name(name):
#             i += 1
#             continue

#         # look ahead safely
#         l2 = lines[i + 1].strip() if i + 1 < len(lines) else ""
#         l3 = lines[i + 2].strip() if i + 2 < len(lines) else ""

#         # CASE 1: job + org in same line
#         if "," in l2:
#             parts = [p.strip() for p in l2.split(",")]
#             job = parts[0]
#             org = parts[1] if len(parts) > 1 else ""

#             i += 2

#         # CASE 2: job then org
#         elif is_job(l2):
#             job = l2

#             if is_org(l3):
#                 org = l3
#                 i += 3
#             else:
#                 i += 2

#         # CASE 3: only org
#         elif is_org(l2):
#             org = l2
#             i += 2

#         # CASE 4: NOTHING FOUND (IMPORTANT FIX)
#         else:
#             i += 1

#         # IMPORTANT: NEVER SKIP RECORD
#         records.append({
#             "Full Name": name,
#             "Job Title": job,
#             "Organization": org
#         })

#     return records


# # ========================= MODULE 7: DEDUP =========================
# def is_duplicate(a, b):
#     return SequenceMatcher(None, a, b).ratio() > 0.90


# def deduplicate(records):
#     unique = []

#     for r in records:
#         if not any(is_duplicate(r["Full Name"], u["Full Name"]) for u in unique):
#             unique.append(r)

#     return unique


# # ========================= PIPELINE =========================
# def process_pdf(pdf_path):
#     print("[INFO] Loading PDF...")

#     images = pdf_to_images(pdf_path)

#     all_records = []

#     for page in tqdm(images, desc="Processing Pages"):

#         img = preprocess_image(page)

#         text = run_ocr(img)

#         lines = clean_text(text)

#         records = parse_records(lines)

#         all_records.extend(records)

#     return deduplicate(all_records)


# # ========================= OUTPUT =========================
# def save_csv(records, output_file):
#     print(f"[INFO] Saving → {output_file}")

#     with open(output_file, "w", newline="", encoding="utf-8") as f:
#         writer = csv.DictWriter(
#             f,
#             fieldnames=["Full Name", "Job Title", "Organization"]
#         )

#         writer.writeheader()

#         for r in records:
#             writer.writerow(r)

#     print("[SUCCESS] Done!")


# # ========================= MAIN =========================
# def main():
#     parser = argparse.ArgumentParser()
#     parser.add_argument("--pdf", required=True)
#     parser.add_argument("--output", default="output.csv")

#     args = parser.parse_args()

#     records = process_pdf(args.pdf)

#     save_csv(records, args.output)


# if __name__ == "__main__":
#     main()


"""
====================================================================
   PRODUCTION AI PDF EMPLOYEE EXTRACTION PIPELINE (ENTERPRISE FIXED)
====================================================================
"""

import os
import re
import csv
import cv2
import pytesseract
import numpy as np
from pdf2image import convert_from_path
import argparse
from tqdm import tqdm
from difflib import SequenceMatcher


# ========================= CONFIG =========================
TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
POPPLER_PATH = r"C:\Users\Haseeb Ishtiaq\Downloads\poppler-26.02.0\Library\bin"

pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH


# ========================= MODULE 1: PDF ENGINE =========================
def pdf_to_images(pdf_path, dpi=250):
    return convert_from_path(
        pdf_path,
        dpi=dpi,
        poppler_path=POPPLER_PATH
    )


# ========================= MODULE 2: IMAGE PREPROCESSING =========================
def preprocess_image(pil_img):
    img = np.array(pil_img)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    gray = cv2.bilateralFilter(gray, 9, 75, 75)

    thresh = cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31, 2
    )

    return thresh


# ========================= MODULE 3: OCR =========================
def run_ocr(image):
    config = r'--oem 3 --psm 6'
    return pytesseract.image_to_string(image, config=config)


# ========================= MODULE 4: CLEANING =========================
def is_noise(line):
    noise_keywords = [
        "laserfiche", "attendees", "home", "contact",
        "search", "filter", "sort", "exhibition", "logo"
    ]

    l = line.lower()

    if any(k in l for k in noise_keywords):
        return True

    if len(line.strip()) < 2:
        return True

    return False


def clean_text(text):
    lines = text.split("\n")
    cleaned = []

    for line in lines:
        line = line.strip()

        if is_noise(line):
            continue

        line = re.sub(r"^\d+\s+", "", line)
        line = re.sub(r"[^\w\s,.-]", "", line)

        if len(line) > 2:
            cleaned.append(line)

    return cleaned


# ========================= MODULE 5: SMART NAME FIX (IMPORTANT UPGRADE) =========================
def fix_name(text):
    if not text:
        return ""

    # remove leading junk like "eer," "és"
    text = re.sub(r"^[^a-zA-Z]+", "", text)

    # remove weird characters
    text = re.sub(r"[^a-zA-Z\s\-']", "", text)

    words = text.split()

    if len(words) < 2 or len(words) > 6:
        return ""

    return " ".join(words).strip()


# ========================= MODULE 6: DETECTION =========================
def is_job(text):
    keywords = [
        "engineer", "developer", "manager", "analyst",
        "designer", "lead", "architect", "consultant",
        "administrator", "director", "specialist",
        "coordinator", "supervisor", "account", "support"
    ]
    return any(k in text.lower() for k in keywords)


def is_org(text):
    keywords = [
        "inc", "ltd", "systems", "solutions",
        "technologies", "company", "university",
        "city", "college", "group", "services",
        "school", "hospital", "council"
    ]
    return any(k in text.lower() for k in keywords)


# ========================= MODULE 7: ENTERPRISE PARSER (FIXED CORE) =========================
def parse_records(lines):
    records = []
    i = 0

    while i < len(lines):

        raw_name = lines[i].strip()
        name = fix_name(raw_name)

        # IMPORTANT: never skip valid recovery cases
        if not name:
            i += 1
            continue

        job = ""
        org = ""

        l2 = lines[i + 1].strip() if i + 1 < len(lines) else ""
        l3 = lines[i + 2].strip() if i + 2 < len(lines) else ""

        # CASE 1: job + org combined
        if "," in l2:
            parts = [p.strip() for p in l2.split(",")]
            job = parts[0] if len(parts) > 0 else ""
            org = parts[1] if len(parts) > 1 else ""
            i += 2

        # CASE 2: job then org
        elif is_job(l2):
            job = l2

            if is_org(l3):
                org = l3
                i += 3
            else:
                i += 2

        # CASE 3: org only
        elif is_org(l2):
            org = l2
            i += 2

        # CASE 4: fallback safe mode (DO NOT LOSE DATA)
        else:
            i += 1

        records.append({
            "Full Name": name,
            "Job Title": job,
            "Organization": org
        })

    return records


# ========================= MODULE 8: DEDUP =========================
def is_duplicate(a, b):
    return SequenceMatcher(None, a, b).ratio() > 0.90


def deduplicate(records):
    unique = []

    for r in records:
        if not any(is_duplicate(r["Full Name"], u["Full Name"]) for u in unique):
            unique.append(r)

    return unique


# ========================= PIPELINE =========================
def process_pdf(pdf_path):
    print("[INFO] Loading PDF...")

    images = pdf_to_images(pdf_path)

    all_records = []

    for page in tqdm(images, desc="Processing Pages"):

        img = preprocess_image(page)

        text = run_ocr(img)

        lines = clean_text(text)

        records = parse_records(lines)

        all_records.extend(records)

    return deduplicate(all_records)


# ========================= OUTPUT =========================
def save_csv(records, output_file):
    print(f"[INFO] Saving → {output_file}")

    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["Full Name", "Job Title", "Organization"]
        )

        writer.writeheader()

        for r in records:
            writer.writerow(r)

    print("[SUCCESS] Done!")


# ========================= MAIN =========================
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pdf", required=True)
    parser.add_argument("--output", default="output.csv")

    args = parser.parse_args()

    records = process_pdf(args.pdf)

    save_csv(records, args.output)


if __name__ == "__main__":
    main()