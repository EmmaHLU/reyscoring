import numpy as np
import math
import random
import config
from shapely.geometry import LineString, MultiLineString


Minor = 'minor'
Major = 'major'
TRANS_TYPE = [Minor,Major]

def calculate_intersection_point(line1, line2):
    x1, y1 = line1[0]
    x2, y2 = line1[1]
    x3, y3 = line2[0]
    x4, y4 = line2[1]
    #if line doesn't exist
    if x1 == -1 or y1 ==-1 or x2 == -1 or y2 == -1:
        x_int = x3
        y_int = y3
    elif x3 == -1 or y3 ==-1 or x4 == -1 or y4 == -1:
        x_int = x2
        y_int = y2
    elif x1 == x2 and x3 == x4:#parallel
        x_int = x1
        y_int = y1
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

        # Calculate intersection point
        x_int = (b2 - b1) / (m1 - m2)
        y_int = m1 * x_int + b1

    return int(x_int), int(y_int)

def get_correct_both(lines, limit_type=1, limit=config.PIXELS_3):
  #type=1:stretch; type=2:translation; type=3:rotation
  new_lines = []
  if limit_type == 1:
    for line in lines:
          noise_start = np.random.uniform(-1 * limit, limit)
          noise_end = np.random.uniform(-1 * limit, limit)
          start_x, start_y = line[0]
          end_x, end_y = line[1]
          # Calculate the angle of the line
          angle = math.atan2(end_y - start_y, end_x - start_x)
          # Calculate the new coordinates of the start point
          new_start_x = start_x + noise_start * math.cos(angle)
          new_start_y = start_y + noise_start * math.sin(angle)
          # Calculate the new coordinates of the end point
          new_end_x = end_x + noise_end * math.cos(angle)
          new_end_y = end_y + noise_end * math.sin(angle)
          new_line = [(int(new_start_x), int(new_start_y)), (int(new_end_x), int(new_end_y))]
          new_lines.append(new_line)
  elif limit_type == 2:
      for line in lines:
          noise = np.random.uniform(-1 * limit, limit)
          start_x, start_y = line[0]
          end_x, end_y = line[1]
          # Calculate the angle of the line
          angle = math.atan2(end_y - start_y, end_x - start_x)
           # Calculate the new coordinates of the start point
          new_start_x = start_x + noise * math.sin(angle)
          new_start_y = start_y + noise * math.cos(angle)
          # Calculate the new coordinates of the end point
          new_end_x = end_x + noise * math.sin(angle)
          new_end_y = end_y + noise * math.cos(angle)
          new_line = [(int(new_start_x), int(new_start_y)), (int(new_end_x), int(new_end_y))]
          new_lines.append(new_line)
  elif limit_type == 3:
      for line in lines:
          noise = math.radians(np.random.uniform(-1 * limit, limit))#important
          start_x, start_y = line[0]
          end_x, end_y = line[1]
          # Calculate the angle of the line
          angle = math.atan2(end_y - start_y, end_x - start_x)
          line_d = np.sqrt((end_x - start_x)**2 + (end_y - start_y)**2)
          mid_x = (start_x + end_x)/2
          mid_y = (start_y + end_y)/2
          new_start_x = mid_x - line_d * math.cos(angle + noise) / 2
          new_start_y = mid_y - line_d * math.sin(angle + noise) / 2
          new_end_x = mid_x + line_d * math.cos(angle + noise) / 2
          new_end_y = mid_y + line_d * math.sin(angle + noise) / 2
          new_line = [(int(new_start_x), int(new_start_y)), (int(new_end_x), int(new_end_y))]
          new_lines.append(new_line)
  return new_lines


def get_correct_shape(lines, shape_limit_type=1, shape_limit=config.PIXELS_3, place_limit=config.PIXELS_6):
    res = get_correct_both(lines, shape_limit_type, shape_limit)
    new_lines = []
    if np.random.rand() < 0.5:
      noise = np.random.uniform(place_limit, place_limit*2)
    else:
      noise = np.random.uniform(-2 * place_limit, -1 * place_limit)
    angle = math.radians(np.random.uniform(0,360))
    noise_x = noise * math.cos(angle)
    noise_y = noise * math.sin(angle)
    for line in res:
      start_x, start_y = line[0]
      end_x, end_y = line[1]
      new_start_x = start_x + noise_x
      new_start_y = start_y + noise_y
      new_end_x = end_x + noise_x
      new_end_y = end_y + noise_y
      new_line = [(int(new_start_x), int(new_start_y)), (int(new_end_x), int(new_end_y))]
      new_lines.append(new_line)
    return new_lines

def get_correct_place(lines, limit_shape_type = 1, limit_shape=config.PIXELS_3, limit_place=config.PIXELS_3):
  new_lines = []
  # noise type = 0: no change; type=1:stretch;  type=2:rotation type = 3: missing
  # ??translation;
  noise_array = [random.randint(0, 2) for _ in range(len(lines))]
  if noise_array.count(0) == len(lines):
      noise_array[random.randint(0,len(lines)-1)] = random.randint(1, 2)
  miss_num = random.randint(0, int(len(lines)/2))
  # Get indices to assign the value
  indices_to_assign = random.sample(range(len(lines)), miss_num)
  for index in indices_to_assign:
      if np.random.rand() < 0.25:
         noise_array[index] = 3

  for i, line in enumerate(lines):
    start_x, start_y = line[0]
    end_x, end_y = line[1]
    if noise_array[i] == 1:#stretch
        ends_to_stretch = [random.randint(0, 1) for _ in range(2)]
        if ends_to_stretch.count(0) == 2:
            ends_to_stretch[random.randint(0,1)] = 1
        noise_start = 0
        noise_end = 0
        if ends_to_stretch[0] == 1:
            if np.random.rand() < 0.5:
                noise_start = np.random.uniform(limit_shape * 1.5, limit_shape * 3)
            else:
                noise_start = np.random.uniform(-3 * limit_shape, -1.5 * limit_shape)
        if ends_to_stretch[1] == 1:
            if np.random.rand() < 0.5:
                noise_end = np.random.uniform(limit_shape * 1.5, limit_shape * 3)
            else:
                noise_end = np.random.uniform(-3 * limit_shape, -1.5 * limit_shape)

        # Calculate the angle of the line
        angle = math.atan2(end_y - start_y, end_x - start_x)
        # Calculate the new coordinates of the start point
        new_start_x = start_x + noise_start * math.cos(angle)
        new_start_y = start_y + noise_start * math.sin(angle)
        # Calculate the new coordinates of the end point
        new_end_x = end_x + noise_end * math.cos(angle)
        new_end_y = end_y + noise_end * math.sin(angle)
        new_line = [(int(new_start_x), int(new_start_y)), (int(new_end_x), int(new_end_y))]
        new_lines.append(new_line)
    # elif noise_array[i] == 2:
        # if np.random.rand() < 0.5:
        #     noise = np.random.uniform(limit_shape, limit_shape * 2)
        # else:
        #     noise = np.random.uniform(-2 * limit_shape, -1 * limit_shape)
        # # Calculate the angle of the line
        # angle = math.atan2(end_y - start_y, end_x - start_x)
        # # Calculate the new coordinates of the start point
        # new_start_x = start_x + noise * math.sin(angle)
        # new_start_y = start_y + noise * math.cos(angle)
        # # Calculate the new coordinates of the end point
        # new_end_x = end_x + noise * math.sin(angle)
        # new_end_y = end_y + noise * math.cos(angle)
        # new_line = [(int(new_start_x), int(new_start_y)), (int(new_end_x), int(new_end_y))]
        # new_lines.append(new_line)
    elif noise_array[i] == 2:
        if np.random.rand() < 0.5:
            noise = np.random.uniform(limit_shape, limit_shape * 2)
        else:
            noise = np.random.uniform(-2 * limit_shape, -1 * limit_shape)
        noise = math.radians(noise)  # important
        start_x, start_y = line[0]
        end_x, end_y = line[1]
        # Calculate the angle of the line
        angle = math.atan2(end_y - start_y, end_x - start_x)
        line_d = np.sqrt((end_x - start_x) ** 2 + (end_y - start_y) ** 2)
        mid_x = (start_x + end_x) / 2
        mid_y = (start_y + end_y) / 2
        new_start_x = mid_x - line_d * math.cos(angle + noise) / 2
        new_start_y = mid_y - line_d * math.sin(angle + noise) / 2
        new_end_x = mid_x + line_d * math.cos(angle + noise) / 2
        new_end_y = mid_y + line_d * math.sin(angle + noise) / 2
        new_line = [(int(new_start_x), int(new_start_y)), (int(new_end_x), int(new_end_y))]
        new_lines.append(new_line)
    elif noise_array[i] == 3:
        new_lines.append([(-1,-1), (-1,-1)])
    else:
        new_lines.append(line)

  return new_lines

def get_correct_none(lines, limit_shape_type = 3, limit_shape=config.PIXELS_3, limit_place=config.PIXELS_6):
    new_lines = []
    res = get_correct_place(lines, limit_shape_type, limit_shape, limit_place)
    res = get_correct_shape(res, limit_shape_type, limit_shape, limit_place)
    # Generate a random number in either of the ranges
    for i, res_line in enumerate(res):
        if np.random.rand() < 0.8:
            new_lines.append([(-1,-1), (-1,-1)])
        else:
            new_lines.append(res_line)
    return new_lines

def do_translation(lines, limit, trans_type=TRANS_TYPE.minor):
    new_lines = []
    if trans_type == TRANS_TYPE.major:
        if np.random.rand() < 0.5:
            noise = np.random.uniform(limit * 2, limit * 4)
        else:
            noise = np.random.uniform(-4 * limit, -2 * limit)
    else:
        noise = np.random.uniform(-1 * limit, limit)
    angle = math.radians(np.random.uniform(0,360))
    noise_x = noise * math.cos(angle)
    noise_y = noise * math.sin(angle)
    for line in lines:
      start_x, start_y = line[0]
      end_x, end_y = line[1]
      new_start_x = start_x + noise_x
      new_start_y = start_y + noise_y
      new_end_x = end_x + noise_x
      new_end_y = end_y + noise_y
      new_line = [(int(new_start_x), int(new_start_y)), (int(new_end_x), int(new_end_y))]
      new_lines.append(new_line)
    return new_lines

def do_stretch(line, limit, trans_type=TRANS_TYPE.minor):
    start_x, start_y = line[0]
    end_x, end_y = line[1]
    ends_to_stretch = [random.randint(0, 1) for _ in range(2)]
    if ends_to_stretch.count(0) == 2:
        ends_to_stretch[random.randint(0, 1)] = 1
    noise_start = 0
    noise_end = 0
    if ends_to_stretch[0] == 1:
        if trans_type == TRANS_TYPE.major:
            if np.random.rand() < 0.5:
                noise_start = np.random.uniform(limit * 2, limit * 4)
            else:
                noise_start = np.random.uniform(-4 * limit, -2 * limit)
        else:
            noise_start = np.random.uniform(-1 * limit, limit)
    if ends_to_stretch[1] == 1:
        if trans_type == TRANS_TYPE.major:
            if np.random.rand() < 0.5:
                noise_end = np.random.uniform(limit * 2, limit * 4)
            else:
                noise_end = np.random.uniform(-4 * limit, -2 * limit)
        else:
            noise_end = np.random.uniform(-1 * limit, limit)

    # Calculate the angle of the line
    angle = math.atan2(end_y - start_y, end_x - start_x)
    # Calculate the new coordinates of the start point
    new_start_x = start_x + noise_start * math.cos(angle)
    new_start_y = start_y + noise_start * math.sin(angle)
    # Calculate the new coordinates of the end point
    new_end_x = end_x + noise_end * math.cos(angle)
    new_end_y = end_y + noise_end * math.sin(angle)
    new_line = [(int(new_start_x), int(new_start_y)), (int(new_end_x), int(new_end_y))]
    return new_line

def do_rotation(lines, limit, trans_type=TRANS_TYPE.minor):
    new_lines = []
    mid_x, mid_y = compute_geometry_center(lines)
    if trans_type == TRANS_TYPE.major:
        if np.random.rand() < 0.5:
            noise = np.random.uniform(limit * 2, limit * 4)
        else:
            noise = np.random.uniform(-4 * limit, -2 * limit)
    else:
        noise = np.random.uniform(-1 * limit, limit)
    noise = math.radians(noise)  # important
    for line in lines:
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
    new_line = [(int(new_start_x), int(new_start_y)), (int(new_end_x), int(new_end_y))]
    return new_line


def compute_geometry_center(lines):
    # Convert the list of lines to a MultiLineString
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
    print("Count of each value:")
    for value, count in result_dict.items():
        if value == 1:
            score += count * 2
        elif value ==2 or value == 3:
            score += count
        print(f"{value}: {count}")
    return score


def generate_type_list_with_sum(score, num_pattern=18):
    # Generate n-1 random numbers in the range [1, 4]
    random_numbers = [random.randint(1, 4) for _ in range(num_pattern - 1)]
    random_numbers[0] = random.randint(1, 2)

    # Adjust the last number to make the sum equal to s
    last_number = score - get_score(random_numbers)

    # Check if the last number is within the desired range [1, 4]
    if 0 <= last_number <= 2:
        if last_number == 0:
            random_numbers.append(4)
        elif last_number == 2:
            random_numbers.append(1)
        elif last_number == 1 and np.random.rand() > 0.5:
            random_numbers.append(2)
        else:
            random_numbers.append(3)
        return random_numbers
    else:
        # If last number is outside the range, retry the generation
        return generate_type_list_with_sum(score, num_pattern)

def generate_type_list_random(num_pattern=18):
    random_numbers = [random.randint(1, 4) for _ in range(num_pattern)]
    random_numbers[0] = random.randint(1, 2)
    return random_numbers

