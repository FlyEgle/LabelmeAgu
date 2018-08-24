import json
import math
import os
from PIL import Image
from PIL import ImageDraw
from manner_image.generate_rotateimg import DoImg
from tqdm import tqdm
import numpy as np
import base64


image = Image.open('0.png')
image2 = Image.open('2.png')
image_array = np.array(image)

center_y, center_x = image_array.shape[0]/2, image_array.shape[1]/2
draw = ImageDraw.Draw(image)
draw2 = ImageDraw.Draw(image2)


# transform point by degree
def transform_points_degree(x, y, degree):
    """ x, y is the input points , degree is rotate angle
        return rotate degree new points
    """
    degree = - math.radians(degree)
    new_x = math.cos(degree) * (x - center_x) - math.sin(degree) * (y - center_y) + center_x
    new_y = math.sin(degree) * (x - center_x) + math.cos(degree) * (y - center_y) + center_y
    return new_x, new_y


# read json file from dir
def read_json(json_file_path):
    """ input: json_file dir path
        return a list of json file
    """
    json_file_list = []
    json_read_list = []
    for json_ in os.listdir(json_file_path):
        if json_.split('.')[1] == 'json':
            json_file_list.append(os.path.join(json_file_path, json_))
        else:
            continue
    for json_single in json_file_list:
        with open(json_single, 'r') as file:
            json_file = file.read()
            img_json = json.loads(json_file)
            json_read_list.append(img_json)
    return json_read_list


# reverse for draw line [A, B, C, D] -> [B, C, D, A]
def reverse_b_c_list(img_points):
    """ This function is only should for 4 points not suitable for more points
        input : img_points which have 4 (x_point, y_point) as a list
        return : reverse [A, B, C, D] TO [B, C, D, A]
    """
    change_end_start_list = []
    for i in range(len(img_points)):
        reverse_end_start = img_points[i]
        reverse_list = reversed(reverse_end_start)
        reversed_list = []
        for j in reverse_list:
            reversed_list.append(j)
        reversed_list[0], reversed_list[2] = reversed_list[2], reversed_list[0]
        change_end_start_list.append(reversed_list)
    return change_end_start_list


# calculate new rotate image points
def translate_points(json_read_list, angle):
    """ input : json file list, degree
        return : new points list for each json file
    """
    new_json_points = []
    for img_json in json_read_list:
        img_points = []
        new_img_points = []
        len_points = img_json["shapes"]
        for i in range(len(len_points)):
            img_points.append(len_points[i]['points'])
        change_end_start_list = reverse_b_c_list(img_points)
        # get the rotate bbox points
        for i in range(len(img_points)):
            each_new_point = []
            for j in range(len(img_points[i])):
                # transform 5 degree example
                x, y = transform_points_degree(img_points[i][j][0], img_points[i][j][1], angle)
                x1, y1 = transform_points_degree(change_end_start_list[i][j][0], change_end_start_list[i][j][1], angle)
                each_new_point = [x, y]
                # draw2.line((x, y, x1, y1), fill=128)
            new_img_points.append(each_new_point)
        new_json_points.append(new_img_points)
    return new_json_points


# translate image data from binary to base64
def get_imagedata_base64(image_path):
    """ input: image_path a list of image path
        return : image data base64 encoding
    """
    f = open(image_path, 'rb')
    file_base64 = base64.b64encode(f.read()).decode('utf-8')
    return file_base64


def generate_rotateimage(src, dst, degree):
    """input is rotate degree
        return is a roated image save file
    """
    if os.path.exists(dst):
        print('dst dir is exists!')
    else:
        os.mkdir(dst)
    print("create sub dir for degree")
    for i in range(len(degree)):
        os.mkdir(os.path.join(dst, 'rotate_%d' % i))
    for image_file in tqdm(os.listdir(src)):
        img = DoImg(os.path.join(src, image_file))
        for j in range(len(degree)):
            roate_image = img.RotateImg(degree[j])
            img.save(roate_image, os.path.join(dst+'rotate_%d' % j,
                                               image_file.split('.jpg')[0] + '_rotate_%d.png' % j))


def draw_new_image(src_image, image_poinst):
    image_list = os
    pass


# generate new jsonfile for rotate image
def generate_json_file(image_path, src, dst, new_json_points):
    """ input: image_path: rotate image
               src: orginal json file path
               dst: destination json file path
               new_json_points: points list
        return : generate a new json file
    """
    js_list = []
    file_list = os.listdir(src)
    image_list = os.listdir(image_path)
    for file_index in range(len(file_list)):
        with open(os.path.join(src, file_list[file_index]), 'r') as f:
            file = f.read()
            js_file = json.loads(file)
            # replace json file new rotate points
            print(file_index)
            # TODO: points is wrong each json file need 4*8 pioints
            for i in range(8):
                js_file['shapes'][i]['points'] = new_json_points[file_index][i]
            js_file['imageData'] = get_imagedata_base64(os.path.join(image_path,
                                                                     image_list[file_index]))
            js_file['imagePath'] = image_list[file_index]
        js_list.append(js_file)

    for i in range(len(js_list)):
        json_str = json.dumps(js_list[i], sort_keys=True, indent=4, separators=(',', ':'))
        file_json = open(dst + file_list[i].split('.json')[0]+"_rotate_%d.json" % i, 'w')
        file_json.write(json_str)
        file_json.close()


if __name__ == '__main__':
    image_path = 'F:/heightpoint_datasests/height_point_train_data/'
    json_file_path = 'F:/heightpoint_datasests/seg_json/'
    new_json_file_path = 'F:/heightpoint_datasests/rotate_json/'
    rotate_image_path = 'F:/heightpoint_datasests/rotate_image/'
    degree = [-4, -8, 4, 8]

    # make sub json dir by degree
    print("make dir for degree json!!")
    if os.path.exists(new_json_file_path):
        print("dir have been maked")
    else:
        for i in range(len(degree)):
            os.mkdir(os.path.join(new_json_file_path, 'rotate_%d' % i))
        # generate rotated image by degree
    print("generate image !!")

    # get 4 rotate new points list
    rotate_list = []
    for i in range(len(degree)):
        orginal_json_list = read_json(json_file_path)

        print(orginal_json_list)

        new_json_list = translate_points(orginal_json_list, degree[i])
        rotate_list.append(new_json_list)

    print(rotate_list[0][0])
        # generate_json_file(os.path.join(rotate_image_path, 'rotate_%d/' % i), json_file_path,
        #                    os.path.join(new_json_file_path, 'rotate_%d/' % i), rotate_list[i])















