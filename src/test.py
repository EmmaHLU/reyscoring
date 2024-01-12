import math
import config
import cv2
import numpy as np
import transform
from logger import Logger
import matplotlib.pyplot as plt
import drawer
from PIL import Image
def test_transformation():

    # Example usage

    lines = [[(100, 100), (200, 100)],
             [(200, 100), (200, 300)],
             [(200, 300), (100, 300)],
             [(100, 300), (100, 100)],
             [(200, 100), (100, 300)],
             [(100, 100), (200, 300)]]
    rotation_angle = 45  # Rotation angle in degrees
    rotation_center = (150, 200)  # Center of rotation

    image1 = np.zeros((config.IMAGE_HEIGHT, config.IMAGE_WIDTH, config.IMAGE_CHANNELS), dtype=np.uint8)
    image1 = cv2.bitwise_not(image1)


    # Rotate the line segment
    new_lines =transform.do_rotation(lines, config.ROTATION_LIMIT, transform.TRANS_TYPE.major)
    for i, new_line in enumerate(new_lines):
        cv2.line(image1, lines[i][0], lines[i][1], (0,0,0), thickness=1)
        cv2.line(image1, new_line[0], new_line[1], (255,0,0), thickness=2)
    #
    # for i, line in enumerate(lines):
    #     new_line = rotate_line_segment(line, 80, rotation_center[0], rotation_center[1])
    #     cv2.line(image1, line[0], line[1], (0,0,0), thickness=1)
    #     cv2.line(image1, new_line[0], new_line[1], (255,0,0), thickness=2)

    cv2.circle(image1, rotation_center, 1, (0,0,0), thickness=3)
    cv2.imshow("image1", image1)
    # cv2.imshow("image2", image2)


    cv2.waitKey(0)
    cv2.destroyAllWindows()

def test_log():
    Logger().record_detail("hello world again")

def find_rectangle_corners(points):
    centroid = [sum(x for x, y in points) / len(points), sum(y for x, y in points) / len(points)]

    for point in points:
        if point[0] <= centroid[0] and point[1] <= centroid[1]:
            upper_left = point
        elif point[0] <= centroid[0] and point[1] >= centroid[1]:
            lower_left = point
        elif point[0] >= centroid[0] and point[1] <= centroid[1]:
            upper_right = point
        elif point[0] >= centroid[0] and point[1] >= centroid[1]:
            lower_right = point
    return upper_left, upper_right, lower_left, lower_right


import random

def generate_type_list_with_sum(score, num_pattern=18):
    list = []
    if score < num_pattern:
        num_2 = np.random.randint(0, score // 2)
        num_1 = score - num_2 * 2
        num_0 = num_pattern - num_1 - num_2
    else:
        if (score - num_pattern) == score // 2:
            num_2 = score // 2
        else:
            num_2 = np.random.randint((score - num_pattern), score // 2)
        num_1 = score - num_2 * 2
        num_0 = num_pattern - num_1 - num_2
    for i in range(num_2):
        list.append(2)
    for i in range(num_1):
        list.append(1)
    for i in range(num_0):
        list.append(0)

    random.shuffle(list)
    return list

# Example usage:
m = 18  # Number of elements in each list
A = 30  # Desired sum of elements in each list

random_lists = generate_type_list_with_sum(A, m)
print(random_lists)
print(sum(random_lists))
