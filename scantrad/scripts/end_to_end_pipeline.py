# scripts/end_to_end_pipeline.py

from scripts.detect_bubbles import detect_bubbles
from ocr.extract_text import extract_text
from translation.translate_text import translate_text
from image_processing.replace_text import add_text_to_image

def process_image(image_path):
    print("[1] Détection des bulles...")
    bubbles = detect_bubbles(image_path)

    if not bubbles:
        print("⚠️ Aucune bulle détectée !")
        return None

    print("[2] Extraction du texte...")
    extracted_texts = extract_text(image_path, bubbles)

    print("[3] Traduction du texte...")
    translated_texts = translate_text(extracted_texts)

    print("[4] Remplacement du texte dans l’image...")
    output_path = "output.jpg"
    add_text_to_image(image_path, translated_texts, bubbles, output_path)

    print("✅ Processus terminé.")
    return output_path

if __name__ == "__main__":
    # Exemple : appelle ce script directement
    # Ajuste le chemin "example.jpg" selon tes données
    process_image("data/scantrad/test/images/example.jpg")
