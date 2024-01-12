import transform
import drawer
import config
from logger import Logger
import utils
import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
import json
def generate_all_by_score(num_images, path, num_pattern=18):
    dir = './'
    folder_files = {}

    for score in range(1, num_pattern*2+1):
        # scoring_types_list = utils.generate_type_list_with_sum(score,num_images, num_pattern)
        for num in range(num_images):
            # scoring_types = scoring_types_list[num]
            scoring_types = utils.generate_type_list_with_sum(score, num_pattern)
            # Create an empty black image (all zeros) using NumPy
            image = np.zeros((config.IMAGE_HEIGHT, config.IMAGE_WIDTH, config.IMAGE_CHANNELS), dtype=np.uint8)
            image = cv2.bitwise_not(image)
            fig, ax = plt.subplots()
            ax.imshow(image, origin='upper')
            ax.axis('off')
            file_num = 1
            if not os.path.exists(f"../images/{path}"):
                # Create the directory if it doesn't exist
                os.makedirs(f"../images/{path}")
            else:
                file_num = len(os.listdir(f"../images/{path}"))
            if score not in folder_files:
                folder_files[score] = file_num
            else:
                folder_files[score] += 1
            # record log
            image_name = f"{score}_{file_num}.jpg"
            Logger().record_metafile(path, image_name, scoring_types)
            Logger().record_txtfile(f"images/{path}/{image_name}", scoring_types)
            print(f"starting ------------ {image_name}")
            # start drawing the shape
            if num_pattern >= 1:
                Logger().record_detail(f"big rectangle type {config.score_map[scoring_types[0]]}")
                print(f"big rectangle type {scoring_types[0]}")
                drawer.draw_big_rectangle(scoring_types[0], image)

            if num_pattern >=2:
                Logger().record_detail(f"big cross type {config.score_map[scoring_types[1]]}")
                print(f"big cross type{scoring_types[1]}")
                drawer.draw_big_cross(scoring_types[1], image)

            if num_pattern >= 3:
                Logger().record_detail(f"horizontal middle line type {config.score_map[scoring_types[2]]}")
                print(f"horizontal middle line type {scoring_types[2]}")
                drawer.draw_horizontal_midline(scoring_types[2], image)

            if num_pattern >= 4:
                Logger().record_detail(f"vertical middle line type{config.score_map[scoring_types[3]]}")
                print(f"vertical middle line type{scoring_types[3]}")
                drawer.draw_vertical_midline(scoring_types[3], image)

            if num_pattern >= 5:
                Logger().record_detail(f"small rectangle with cross type{config.score_map[scoring_types[4]]}")
                print(f"small rectangle with cross type{scoring_types[4]}")
                drawer.draw_small_rectangle(scoring_types[4], image)

            if num_pattern >= 6:
                Logger().record_detail(f"horizontal small line type{config.score_map[scoring_types[5]]}")
                print(f"horizontal small line type{scoring_types[5]}")
                drawer.draw_HORIZONTAL_SMALL_LINE(scoring_types[5])

            if num_pattern >= 7:
                Logger().record_detail(f"four parallel lines type{config.score_map[scoring_types[6]]}")
                print(f"four parallel lines type{scoring_types[6]}")
                drawer.draw_FOUR_PARALLEL_LINE(scoring_types[6])

            if num_pattern >= 8:
                Logger().record_detail(f"small rectangle type{config.score_map[scoring_types[7]]}")
                print(f"small rectangle type{scoring_types[7]}")
                drawer.draw_SMALL_TRIANGLE(scoring_types[7])

            if num_pattern >= 9:
                Logger().record_detail(f"small vertical line type{config.score_map[scoring_types[8]]}")
                print(f"small vertical line type{scoring_types[8]}")
                drawer.draw_VERTICAL_SMALL_LINE(scoring_types[8])

            if num_pattern >= 10:
                Logger().record_detail(f"circle type{config.score_map[scoring_types[9]]}")
                print(f"circle type{scoring_types[9]}")
                drawer.draw_circle(scoring_types[9])

            if num_pattern >= 11:
                Logger().record_detail(f"FIVE_PARALLEL_LINE type{config.score_map[scoring_types[10]]}")
                print(f"FIVE_PARALLEL_LINE type{scoring_types[10]}")
                drawer.draw_FIVE_PARALLEL_LINE(scoring_types[10])

            if num_pattern >= 12:
                Logger().record_detail(f"draw_RIGHT_JOIN_LINE type{config.score_map[scoring_types[11]]}")
                print(f"draw_RIGHT_JOIN_LINE type{scoring_types[11]}")
                drawer.draw_RIGHT_JOIN_LINE(scoring_types[11])

            if num_pattern >= 13:
                Logger().record_detail(f"draw_RHOMBUS type{config.score_map[scoring_types[12]]}")
                print(f"draw_RHOMBUS type{scoring_types[12]}")
                drawer.draw_RHOMBUS(scoring_types[12])

            if num_pattern >= 14:
                Logger().record_detail(f"draw_VERTICAL_RIGHT_LINE type{config.score_map[scoring_types[13]]}")
                print(f"draw_VERTICAL_RIGHT_LINE type{scoring_types[13]}")
                drawer.draw_VERTICAL_RIGHT_LINE(scoring_types[13])

            if num_pattern >= 15:
                Logger().record_detail(f"draw_HORIZENTAL_RIGHT_LINE type{config.score_map[scoring_types[14]]}")
                print(f"draw_HORIZENTAL_RIGHT_LINE type{scoring_types[14]}")
                drawer.draw_HORIZENTAL_RIGHT_LINE(scoring_types[14])

            if num_pattern >= 16:
                Logger().record_detail(f"draw_BOTTOM_RECTANGLE type{config.score_map[scoring_types[15]]}")
                print(f"draw_BOTTOM_RECTANGLE type{scoring_types[15]}")
                drawer.draw_BOTTOM_RECTANGLE(scoring_types[15])

            if num_pattern >= 17:
                Logger().record_detail(f"draw_HORIZENTAL_CROSS type{config.score_map[scoring_types[16]]}")
                print(f"draw_HORIZENTAL_CROSS type{scoring_types[16]}")
                drawer.draw_HORIZENTAL_CROSS(scoring_types[16])

            if num_pattern >= 18:
                Logger().record_detail(f"draw_VERTICAL_CROSS type{config.score_map[scoring_types[17]]}")
                print(f"draw_VERTICAL_CROSS type{scoring_types[17]}")
                drawer.draw_VERTICAL_CROSS(scoring_types[17])

            # print(config.POINTS_DIC)
            plt.savefig(f'../images/{path}/{image_name}')



def generate_all_by_type(num_images, path, prefix, num_pattern=18):# four score types: both correct, place correct, shape correct, both wrong
    folder_files = {}
    for num in range(num_images):
        scoring_types = utils.generate_type_list_random(num_pattern)
        # Create an empty black image (all zeros) using NumPy
        image = np.zeros((config.IMAGE_HEIGHT, config.IMAGE_WIDTH, config.IMAGE_CHANNELS), dtype=np.uint8)
        image = cv2.bitwise_not(image)
        fig, ax = plt.subplots()
        ax.imshow(image, origin='upper')
        ax.axis('off')

        file_num = 0
        if not os.path.exists(f"../images/{path}"):
            # Create the directory if it doesn't exist
            os.makedirs(f"../images/{path}")
        else:
            file_num = len(os.listdir(f"../images/{path}"))
        score = transform.get_score(scoring_types)
        if score not in folder_files:
            folder_files[score] = file_num
        else:
            folder_files[score] += 1
        # record metadata
        # record log
        image_name = f"{prefix}_{score}_{file_num}.jpg"
        Logger().record_metafile(path, image_name, scoring_types)
        Logger().record_txtfile(f"images/{path}/{image_name}", scoring_types)

        # start drawing the shape
        if num_pattern >= 1:
            Logger().record_detail(f"big rectangle type {config.score_map[scoring_types[0]]}")
            print(f"big rectangle type {scoring_types[0]}")
            drawer.draw_big_rectangle(scoring_types[0], image)

        if num_pattern >= 2:
            Logger().record_detail(f"big cross type {config.score_map[scoring_types[1]]}")
            print(f"big cross type{scoring_types[1]}")
            drawer.draw_big_cross(scoring_types[1], image)

        if num_pattern >= 3:
            Logger().record_detail(f"horizontal middle line type {config.score_map[scoring_types[2]]}")
            print(f"horizontal middle line type {scoring_types[2]}")
            drawer.draw_horizontal_midline(scoring_types[2], image)

        if num_pattern >= 4:
            Logger().record_detail(f"vertical middle line type{config.score_map[scoring_types[3]]}")
            print(f"vertical middle line type{scoring_types[3]}")
            drawer.draw_vertical_midline(scoring_types[3], image)

        if num_pattern >= 5:
            Logger().record_detail(f"small rectangle with cross type{config.score_map[scoring_types[4]]}")
            print(f"small rectangle with cross type{scoring_types[4]}")
            drawer.draw_small_rectangle(scoring_types[4], image)
        if num_pattern >= 6:
            Logger().record_detail(f"horizontal small line type{config.score_map[scoring_types[5]]}")
            print(f"horizontal small line type{scoring_types[5]}")
            drawer.draw_HORIZONTAL_SMALL_LINE(scoring_types[5])

        if num_pattern >= 7:
            Logger().record_detail(f"four parallel lines type{config.score_map[scoring_types[6]]}")
            print(f"four parallel lines type{scoring_types[6]}")
            drawer.draw_FOUR_PARALLEL_LINE(scoring_types[6])

        if num_pattern >= 8:
            Logger().record_detail(f"small rectangle type{config.score_map[scoring_types[7]]}")
            print(f"small rectangle type{scoring_types[7]}")
            drawer.draw_SMALL_TRIANGLE(scoring_types[7])

        if num_pattern >= 9:
            Logger().record_detail(f"small vertical line type{config.score_map[scoring_types[8]]}")
            print(f"small vertical line type{scoring_types[8]}")
            drawer.draw_VERTICAL_SMALL_LINE(scoring_types[8])

        if num_pattern >= 10:
            Logger().record_detail(f"circle type{config.score_map[scoring_types[9]]}")
            print(f"circle type{scoring_types[9]}")
            drawer.draw_circle(scoring_types[9])

        if num_pattern >= 11:
            Logger().record_detail(f"FIVE_PARALLEL_LINE type{config.score_map[scoring_types[10]]}")
            print(f"FIVE_PARALLEL_LINE type{scoring_types[10]}")
            drawer.draw_FIVE_PARALLEL_LINE(scoring_types[10])

        if num_pattern >= 12:
            Logger().record_detail(f"draw_RIGHT_JOIN_LINE type{config.score_map[scoring_types[11]]}")
            print(f"draw_RIGHT_JOIN_LINE type{scoring_types[11]}")
            drawer.draw_RIGHT_JOIN_LINE(scoring_types[11])

        if num_pattern >= 13:
            Logger().record_detail(f"draw_RHOMBUS type{config.score_map[scoring_types[12]]}")
            print(f"draw_RHOMBUS type{scoring_types[12]}")
            drawer.draw_RHOMBUS(scoring_types[12])

        if num_pattern >= 14:
            Logger().record_detail(f"draw_VERTICAL_RIGHT_LINE type{config.score_map[scoring_types[13]]}")
            print(f"draw_VERTICAL_RIGHT_LINE type{scoring_types[13]}")
            drawer.draw_VERTICAL_RIGHT_LINE(scoring_types[13])

        if num_pattern >= 15:
            Logger().record_detail(f"draw_HORIZENTAL_RIGHT_LINE type{config.score_map[scoring_types[14]]}")
            print(f"draw_HORIZENTAL_RIGHT_LINE type{scoring_types[14]}")
            drawer.draw_HORIZENTAL_RIGHT_LINE(scoring_types[14])

        if num_pattern >= 16:
            Logger().record_detail(f"draw_BOTTOM_RECTANGLE type{config.score_map[scoring_types[15]]}")
            print(f"draw_BOTTOM_RECTANGLE type{scoring_types[15]}")
            drawer.draw_BOTTOM_RECTANGLE(scoring_types[15])

        if num_pattern >= 17:
            Logger().record_detail(f"draw_HORIZENTAL_CROSS type{config.score_map[scoring_types[16]]}")
            print(f"draw_HORIZENTAL_CROSS type{scoring_types[16]}")
            drawer.draw_HORIZENTAL_CROSS(scoring_types[16])

        if num_pattern >= 18:
            Logger().record_detail(f"draw_VERTICAL_CROSS type{config.score_map[scoring_types[17]]}")
            print(f"draw_VERTICAL_CROSS type{scoring_types[17]}")
            drawer.draw_VERTICAL_CROSS(scoring_types[17])

        plt.savefig(f'../images/{path}/{image_name}')

    # # plt.show()

def generate_by_onetype(scoring_types,num_images, path, num_pattern=18):
    folder_files = {}
    for num in range(num_images):
        # Create an empty black image (all zeros) using NumPy
        image = np.zeros((config.IMAGE_HEIGHT, config.IMAGE_WIDTH, config.IMAGE_CHANNELS), dtype=np.uint8)
        image = cv2.bitwise_not(image)
        fig, ax = plt.subplots()
        ax.imshow(image, origin='upper')
        ax.axis('off')


        file_num = 0
        if not os.path.exists(f"../images/{path}"):
            # Create the directory if it doesn't exist
            os.makedirs(f"../images/{path}")
        else:
            file_num = len(os.listdir(f"../images/{path}"))
        score = transform.get_score(scoring_types)
        if score not in folder_files:
            folder_files[score] = file_num
        else:
            folder_files[score] += 1
        # record metadata
        # record log
        image_name = f"onetype_{score}_{file_num}.jpg"
        Logger().record_metafile(path, image_name, scoring_types)
        Logger().record_txtfile(f"images/{path}/{image_name}", scoring_types)

        # start drawing the shape
        if num_pattern >= 1:
            Logger().record_detail(f"big rectangle type {config.score_map[scoring_types[0]]}")
            drawer.draw_big_rectangle(scoring_types[0], image)

        if num_pattern >= 2:
            Logger().record_detail(f"big cross type {config.score_map[scoring_types[1]]}")
            drawer.draw_big_cross(scoring_types[1], image)

        if num_pattern >= 3:
            Logger().record_detail(f"horizontal middle line type {config.score_map[scoring_types[2]]}")
            drawer.draw_horizontal_midline(scoring_types[2], image)

        if num_pattern >= 4:
            Logger().record_detail(f"vertical middle line type{config.score_map[scoring_types[3]]}")
            drawer.draw_vertical_midline(scoring_types[3], image)

        if num_pattern >= 5:
            Logger().record_detail(f"small rectangle with cross type{config.score_map[scoring_types[4]]}")
            drawer.draw_small_rectangle(scoring_types[4], image)

        if num_pattern >= 6:
            Logger().record_detail(f"horizontal small line type{config.score_map[scoring_types[5]]}")
            drawer.draw_HORIZONTAL_SMALL_LINE(scoring_types[5])

        if num_pattern >= 7:
            Logger().record_detail(f"four parallel lines type{config.score_map[scoring_types[6]]}")
            drawer.draw_FOUR_PARALLEL_LINE(scoring_types[6])

        if num_pattern >= 8:
            Logger().record_detail(f"small rectangle type{config.score_map[scoring_types[7]]}")
            drawer.draw_SMALL_TRIANGLE(scoring_types[7])

        if num_pattern >= 9:
            Logger().record_detail(f"small vertical line type{config.score_map[scoring_types[8]]}")
            drawer.draw_VERTICAL_SMALL_LINE(scoring_types[8])

        if num_pattern >= 10:
            Logger().record_detail(f"circle type{config.score_map[scoring_types[9]]}")
            drawer.draw_circle(scoring_types[9])

        if num_pattern >= 11:
            Logger().record_detail(f"FIVE_PARALLEL_LINE type{config.score_map[scoring_types[10]]}")
            drawer.draw_FIVE_PARALLEL_LINE(scoring_types[10])

        if num_pattern >= 12:
            Logger().record_detail(f"draw_RIGHT_JOIN_LINE type{config.score_map[scoring_types[11]]}")
            drawer.draw_RIGHT_JOIN_LINE(scoring_types[11])

        if num_pattern >= 13:
            Logger().record_detail(f"draw_RHOMBUS type{config.score_map[scoring_types[12]]}")
            drawer.draw_RHOMBUS(scoring_types[12])

        if num_pattern >= 14:
            Logger().record_detail(f"draw_VERTICAL_RIGHT_LINE type{config.score_map[scoring_types[13]]}")
            drawer.draw_VERTICAL_RIGHT_LINE(scoring_types[13])

        if num_pattern >= 15:
            Logger().record_detail(f"draw_HORIZENTAL_RIGHT_LINE type{config.score_map[scoring_types[14]]}")
            drawer.draw_HORIZENTAL_RIGHT_LINE(scoring_types[14])

        if num_pattern >= 16:
            Logger().record_detail(f"draw_BOTTOM_RECTANGLE type{config.score_map[scoring_types[15]]}")
            drawer.draw_BOTTOM_RECTANGLE(scoring_types[15])

        if num_pattern >= 17:
            Logger().record_detail(f"draw_HORIZENTAL_CROSS type{config.score_map[scoring_types[16]]}")
            drawer.draw_HORIZENTAL_CROSS(scoring_types[16])

        if num_pattern >= 18:
            Logger().record_detail(f"draw_VERTICAL_CROSS type{config.score_map[scoring_types[17]]}")
            drawer.draw_VERTICAL_CROSS(scoring_types[17])

        plt.savefig(f'../images/{path}/{image_name}')


def generate_specific_type_test(num_images=10):
    big_rec = 2
    big_cross = 4
    horizontal_midline = 4
    vertical_midline = 4
    smallrec_cross = 4
    horizontal_small_line = 2
    four_para_line = 1
    small_triangle = 1
    vertical_small_line = 2
    circle = 1
    five_para_line = 1
    right_join_line = 2
    rhombus = 1
    right_vertical_line = 2
    right_horizontal_line = 2
    bottom_rec = 1
    horizontal_cross = 1
    vertical_cross = 1
    score_type = [big_rec, big_cross, horizontal_midline, vertical_midline, smallrec_cross,
                  horizontal_small_line, four_para_line, small_triangle, vertical_small_line,
                  circle, five_para_line, right_join_line, rhombus, right_vertical_line,
                  right_horizontal_line, bottom_rec, horizontal_cross, vertical_cross]
    score_type = [1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3]
    score_type = [score + 1 for score in score_type]


    generate_by_onetype(score_type, num_images, "train")

def generate_all_test_200():
    generate_all_by_score(3, "200/train", 18)
    # generate_all_by_score(30, "20000/test", 18)
    generate_all_by_type(92, "200/train","type", 18)
    # generate_all_by_type(920, "20000/test", 'type', 18)

def generate_all_test_3000():
    generate_all_by_score(50, "3000/train",  18)
    generate_all_by_score(5, "3000/test", 18)
    generate_all_by_type(1200, "3000/train","type", 18)
    generate_all_by_type(120, "3000/test", "type",18)

def generate_5pattern_test_1500():
    generate_all_by_score(100, "1500/train", 5)
    generate_all_by_score(10, "1500/test", 5)
    generate_all_by_type(500, "1500/train", 5)
    generate_all_by_type(50, "1500/test", 5)

def generate_All_test_36():
    generate_all_by_score(1, "36/train", 18)
    # generate_all_by_score(1, "1000/test", 18)
    # generate_all_by_type(500, "1000/train", 18)
    # generate_all_by_type(50, "1000/test", 18)
if __name__ == "__main__":
    # generate_all_test_20000()
    # generate_all_test_1000()
    # generate_5pattern_test_1500()
    # generate_specific_type_test(num_images=20)
    # generate_All_test_36()
    # generate_all_by_type(1, "add", "add", 18)
    generate_all_test_3000()
    # generate_all_by_score(10, "train", 18)
    # generate_specific_type_test(num_images=10)
