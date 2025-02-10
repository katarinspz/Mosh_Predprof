import cv2
import numpy as np
from addtional import find_contours


def canny_edge_detection(image_path):
    image = cv2.imread(image_path)
    num_edges = find_contours(image)
    if image is None:
        raise ValueError("Не удалось загрузить изображение. Проверьте путь к файлу.")

    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 1.5)

    edges = cv2.Canny(blurred_image, 50, 150)

    kernel = np.ones((2, 2), np.uint8)
    thick_edges = cv2.dilate(edges, kernel)

    # num_edges = np.sum(thick_edges > 0)
    edges_colored = np.zeros_like(image)
    edges_colored[thick_edges > 1] = [2, 255, 0]

    combined_image = cv2.addWeighted(image, 0.8, edges_colored, 1.0, 0)
    img_path = image_path.split('\\')[-1]

    # output_image_path = 'output_image.jpg'
    # cv2.imwrite(output_image_path, combined_image)
    return [img_path, num_edges, combined_image]