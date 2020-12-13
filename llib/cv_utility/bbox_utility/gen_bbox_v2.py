from llib.cv_utility.image_opt_utility import read_image


class BBoxGeneratorV2:
    def __init__(self, pixel):
        self.text_area_pixel = pixel


def main():
    pixel = read_image('imgs/1.jpg') / 255
    pass


if __name__ == '__main__':
    main()
