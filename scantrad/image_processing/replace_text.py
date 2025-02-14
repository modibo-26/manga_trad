from PIL import Image, ImageDraw, ImageFont
import textwrap

def add_text_to_image(image_path, texts, bubbles, output_path):
    """
    Ajoute du texte traduit dans les bulles détectées sur l'image,
    en supprimant le texte d'origine (zone blanche) et en insérant le nouveau.
    """
    try:
        image = Image.open(image_path)
        draw = ImageDraw.Draw(image)
        
        # Choix de la police
        try:
            font = ImageFont.truetype("arial.ttf", 20)
        except IOError:
            font = ImageFont.load_default()

        for text, bubble in zip(texts, bubbles):
            if not isinstance(bubble, (list, tuple)) or len(bubble) != 4:
                print(f"⚠️ Erreur : Format inattendu pour bubble -> {bubble}")
                continue
            
            x, y, w, h = bubble

            # 1) Effacer la zone (rectangle blanc)
            draw.rectangle([x, y, x + w, y + h], fill="white")

            # 2) Gérer le wrap pour éviter de dépasser horizontalement
            wrapped_text = textwrap.wrap(text, width=15)  
            # Ajustez 'width' selon la taille moyenne de vos bulles

            # 3) Dessiner chaque ligne
            # Utiliser draw.textsize(...) pour obtenir la taille du texte
            line_height = draw.textsize("A", font=font)[1] + 2
            offset_y = y

            # Calculer la hauteur totale (pour un éventuel centrage vertical)
            total_text_height = line_height * len(wrapped_text)
            start_y = y + (h - total_text_height) // 2
            current_y = start_y

            for line in wrapped_text:
                line_width, _ = draw.textsize(line, font=font)
                # Centrage horizontal dans la bulle
                text_x = x + (w - line_width) // 2
                draw.text((text_x, current_y), line, fill="black", font=font)
                current_y += line_height

        image.save(output_path)
        print(f"✅ Image enregistrée avec texte ajouté : {output_path}")

    except Exception as e:
        print(f"❌ Erreur lors du traitement de l'image : {e}")
