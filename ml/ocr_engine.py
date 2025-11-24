# ml/ocr_engine.py
import re
import tempfile
import os
from pathlib import Path
from typing import Dict, Any, Optional

from PIL import Image, ImageOps, ImageFilter
import pytesseract

# Optionnel: support PDF -> images
try:
    from pdf2image import convert_from_path
    PDF2IMAGE_AVAILABLE = True
except Exception:
    PDF2IMAGE_AVAILABLE = False

# --- Helpers de nettoyage image ---
def preprocess_image(img: Image.Image) -> Image.Image:
    """
    Applique transformations simples pour améliorer OCR :
    - conversion en niveau de gris
    - augmentation contraste, léger filtre
    - inversion si nécessaire
    """
    img = img.convert("L")  # grayscale
    img = ImageOps.autocontrast(img)
    img = img.filter(ImageFilter.MedianFilter(size=3))
    return img

# --- Extraction texte brut depuis une image path ---
def image_to_text(image_path: str) -> str:
    img = Image.open(image_path)
    img = preprocess_image(img)
    # pytesseract configuration: OCR en français et anglais (si dispo)
    try:
        text = pytesseract.image_to_string(img, lang='fra+eng')
    except Exception:
        text = pytesseract.image_to_string(img)
    return text

# --- Extraction depuis PDF (converti en images) ---
def pdf_to_text(pdf_path: str, dpi: int = 200) -> str:
    if not PDF2IMAGE_AVAILABLE:
        raise RuntimeError("pdf2image not available. Install poppler and pdf2image to process PDFs.")
    pages = convert_from_path(pdf_path, dpi=dpi)
    texts = []
    for page in pages:
        page = preprocess_image(page)
        texts.append(pytesseract.image_to_string(page, lang='fra+eng'))
    return "\n".join(texts)

# --- Regex parsing basique ---
DATE_PATTERNS = [
    r'(\d{1,2}[\/\-\.\s]\d{1,2}[\/\-\.\s]\d{2,4})',   # 01/02/2024 or 1-2-24
    r'(\d{4}[\/\-\.\s]\d{1,2}[\/\-\.\s]\d{1,2})',     # 2024-02-01
]
AMOUNT_PATTERN = r'((?:\d{1,3}(?:[ \.\,]\d{3})+|\d+)(?:[\,\.]\d{1,2})?)'  # 1 234,56 or 1234.56
INVOICE_NUMBER_PATTERN = r'(?:Facture|Invoice|No[:\s]|N°|Numero|Numéro)[\s\:\-]*([A-Za-z0-9\-\/]+)'
SUPPLIER_LINE_PATTERN = r'(?:(Fournisseur|Supplier|Soci[eé]t[eé]|Raison sociale)[:\s\-]*)?(.{3,60})'

def find_first(patterns, text):
    for p in patterns:
        m = re.search(p, text, re.IGNORECASE)
        if m:
            return m.group(1)
    return None

def parse_amount_candidates(text: str) -> Optional[str]:
    # Cherche le montant total (on prend généralement le dernier montant avec motif € ou CFA)
    # Rechercher montants suivis de devise
    currency_markers = ['fcfa', 'cfa', 'xof', '€', 'eur', 'f cfa']
    matches = re.findall(AMOUNT_PATTERN, text)
    if not matches:
        return None
    # choix heuristique : retourner le dernier match qui est raisonnable
    candidate = matches[-1]
    # nettoyer : remplacer espace milliers
    cleaned = candidate.replace(' ', '').replace('\u202f', '')  # non-breaking space
    return cleaned

def extract_invoice_fields_from_text(text: str) -> Dict[str, Any]:
    # Normalize text
    txt = text.replace('\r', '\n')
    # invoice number
    inv = None
    m = re.search(INVOICE_NUMBER_PATTERN, txt, re.IGNORECASE)
    if m:
        inv = m.group(1).strip()
    # date
    date = find_first(DATE_PATTERNS, txt)
    # amount
    amount = parse_amount_candidates(txt)
    # supplier: heuristic - chercher les premières lignes qui ressemblent à un nom de société
    supplier = None
    lines = [l.strip() for l in txt.splitlines() if l.strip()]
    if lines:
        # parcourir premières 6 lignes pour trouver un nom plausible
        for ln in lines[:6]:
            # skip if line looks like address/phone (digits very long)
            if re.search(r'\d{6,}', ln):
                continue
            # skip if line contains "Facture" etc
            if re.search(r'facture|invoice|montant|total|date|tva', ln, re.IGNORECASE):
                continue
            # accept this as supplier candidate
            supplier = ln
            break

    return {
        'invoice_number': inv,
        'date': date,
        'amount': amount,
        'supplier': supplier,
        'raw_text_snippet': '\n'.join(lines[:20])
    }

# --- Public function principale ---
def extract_invoice_data(file_path: str) -> Dict[str, Any]:
    """
    Prend le chemin d'un fichier (image ou pdf) et retourne un dict:
    {
      'status': 'ok'|'error',
      'text': 'texte brute',
      'fields': {...}
    }
    """
    try:
        suffix = Path(file_path).suffix.lower()
        if suffix in ['.pdf']:
            text = pdf_to_text(file_path)
        else:
            text = image_to_text(file_path)
    except Exception as e:
        return {'status': 'error', 'error': str(e)}

    fields = extract_invoice_fields_from_text(text)
    return {'status': 'ok', 'text': text, 'fields': fields}
