import os
import glob
import cv2

def detect_bubbles(image_path):
    """
    Détecte les bulles de texte dans une image avec YOLOv5.
    Args:
        image_path (str): Chemin de l'image à analyser.
    Returns:
        list: Liste des coordonnées [x, y, w, h] en pixels pour chaque bulle détectée.
    """
    output_dir = "yolov5/runs/detect/exp"
    os.makedirs(output_dir, exist_ok=True)
    
    # Exécution de YOLOv5 sur l'image
    # Assure-toi que "yolov5/detect.py" existe et que "yolov5/runs/train/exp3/weights/best.pt" est le bon chemin de ton modèle
    os.system(
        f"python yolov5/detect.py --weights yolov5/runs/train/exp3/weights/best.pt "
        f"--img 640 --conf 0.25 --source {image_path} --save-txt "
        f"--project yolov5/runs/detect --name exp --exist-ok"
    )

    # Chemin du dossier contenant les prédictions .txt
    labels_dir = os.path.join(output_dir, "labels")
    if not os.path.exists(labels_dir):
        print("⚠️ Aucune annotation trouvée !")
        return []

    # Récupérer les .txt générés
    txt_files = glob.glob(os.path.join(labels_dir, "*.txt"))
    if not txt_files:
        print("⚠️ Aucune bulle détectée.")
        return []

    # Pour la conversion en pixels, on a besoin de la taille réelle de l'image
    image = cv2.imread(image_path)
    if image is None:
        print(f"❌ Impossible de lire l'image {image_path} avec OpenCV.")
        return []
    height, width, _ = image.shape

    annotations = []
    for txt_file in txt_files:
        with open(txt_file, "r") as f:
            lines = f.readlines()
            for line in lines:
                data = line.strip().split()
                # Format YOLOv5 : [class, x_center, y_center, width, height]
                if len(data) == 5:
                    class_id, x_center_norm, y_center_norm, w_norm, h_norm = map(float, data)
                    if int(class_id) != 0:
                        continue


                    # Filtrer si nécessaire, par ex. si class_id == 0
                    # Ici on suppose qu'il n'y a qu'une seule classe (text),
                    # sinon décommente ci-dessous :
                    # if int(class_id) != 0:
                    #     continue

                    # Convertir coordonnées normalisées → pixels
                    x_center = x_center_norm * width
                    y_center = y_center_norm * height
                    w = w_norm * width
                    h = h_norm * height

                    # Trouver (x, y) = coin supérieur gauche
                    x = int(x_center - w / 2)
                    y = int(y_center - h / 2)
                    w = int(w)
                    h = int(h)

                    annotations.append([x, y, w, h])

                    print([x, y, w, h])

    # (Optionnel) Nettoyage : on peut supprimer le .txt pour ne pas polluer l’analyse des images suivantes
    for file_to_remove in txt_files:
        os.remove(file_to_remove)

    return annotations
