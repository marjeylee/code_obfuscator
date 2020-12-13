# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     image_transform
   Description :
   Author :       'li'
   date：          2020/6/16
-------------------------------------------------
   Change Activity:
                   2020/6/16:
-------------------------------------------------
"""
import base64


class ImageTransform:
    @staticmethod
    def img_to_base64(img_path):
        """

        :param img_path:
        :return:
        """
        with open(img_path, "rb") as f:
            base64_data = base64.b64encode(f.read())
            base64_data = base64_data.decode('utf8')
            return base64_data

    @staticmethod
    def base64_to_img(base64_encoding, des_img_path):
        """

        :param des_img_path:
        :param base64_encoding:
        :return:
        """
        base64_encoding = base64_encoding.encode('utf8')
        img_data = base64.b64decode(base64_encoding)
        with open(des_img_path, 'wb') as file:
            file.write(img_data)


def main():
    base_encoding = ImageTransform.img_to_base64('1.jpg')
    ImageTransform.base64_to_img(base_encoding, '2.jpg')


if __name__ == '__main__':
    main()
