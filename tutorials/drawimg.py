import cv2
import os
import json
import torch


def read_tensors_from_file(file_path):
    with open(file_path, 'r') as file:
        # Dies lädt eine Liste von Listen von Koordinaten
        data_lists = json.load(file)
        tensors = [torch.tensor(data, dtype=torch.float32)
                   for data in data_lists]
    return tensors


def draw_keypoints(tensors, img_size=(640, 480)):
    # Direkt als NumPy-Array
    image = torch.zeros(
        (img_size[1], img_size[0], 3), dtype=torch.uint8).numpy()
    for tensor in tensors:
        for point in tensor:
            x, y = int(point[0] * img_size[0]), int(point[1] * img_size[1])
            cv2.circle(image, (x, y), 5, (0, 255, 0), -1)
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
