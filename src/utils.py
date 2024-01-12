import math
import config
import numpy as np
import random

def generate_type_list_with_sum(score, num_pattern=18):
    list = []
    if score < num_pattern:
        if score // 2 == 0:
            num_2 = 0
        else:
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
        list.append(1)
    for i in range(num_1):
        if np.random.rand() <= 0.5:
            list.append(2)
        else:
            list.append(3)
    for i in range(num_0):
        list.append(4)

    random.shuffle(list)
    # the first pattern can only have value 1, or 2
    if list[0] == 4:
        for i in range(1, num_pattern):
            if list[i] != 4:
                temp = list[i]
                list[i] = 4
                list[0] = temp
                break
    if list[0] == 3:
        list[0] = 2
    return list
def generate_type_list_random(num_pattern=18):
    random_numbers = [random.randint(1, 4) for _ in range(num_pattern)]
    random_numbers[0] = random.randint(1, 2)
    return random_numbers

# if __name__ == "__main__":
#     res = generate_type_list_with_sum(3, 5)
#     print(len(res))
#     for s in res:
#         print(s)
#

def get_point_point_distance(point1, point2):
    return np.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1])**2)

def calculate_intersection_point(line1, line2):
    x1, y1 = line1[0]
    x2, y2 = line1[1]
    x3, y3 = line2[0]
    x4, y4 = line2[1]

    if x1 == x2 and x3 == x4:#parallel
        x_int = -1
        y_int = -1
    # Check if the lines are vertical (x2 equals x1)
    elif x1 == x2:
        m2 = (y4 - y3) / (x4 - x3)
        x_int = x1
        y_int = m2 * (x_int - x3) + y3
    elif x3 == x4:
        m1 = (y2 - y1) / (x2 - x1)
        x_int = x3
        y_int = m1 * (x_int - x1) + y1
    else:
        # Calculate slopes
        m1 = (y2 - y1) / (x2 - x1)
        m2 = (y4 - y3) / (x4 - x3)

        # Calculate y-intercepts
        b1 = y1 - m1 * x1
        b2 = y3 - m2 * x3
        if m1 == m2:#horizental parallel
            x_int = -1
            y_int = -1
        else:
            # Calculate intersection point
            x_int = (b2 - b1) / (m1 - m2)
            y_int = m1 * x_int + b1

    return int(x_int), int(y_int)
def calculate_point_line_distance(point, line):
    x, y = point
    x1, y1 = line[0]
    x2, y2 = line[1]

    # Calculate line coefficients
    A = y2 - y1
    B = x1 - x2
    C = x2 * y1 - x1 * y2

    # Calculate distance
    distance = abs(A * x + B * y + C) / math.sqrt(A ** 2 + B ** 2)

    return distance

def get_inscribed_circle(triangle):
    # Extract vertices of the triangle
    v1, v2, v3 = triangle
    A = np.array([v1[0], v1[1]])
    B = np.array([v2[0], v2[1]])
    C = np.array([v3[0], v3[1]])

    # Lengths of sides
    a = np.linalg.norm(B - C)
    b = np.linalg.norm(C - A)
    c = np.linalg.norm(A - B)

    # Semiperimeter
    s = (a + b + c) / 2

    # Inradius
    inradius = np.sqrt((s - a) * (s - b) * (s - c) / s)

    # Calculate angles
    alpha = np.arccos((b**2 + c**2 - a**2) / (2 * b * c))
    beta = np.arccos((c**2 + a**2 - b**2) / (2 * c * a))
    gamma = np.arccos((a**2 + b**2 - c**2) / (2 * a * b))

    # Incenter
    incenter = ((a * A + b * B + c * C) / (a + b + c))

    return incenter, int(inradius)

def get_mid_point(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return int((x1 + x2)/2), int((y1 + y2)/2)

def is_missing(line):
    x1, y1 = line[0]
    x2, y2 = line[1]
    if x1 == -1 and x2 == -1:
        return True
def count_missing_lines(lines):
    count = 0
    for line in lines:
        if is_missing(line):
            count += 1
    return count

def update_corners_bigrec(lines):
    num_miss_line = count_missing_lines(lines)
    intersections = []
    # update the points of the big rectangle
    if num_miss_line == 1 or num_miss_line == 0:
        for i, line in enumerate(lines):
            j = i + 1
            if i == 3:
                j = 0
            if is_missing(line):
                intersection = lines[j][0]
            elif is_missing(lines[j]):
                intersection = line[1]
            else:
                intersection = calculate_intersection_point(line, lines[j])
            intersections.append(intersection)
    else:# two lines are missing
        indexs = []
        two_lines = []
        for i, line in enumerate(lines):
            if not is_missing(line):
                indexs.append(i)
                two_lines.append(line)
        if indexs[1] - indexs[0] == 2:#parallel lines
            intersections.append(two_lines[0][0])
            intersections.append(two_lines[1][0])
            intersections.append(two_lines[0][1])
            intersections.append(two_lines[1][1])
        elif indexs[1] - indexs[0] == 1:#adjacent lines
            intersections.append(calculate_intersection_point(two_lines[0], two_lines[1]))
            intersections.append(two_lines[0][0])
            intersections.append(two_lines[1][1])
            if indexs[0] == 1:
                intersections.append((two_lines[1][1][0],two_lines[0][0][1]))
            else:
                intersections.append((two_lines[0][0][0], two_lines[1][1][1]))
        elif indexs[1] - indexs[0] ==3: # the first and the last lines
            intersections.append(calculate_intersection_point(two_lines[0], two_lines[1]))
            intersections.append(two_lines[0][1])
            intersections.append(two_lines[1][0])
            intersections.append((two_lines[0][1][0], two_lines[1][0][1]))
    upper_left, upper_right, lower_left, lower_right = find_rectangle_corners(intersections)
    # update the points of the big rectangle

    config.POINTS_DIC['bigrec_up_left'] = upper_left
    config.POINTS_DIC['bigrec_up_right'] = upper_right
    config.POINTS_DIC['bigrec_down_left'] = lower_left
    config.POINTS_DIC['bigrec_down_right'] = lower_right

def update_corners_bigcross(lines):
    if is_missing(lines[0]):
        config.POINTS_DIC['bigcross_up_left'] = config.POINTS_DIC['bigrec_up_left']
        config.POINTS_DIC['bigcross_down_right'] = config.POINTS_DIC['bigrec_down_right']
    else:
        #update the left uppper
        rec_lines = [config.BIG_RECTANGLE[0], config.BIG_RECTANGLE[3]]
        intersection_0, intersection_1 = compute_bigcross_bigrec_inter(rec_lines, lines[0])
        if intersection_0 == (-1, -1) and intersection_1 == (-1, -1):
            config.POINTS_DIC['bigcross_up_left'] = lines[0][0]
        elif intersection_1 == (-1, -1):
            config.POINTS_DIC['bigcross_up_left'] = intersection_0
        elif intersection_0 == (-1, -1):
            config.POINTS_DIC['bigcross_up_left'] = intersection_1
        else:
            config.POINTS_DIC['bigcross_up_left'] = get_bigx_bigy(intersection_0,intersection_1)
        # update the down right
        rec_lines = [config.BIG_RECTANGLE[1], config.BIG_RECTANGLE[2]]
        intersection_0, intersection_1 = compute_bigcross_bigrec_inter(rec_lines, lines[0])
        if intersection_0 == (-1, -1) and intersection_1 == (-1, -1):
            config.POINTS_DIC['bigcross_down_right'] = lines[0][1]
        elif intersection_1 == (-1, -1):
            config.POINTS_DIC['bigcross_down_right'] = intersection_0
        elif intersection_0 == (-1, -1):
            config.POINTS_DIC['bigcross_down_right'] = intersection_1
        else:
            config.POINTS_DIC['bigcross_down_right'] = get_smallx_smally(intersection_0, intersection_1)
    if is_missing(lines[1]):
        config.POINTS_DIC['bigcross_up_right'] = config.POINTS_DIC['bigrec_up_right']
        config.POINTS_DIC['bigcross_down_left'] = config.POINTS_DIC['bigrec_down_left']
    else:
        #update the left uppper
        rec_lines = [config.BIG_RECTANGLE[0], config.BIG_RECTANGLE[1]]
        intersection_0, intersection_1 = compute_bigcross_bigrec_inter(rec_lines, lines[1])
        if intersection_0 == (-1, -1) and intersection_1 == (-1, -1):
            config.POINTS_DIC['bigcross_up_right'] = lines[1][0]
        elif intersection_1 == (-1, -1):
            config.POINTS_DIC['bigcross_up_right'] = intersection_0
        elif intersection_0 == (-1, -1):
            config.POINTS_DIC['bigcross_up_right'] = intersection_1
        else:
            config.POINTS_DIC['bigcross_up_right'] = get_smallx_bigy(intersection_0, intersection_1)

        # update the down right
        rec_lines = [config.BIG_RECTANGLE[2], config.BIG_RECTANGLE[3]]
        intersection_0, intersection_1 = compute_bigcross_bigrec_inter(rec_lines, lines[1])
        if intersection_0 == (-1, -1) and intersection_1 == (-1, -1):
            config.POINTS_DIC['bigcross_down_left'] = lines[1][1]
        elif intersection_1 == (-1, -1):
            config.POINTS_DIC['bigcross_down_left'] = intersection_0
        elif intersection_0 == (-1, -1):
            config.POINTS_DIC['bigcross_down_left'] = intersection_1
        else:
            config.POINTS_DIC['bigcross_down_left'] = get_bigx_smally(intersection_0, intersection_1)

    config.POINTS_DIC['bigcross_center'] = calculate_intersection_point([config.POINTS_DIC['bigcross_up_left'], config.POINTS_DIC['bigcross_down_right']], [config.POINTS_DIC['bigcross_down_left'], config.POINTS_DIC['bigcross_up_right']])
def update_horizontal_midline_corner(lines):
    left_line = config.BIG_RECTANGLE[3]
    right_line = config.BIG_RECTANGLE[1]
    if is_missing(lines[0]):
        config.POINTS_DIC['hori_midline_left'] = get_mid_point(config.POINTS_DIC['bigrec_down_left'], config.POINTS_DIC['bigrec_up_left'])
        config.POINTS_DIC['hori_midline_right'] = get_mid_point(config.POINTS_DIC['bigrec_down_right'], config.POINTS_DIC['bigrec_up_right'])
    else:
        if is_missing(config.BIG_RECTANGLE[3]):
            left_line = [config.POINTS_DIC['bigrec_up_left'], config.POINTS_DIC['bigrec_down_left']]
        elif is_missing(config.BIG_RECTANGLE[1]):
            right_line = [config.POINTS_DIC['bigrec_up_right'], config.POINTS_DIC['bigrec_down_right']]
        config.POINTS_DIC['hori_midline_left'] = calculate_intersection_point(lines[0], left_line)
        config.POINTS_DIC['hori_midline_right'] = calculate_intersection_point(lines[0], right_line)

def update_vertical_midline_corner(lines):
    up_line = config.BIG_RECTANGLE[0]
    down_line = config.BIG_RECTANGLE[2]
    if is_missing(lines[0]):
        config.POINTS_DIC['vert_midline_up'] = get_mid_point(config.POINTS_DIC['bigrec_up_right'], config.POINTS_DIC['bigrec_up_left'])
        config.POINTS_DIC['vert_midline_down'] = get_mid_point(config.POINTS_DIC['bigrec_down_right'], config.POINTS_DIC['bigrec_down_left'])
    else:
        if is_missing(config.BIG_RECTANGLE[0]):
            up_line = [config.POINTS_DIC['bigrec_up_left'], config.POINTS_DIC['bigrec_up_right']]
        elif is_missing(config.BIG_RECTANGLE[2]):
            down_line = [config.POINTS_DIC['bigrec_down_left'], config.POINTS_DIC['bigrec_down_right']]
        config.POINTS_DIC['vert_midline_up'] = calculate_intersection_point(lines[0], up_line)
        config.POINTS_DIC['vert_midline_down'] = calculate_intersection_point(lines[0], down_line)

def update_right_triangle_tip(lines):
    if is_missing(lines[0]) and is_missing(lines[1]):
        up_point = config.POINTS_DIC['bigrec_up_right']
        down_point = config.POINTS_DIC['bigrec_down_right']
        mid_point = get_mid_point(up_point, down_point)
        width = up_point[0] - config.POINTS_DIC['bigrec_up_left'][0]
        rand_num = np.random.uniform(1 / 4, 1 / 2)
        config.POINTS_DIC['right_triangle_tip'] = (mid_point[0] + int(width * rand_num), mid_point[1])
    elif is_missing(lines[0]):
        config.POINTS_DIC['right_triangle_tip'] = lines[1][1]
    elif is_missing(lines[1]):
        config.POINTS_DIC['right_triangle_tip'] = lines[0][1]
    else:
        config.POINTS_DIC['right_triangle_tip'] = calculate_intersection_point(lines[0], lines[1])
    if config.POINTS_DIC['right_triangle_tip'][0] < config.POINTS_DIC['hori_midline_right'][0]:
        config.POINTS_DIC['right_triangle_tip'] = (2 * config.POINTS_DIC['hori_midline_right'][0] - config.POINTS_DIC['right_triangle_tip'][0], config.POINTS_DIC['right_triangle_tip'][1])

def update_bottom_rec_down_right(lines):
    if not is_missing(lines[1]) and not is_missing(lines[2]):
        config.POINTS_DIC['bottom_rec_down_right'] = calculate_intersection_point(lines[1], lines[2])
    elif is_missing(lines[1]) and not is_missing(lines[2]):
        if is_missing(lines[4]):
            config.POINTS_DIC['bottom_rec_down_right'] = lines[2][1]
        else:
            config.POINTS_DIC['bottom_rec_down_right'] = calculate_intersection_point(lines[2], lines[4])
    elif is_missing(lines[2]) and not is_missing(lines[1]):
        if is_missing(lines[4]):
            config.POINTS_DIC['bottom_rec_down_right'] = lines[1][1]
        else:
            config.POINTS_DIC['bottom_rec_down_right'] = calculate_intersection_point(lines[1], lines[4])
    else:
        if not is_missing(lines[4]):
            config.POINTS_DIC['bottom_rec_down_right'] = lines[4][1]
        else:
            bottom_rec_topleft = config.POINTS_DIC['bigrec_down_left']
            big_rec_downright = config.POINTS_DIC['bigrec_down_right']
            bottom_rec_topright_x = int(3 * bottom_rec_topleft[0] / 4 + big_rec_downright[0] / 4)
            bottom_rec_topright_y = int(3 * bottom_rec_topleft[1] / 4 + big_rec_downright[1] / 4)
            edge_len = bottom_rec_topright_x - bottom_rec_topleft[0]
            config.POINTS_DIC['bottom_rec_down_right'] = (bottom_rec_topright_x, bottom_rec_topright_y + edge_len)


def compute_bigcross_bigrec_inter(rec_lines, cross_line):
    intersection_0 = (-1, -1)
    intersection_1 = (-1, -1)
    if not is_missing(rec_lines[0]):
        intersection_0 = calculate_intersection_point(rec_lines[0], cross_line)
    if not is_missing(rec_lines[1]):
        intersection_1 = calculate_intersection_point(rec_lines[1], cross_line)
    return intersection_0, intersection_1

def get_bigx_bigy(point1, point2):
    x1, y1 = point1
    x2, y2 = point2

    if x1 >= x2 and y1 >= y2:
        return point1
    elif x2 >= x1 and y2 >= y1:
        return point2
    else:
        # If both points have the same or smaller axes, return None or handle as needed
        return (-1, -1)
def get_smallx_smally(point1, point2):
    x1, y1 = point1
    x2, y2 = point2

    if x1 <= x2 and y1 <= y2:
        return point1
    elif x2 <= x1 and y2 <= y1:
        return point2
    else:
        # If both points have the same or smaller axes, return None or handle as needed
        return (-1, -1)

def get_smallx_bigy(point1, point2):
    x1, y1 = point1
    x2, y2 = point2

    if x1 <= x2 and y1 >= y2:
        return point1
    elif x2 <= x1 and y2 >= y1:
        return point2
    else:
        # If both points have the same or smaller axes, return None or handle as needed
        return (-1, -1)
def get_bigx_smally(point1, point2):
    x1, y1 = point1
    x2, y2 = point2

    if x1 >= x2 and y1 <= y2:
        return point1
    elif x2 >= x1 and y2 <= y1:
        return point2
    else:
        # If both points have the same or smaller axes, return None or handle as needed
        return (-1, -1)

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


def calculate_cover_line_rec(point1, point2, rectangle_width=3):

    angle = np.arctan2(point2[1] - point1[1], point2[0] - point1[0])
    offset_x = 0
    offset_y = 0
    if angle >= -1 * math.pi / 2 and angle <= math.pi / 2:
        # Calculate the offset to create a rectangle around the line
        offset_x = int(np.sin(angle) * rectangle_width)
        offset_y = int(np.cos(angle) * rectangle_width)
    else:
        # Calculate the offset to create a rectangle around the line
        offset_x = int(np.sin(angle + math.pi) * rectangle_width)
        offset_y = int(np.cos(angle + math.pi) * rectangle_width)

    # Calculate the four corners of the rectangle
    rectangle_points = [
        [point1[0] + offset_x, point1[1] - offset_y],
        [point1[0] - offset_x, point1[1] + offset_y],
        [point2[0] - offset_x, point2[1] + offset_y],
        [point2[0] + offset_x, point2[1] - offset_y]]

    return rectangle_points
