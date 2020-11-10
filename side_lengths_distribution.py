# === Observe the sides of images ===
# This will help us to determine what size to reshape.
import os
import cv2
import matplotlib.pyplot as plt
import statistics

#########################################
ORIGINAL_TRAINING_DATA_DIR = ""
#########################################

if ORIGINAL_TRAINING_DATA_DIR == "":
    print("Error: You did not give the constant value.")
    exit()


class ImageSidesInfo:
    def __init__(self, image_dir):
        self.__filenames = []
        self.__max_len_list = []
        self.__height_list = []
        self.__width_list = []
        self.__num_failed = 0
        self.__has_checked_count = 0
        self.__from_dir(image_dir)

    def __from_dir(self, image_dir):
        for root, dirs, files in os.walk(image_dir):
            n_files = len(files)
            print("There are {} files in \"{}\"\n".format(n_files, root))
            for file in files:
                # print("\r")
                filename = os.path.join(root, file)
                self.__filenames.append(filename)
                img = cv2.imread(filename, cv2.IMREAD_COLOR)
                try:
                    height, width, channels = img.shape
                    try:
                        max_len = height if height >= width else width
                        self.__max_len_list.append(max_len)
                        self.__height_list.append(height)
                        self.__width_list.append(width)
                    except:
                        self.__num_failed += 1
                        print("There is an error when getting size information of \"{}\".".format(filename))
                except:
                    self.__num_failed += 1
                    print("There is an error when reading \"{}\" as a color img.".format(filename))
                self.__has_checked_count += 1
                print("\rHas checked: {} files.".format(self.__has_checked_count))

        self.summary()

    def summary(self):
        num_files = len(self.__filenames)
        num_max_len = len(self.__max_len_list)
        num_heights = len(self.__height_list)
        num_widths = len(self.__width_list)
        print("Total: {} files. ({} successful, {} failed.)".format(num_files, num_files - self.__num_failed,
                                                                    self.__num_failed))
        print("{} images were processed failed.".format(self.__num_failed))
        if num_files != num_max_len:
            print("Error: number of files {} does NOT EQUAL to number of max side lengths {}.".format(num_files,
                                                                                                      num_max_len))
        if num_heights != num_widths:
            print("Error: number of heights {} does NOT EQUAL to number of widths {}.".format(
                num_heights, num_widths))

        # Plot max length scatter
        plt.figure(figsize=(10, 10))
        plt.xlabel('Width')
        plt.ylabel('Height')
        plt.scatter(self.__width_list, self.__height_list, s=5)
        plt.show()
        #
        print("=== Statistics about max side lengths ===")
        print("Mean:", statistics.mean(self.__max_len_list))
        print("Median:", statistics.median(self.__max_len_list))
        print("Max:", max(self.__max_len_list))
        print("Min:", min(self.__max_len_list))


image_sides_info = ImageSidesInfo(ORIGINAL_TRAINING_DATA_DIR)
