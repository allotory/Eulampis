# -*- coding: utf-8 -*-

from PIL import Image
import argparse
import os

class Img2Ascii(object):

    def __init__(self):
        # self.ascii_char = list("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. ")
        self.ascii_char = list('m&dn1+. ')
        self.txt = ''

    def get_char(self, r, b, g, alpha = 256):
        # 灰度值：指黑白图像中点的颜色深度，范围一般从0到255，白色为255，黑色为0，故黑白图片也称灰度图像
        # 灰度值 ＝ 0.2126 * r + 0.7152 * g + 0.0722 * b
        # 将256灰度映射到ascii_char字符上
        if alpha == 0:
            return ' '

        length = len(self.ascii_char)
        gray = int(0.2126 * r + 0.7152 * g + 0.0722 * b)
        unit = (256.0 + 1) / length

        return self.ascii_char[int(gray / unit)]

    def get_text(self, src):
        im = Image.open(src)
        width, height = im.size
        height = height / 2
        im = im.resize((int(width*0.3), int(height*0.3)), Image.NEAREST)

        for i in range(int(height * 0.3)):
            for j in range(int(width * 0.3)):
                self.txt += self.get_char(*im.getpixel((j,i)))
            self.txt += '\n'

        print(self.txt)

    def out_put(self, dest):
        with open(dest, 'w') as f:
            f.write(self.txt)

if __name__ == '__main__':
    img = Img2Ascii()
    img.get_text('c.png')
    img.out_put('image.txt')
