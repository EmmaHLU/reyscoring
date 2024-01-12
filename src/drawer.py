import transform
import config
import utils
import numpy as np
import math
import handdrawing as handline
from logger import Logger
import matplotlib.pyplot as plt


def draw_big_rectangle(score_type, image):
  # global BIG_RECTANGLE
  #update BIG_RECTANGLE randomly
  ratio = np.random.uniform(config.BIGREC_WIDTH_HEIGHT_RATIO[0], config.BIGREC_WIDTH_HEIGHT_RATIO[1])
  height = min(int(config.BIGRECHEIGHT_IMAGEHEIGHT_RATION * config.IMAGE_HEIGHT * (1 + np.random.uniform(-0.03, 0.03))), int (2 * config.IMAGE_WIDTH / (3 * ratio)))
  width = int(height * ratio)
  upleft_x = int(np.random.uniform(440/(ratio * height) * 70, config.IMAGE_WIDTH - (3 * width/2)))
  upleft_y = int(np.random.uniform(ratio * height / 4, config.IMAGE_HEIGHT - height * (1 + ratio/4)))
  # print(f"{ratio}, {height},{width}, {upleft_x}, {upleft_y}")
  BIG_RECTANGLE=[[(upleft_x, upleft_y), (upleft_x + width, upleft_y)],[(upleft_x + width, upleft_y), (upleft_x + width, upleft_y+height)],
                [(upleft_x + width, upleft_y+height), (upleft_x, upleft_y+height)],[(upleft_x, upleft_y+height),(upleft_x, upleft_y)]]
  # print(f"before drawing {BIG_RECTANGLE}")
  new_lines = []
  if score_type == 1:
    new_lines = transform.get_correct_both(BIG_RECTANGLE, 1, config.PIXELS_3)
  elif score_type == 2:
    new_lines = transform.get_correct_place(BIG_RECTANGLE, config.PATTERN.BIG_RECTANGLE)
  else:
    return -1
  # print(new_lines)
  #update the actual points of the four lines
  for i, line in enumerate(new_lines):
    config.BIG_RECTANGLE[i] = line
    Logger().record_detail(f"big rectangle lines {line}")

  # update the points of the big rectangle
  utils.update_corners_bigrec(new_lines)
  for line in new_lines:
    if line[0][0] != -1:#line doesn't exist
        handline.drawLine(line[0], line[1])
  return new_lines
def draw_big_cross(score_type, image):
    # global BIG_CROSS
    #update the lines accroding to the intersections of the big rectangle
    BIG_CROSS = [[config.POINTS_DIC['bigrec_up_left'], config.POINTS_DIC['bigrec_down_right']], [config.POINTS_DIC['bigrec_up_right'],config.POINTS_DIC['bigrec_down_left']]]
    if score_type == 1:
        new_lines = transform.get_correct_both(BIG_CROSS)
    elif score_type == 2:
        new_lines = transform.get_correct_place(BIG_CROSS, pattern_type=config.PATTERN.BIG_CROSS)
    elif score_type == 3:
        new_lines = transform.get_correct_shape(BIG_CROSS, pattern_type=config.PATTERN.BIG_CROSS)
    elif score_type == 4:
        new_lines = transform.get_correct_none(BIG_CROSS, pattern_type=config.PATTERN.BIG_CROSS)
    else:
        return -1
    # config.BIG_CROSS = new_lines
    for i, line in enumerate(new_lines):
        config.BIG_CROSS[i] = line
        Logger().record_detail(f"big cross lines {line}")
    utils.update_corners_bigcross(new_lines)

    for line in new_lines:
        if line[0][0] != -1:  # line doesn't exist
            handline.drawLine(line[0], line[1])
            # x, y = handline.hand_drawn_segment(image, line[0], line[1])
            # plt.plot(x, y, '-o', linewidth=3, markersize=0, color=(0, 0, 0))

    return new_lines

def draw_horizontal_midline(score_type, image):
    # global HORIZONTAL_MIDLINE
    #update the lines accroding to the intersections of the big rectangle
    up_left_x, up_left_y = config.POINTS_DIC['bigrec_up_left']
    down_left_x, down_left_y = config.POINTS_DIC['bigrec_down_left']
    up_right_x, up_right_y = config.POINTS_DIC['bigrec_up_right']
    down_right_x, down_right_y = config.POINTS_DIC['bigrec_down_right']
    left_x = int((up_left_x + down_left_x)/2)
    left_y = int((up_left_y + down_left_y)/2)
    right_x = int((up_right_x + down_right_x)/2)
    right_y = int((up_right_y + down_right_y)/2)
    HORIZONTAL_MIDLINE = [[(left_x,left_y), (right_x,right_y)]]
    if score_type == 1:
        new_lines = transform.get_correct_both(HORIZONTAL_MIDLINE)
    elif score_type == 2:
        new_lines = transform.get_correct_place(HORIZONTAL_MIDLINE, pattern_type=config.PATTERN.HORIZONTAL_MIDLINE)
    elif score_type == 3:
        new_lines = transform.get_correct_shape(HORIZONTAL_MIDLINE)
    elif score_type == 4:
        new_lines = transform.get_correct_none(HORIZONTAL_MIDLINE)
    else:
        return -1
    for i, line in enumerate(new_lines):
        config.HORIZONTAL_MIDLINE[i] = line
        Logger().record_detail(f"horizontal middle line {line}")
    utils.update_horizontal_midline_corner(new_lines)
    for line in new_lines:
        if line[0][0] != -1:  # line doesn't exist
            handline.drawLine(line[0], line[1])
            # x, y = handline.hand_drawn_segment(image, line[0], line[1])
            # plt.plot(x, y, '-o', linewidth=3, markersize=0, color=(0, 0, 0))

def draw_vertical_midline(score_type, image):
    new_coordinations = []
    #update the lines accroding to the intersections of the big rectangle
    up_left_x, up_left_y = config.POINTS_DIC['bigrec_up_left']
    down_left_x, down_left_y = config.POINTS_DIC['bigrec_down_left']
    up_right_x, up_right_y = config.POINTS_DIC['bigrec_up_right']
    down_right_x, down_right_y = config.POINTS_DIC['bigrec_down_right']
    up_x = int((up_left_x + up_right_x)/2)
    up_y = int((up_left_y + up_right_y)/2)
    down_x = int((down_left_x + down_right_x)/2)
    down_y = int((down_left_y + down_right_y)/2)
    VERTICAL_MIDELINE = [[(up_x,up_y), (down_x,down_y)]]
    if score_type == 1:
        new_lines = transform.get_correct_both(VERTICAL_MIDELINE)
    elif score_type == 2:
        new_lines = transform.get_correct_place(VERTICAL_MIDELINE, pattern_type=config.PATTERN.VERTICAL_MIDELINE)
    elif score_type == 3:
        new_lines = transform.get_correct_shape(VERTICAL_MIDELINE)
    elif score_type == 4:
        new_lines = transform.get_correct_none(VERTICAL_MIDELINE)
    else:
        return -1
    for i, line in enumerate(new_lines):
        config.VERTICAL_MIDELINE[i] = line
        Logger().record_detail(f"vertical middle line: {line}")
    utils.update_vertical_midline_corner(new_lines)
    for line in new_lines:
        if line[0][0] != -1:  # line doesn't exist
            handline.drawLine(line[0], line[1])
            # x, y = handline.hand_drawn_segment(image, line[0], line[1])
            # plt.plot(x, y, '-o', linewidth=3, markersize=0, color=(0, 0, 0))

def draw_small_rectangle(score_type, image):
    #update the lines accroding to the intersections of the big rectangle
    rec_left_line = config.BIG_RECTANGLE[3]
    cross_line_1 = config.BIG_CROSS[0]
    cross_line_2 = config.BIG_CROSS[1]
    if utils.is_missing(rec_left_line):
        rec_left_line = [config.POINTS_DIC['bigrec_down_left'], config.POINTS_DIC['bigrec_up_left']]
    if utils.is_missing(cross_line_1):
        cross_line_1 = [config.POINTS_DIC['bigcross_up_left'], config.POINTS_DIC['bigcross_down_right']]
    if utils.is_missing(cross_line_2):
        cross_line_2 = [config.POINTS_DIC['bigcross_up_right'], config.POINTS_DIC['bigcross_down_left']]
    range_up = rec_left_line[1]
    range_down = rec_left_line[0]
    if range_up[1] < config.POINTS_DIC['bigcross_up_left'][1]:
        range_up = config.POINTS_DIC['bigcross_up_left']
    if range_down[1] > config.POINTS_DIC['bigcross_down_left'][1]:
        range_down = config.POINTS_DIC['bigcross_down_left']
    up_left_x = int((3 * config.POINTS_DIC['bigrec_up_left'][0] + config.POINTS_DIC['bigrec_down_left'][0]) / 4)
    up_left_y = int((3 * range_up[1] + range_down[1]) / 4)
    up_left = (up_left_x, up_left_y)
    up_right = utils.calculate_intersection_point([(up_left_x, up_left_y), (up_left_x + config.PIXELS_12, up_left_y)], cross_line_1)
    down_right = utils.calculate_intersection_point([(up_right), (up_right[0], up_right[1] + config.PIXELS_12)], cross_line_2)
    down_left = utils.calculate_intersection_point([(down_right), (down_right[0] - config.PIXELS_12, down_right[1])], rec_left_line)
    SMALL_RECTANGLE_CROSS = [[up_left, (up_right)], [(up_right), (down_right)],
                             [(down_right), down_left], [down_left, up_left],[up_left, (down_right)],
                             [(up_right), (down_left)]]
    if score_type == 1:
        new_lines = transform.get_correct_both(SMALL_RECTANGLE_CROSS)
    elif score_type == 2:
        new_lines = transform.get_correct_place(SMALL_RECTANGLE_CROSS, pattern_type=config.PATTERN.SMALL_RECTANGLE_CROSS)
    elif score_type == 3:
        new_lines = transform.get_correct_shape(SMALL_RECTANGLE_CROSS)
    elif score_type == 4:
        new_lines = transform.get_correct_none(SMALL_RECTANGLE_CROSS)
    else:
        return -1
    for i, line in enumerate(new_lines):
        config.SMALL_RECTANGLE_CROSS[i] = line
        Logger().record_detail(f"small rectangle with cross lines: {line}")
    for line in new_lines:
        if line[0][0] != -1:  # line doesn't exist
            handline.drawLine(line[0], line[1])
            # x, y = handline.hand_drawn_segment(image, line[0], line[1])
            # plt.plot(x, y, '-o', linewidth=3, markersize=0, color=(0,0,0))


def draw_HORIZONTAL_SMALL_LINE(score_type):
    up_y = max(config.POINTS_DIC['bigrec_up_left'][1], config.POINTS_DIC['bigcross_up_left'][1])
    up_x = config.POINTS_DIC['bigrec_up_left'][0]

    rec_left_line = config.BIG_RECTANGLE[3]
    cross_line = config.BIG_CROSS[0]
    small_rec_up_line_y = config.SMALL_RECTANGLE_CROSS[0][0][1]
    if utils.is_missing(rec_left_line):
        rec_left_line = [config.POINTS_DIC['bigrec_down_left'], config.POINTS_DIC['bigrec_up_left']]
    if utils.is_missing(cross_line):
        cross_line = [config.POINTS_DIC['bigcross_up_left'], config.POINTS_DIC['bigcross_down_right']]
    if utils.is_missing(config.SMALL_RECTANGLE_CROSS[0]):
        range_down = rec_left_line[0]
        if range_down[1] > config.POINTS_DIC['bigcross_down_left'][1]:
            range_down = config.POINTS_DIC['bigcross_down_left']
        small_rec_up_line_y = int((3 * up_y + range_down[1]) / 4)

    delta_y = small_rec_up_line_y - up_y
    left_point_x = up_x
    left_point_y = up_y + int(np.random.uniform(1/2, 3/4) * delta_y)
    left_point = utils.calculate_intersection_point([(left_point_x,left_point_y),(left_point_x + 20,left_point_y)], rec_left_line)
    right_point = utils.calculate_intersection_point([(left_point_x,left_point_y),(left_point_x + 20,left_point_y)], cross_line)
    HORIZONTAL_SMALL_LINE = [[left_point, right_point]]
    if score_type == 1:
        new_lines = transform.get_correct_both(HORIZONTAL_SMALL_LINE, limit=config.PIXELS_3/2)
    elif score_type == 2:
        new_lines = transform.get_correct_place(HORIZONTAL_SMALL_LINE, pattern_type=config.PATTERN.HORIZONTAL_SMALL_LINE)
    elif score_type == 3:
        new_lines = transform.get_correct_shape(HORIZONTAL_SMALL_LINE)
    elif score_type == 4:
        new_lines = transform.get_correct_none(HORIZONTAL_SMALL_LINE)
    else:
        return -1
    for i, line in enumerate(new_lines):
        config.HORIZONTAL_SMALL_LINE[i] = line
        Logger().record_detail(f"horizontal small line: {line}")
    for line in new_lines:
        if line[0][0] != -1:  # line doesn't exist
            handline.drawLine(line[0], line[1])

def draw_FOUR_PARALLEL_LINE(score_type):
    cross_line = config.BIG_CROSS[0]
    vertical_line = config.VERTICAL_MIDELINE[0]
    if utils.is_missing(cross_line):
        cross_line = [config.POINTS_DIC['bigcross_up_left'], config.POINTS_DIC['bigcross_down_right']]
    if utils.is_missing(vertical_line):
        vertical_line = [config.POINTS_DIC['vert_midline_up'], config.POINTS_DIC['vert_midline_down']]
    cross_vertical_inter = utils.calculate_intersection_point(cross_line, vertical_line)
    delta_y = int((cross_vertical_inter[1] - config.POINTS_DIC['vert_midline_up'][1]) /5)
    FOUR_PARALLEL_LINE = []
    for i in range(4):
        y = config.POINTS_DIC['vert_midline_up'][1] + delta_y * (i + 1)
        if not utils.is_missing(config.HORIZONTAL_SMALL_LINE[0]) and y == config.HORIZONTAL_SMALL_LINE[0][1]:
            y += np.random.randint(config.PIXELS_3/2, delta_y - config.PIXELS_3/2)
        line = [(0, y), (20, y)]
        left_inter = utils.calculate_intersection_point(line, cross_line)
        right_inter = utils.calculate_intersection_point(line, vertical_line)
        if left_inter[0] < config.POINTS_DIC['bigrec_up_left'][0]:
            x = config.POINTS_DIC['bigrec_up_left'][0]
            y = left_inter[1]
            left_inter = (x, y)
        FOUR_PARALLEL_LINE.append([left_inter, right_inter])
    if score_type == 1:
        new_lines = transform.get_correct_both(FOUR_PARALLEL_LINE, limit=config.PIXELS_3/2)
    elif score_type == 2:
        new_lines = transform.get_correct_place(FOUR_PARALLEL_LINE, pattern_type=config.PATTERN.FOUR_PARALLEL_LINE, limit_shape=config.PIXELS_3/2)
    elif score_type == 3:
        new_lines = transform.get_correct_shape(FOUR_PARALLEL_LINE)
    elif score_type == 4:
        new_lines = transform.get_correct_none(FOUR_PARALLEL_LINE)
    else:
        return -1
    for i, line in enumerate(new_lines):
        config.FOUR_PARALLEL_LINE[i] = line
        Logger().record_detail(f"four parallel lines: {line}")
    for line in new_lines:
        if line[0][0] != -1:  # line doesn't exist
            handline.drawLine(line[0], line[1])

def draw_SMALL_TRIANGLE(score_type):
    bigrec_up_line = config.BIG_RECTANGLE[0]
    if utils.is_missing(bigrec_up_line):
        bigrec_up_line = [config.POINTS_DIC['bigrec_up_left'], config.POINTS_DIC['bigrec_up_right']]
    mid_point = utils.get_mid_point(bigrec_up_line[0], bigrec_up_line[1])
    right_point = bigrec_up_line[1]
    width = right_point[0] - mid_point[0]
    top_point = (mid_point[0], max(0, mid_point[1] - int (width/2)))
    SMALL_TRIANGLE = [[top_point, mid_point], [mid_point, right_point], [right_point, top_point]]
    if score_type == 1:
        new_lines = transform.get_correct_both(SMALL_TRIANGLE)
    elif score_type == 2:
        new_lines = transform.get_correct_place(SMALL_TRIANGLE, pattern_type=config.PATTERN.SMALL_TRIANGLE)
    elif score_type == 3:
        new_lines = transform.get_correct_shape(SMALL_TRIANGLE)
    elif score_type == 4:
        new_lines = transform.get_correct_none(SMALL_TRIANGLE)
    else:
        return -1
    for i, line in enumerate(new_lines):
        config.SMALL_TRIANGLE[i] = line
        Logger().record_detail(f"small triangle lines {line}")
    for line in new_lines:
        if line[0][0] != -1:  # line doesn't exist
            handline.drawLine(line[0], line[1])

def draw_VERTICAL_SMALL_LINE(score_type):
    bigrec_up_line = config.BIG_RECTANGLE[0]
    cross_line = config.BIG_CROSS[1]
    if utils.is_missing(bigrec_up_line):
        bigrec_up_line = [config.POINTS_DIC['bigrec_up_left'], config.POINTS_DIC['bigrec_up_right']]
    if utils.is_missing(cross_line):
        cross_line = [config.POINTS_DIC['bigcross_up_right'], config.POINTS_DIC['bigcross_down_left']]

    mid_point = utils.get_mid_point(bigrec_up_line[0], bigrec_up_line[1])
    x = np.random.randint(mid_point[0] + config.PIXELS_3, utils.get_mid_point(bigrec_up_line[1],mid_point)[0])
    up_inter = utils.calculate_intersection_point(bigrec_up_line, [(x, 0), (x, 10)])
    down_inter = utils.calculate_intersection_point(cross_line, [(x, 0), (x, 10)])
    VERTICAL_SMALL_LINE = [[up_inter, down_inter]]
    if score_type == 1:
        new_lines = transform.get_correct_both(VERTICAL_SMALL_LINE, limit=config.PIXELS_3/2)
    elif score_type == 2:
        new_lines = transform.get_correct_place(VERTICAL_SMALL_LINE, pattern_type=config.PATTERN.VERTICAL_SMALL_LINE)
    elif score_type == 3:
        new_lines = transform.get_correct_shape(VERTICAL_SMALL_LINE)
    elif score_type == 4:
        new_lines = transform.get_correct_none(VERTICAL_SMALL_LINE)
    else:
        return -1
    for i, line in enumerate(new_lines):
        config.VERTICAL_SMALL_LINE[i] = line
        Logger().record_detail(f"vertical small line: {line}")
    for line in new_lines:
        if line[0][0] != -1:  # line doesn't exist
            handline.drawLine(line[0], line[1])

def draw_circle(score_type):
    cross_line = config.BIG_CROSS[1]
    horizontal_midline = config.HORIZONTAL_MIDLINE[0]
    rec_right_line = config.BIG_RECTANGLE[1]
    if utils.is_missing(cross_line):
        cross_line = [config.POINTS_DIC['bigcross_up_right'], config.POINTS_DIC['bigcross_down_left']]
    if utils.is_missing(horizontal_midline):
        horizontal_midline = [config.POINTS_DIC['hori_midline_left'], config.POINTS_DIC['hori_midline_right']]
    if utils.is_missing(rec_right_line):
        rec_right_line = [config.POINTS_DIC['bigrec_up_right'], config.POINTS_DIC['bigrec_down_right']]
    top_vertice = utils.calculate_intersection_point(cross_line,rec_right_line)
    left_vertice = utils.calculate_intersection_point(cross_line, horizontal_midline)
    right_vertice = utils.calculate_intersection_point(horizontal_midline, rec_right_line)
    center_, r = utils.get_inscribed_circle([top_vertice, left_vertice, right_vertice])
    center = (int(center_[0]), int(center_[1]))
    r = r - config.PIXELS_3
    angle = np.random.uniform(math.pi/6, 5 * math.pi / 12)
    distance = r * np.random.uniform(1/2, 2/3)
    x_delta = int(distance * np.cos(angle))
    y_delta = int(distance * np.sin(angle))
    points = []
    points.append([center, center])
    points.append([(center[0] - x_delta, center[1] - y_delta), (center[0] - x_delta, center[1] - y_delta)])
    points.append([(center[0] + x_delta, center[1] - y_delta), (center[0] + x_delta, center[1] - y_delta)])
    # Do some transformation....
    new_center, new_points, new_radius = do_circle_transform(center, points, r, score_type)
    print(f'new-center: {new_center}')
    Logger().record_detail(f"circle center: {new_center}")
    Logger().record_detail(f"circle radius: {new_radius}")
    Logger().record_detail(f"circle points: {new_points}")

    if new_center != (-1, -1):
        handline.draw_circle(new_center, new_radius)
    for i in range(len(new_points)):
        if new_points[i][0] != (-1, -1):
            handline.drawLine(new_points[i][0], new_points[i][1])

def draw_FIVE_PARALLEL_LINE(score_type):
    cross_line = [config.POINTS_DIC['bigcross_center'], config.POINTS_DIC['bigcross_down_right']]
    rand_num = np.random.uniform(1/8, 1/3)
    up_middle_point_x = int(cross_line[0][0] + rand_num * (cross_line[1][0] - cross_line[0][0]))
    up_middle_point_y = int(cross_line[0][1] + rand_num * (cross_line[1][1] - cross_line[0][1]))
    down_middle_point_x = int(cross_line[0][0] + (1 - rand_num) * (cross_line[1][0] - cross_line[0][0]))
    down_middle_point_y = int(cross_line[0][1] + (1- rand_num) * (cross_line[1][1] - cross_line[0][1]))
    rec_points = utils.calculate_cover_line_rec((up_middle_point_x,up_middle_point_y), (down_middle_point_x, down_middle_point_y), np.random.randint(20, 30))
    first_line = [rec_points[0], rec_points[1]]
    fifth_line = [rec_points[3], rec_points[2]]
    third_line = [utils.get_mid_point(first_line[0], fifth_line[0]), utils.get_mid_point(first_line[1], fifth_line[1])]
    secod_line = [utils.get_mid_point(first_line[0], third_line[0]), utils.get_mid_point(first_line[1], third_line[1])]
    forth_line = [utils.get_mid_point(fifth_line[0], third_line[0]), utils.get_mid_point(fifth_line[1], third_line[1])]
    FIVE_PARALLEL_LINE = [first_line, secod_line, third_line, forth_line, fifth_line]
    # new_lines = do_transform(FIVE_PARALLEL_LINE, score_type,pattern_type=config.PATTERN.FIVE_PARALLEL_LINE)
    if score_type == 1:
        new_lines = transform.get_correct_both(FIVE_PARALLEL_LINE)
    elif score_type == 2:
        new_lines = transform.get_correct_place(FIVE_PARALLEL_LINE, pattern_type=config.PATTERN.FIVE_PARALLEL_LINE)
    elif score_type == 3:
        new_lines = transform.get_correct_shape(FIVE_PARALLEL_LINE,limit = config.PIXELS_6)
    elif score_type == 4:
        new_lines = transform.get_correct_none(FIVE_PARALLEL_LINE)
    else:
        return -1
    for i, line in enumerate(new_lines):
        config.FIVE_PARALLEL_LINE[i] = line
        Logger().record_detail(f"five parallel lines: {line}")
    for line in new_lines:
        if line[0][0] != -1:  # line doesn't exist
            handline.drawLine(line[0], line[1])

def draw_RIGHT_JOIN_LINE(score_type):
    up_point = config.POINTS_DIC['bigrec_up_right']
    down_point = config.POINTS_DIC['bigrec_down_right']
    mid_point = utils.get_mid_point(up_point, down_point)
    width = up_point[0] - config.POINTS_DIC['bigrec_up_left'][0]
    rand_num = np.random.uniform(1 / 4, 1 / 2)
    right_point = (min(config.IMAGE_WIDTH - config.PIXELS_6, mid_point[0] + int(width * rand_num)), mid_point[1])
    RIGHT_JOIN_LINE = [[up_point, right_point], [down_point, right_point]]
    new_lines = do_transform(RIGHT_JOIN_LINE, score_type,pattern_type=config.PATTERN.RIGHT_JOIN_LINE)
    utils.update_right_triangle_tip(new_lines)
    for i, line in enumerate(new_lines):
        config.RIGHT_JOIN_LINE[i] = line
        Logger().record_detail(f"right join lines: {line}")
    for line in new_lines:
        if line[0][0] != -1:  # line doesn't exist
            handline.drawLine(line[0], line[1])

def draw_RHOMBUS(score_type):
    up_point = config.POINTS_DIC['right_triangle_tip']
    rec_height = config.POINTS_DIC['bigrec_down_right'][1] -config.POINTS_DIC['bigrec_up_right'][1]
    rhombus_height = int (rec_height * np.random.uniform(1/4, 1/2))
    down_point = (up_point[0], up_point[1] + rhombus_height)
    rhombus_width = int(rhombus_height * np.random.uniform(1/5, 1/3))
    if not utils.is_missing(config.RIGHT_JOIN_LINE[1]):
        line = config.RIGHT_JOIN_LINE[1]
        angle = np.arctan2(line[0][1] - line[1][1], line[0][0] - line[1][0])
        if angle != math.pi:
            rhombus_width = min(int(rhombus_height / (np.tan(math.pi - angle) * 2 )) - config.PIXELS_3, rhombus_width)
    left_point = (up_point[0] - rhombus_width, int((up_point[1] + down_point[1])/2))
    right_point = (up_point[0] + rhombus_width, int((up_point[1] + down_point[1])/2))
    RHOMBUS = [[up_point, right_point], [right_point, down_point], [down_point, left_point], [left_point,up_point]]
    # new_lines = do_transform(RHOMBUS, score_type, pattern_type=config.PATTERN.RHOMBUS)
    if score_type == 1:
        new_lines = transform.get_correct_both(RHOMBUS,limit = config.PIXELS_3/2)
    elif score_type == 2:
        new_lines = transform.get_correct_place(RHOMBUS, pattern_type=config.PATTERN.RHOMBUS)
    elif score_type == 3:
        new_lines = transform.get_correct_shape(RHOMBUS)
    elif score_type == 4:
        new_lines = transform.get_correct_none(RHOMBUS)
    else:
        return -1
    for i, line in enumerate(new_lines):
        config.RHOMBUS[i] = line
        Logger().record_detail(f"rhombus lines: {line}")

    for line in new_lines:
        if line[0][0] != -1:  # line doesn't exist
            handline.drawLine(line[0], line[1])

def draw_VERTICAL_RIGHT_LINE(score_type):
    up_joint_line = config.RIGHT_JOIN_LINE[0]
    down_joint_line = config.RIGHT_JOIN_LINE[1]
    if utils.is_missing(up_joint_line):
        up_joint_line = [config.POINTS_DIC['bigrec_up_right'], config.POINTS_DIC['right_triangle_tip']]
    if utils.is_missing(down_joint_line):
        down_joint_line = [config.POINTS_DIC['bigrec_down_right'], config.POINTS_DIC['right_triangle_tip']]
    mid = utils.get_mid_point(config.POINTS_DIC['hori_midline_right'], config.POINTS_DIC['right_triangle_tip'])
    rand_num = np.random.uniform(1/10, 1/8) * (mid[0] - config.POINTS_DIC['hori_midline_right'][0])
    print(f"lowerbound: {config.POINTS_DIC['hori_midline_right'][0]+rand_num}")
    print(f'upperbound: {mid[0]}')
    print(f"config.POINTS_DIC['hori_midline_right'][0]:{config.POINTS_DIC['hori_midline_right'][0]}")
    vertical_line_x = np.random.randint(config.POINTS_DIC['hori_midline_right'][0]+rand_num, mid[0] + 1)
    top_point = utils.calculate_intersection_point(up_joint_line, [(vertical_line_x, config.POINTS_DIC['hori_midline_right'][1]),(vertical_line_x, config.POINTS_DIC['hori_midline_right'][1] - 20)])
    down_point = utils.calculate_intersection_point(down_joint_line, [(vertical_line_x, config.POINTS_DIC['hori_midline_right'][1]),(vertical_line_x, config.POINTS_DIC['hori_midline_right'][1] - 20)])
    VERTICAL_RIGHT_LINE = [[top_point, down_point]]
    new_lines = do_transform(VERTICAL_RIGHT_LINE, score_type,pattern_type=config.PATTERN.VERTICAL_RIGHT_LINE)
    for i, line in enumerate(new_lines):
        config.VERTICAL_RIGHT_LINE[i] = line
        Logger().record_detail(f"right vertical line: {line}")

    for line in new_lines:
        if line[0][0] != -1:  # line doesn't exist
            handline.drawLine(line[0], line[1])

def draw_HORIZENTAL_RIGHT_LINE(score_type):
    left_point = utils.get_mid_point(config.POINTS_DIC['bigrec_up_right'],config.POINTS_DIC['bigrec_down_right'])
    right_point = config.POINTS_DIC['right_triangle_tip']
    HORIZENTAL_RIGHT_LINE = [[left_point, right_point]]
    new_lines = do_transform(HORIZENTAL_RIGHT_LINE, score_type, pattern_type=config.PATTERN.HORIZENTAL_RIGHT_LINE)
    for i, line in enumerate(new_lines):
        config.HORIZENTAL_RIGHT_LINE[i] = line
        Logger().record_detail(f"right horizontal line: {line}")

    for line in new_lines:
        if line[0][0] != -1:  # line doesn't exist
            handline.drawLine(line[0], line[1])

def draw_BOTTOM_RECTANGLE(score_type):
    bottom_rec_topleft = config.POINTS_DIC['bigrec_down_left']
    big_rec_downright = config.POINTS_DIC['bigrec_down_right']
    bottom_rec_topright_x = int(3 * bottom_rec_topleft[0] /4 + big_rec_downright[0] /4)
    bottom_rec_topright_y = int(3 * bottom_rec_topleft[1] /4 + big_rec_downright[1] /4)
    bottom_rec_topright = (bottom_rec_topright_x, bottom_rec_topright_y)
    edge_len = bottom_rec_topright_x - bottom_rec_topleft[0]
    bottom_rec_downleft = (bottom_rec_topleft[0], bottom_rec_topleft[1] + edge_len)
    bottom_rec_downright = (bottom_rec_topright_x, bottom_rec_topright_y + edge_len)
    BOTTOM_RECTANGLE = [[bottom_rec_topleft, bottom_rec_topright], [bottom_rec_topright, bottom_rec_downright],
                        [bottom_rec_downright, bottom_rec_downleft], [bottom_rec_downleft, bottom_rec_topleft],
                        [bottom_rec_topleft, bottom_rec_downright]]
    new_lines = do_transform(BOTTOM_RECTANGLE, score_type, pattern_type=config.PATTERN.BOTTOM_RECTANGLE)
    utils.update_bottom_rec_down_right(new_lines)
    for i, line in enumerate(new_lines):
        config.BOTTOM_RECTANGLE[i] = line
        Logger().record_detail(f"bottom rectangle lines: {line}")
    for line in new_lines:
        if line[0][0] != -1:  # line doesn't exist
            handline.drawLine(line[0], line[1])

def draw_HORIZENTAL_CROSS(score_type):
    bottom_rec_line = config.BOTTOM_RECTANGLE[1]
    big_rec_width = config.POINTS_DIC['bigrec_down_right'][0] - config.POINTS_DIC['bigrec_down_left'][0]
    if utils.is_missing(bottom_rec_line):
        bottom_rec_topleft = config.POINTS_DIC['bigrec_down_left']
        big_rec_downright = config.POINTS_DIC['bigrec_down_right']
        bottom_rec_topright_x = int(3 * bottom_rec_topleft[0] / 4 + big_rec_downright[0] / 4)
        bottom_rec_topright_y = int(3 * bottom_rec_topleft[1] / 4 + big_rec_downright[1] / 4)
        bottom_rec_line = [(bottom_rec_topright_x, bottom_rec_topright_y), config.POINTS_DIC['bottom_rec_down_right']]

    left_point = utils.get_mid_point(bottom_rec_line[0], bottom_rec_line[1])
    horizon_len = int (big_rec_width * np.random.uniform(1/2, 3/4))
    right_point = (left_point[0] + horizon_len, left_point[1])
    middle_up_point = config.POINTS_DIC['vert_midline_down']
    middle_down_point = utils.calculate_intersection_point([left_point, right_point], [middle_up_point, (middle_up_point[0], middle_up_point[1] + 20)])
    bottom_rec_edge = bottom_rec_line[1][1] - bottom_rec_line[0][1]
    short_vertical_line_len = int (bottom_rec_edge * np.random.uniform(1/4, 1/2) / 2)
    right_up_point_y = left_point[1] - short_vertical_line_len
    right_down_point_y = left_point[1] + short_vertical_line_len
    right_vertical_point_x_lower = int((left_point[0]/3 + 2 * right_point[0])/3)
    right_vertical_point_x_upper = int((left_point[0]/8 + 7 * right_point[0])/8)
    right_vertical_point_x = np.random.randint(right_vertical_point_x_lower, right_vertical_point_x_upper)
    right_up_point = (right_vertical_point_x, right_up_point_y)
    right_down_point = (right_vertical_point_x, right_down_point_y)
    HORIZENTAL_CROSS = [[left_point,right_point], [middle_up_point, middle_down_point], [right_up_point, right_down_point]]
    new_lines = do_transform(HORIZENTAL_CROSS, score_type, pattern_type=config.PATTERN.HORIZENTAL_CROSS)
    for i, line in enumerate(new_lines):
        config.HORIZENTAL_CROSS[i] = line
        Logger().record_detail(f"horizental cross lines: {line}")

    for line in new_lines:
        if line[0][0] != -1:  # line doesn't exist
            handline.drawLine(line[0], line[1])
def draw_VERTICAL_CROSS(score_type):
    rec_line = config.BIG_RECTANGLE[3]
    if utils.is_missing(rec_line):
        rec_line = [config.POINTS_DIC['bigrec_down_left'], config.POINTS_DIC['bigrec_up_left']]
    rand_num = np.random.uniform(0.01, 1/8)
    big_rec_height = rec_line[0][1] - rec_line[1][1]
    middle_right_x = rec_line[1][0]
    middle_right_y = max(rec_line[1][1] + int (rand_num * big_rec_height), config.POINTS_DIC['bigrec_up_left'][1] + config.PIXELS_3)
    middle_right_point = (middle_right_x, middle_right_y)
    middle_left_x = middle_right_x - int (np.random.uniform(0.5, 0.55) * middle_right_x)
    middle_left_point = (middle_left_x, middle_right_y)
    small_rec_upleft = utils.get_mid_point(config.POINTS_DIC['bigrec_up_left'], config.POINTS_DIC['hori_midline_left'])

    bottom_y = np.random.randint(small_rec_upleft[1], config.POINTS_DIC['hori_midline_left'][1])
    big_rec_width = config.POINTS_DIC['bigrec_up_right'][0] - config.POINTS_DIC['bigrec_up_left'][0]
    rand_num = np.random.uniform(1/4, 1/2)
    top_y = max(0, config.POINTS_DIC['bigrec_up_left'][1] - int(rand_num * big_rec_width))
    short_len = np.random.randint((bottom_y - top_y)/8, (bottom_y - top_y)/6)
    top_right_point = (middle_right_point[0], top_y + short_len)
    top_left_point = (2 * middle_left_x - middle_right_x,top_y + short_len)
    VERTICAL_CROSS = [[middle_left_point, middle_right_point], [(middle_left_x, bottom_y),(middle_left_x, top_y)],
                      [top_left_point, top_right_point]]
    print(VERTICAL_CROSS)
    new_lines = do_transform(VERTICAL_CROSS, score_type, pattern_type=config.PATTERN.VERTICAL_CROSS)
    for i, line in enumerate(new_lines):
        config.VERTICAL_CROSS[i] = line
        Logger().record_detail(f"vertical cross lines: {line}")

    for line in new_lines:
        if line[0][0] != -1:  # line doesn't exist
            handline.drawLine(line[0], line[1])

def do_transform(lines, score_type, pattern_type):
    new_lines = []
    if score_type == 1:
        new_lines = transform.get_correct_both(lines)
    elif score_type == 2:
        new_lines = transform.get_correct_place(lines, pattern_type)
    elif score_type == 3:
        new_lines = transform.get_correct_shape(lines)
    elif score_type == 4:
        new_lines = transform.get_correct_none(lines)
    else:
        return -1
    return new_lines

def do_circle_transform(center, points, radius, score_type):
    new_center = ()
    new_points = []
    new_radius = 0
    if score_type == 1:
        new_center, new_points, new_radius = transform.get_both_correct_circle(center, points, radius)
    elif score_type == 2:
        new_center, new_points, new_radius = transform.get_place_correct_circle(center, points, radius)
    elif score_type == 3:
        new_center, new_points, new_radius = transform.get_shape_correct_circle(center, points, radius)
    elif score_type == 4:
        new_center, new_points, new_radius = transform.get_none_correct_circle(center, points, radius)
    else:
        return -1
    return new_center, new_points, new_radius