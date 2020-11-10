# === Train Valid Split Save Images ===
# Should classify training data first.(Save them in their classes' directories.
# Split Training and Validation Data and save to class directories.
# All images will be saved as squares with zero-padding.
import cv2
import os
import pandas as pd
from sklearn.model_selection import train_test_split
from functions import square_image_np_arr

########################################
# Constants
CLASSIFIED_DIR = ""
TRAIN_VALID_SPLIT_DEST_DIR = ""
IMG_HEIGHT = -1
IMG_WIDTH = -1
DATA_SPLIT_RATE = -1.0
SAVE_AS_SQUARE = True

########################################

if CLASSIFIED_DIR == "" or TRAIN_VALID_SPLIT_DEST_DIR == "" or IMG_HEIGHT < 0 or IMG_WIDTH < 0 or DATA_SPLIT_RATE < 0:
    print("Error: Please set constants first.")
    exit()


def data_train_valid_split_save(data_path, new_path, img_width, img_height, data_split_rate=(0.9, 0.1), square=True):
    data_path_list, data_label_list = [], []
    split_names = ['train', 'valid']
    print('Start walking in dirs.')
    for root, dirs, files in os.walk(data_path):
        if len(files) != 0:
            label = root.split("/")[-1]
            for split_name in split_names:
                new_root = os.path.join(new_path, split_name, label)
                if not os.path.exists(new_root):
                    os.makedirs(new_root)
        for file in files:
            img_path = os.path.join(root, file)
            label = root.split("/")[-1]
            data_path_list.append(img_path)
            data_label_list.append(label)

    data_list = pd.DataFrame({"img_path": data_path_list, "label": data_label_list})
    class_map = {label: i for i, label in enumerate(data_list["label"].unique().copy())}
    data_list["label_class"] = data_list["label"].map(class_map)

    train_list, valid_list = train_test_split(data_list,
                                              test_size=data_split_rate[-1],
                                              random_state=7,
                                              stratify=data_list["label_class"])

    data_types = [train_list["img_path"].values, valid_list["img_path"].values]
    print('Start preprocessing and saving.')
    passed = 0
    for each_list, each_name in zip(data_types, split_names):
        for img_path in each_list:
            label, file = img_path.split("/")[-2:]
            new_root = os.path.join(new_path, each_name, label)
            img_newpath = os.path.join(new_root, file)
            try:
                # preprocessing here

                img_arr = cv2.imread(img_path)
                if square:
                    img_arr = square_image_np_arr(img_arr)
                cv2.imwrite(img_newpath, img_arr)
                # if RESIZED_MODE == 'rgb':
                #   img_rgb = Image.open(img_path)
                #   # resized_img = img_rgb.resize((img_width,img_height))
                #   img_rgb.save(img_newpath)

                # elif RESIZED_MODE == 'grayscale':
                #   img_rgb = Image.open(img_path)
                #   img_rgb_arr = np.array(img_rgb)
                #   img_gray = img_rgb
                #   if len(img_rgb_arr.shape) >= 3:
                #       img_arr_gray = rgbtogray.np_rgb_to_gray(img_rgb_arr)
                #       img_gray = Image.fromarray(img_arr_gray)
                #   else:
                #       img_gray = img_rgb
                #   # resized_img = img_gray.resize((img_width,img_height))
                #   img_gray = img_gray.convert('L')
                #   img_gray.save(img_newpath)
            except:
                print('+++ ERROR: {} +++'.format(img_path))
            passed += 1
            print('have passed: {}'.format(passed))


if input('Type true to continue splitting:') == 'true':
    data_train_valid_split_save(CLASSIFIED_DIR, TRAIN_VALID_SPLIT_DEST_DIR, img_width=IMG_WIDTH,
                                img_height=IMG_HEIGHT, data_split_rate=DATA_SPLIT_RATE, square=True)
else:
    print('Abort')
