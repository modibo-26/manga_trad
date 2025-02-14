import pytesseract
import cv2
import os

# 🔹 Vérification du chemin de Tesseract
tesseract_path = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
if os.path.exists(tesseract_path):
    pytesseract.pytesseract.tesseract_cmd = tesseract_path
    print(f"✅ Tesseract OCR détecté : {pytesseract.get_tesseract_version()}")
else:
    raise FileNotFoundError("❌ Tesseract OCR non trouvé ! Installez-le et ajoutez-le à votre PATH.")

def extract_text(image_path, bubbles):
    """
    Extrait le texte des bulles détectées avec Tesseract OCR.
    Args:
        image_path (str): Chemin de l'image.
        bubbles (list): Liste des coordonnées [x, y, w, h] en pixels.
    Returns:
        list: Liste des textes extraits (chaînes).
    """
    image = cv2.imread(image_path)
    if image is None:
        print(f"❌ Impossible de lire l'image {image_path} avec OpenCV.")
        return []

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    extracted_texts = []

    for bubble in bubbles:
        try:
            x, y, w, h = map(int, bubble)
            # Sécuriser le crop (ne pas dépasser l'image)
            x1 = max(0, x)
            y1 = max(0, y)
            x2 = min(x + w, gray.shape[1])
            y2 = min(y + h, gray.shape[0])

            bubble_crop = gray[y1:y2, x1:x2]
            text = pytesseract.image_to_string(bubble_crop, lang="eng").strip()
            extracted_texts.append(text)
        except Exception as e:
            print(f"⚠️ Erreur OCR sur une bulle : {e}")
            extracted_texts.append("")

    return extracted_texts
