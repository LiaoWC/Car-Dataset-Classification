import numpy as np


# Make images to be square images (by adding zero-padding)
def square_image_np_arr(img_arr):
    h, w, channels = img_arr.shape
    maxLen = max(h, w)
    # Make it to be a square
    if h != w and maxLen == h:
        err = h - w
        img_arr = np.concatenate([np.zeros((h, err // 2, 3), dtype="uint8"), img_arr, np.zeros((h, err - err // 2, 3))],
                                 axis=1)
    elif h != w and maxLen == w:
        err = w - h
        img_arr = np.concatenate([np.zeros((err // 2, w, 3), dtype="uint8"), img_arr, np.zeros((err - err // 2, w, 3))],
                                 axis=0)
    return img_arr


# Turn a RGB image numpy array into a grayscale image
# (data type: numpy array; input and output are in same dimensions.)
def np_rgb_to_gray(rgb):
    r, g, b = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
    gray = 0.2989 * r + 0.5870 * g + 0.1140 * b
    return gray
