# utils/pdf_reader.py

import pdfplumber
import PyPDF2
import fitz  # pymupdf
from PIL import Image

import io
import os

# Set tesseract path for Windows


def extract_text_normal(uploaded_file):
    """Try normal text extraction first"""
    text = ""
    try:
        with pdfplumber.open(uploaded_file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        if text.strip():
            return text.strip()
    except Exception as e:
        print(f"pdfplumber failed: {e}")

    try:
        uploaded_file.seek(0)
        reader = PyPDF2.PdfReader(uploaded_file)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        if text.strip():
            return text.strip()
    except Exception as e:
        print(f"PyPDF2 failed: {e}")

    return ""

def extract_text_ocr(uploaded_file):
    """Use OCR for scanned/image PDFs"""
    text = ""
    try:
        uploaded_file.seek(0)
        pdf_bytes = uploaded_file.read()
        
        # Open PDF with pymupdf
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            
            # Convert page to image
            mat = fitz.Matrix(2, 2)  # 2x zoom for better quality
            pix = page.get_pixmap(matrix=mat)
            img_bytes = pix.tobytes("png")
            
            # Convert to PIL Image
            img = Image.open(io.BytesIO(img_bytes))
            
            # OCR the image
            page_text = pytesseract.image_to_string(img)
            text += page_text + "\n"
        
        doc.close()
        return text.strip()
        
    except Exception as e:
        print(f"OCR failed: {e}")
        return ""

def extract_text(uploaded_file):
    """Main function - tries normal first, then OCR"""
    
    # Try normal extraction first
    text = extract_text_normal(uploaded_file)
    
    # If normal extraction got good text, return it
    if text and len(text) > 50:
        print(f"✅ Normal extraction worked: {len(text)} chars")
        return text
    
    # Otherwise use OCR
    print("🔄 Trying OCR extraction...")
    text = extract_text_ocr(uploaded_file)
    
    if text and len(text) > 50:
        print(f"✅ OCR extraction worked: {len(text)} chars")
        return text
    

    return ""
