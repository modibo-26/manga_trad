from PIL import Image, ImageDraw, ImageFont
import textwrap

def add_text_to_image(
    image_path, 
    texts, 
    bubbles, 
    output_path,
    font_path="fonts/Arial.ttf",  # Police à large couverture (ex. Arial, DejaVuSans, etc.)
    max_font_size=12,
    min_font_size=6
):
    """
    Efface le texte d'origine dans les bulles et y insère le texte traduit (avec gestion des accents).
    'texts' doit contenir du texte UTF-8 correct (avec é, è, à...), 
    'bubbles' est la liste [x, y, w, h].
    """
    # 1) Ouvrir l'image
    image = Image.open(image_path).convert("RGB")
    draw = ImageDraw.Draw(image)

    for text, (x, y, w, h) in zip(texts, bubbles):
        # Vérif: imprimer le texte pour s'assurer qu'il contient les accents attendus
        # print("Debug - texte à dessiner:", text)

        # 2) Effacer la zone
        draw.rectangle([x, y, x + w, y + h], fill="white")

        # 3) Marge interne
        margin = 5
        in_x = x + margin
        in_y = y + margin
        in_w = w - 2*margin
        in_h = h - 2*margin

        # 4) Trouver la meilleure taille de police
        best_size = find_best_font_size(
            draw, text, in_w, in_h,
            font_path=font_path,
            max_font_size=max_font_size,
            min_font_size=min_font_size
        )

        # 5) Charger la police
        try:
            font = ImageFont.truetype(font_path, best_size)
        except Exception as e:
            print(f"⚠️ Impossible de charger la police {font_path} : {e}")
            font = ImageFont.load_default()

        # 6) Couper le texte en lignes (wrap)
        wrap_width = max(5, int(in_w // (best_size * 0.5)))
        lines = textwrap.wrap(text, width=wrap_width)

        # 7) Calculer la hauteur d'une ligne
        a_left, a_top, a_right, a_bottom = draw.textbbox((0,0), "A", font=font)
        line_height = (a_bottom - a_top) + 2
        total_height = line_height * len(lines)

        # 8) Centrage vertical approximatif
        current_y = in_y + (in_h - total_height)//2

        for line in lines:
            # Largeur de la ligne
            l_left, l_top, l_right, l_bottom = draw.textbbox((0,0), line, font=font)
            line_width = l_right - l_left
            # Centrage horizontal
            text_x = in_x + (in_w - line_width)//2

            # 9) Dessiner la ligne en noir
            draw.text((text_x, current_y), line, font=font, fill="black")

            current_y += line_height

    # 10) Sauvegarder l'image finale
    image.save(output_path)
    print(f"✅ Image enregistrée : {output_path}")


def find_best_font_size(draw, text, box_w, box_h,
                        font_path="fonts/Arial.ttf",
                        max_font_size=12,
                        min_font_size=6):
    """
    Teste différentes tailles de police (max->min) 
    pour faire tenir `text` dans la zone [box_w x box_h].
    Gère les accents si la police inclut ces glyphes.
    """
    import textwrap

    for size in range(max_font_size, min_font_size - 1, -1):
        try:
            font = ImageFont.truetype(font_path, size)
        except Exception as e:
            print(f"⚠️ Erreur chargement police: {e}")
            font = ImageFont.load_default()

        # On essaye de wrap le texte
        test_wrap = max(5, int(box_w // (size * 0.5)))
        wrapped = textwrap.wrap(text, width=test_wrap)

        # Calcul hauteur
        a_left, a_top, a_right, a_bottom = draw.textbbox((0,0), "A", font=font)
        line_height = (a_bottom - a_top) + 2
        total_height = line_height * len(wrapped)

        fits = True
        if total_height > box_h:
            fits = False
        else:
            # Vérifier la largeur de chaque ligne
            for line in wrapped:
                l_left, l_top, l_right, l_bottom = draw.textbbox((0,0), line, font=font)
                if (l_right - l_left) > box_w:
                    fits = False
                    break

        if fits:
            return size

    return min_font_size
