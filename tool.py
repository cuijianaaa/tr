# coding: utf-8
print('###')
import clipboard
print('12')
import tr
print('32')
import sys, cv2, time, os
import math
from PIL import Image, ImageDraw, ImageFont
import numpy as np

print('aaa')
from PyQt5.QtGui import QGuiApplication
app = QGuiApplication(sys.argv)
cb = app.clipboard()
print('bbb')
#tab_pixels = 42.
debug = len(sys.argv) >= 2 and sys.argv[1] == 'debug'
_BASEDIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(_BASEDIR)
#pixels_per_space = tab_pixels / 4.
def test(img_pil):
    print('0')
    strings = ''
    MAX_SIZE = 1600
    if img_pil.height > MAX_SIZE or img_pil.width > MAX_SIZE:
        scale = max(img_pil.height / MAX_SIZE, img_pil.width / MAX_SIZE)
        new_width = int(img_pil.width / scale + 0.5)
        new_height = int(img_pil.height / scale + 0.5)
        img_pil = img_pil.resize((new_width, new_height), Image.ANTIALIAS)
    if debug:
        color_pil = img_pil.convert("RGB")
        img_draw = ImageDraw.Draw(color_pil)
        colors = ['red', 'green', 'blue', "purple"]
    gray_pil = img_pil.convert("L")
    print("33333333333333333333333333333333331")
    tr.detect(gray_pil, flag=tr.FLAG_RECT)
    print("33333333333333333333333333333333332")
    results = tr.run(gray_pil, flag=tr.FLAG_ROTATED_RECT)
    print("33333333333333333333333333333333333")
    last_rect = None
    last_str = None

    all_pixels = sum([rect[0][2] for rect in results if rect[2] > 0.1 and len(rect[1]) > 0])
    all_str_len = sum([len(rect[1]) for rect in results if rect[2] > 0.1 and len(rect[1]) > 0])
    pixels_per_space = all_pixels / all_str_len
    print("33333333333333333333333333333333334")
    for i, rect in enumerate(results):
        cx, cy, w, h, a = tuple(rect[0])
        if debug:
            print(i, "\t", cx - w / 2., rect[1], rect[2])
        # same line
        if last_rect is not None and abs(cy - last_rect[1]) < (h / 2.):
            spaces1 = round(((cx - w / 2.) - (last_rect[0] + last_rect[2] / 2.)) / pixels_per_space)
            spaces2 = round(((cx - w / 2) - (last_rect[0] - last_rect[2] / 2.)) / pixels_per_space) - len(last_str)
            spaces = max(spaces1, spaces2)
            strings += ' ' * spaces + rect[1]
        else:
            spaces = int(round((cx - w / 2) / pixels_per_space))
            strings += '\n' + ' ' * spaces + rect[1]
        last_rect = tuple(rect[0])
        last_str = rect[1]
        if debug:
            box = cv2.boxPoints(((cx, cy), (w, h), a))
            box = np.int0(np.round(box))
            for p1, p2 in [(0, 1), (1, 2), (2, 3), (3, 0)]:
                img_draw.line(xy=(box[p1][0], box[p1][1], box[p2][0], box[p2][1]), fill=colors[i % len(colors)], width=2)
    print(strings)
    clipboard.copy(strings)
    if debug:
        color_pil.show()

if __name__ == "__main__":
    print('000')
    if cb.mimeData().hasImage():
        qt_img = cb.image()
        pil_img = Image.fromqimage(qt_img)
        test(pil_img)

