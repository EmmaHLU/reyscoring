import numpy as np
import math
import random
import config
import utils
from logger import Logger
from shapely.geometry import LineString, MultiLineString

class TRANS_TYPE:
    minor = 'minor'
    major = 'major'

def get_correct_both(lines, pattern_type=-1, limit=config.PIXELS_3):
  Logger().record_detail('********both correct')
  #type=1:stretch; type=2:translation; type=3:rotation
  new_lines = []
  rand = np.random.rand()
  if rand <= 0.5:
    for line in lines:
          new_line = do_stretch(line, limit=[int(limit),int(limit)], trans_type=TRANS_TYPE.minor)
          new_lines.append(new_line)
          Logger().record_detail('both correct stretch')
  elif rand > 0.5 and rand < 0.8:
      for line in lines:
          new_line = do_translation([line], int(limit), TRANS_TYPE.minor)
          new_lines.append(new_line[0])
          Logger().record_detail('both correct translation')
  elif rand > 0.8:
      for line in lines:
          new_line = do_rotation([line], config.ROTATION_LIMIT/2, TRANS_TYPE.minor)
          new_lines.append(new_line[0])
          Logger().record_detail('both correct rotation')
  Logger().record_detail('********both correct')
  return new_lines


def get_correct_shape(lines, pattern_type=-1, limit=config.PIXELS_6):
    Logger().record_detail('&&&&&&&&shape correct')
    res = get_correct_both(lines, pattern_type, limit)
    new_lines = []
    if np.random.rand() < 0.5:
        new_lines = do_rotation(res, config.ROTATION_LIMIT,TRANS_TYPE.major)
        Logger().record_detail(f'shape correct rotation')

    else:
        new_lines = do_translation(res, limit,TRANS_TYPE.major)
        Logger().record_detail('shape correct translation')
    Logger().record_detail('&&&&&&&&shape correct')

    return new_lines

def get_correct_place(lines, pattern_type = "None", limit_shape=config.PIXELS_3):
  new_lines = []
  # noise type = 0: no change; type=1:stretch;  type=2:rotation type = 3: missing
  # ??translation;
  if len(lines) > 2 and pattern_type != config.PATTERN.BIG_RECTANGLE:
      noise_array = [random.randint(0, 2) for _ in range(len(lines))]
      if noise_array.count(0) == len(lines):
          noise_array[random.randint(0, len(lines) - 1)] = random.randint(1, 2)
  else:
      noise_array = [random.randint(0, 1) for _ in range(len(lines))]
      if noise_array.count(0) == len(lines):
          noise_array[random.randint(0, len(lines) - 1)] = 1

  miss_num = random.randint(0, int(len(lines)/2))
  # Get indices to assign the value
  indices_to_assign = random.sample(range(len(lines)), miss_num)
  for index in indices_to_assign:
      if np.random.rand() < 0.2:
         noise_array[index] = 3
  Logger().record_detail('##########place correct')

  for i, line in enumerate(lines):
    start_x, start_y = line[0]
    end_x, end_y = line[1]
    if noise_array[i] == 1:#stretch
        distance = utils.get_point_point_distance(line[0], line[1])
        # analyzing the correct way and limit to stretch..
        flag, limit = get_stretch_flag_limit(pattern_type, i, distance, config.PIXELS_6)

        if flag[0] == 9 and flag[1] == 9 and sum(noise_array) == 1:# the left line of small rectangle with cross
            noise_array[i + 1] = np.random.randint(1, 3)
            break
        new_line = do_stretch(line, flag, limit, TRANS_TYPE.major)
        new_lines.append(new_line)
        Logger().record_detail('place correct stretch')

    elif noise_array[i] == 2:# rotation
        new_line = do_rotation([line],config.ROTATION_LIMIT, TRANS_TYPE.major)
        new_lines.append(new_line[0])
        Logger().record_detail('place correct rotation')

    elif noise_array[i] == 3:
        new_lines.append([(-1,-1), (-1,-1)])
        Logger().record_detail('place correct missing line')

    else:
        new_lines.append(line)
        Logger().record_detail('place correct no change')
  Logger().record_detail('##########place correct')

  return new_lines

def get_correct_none(lines, pattern_type = -1, limit_shape=config.PIXELS_3, limit_place=config.PIXELS_6):
    new_lines = []
    Logger().record_detail('%%%%%%%%%%both wrong')
    # print(f'before both wrong: {lines}')
    res = get_correct_place(lines, pattern_type, limit_shape)
    # print(f"both wrong after change the shape: {res}")
    res = get_correct_shape(res, pattern_type, limit_place)
    # print(f'both wrong after change the place: {res}')
    # Generate a random number in either of the ranges
    for i, res_line in enumerate(res):
        if np.random.rand() < 0.8:
            new_lines.append([(-1,-1), (-1,-1)])
            Logger().record_detail('both wrong missing line')

        else:
            new_lines.append(res_line)
    Logger().record_detail('%%%%%%%%%%both wrong')


    return new_lines

def do_translation(lines, limit, trans_type=TRANS_TYPE.minor):
    new_lines = []
    if trans_type == TRANS_TYPE.major:
        if np.random.rand() < 0.5:
            noise = np.random.uniform(limit, limit * 2)
        else:
            noise = np.random.uniform(-2 * limit, -1 * limit)
    else:
        noise = np.random.uniform(-1 * limit, limit)
    angle = np.random.uniform(-1 * math.pi,math.pi)
    noise_x = noise
    noise_y = noise
    noise_y = noise * math.sin(angle)
    if angle >= -0.5 * math.pi and angle <= 0.5 * math.pi:
        noise_x = noise * math.cos(angle)
        noise_y = noise * math.sin(angle)
    elif angle > 0.5 * math.pi and angle <= math.pi:
        noise_x = -1 * noise * math.cos(math.pi - angle)
        noise_y = noise * math.sin(math.pi - angle)
    else:
        noise_x = -1 * noise * math.cos(math.pi + angle)
        noise_y = -1 * noise * math.sin(math.pi + angle)

    for line in lines:
      if utils.is_missing(line):
          new_lines.append(line)
      else:
          start_x, start_y = line[0]
          end_x, end_y = line[1]
          new_start_x = start_x + noise_x
          new_start_y = start_y + noise_y
          new_end_x = end_x + noise_x
          new_end_y = end_y + noise_y
          new_line = [(int(max(0, new_start_x)), int(max(0, new_start_y))), (int(max(0, new_end_x)), int(max(0, new_end_y)))]
          new_lines.append(new_line)
    return new_lines

def do_stretch(line, flag = [0, 0], limit=[config.PIXELS_3,config.PIXELS_3], trans_type=TRANS_TYPE.minor):#flag =0: both way, 1: out; -1: in
    if utils.is_missing(line):
        return line
    start_x, start_y = line[0]
    end_x, end_y = line[1]
    start_flag = flag[0]
    end_flag = flag[1]
    start_limit = limit[0]
    end_limit = limit[1]
    ends_to_stretch = []
    if flag[0] == 9:
        ends_to_stretch = [0, 1]
    elif flag[1] == 9:
        ends_to_stretch = [1, 0]
    else:
        ends_to_stretch = [random.randint(0, 1) for _ in range(2)]
    if ends_to_stretch.count(0) == 2:
        ends_to_stretch[random.randint(0, 1)] = 1
    noise_start = 0
    noise_end = 0
    if ends_to_stretch[0] == 1:
        if trans_type == TRANS_TYPE.major:
            if start_flag == 0:
                if np.random.rand() < 0.5:
                    noise_start = np.random.uniform(start_limit * 2, start_limit * 4)
                else:
                    noise_start = np.random.uniform(-4 * start_limit, -2 * start_limit)
            elif start_flag == -1:#stretch in
                noise_start = np.random.uniform(start_limit * 2, start_limit * 4)
            elif start_flag == 1:#stretch out
                noise_start = np.random.uniform(-4 * start_limit, -2 * start_limit)
        else:
            noise_start = np.random.uniform(-1 * start_limit, start_limit)
    if ends_to_stretch[1] == 1:
        if trans_type == TRANS_TYPE.major:
            if end_flag == 0:
                if np.random.rand() < 0.5:
                    noise_end = np.random.uniform(end_limit * 2, end_limit * 4)
                else:
                    noise_end = np.random.uniform(-4 * end_limit, -2 * end_limit)
            elif end_flag == 1:#stretch out
                noise_end = np.random.uniform(end_limit * 2, end_limit * 4)
            elif end_flag == -1:# stretch in
                noise_end = np.random.uniform(-4 * end_limit, -2 * end_limit)
        else:
            noise_end = np.random.uniform(-1 * end_limit, end_limit)

    # Calculate the angle of the line
    angle = math.atan2(end_y - start_y, end_x - start_x)
    if angle >= -0.5 * math.pi and angle <= 0.5 * math.pi:
        # Calculate the new coordinates of the start point
        new_start_x = start_x + noise_start * math.cos(angle)
        new_start_y = start_y + noise_start * math.sin(angle)
        # Calculate the new coordinates of the end point
        new_end_x = end_x + noise_end * math.cos(angle)
        new_end_y = end_y + noise_end * math.sin(angle)
    elif angle > 0.5 * math.pi and angle <= math.pi:
        # Calculate the new coordinates of the start point
        new_start_x = start_x - noise_start * math.cos(math.pi - angle)
        new_start_y = start_y + noise_start * math.sin(math.pi - angle)
        # Calculate the new coordinates of the end point
        new_end_x = end_x - noise_end * math.cos(math.pi - angle)
        new_end_y = end_y + noise_end * math.sin(math.pi - angle)
    else:
        # Calculate the new coordinates of the start point
        new_start_x = start_x - noise_start * math.cos(math.pi + angle)
        new_start_y = start_y - noise_start * math.sin(math.pi + angle)
        # Calculate the new coordinates of the end point
        new_end_x = end_x - noise_end * math.cos(math.pi + angle)
        new_end_y = end_y - noise_end * math.sin(math.pi + angle)
    # # Calculate the new coordinates of the start point
    # new_start_x = start_x + noise_start * math.cos(angle)
    # new_start_y = start_y + noise_start * math.sin(angle)
    # # Calculate the new coordinates of the end point
    # new_end_x = end_x + noise_end * math.cos(angle)
    # new_end_y = end_y + noise_end * math.sin(angle)
    new_line = [(int(max(0, new_start_x)), int(max(0, new_start_y))), (int(max(0, new_end_x)), int(max(0, new_end_y)))]
    return new_line

def do_rotation(lines, limit=config.ROTATION_LIMIT, trans_type=TRANS_TYPE.minor):
    new_lines = []
    mid_x, mid_y = compute_geometry_center(lines)
    if trans_type == TRANS_TYPE.major:
        if np.random.rand() < 0.5:
            noise = np.random.uniform(limit * 2, 15)
        else:
            noise = np.random.uniform(-15, -limit * 2)
    else:
        noise = np.random.uniform(-1 * limit, limit)

    # print(f'the rotation angle is {noise}')
    for line in lines:
        if utils.is_missing(line):
            new_lines.append(line)
        else:
            new_line = rotate_line_segment(line, noise, mid_x, mid_y)
            new_lines.append(new_line)
    return new_lines
def rotate_point(x, y, angle, center_x, center_y):
    # Convert the angle to radians
    angle_rad = math.radians(angle)# important

    # Perform the rotation using the rotation matrix
    new_x = center_x + (x - center_x) * math.cos(angle_rad) - (y - center_y) * math.sin(angle_rad)
    new_y = center_y + (x - center_x) * math.sin(angle_rad) + (y - center_y) * math.cos(angle_rad)

    return new_x, new_y

def rotate_line_segment(line, angle, center_x, center_y):
    x1, y1 = line[0]
    x2, y2 = line[1]
    # Rotate the two endpoints of the line segment
    new_start_x, new_start_y = rotate_point(x1, y1, angle, center_x, center_y)
    new_end_x, new_end_y = rotate_point(x2, y2, angle, center_x, center_y)
    new_line = [(int(max(0, new_start_x)), int(max(0, new_start_y))), (int(max(0, new_end_x)), int(max(0, new_end_y)))]
    return new_line

def get_stretch_flag_limit(pattern_type = "None", line_id=0, distance = 0, limit_shape=config.PIXELS_6):
    flag = [0, 0]
    limit = [limit_shape, limit_shape]
    if pattern_type == config.PATTERN.VERTICAL_MIDELINE:
        flag = [-1, -1]
    elif pattern_type == config.PATTERN.HORIZONTAL_MIDLINE:
        flag = [0, -1]
    elif pattern_type == config.PATTERN.SMALL_RECTANGLE_CROSS and line_id == 3:
        flag = [9, 9]
    elif pattern_type == config.PATTERN.SMALL_TRIANGLE:
        if line_id == 0:#left line
            if utils.is_missing(config.VERTICAL_MIDELINE[0]):
                flag = [0, 0]
            else:
                flag = [0, -1]
        elif line_id == 1:#bottom line
            flag = [9, 1]
    elif pattern_type == config.PATTERN.HORIZONTAL_SMALL_LINE or pattern_type == config.PATTERN.VERTICAL_SMALL_LINE:
        flag = [0, 0]
        max_limit = min(distance/3, 2 * limit_shape/3)
        limit = [max_limit, max_limit]
    elif pattern_type == config.PATTERN.FIVE_PARALLEL_LINE:
        limit = [2 * limit_shape, 2 * limit_shape]
    elif pattern_type == config.PATTERN.BOTTOM_RECTANGLE:
        if line_id == 0: #top line
            if utils.is_missing(config.BIG_RECTANGLE[2]):
                flag = [0, 0]
            else:
                flag = [1, 9]
        elif line_id == 3: #left line
            if utils.is_missing(config.BIG_RECTANGLE[3]):
                flag = [0, 0]
            else:
                flag = [0, -1]
    elif pattern_type == config.PATTERN.HORIZENTAL_RIGHT_LINE:
        if utils.is_missing(config.RIGHT_JOIN_LINE[0]) and utils.is_missing(config.RIGHT_JOIN_LINE[1]):
            flag[1] = 9
        if not utils.is_missing(config.HORIZONTAL_MIDLINE[0]):
            flag[0] = -1
    elif pattern_type == config.PATTERN.HORIZENTAL_CROSS:
        if line_id == 0:#horizontal line
            flag = [0, 1]
            max_limit = min(distance / 3, 3 * limit_shape)
            limit = [limit_shape, max_limit]
        elif line_id == 1: #middle vertical line
            flag = [-1, 0]
        else: #right vertical line
            flag = [1, 1]
            max_limit = min(distance / 3, 2 * limit_shape)
            limit = [max_limit, max_limit]
    elif pattern_type == config.PATTERN.VERTICAL_CROSS:
        if line_id == 1 or line_id == 2:
            limit = [2 * limit_shape, 2 * limit_shape]

    return flag, limit

def get_translation_flag_limit(pattern_type = "None", line_id=0, distance = 0, limit_shape=config.PIXELS_6):
    pass

def compute_geometry_center(lines):
    # Convert the list of lines to a MultiLineString
    # print("to compute the center of the lines:")
    # print(lines)

    multi_line = MultiLineString(lines)

    # Calculate the centroid
    centroid = multi_line.centroid

    return centroid.x, centroid.y

def get_score(scoring_types):
    # Example array
    data_array = np.array(scoring_types)
    score = 0
    # Get the count of each unique value
    unique_values, counts = np.unique(data_array, return_counts=True)

    # Create a dictionary to store the results
    result_dict = dict(zip(unique_values, counts))

    # Print the results
    # print("Count of each value:")
    for value, count in result_dict.items():
        if value == 1:
            score += count * 2
        elif value ==2 or value == 3:
            score += count
        # print(f"{value}: {count}")
    return score
def get_none_correct_circle(center, points, radius):
    Logger().record_detail('circle none correct')
    center, new_points, radius = get_shape_correct_circle(center, points, radius)
    center, new_points, radius = get_place_correct_circle(center, points, radius)
    if np.random.rand() < 0.8:
        center = (-1, -1)
        for i in range(len(points)):
            new_points[i] = [(-1, -1), (-1, -1)]
    return center, new_points, radius

def get_both_correct_circle(center, points, radius):
    rand_num = np.random.randint(1, config.PIXELS_3)
    if np.random.rand() < 0.5: #translation
        center, new_points, new_raius = do_circle_translation(center, points, radius, limit=rand_num)
    else:#zoom
        center, new_points, new_raius = do_circle_zoom(center, points, radius, limit=rand_num)
    if np.random.rand() < 0.3:
        new_raius -= np.random.randint(0, config.PIXELS_3)
    Logger().record_detail('circle both correct ')
    return center, new_points, new_raius

def get_place_correct_circle(center, points, radius):
    # noise type = 0: no change; type=1:stretch; type = 2: missing  type=3:point translation
    tran_types = [np.random.randint(0,3) for i in range(4)]
    tran_types[0] = random.choice([0, 2])
    if tran_types.count(0) == len(points) + 1:
        if np.random.rand() < 0.25:
            tran_types[0] = 2
        else:
            tran_types[np.random.randint(1, 3)] = np.random.randint(1, 3)
    if tran_types.count(2) == len(points) + 1:
        if np.random.rand() < 0.25:
            tran_types[0] = 0
        else:
            tran_types[np.random.randint(1, 3)] = random.choice([0, 1, 3])
    # transform the center
    if tran_types[0] == 2:# missing
        center = (-1, -1)
        Logger().record_detail('cicle place correct center missing')
    for i in range(len(points)):
        if tran_types[i + 1] == 1: #stretch
            noise = np.random.randint(config.PIXELS_3, config.PIXELS_3 * 1.5)
            x = points[i][0][0]
            y = points[i][0][1]
            points[i] = [(x - noise, y), (x + noise, y)]
            Logger().record_detail('circle place correct stretch')
        elif tran_types[i + 1] == 2:
            print(f'i:{i}')
            points[i] = [(-1, -1), (-1, -1)]
            Logger().record_detail('circle place correct point missing')
        elif tran_types[i + 1] == 3:
            if np.random.rand() > 0.5:
                noise = np.random.randint(-2 * config.PIXELS_3, -1 * config.PIXELS_3)
            else:
                noise = np.random.randint( config.PIXELS_3, 2 * config.PIXELS_3)
            x = points[i][0][0]
            y = points[i][0][1]
            points[i] = [(x + noise, y + noise), (x + noise, y + noise)]
            Logger().record_detail('circle place correct translation')
    return center, points, radius

def get_shape_correct_circle(center, points, radius):
    rand_num = np.random.randint(config.PIXELS_3 + 1, config.PIXELS_6)
    if np.random.rand() < 0.5:  # translation
        center, new_points, new_raius = do_circle_translation(center, points, radius, limit=rand_num, trans_type=TRANS_TYPE.major)
        Logger().record_detail('circle shape correct translation')
    else:  # zoom
        center, new_points, new_raius = do_circle_zoom(center, points, radius, limit=rand_num, trans_type=TRANS_TYPE.major)
        Logger().record_detail('circle shape correct zoom')

    return center, new_points, new_raius
def do_circle_translation(center, points, radius, limit=config.PIXELS_3, trans_type=TRANS_TYPE.minor):
    if trans_type == TRANS_TYPE.major:
        if np.random.rand() < 0.5:
            noise = np.random.uniform(limit, limit * 2)
        else:
            noise = np.random.uniform(-2 * limit, -1 * limit)
    else:
        noise = np.random.uniform(-1 * limit, limit)
    angle = math.radians(np.random.uniform(0,360))
    noise_x = int(noise * math.cos(angle))
    noise_y = int(noise * math.sin(angle))
    center = (center[0] + noise_x, center[1] + noise_y)
    for i in range(len(points)):
        points[i] = [(points[i][0][0] + noise_x, points[i][0][1] + noise_y),(points[i][0][0] + noise_x, points[i][0][1] + noise_y)]

    return center, points, radius


def do_circle_zoom(center, points, radius, limit=config.PIXELS_3, trans_type=TRANS_TYPE.minor):
    if trans_type == TRANS_TYPE.major:
        noise = np.random.uniform(limit, limit * 2)
    else:
        noise = np.random.uniform(-1 * limit, limit)
    radius += noise

    return center, points, radius



