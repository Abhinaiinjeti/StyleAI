import cv2
import numpy as np

def detect_skin_tone(image_path):

    image = cv2.imread(image_path)

    if image is None:
        return "Medium"

    image = cv2.resize(image, (300, 300))

    brightness = np.mean(image)

    if brightness > 170:
        return "Fair"

    elif brightness > 100:
        return "Medium"

    else:
        return "Dark"