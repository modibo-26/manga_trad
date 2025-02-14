import os
import mimetypes
from PIL import Image
import cv2

# Chemin des données
data_path = r"C:\Users\mmoh7\Desktop\IPSSI-2023-2025\IA_Machine_Learning_Deep_Learning\Projet\scantrad\data\scantrad"

# Fonction pour vérifier les fichiers dans les dossiers train, valid et test
def verify_images():
    for subset in ["train", "valid", "test"]:
        images_dir = os.path.join(data_path, subset, "images")

        if not os.path.exists(images_dir):
            print(f"❌ Le dossier {images_dir} n'existe pas !")
            continue

        print(f"\n📂 Vérification des images dans {subset}/images :")
        
        for file in os.listdir(images_dir):
            file_path = os.path.join(images_dir, file)
            
            # Vérifier si le fichier existe et sa taille
            if not os.path.exists(file_path):
                print(f"❌ Le fichier {file} n'existe pas.")
                continue
            
            file_size = os.path.getsize(file_path)
            if file_size == 0:
                print(f"⚠️ L'image {file} est vide (0B) et doit être supprimée ou remplacée.")
                continue
            else:
                print(f"✅ {file} - Taille : {file_size} octets")

            # Vérifier le format réel de l'image avec mimetypes
            mime_type, _ = mimetypes.guess_type(file_path)
            if mime_type not in ["image/jpeg", "image/png"]:
                print(f"❌ {file} n'est pas un JPEG/PNG mais {mime_type} !")
                continue

            # Tester l'ouverture avec Pillow (PIL)
            try:
                img = Image.open(file_path)
                img.verify()  # Vérifie l'intégrité de l'image
                print(f"✅ {file} est valide avec PIL")
            except Exception as e:
                print(f"❌ {file} est corrompue pour PIL : {e}")

            # Tester l'ouverture avec OpenCV
            img_cv2 = cv2.imread(file_path)
            if img_cv2 is None:
                print(f"❌ {file} ne peut pas être lue par OpenCV")
            else:
                print(f"✅ {file} est valide avec OpenCV")

# Fonction pour réparer les images corrompues
def repair_image(file_path):
    try:
        image = Image.open(file_path).convert("RGB")
        new_path = file_path.replace(".jpg", "_fixed.jpg")
        image.save(new_path, "JPEG")
        print(f"✅ Image réparée : {new_path}")
    except Exception as e:
        print(f"❌ Impossible de réparer {file_path} : {e}")

# Fonction principale
def main():
    print("\n🔍 Début de la vérification des images...")
    verify_images()

    print("\n🛠 Tentative de réparation des images corrompues...")
    for subset in ["train", "valid", "test"]:
        images_dir = os.path.join(data_path, subset, "images")
        if not os.path.exists(images_dir):
            continue
        for file in os.listdir(images_dir):
            file_path = os.path.join(images_dir, file)
            repair_image(file_path)

    print("\n✅ Vérification et réparation terminées.")

if __name__ == "__main__":
    main()
