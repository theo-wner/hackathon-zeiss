import cv2
import os
import json
import torch


def read_tensor_from_file(file_path):
    # Die Datei lesen und den Inhalt in einen Tensor konvertieren
    with open(file_path, 'r') as file:
        data_list = json.load(file)  # Lade die Datenliste aus der JSON-Datei
        # Konvertiere in einen PyTorch Tensor
        tensor = torch.tensor(data_list, dtype=torch.float32)
    return tensor


def draw_keypoints(tensor, img_size=(640, 480)):
    # Ein leeres Bild erstellen
    image = torch.zeros((img_size[1], img_size[0], 3), dtype=torch.uint8)
    # Koordinaten durchlaufen und zeichnen
    for point in tensor:
        x, y = int(point[0] * img_size[0]), int(point[1] * img_size[1])
        # Einen Kreis am Keypoint zeichnen
        cv2.circle(image, (x, y), 5, (0, 255, 0), -1)
    return image


def process_files(directory, output_dir):
    # Ordner erstellen, falls nicht vorhanden
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Alle Dateien im Verzeichnis durchlaufen
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            file_path = os.path.join(directory, filename)
            tensor = read_tensor_from_file(file_path)
            image = draw_keypoints(tensor)
            # Das Bild speichern
            output_file = os.path.join(
                output_dir, filename.replace('.txt', '.jpg'))
            cv2.imwrite(output_file, image.numpy())


# Verzeichnis der Textdateien und Ausgabeverzeichnis für die Bilder
txt_directory = 'txt'
img_directory = 'img'

# Die Funktion aufrufen
process_files(txt_directory, img_directory)
