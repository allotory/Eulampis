# -*- coding: utf-8 -*-

import string
import random
from PIL import Image,ImageDraw,ImageFont,ImageFilter

class Captcha(object):

    def __init__(self):
        self.number = 5
        self.image_size = (100, 40)
        self.bgcolor = (255, 255, 255)
        self.fontcolor = (0, 0, 0)
        self.font_path = '/MONACO.TTF'

    def gene_text(self):
        # generate captcha text
        source = list(string.ascii_uppercase)
        for i in range(0, 10):
            source.append(str(i))
        text = ''.join(random.sample(source, self.number))
        return text

    def create_points(self):
        # draw disturbance point
        x = 10
        chance = min(100, max(0, x))
       
        for w in range(self.image_size[0]):
            for h in range(self.image_size[1]):
                tmp = random.randint(0, 100)
                if tmp > 100 - chance:
                    self.draw.point((w, h), fill=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))

    def gene_code(self):
        # image width and height
        width, height = self.image_size
        # create image
        image = Image.new('RGBA', (width, height), self.bgcolor)
        # font type and size
        font = ImageFont.truetype(self.font_path, size=25)
        # create draw object
        self.draw = ImageDraw.Draw(image)
        # generate captcha text
        text = self.gene_text()
        # font width and height
        font_width, font_height = font.getsize(text)
        # draw captcha text
        self.draw.text(((width - font_width) / 3, (height - font_height) / 3),
            text, font= font, fill=self.fontcolor, align='center')
        # draw disturbance point
        self.create_points()

        # transforms image data
        params = [1 - float(random.randint(1, 2)) / 100, 0, 0, 0, 
            1 - float(random.randint(1, 10)) / 100, float(random.randint(1, 2)) / 500,
            0.001, float(random.randint(1, 2)) / 500]
        # transforms this image
        image = image.transform(self.image_size, Image.PERSPECTIVE, params, Image.BILINEAR) # 创建扭曲
        # filters this image
        image = image.filter(ImageFilter.EDGE_ENHANCE_MORE)

        # save image
        image.save('captcha.PNG')

if __name__ == '__main__':
    captcha = Captcha()
    captcha.gene_code()