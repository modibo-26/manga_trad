import os

# Chemin vers le fichier de configuration des données
data_yaml = "scantrad/data.yaml"

# Commande d'entraînement
train_cmd = f"python train.py --img 640 --batch 16 --epochs 50 --data {data_yaml} --weights yolov5s.pt --device 0"

# Exécuter la commande
os.system(train_cmd)
