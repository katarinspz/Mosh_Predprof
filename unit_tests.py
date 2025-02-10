import os
from pathlib import Path

from bnr import *
from addtional import save_res_unit

# 1 access to files/correct processing
def unit1():
    project_dir = Path(__file__).parent.parent
    images_dir = project_dir / 'templates'
    image_files = list(images_dir.glob('*'))
    for image_file in image_files:
        print(load_image(image_file.resolve()) if load_image(image_file.resolve()) != [] else 'False')

# unit1()


# 2 try to save/correct input and metadata
def unit2():
    project_dir = Path(__file__).parent.parent
    images_dir = project_dir / 'templates'
    image_files = list(images_dir.glob('*'))
    for image_file in image_files:
        res = load_image(image_file.resolve())
        print(save_res_unit(res, 'zxc.csv', '../'))

#unit2()

