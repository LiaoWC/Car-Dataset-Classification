# === Resize to be square ===
# Make all images in a directory become squares by adding zero-padding.

import cv2
import os
from functions import square_image_np_arr

#######################################
TO_BE_RESIZED_DIR = ""
RESIZED_RESULT_DIR = ""
#######################################

if TO_BE_RESIZED_DIR == "" or RESIZED_RESULT_DIR == "":
    print("Error: You didn't give directory constants values.")
    exit()


# Check if the file name is valid in case there's dirty file in your directory.
def valid_filename(filename):
    deepestDirFileName = filename.split('/')[-1]
    if len(deepestDirFileName) != 10:
        return False
    filename_split_by_dot = deepestDirFileName.split('.')
    if len(filename_split_by_dot) != 2:
        return False
    if len(filename_split_by_dot[0]) != 6 or (not filename_split_by_dot[0].isdigit()) or (
            filename_split_by_dot[1] != 'jpg'):
        return False
    return True


def resize_imgs_to_square(from_dir, save_dir):
    if (
            input('Is the directory you want to place your resized images: "{}"'
                          .format(save_dir) +
                  '\nType: true if you are sure: ') != 'true'):
        print('Abort')
    else:
        print('Start to resize images!')
        filenames = []
        for root, dirs, files in os.walk(from_dir):
            for file in files:
                filenames.append(file)
        haveDone = 1
        for filename in filenames:
            try:
                if valid_filename(filename=filename):
                    img_arr = cv2.imread(from_dir + '/' + filename)
                    img_arr = square_image_np_arr(img_arr)
                    cv2.imwrite(save_dir + '/' + filename, img_arr)
                    print('Have done: {}'.format(haveDone))
                    haveDone += 1
            except:
                print('An exception')
                continue
        print('All Done!')


resize_imgs_to_square(TO_BE_RESIZED_DIR, RESIZED_RESULT_DIR)
