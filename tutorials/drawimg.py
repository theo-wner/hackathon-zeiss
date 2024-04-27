import cv2
import os
import json
import torch


def read_tensors_from_file(file_path):
    with open(file_path, 'r') as file:
        data_lists = json.load(file)
        tensors = [torch.tensor(data, dtype=torch.float32)
                   for data in data_lists]
    return tensors


def draw_keypoints(tensors, img_size=(640, 480)):
    image = torch.zeros(
        (img_size[1], img_size[0], 3), dtype=torch.uint8).numpy()
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.4
    color = (255, 255, 255)  # Weiß für die Nummerierung
    thickness = 1
    line_color = (0, 0, 255)  # Rot für die Linien
    line_thickness = 2

    # Verbindungen, die gezeichnet werden sollen (0-basierte Indizes)
    connections = [(10, 8), (8, 6), (6, 12), (12, 11), (11, 5), (5, 6), (5, 7), (7, 9), (12, 14), (14, 16), (11, 13), (13, 15), (4, 2), (2, 1), (1, 3), (0, 4), (3, 0), (4,6), (3,5)]

    for tensor in tensors:
        points = [(int(p[0] * img_size[0]), int(p[1] * img_size[1]))
                  for p in tensor]

        # Zeichne die Punkte
        for i, (x, y) in enumerate(points):
            if x > 0 and y > 0:  # Nur sichtbare Punkte zeichnen und nummerieren
                cv2.circle(image, (x, y), 5, (0, 255, 0), -1)
                cv2.putText(image, str(i + 1), (x + 6, y + 6),
                            font, font_scale, color, thickness)

        # Zeichne die Verbindungen zwischen den Punkten
        for start_idx, end_idx in connections:
            if start_idx < len(points) and end_idx < len(points):
                start_point = points[start_idx]
                end_point = points[end_idx]
                if start_point[0] > 0 and start_point[1] > 0 and end_point[0] > 0 and end_point[1] > 0:
                    cv2.line(image, start_point, end_point,
                             line_color, line_thickness)

    return image


def process_files(directory, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            file_path = os.path.join(directory, filename)
            tensors = read_tensors_from_file(file_path)
            image = draw_keypoints(tensors)
            output_file = os.path.join(
                output_dir, filename.replace('.txt', '.jpg'))
            cv2.imwrite(output_file, image)


txt_directory = 'txt'
img_directory = 'img'
process_files(txt_directory, img_directory)
