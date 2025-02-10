import cv2
import csv
import os


def find_contours(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary_image = cv2.threshold(gray_image, 240, 255, cv2.THRESH_BINARY_INV)

    contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    num_contours = len(contours)
    return num_contours


def save_results(lst, output_csv, dest):  # в файл
    k = 1
    csv_lst = []
    for i in lst:
        cv2.imwrite(f'{dest}\\result{k}.jpg', i[2])
        csv_lst += [[i[0], i[1]]]
        k += 1
    with open(output_csv, mode='w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        for i in csv_lst:
            writer.writerow([f"{i[0]}", i[1]])

def save_res_unit(lst, output_csv, dest):
    # k = 1
    csv_lst = []
    # print('ok')
    # cv2.imwrite(f'{dest}\\result{k}.jpg', i[2])
    csv_lst += [[lst[0], lst[1]]]
    # k += 1
    return [csv_lst, 'ok']
    # with open(output_csv, mode='w', newline='') as file:
    #     writer = csv.writer(file, delimiter=';')
    #     for i in csv_lst:
    #         writer.writerow([f"{i[0]}", i[1]])