from transformers import pipeline

# Vérification du modèle de traduction
try:
    translator = pipeline("translation_en_to_fr", model="Helsinki-NLP/opus-mt-en-fr")
    print("✅ Modèle de traduction chargé.")
except Exception as e:
    raise RuntimeError(f"❌ Erreur lors du chargement du modèle de traduction : {e}")

def translate_text(texts):
    """
    Traduit une liste de textes de l'anglais vers le français.
    Args:
        texts (list): Liste de chaînes de texte en anglais.
    Returns:
        list: Liste des traductions en français.
    """
    if not texts:
        return []
    
    # On applique la traduction sur chaque élément
    translated = []
    for text in texts:
        if text:
            res = translator(text)[0]['translation_text']
            translated.append(res)
        else:
            translated.append("")
    return translated
