import dearpygui.dearpygui as dpg
import ctypes
import os

from addtional import save_results
from canny import *
from bnr import *
from dotenv import load_dotenv

load_dotenv()
user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
view_pos = [screensize[0] // 2 - 70, screensize[1] // 2 - 270]
dpg.create_context()

WIDTH = int(os.getenv("WIDTH"))
HEIGHT = int(os.getenv("HEIGHT"))
PROCESSED = {}


def main_window():
    dpg.set_viewport_width(WIDTH)
    dpg.set_viewport_height(HEIGHT)
    dpg.set_primary_window('main', value=True)
    dpg.configure_item('main', show=True)


def update_texture(lst, parent='TextureWindow'):
    now = lst
    image = texture_convert(resize(now[2]))
    width, height, _ = image.shape
    texture_data = image.flatten()

    with dpg.texture_registry():
        texture_id = dpg.add_dynamic_texture(width, height, texture_data)

    if dpg.does_item_exist('imgg'):
        dpg.delete_item('imgg')
        dpg.add_image(texture_id, parent=parent, tag='imgg')
        dpg.set_value('txt_nums', f'num of structures: {now[1]}')
        dpg.set_value('pr_fl', f'processed files: {len(PROCESSED.keys())}')
    else:
        dpg.add_image(texture_id, parent=parent, tag='imgg')
        dpg.add_text(parent=parent, pos=[420, 5], default_value=f'num of structures: {now[1]}', tag='txt_nums')
        dpg.add_text(parent=parent, pos=[420, 20], default_value=f'processed files: {1}', tag='pr_fl')


def upload_file(sender, data):
    global PROCESSED
    try:
        if dpg.get_value('radiohead') == 'binarization':
            response = load_image(data['file_path_name'])
        else:
            response = canny_edge_detection(data['file_path_name'])

        PROCESSED[response[0]] = response
        update_texture(response)

        # dpg.set_item_pos('popup', [300, 100])
        # dpg.configure_item('popup', show=True)

    except Exception as e:
        dpg.set_item_pos('popup_error', [300, 100])
        dpg.configure_item('popup_error', show=True)


def save_image(sender, data):
    save_results(PROCESSED.values(), data["file_path_name"]+'\\output.csv', data["file_path_name"])


def open_save():
    dpg.add_file_dialog(
        directory_selector=True,
        callback=save_image,
        height=400,
        width=600,
    )


with dpg.file_dialog(show=False, tag="upload_file_dia", callback=upload_file, width=600, height=400):
    dpg.add_file_extension('(*.jpg){.jpg}')
    dpg.add_file_extension('.jpg', color=(121, 200, 158), custom_text='[JPG]')


with dpg.window(tag="main", label="work", no_resize=True, no_move=True, no_title_bar=False) as work_window:
    with dpg.group(horizontal=True):

        with dpg.child_window(width=WIDTH - 190, height=HEIGHT - 60, no_scrollbar=True, no_scroll_with_mouse=True,
                             tag='TextureWindow'):
            pass

        with dpg.child_window(width=150, height=100, no_scrollbar=True, no_scroll_with_mouse=True):
            dpg.add_button(label="Choose file", callback=lambda: dpg.show_item("upload_file_dia"), width=130)
            dpg.add_button(label="Save", callback=open_save, width=130)
            dpg.add_radio_button(['binarization', 'canny'], tag='radiohead', default_value='binarization')
            dpg.add_text("", tag='anchor')

with dpg.popup(parent='anchor', modal=True, tag='popup'):
    dpg.add_text('File is processed already')

with dpg.popup(parent='anchor', modal=True, tag='popup_error'):
    dpg.add_text('Choose file')

dpg.create_viewport(title='kai', resizable=False)
main_window()
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_viewport_pos(view_pos)
dpg.start_dearpygui()
dpg.destroy_context()