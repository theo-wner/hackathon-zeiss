import cv2
from ultralytics import YOLO
import torch

# Modell initialisieren
model = YOLO("yolo-Weights/yolov8n-pose.pt")

# Videoquelle (Webcam) definieren
source = "0"  # Normalerweise '0' für die erste Webcam
results = model.predict(source=source, stream=True)

# Frame-Zähler
frame_count = 0

for result in results:
    keypoints = result.keypoints

    # Dateinamen für das Speichern der Keypoints-Daten
    filename = f'txt/keypoints_data_{frame_count}.txt'

    # Datei öffnen und die Keypoints-Daten speichern
    with open(filename, 'w') as f:
        f.write(str(keypoints.xyn))  # Die xyn-Daten als String speichern

    frame_count += 1  # Zähler für jedes Frame erhöhen

    # Optional: Ergebnisse anzeigen (entfernen, wenn nicht benötigt)
    result.show()

    # Schleife nach einer bestimmten Anzahl von Frames beenden (optional)
    if frame_count >= 10:  # Zum Beispiel nach 100 Frames beenden
        break

# Ressourcen freigeben (falls die Schleife irgendwann endet)
model.close()
