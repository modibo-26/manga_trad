# app/app.py

import sys
import os
import streamlit as st
from PIL import Image
import io
import imghdr
import cv2
import numpy as np

# Ajout du chemin du projet pour trouver "scripts/"
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scripts.end_to_end_pipeline import process_image  # Pipeline complet

st.title("ScanTrad - Traduction automatique de mangas")

# Upload de l'image
uploaded_file = st.file_uploader("Upload une image", type=["jpg", "png"])

if uploaded_file is not None:
    try:
        # Lire le fichier en mode binaire
        file_bytes = uploaded_file.read()
        
        if len(file_bytes) == 0:
            st.error("⚠️ Le fichier est vide. Essayez avec une autre image.")
        else:
            st.success(f"✅ Fichier reçu, taille : {len(file_bytes)} octets")

            # Vérifier le vrai format de l'image
            image_type = imghdr.what(io.BytesIO(file_bytes))
            st.write(f"🧐 Format détecté : {image_type}")

            if image_type not in ["jpeg", "png"]:
                st.error(f"❌ Ce fichier n'est pas un JPEG ou un PNG. Type détecté : {image_type}")
            else:
                try:
                    # Ouvrir avec Pillow
                    image = Image.open(io.BytesIO(file_bytes))
                    image_path = "uploaded_image.jpg"
                    # Sauvegarder l'image (en local) pour que le pipeline puisse la relire
                    image.save(image_path)
                    st.image(image, caption="Image originale", use_container_width=True)

                    # Lancer le pipeline complet
                    processed_image_path = process_image(image_path)

                    if processed_image_path:
                        st.image(processed_image_path, caption="Image traduite", use_container_width=True)
                    else:
                        st.error("❌ Une erreur est survenue lors du traitement.")
                
                except Exception as e:
                    st.warning(f"⚠️ Erreur avec Pillow : {e}")
                    st.info("🔄 Tentative d'ouverture avec OpenCV...")

                    try:
                        # Lecture via OpenCV
                        image_array = np.frombuffer(file_bytes, dtype=np.uint8)
                        image_cv2 = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

                        if image_cv2 is not None:
                            st.success("✅ OpenCV a chargé l'image avec succès.")
                            image_cv2_rgb = cv2.cvtColor(image_cv2, cv2.COLOR_BGR2RGB)
                            image_pil = Image.fromarray(image_cv2_rgb)
                            image_pil.save("image_corrigee.jpg", "JPEG")
                            st.image("image_corrigee.jpg", caption="Image corrigée", use_container_width=True)

                    except Exception as e:
                        st.error(f"❌ Impossible d'ouvrir l'image même avec OpenCV : {e}")

    except Exception as e:
        st.error(f"⚠️ Une erreur s'est produite : {e}")
