# data argument
from PIL import Image
from tqdm import tqdm
import os


class DoImg:

    def __init__(self, path):
        self.path = path
        self.img = Image.open(path)

    def ResizeImg(self, size, ifpadding=False):
        if ifpadding:
            img_resize = self.img.resize(size)
            return img_resize

    def RotateImg(self, degree):
        img_rotate = self.img.rotate(degree)
        return img_rotate

    def FlipImg(self, flag):
        if flag == 0:
            img_flip = self.img.transpose(Image.FLIP_LEFT_RIGHT)
            return img_flip
        elif flag == 1:
            img_flip = self.img.transpose(Image.FLIP_TOP_BOTTOM)
            return img_flip

    def showImg(self, img):
        img.show()

    def save(self, img, dst):
        img.save(dst)


def generate_rotateimage(src, dst, degree):
    """input is rotate degree
        return is a roated image save file
    """
    if os.path.exists(dst):
        print('dst dir is exists!')
    else:
        os.mkdir(dst)
    for image_file in tqdm(os.listdir(src)):
        img = DoImg(os.path.join(src, image_file))
        for i in range(len(degree)):
            roate_image = img.RotateImg(degree[i])
            img.save(roate_image, os.path.join(dst, image_file.split('.jpg')[0] + '_rotate_%d.png' % i))


if __name__ == '__main__':
    degree = [-4, -8, 4, 8]
    src_path = 'F:/heightpoint_datasests/height_point_train_data/'
    dst_path = 'F:/heightpoint_datasests/rotate_image/'
    generate_rotateimage(src_path, dst_path, degree)
