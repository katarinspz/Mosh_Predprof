import csv
import cv2
import numpy as np


def texture_convert(image):
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGBA)
    return image_rgb.astype(np.float32) / 255.0

def resize(image):
    return cv2.resize(image, (400, 400))


def preprocess_image(image):  # препроцесс
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    lower_blue = np.array([100, 150, 50])  # low
    upper_blue = np.array([140, 255, 255])  # high

    mask = cv2.inRange(hsv_image, lower_blue, upper_blue)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    mask_cleaned = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=3)
    mask_cleaned = cv2.morphologyEx(mask_cleaned, cv2.MORPH_OPEN, kernel, iterations=3)

    return mask_cleaned


def detect_contours(mask):
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return contours


def draw_contours(image, contours):
    contoured_image = image.copy()
    for contour in contours:
        cv2.drawContours(contoured_image, [contour], -1, (0, 100, 255), 2)
    return contoured_image

def load_image(img_path):  # загрузка и обработка
    im_name = str(img_path).split("\\")[-1]

    image = cv2.imread(img_path)

    mask_cleaned = preprocess_image(image)

    contours = detect_contours(mask_cleaned)

    contoured_image = draw_contours(image, contours)
    return [im_name, len(contours), contoured_image]

