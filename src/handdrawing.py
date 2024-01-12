import matplotlib.pyplot as plt
import numpy as np
import cv2
import config
import math

def hand_drawn_segment_test(image, point1, point2, complexity=10,color = (0, 0, 0), line_thickness =20):
    x1, y1 = point1
    x2, y2 = point2
    num_points = 100
    t = np.linspace(0, 1, num_points)
    noise_x = np.cumsum(np.random.normal(0, 4, num_points))
    noise_y = np.cumsum(np.random.normal(0, 4, num_points))

    x = x1 + t * (x2 - x1) + complexity * noise_x / num_points
    y = y1 + t * (y2 - y1) + complexity * noise_y / num_points


    # Draw the line on the canvas
    for i in range(1, num_points):
        thickness = np.random.randint(1, line_thickness + 1)
        # thickness = 0
        gray_shade = np.random.randint(0, 100)
        image[int(y[i - 1]):int(y[i] + thickness), int(x[i - 1]):int(x[i] + thickness)] = gray_shade

    # Add some discrete white points
    num_points = 10
    point_size = 1
    random_points_x = np.random.randint(0, config.IMAGE_WIDTH, num_points)
    random_points_y = np.random.randint(0, config.IMAGE_HEIGHT, num_points)
    for i in range(num_points):
        image[random_points_y[i]:random_points_y[i] + point_size,
        random_points_x[i]:random_points_x[i] + point_size] = 0

    return image


def hand_drawn_segment(point1, point2, complexity=20,color = (0, 0, 0), line_thickness =3):
    x1, y1 = point1
    x2, y2 = point2
    num_points = int(np.sqrt((point2[0] - point1[0])**2 + (point2[1] - point1[1])**2))
    t = np.linspace(0, 1, num_points)
    noise_x = np.cumsum(np.random.normal(0, 3, num_points))
    noise_y = np.cumsum(np.random.normal(0, 3, num_points))

    x = x1 + t * (x2 - x1) + complexity * noise_x / num_points
    y = y1 + t * (y2 - y1) + complexity * noise_y / num_points
    plt.plot(x, y, '-o', linewidth=line_thickness, markersize=0, color=color)

    return x, y


def timeToPoint(sx, sy, fx, fy, t):
    # scale the time value, which should be between 0 and 2, to 0 and 1
    tau = t / 2.0
    polyTerm = 15 * math.pow(tau, 4) - 6 * math.pow(tau, 5) - 10 * math.pow(tau, 3)

    return [int(sx + (sx - fx) * polyTerm),int(sy + (sy - fy) * polyTerm)]

def timeToAngle(t):
    tau = t / 2.0
    polyTerm = 15 * math.pow(tau, 4) - 6 * math.pow(tau, 5) - 10 * math.pow(tau, 3)

    return (- 2 * math.pi * polyTerm)


def getSquiggle(prev, next):
    # find the midpoint const
    midpoint = [int((prev[0] + next[0])/2), int((prev[1] + next[1])/2)]
    #displace by a random value between - 5 and 5

    midpoint[0] += np.random.randint(-1 * config.PIXELS_3 /2, config.PIXELS_3/2)
    midpoint[1] += np.random.randint(-1 * config.PIXELS_3/2, config.PIXELS_3/2)

    return midpoint

def draw_quadratic_bezier_curve(p0, p1, p2, color, thickness=3, num_segments=100):
    t = np.linspace(0, 1, num_segments)
    x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t ** 2 * p2[0]
    y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t ** 2 * p2[1]
    plt.plot(x, y, '-o', linewidth=3, markersize=0, color=color)


def drawLine(point_start, point_end):

    sx, sy = point_start
    fx, fy = point_end
    dist = math.sqrt(math.pow(sx - fx, 2) + math.pow(sy - fy, 2))
    lower_bound = np.random.randint(100, 200)
    upper_bound = np.random.randint(300, 400)

    if (dist < lower_bound):
        dt = 1
    elif (dist < upper_bound):
        dt = 0.5
    else:
        dt = 0.2


    lastPoint = [sx, sy]
    t = 0
    for num in range(int(2.0/dt) + 1):
        t += dt
        if t <= 2.0:
            currentPoint = timeToPoint(sx, sy, fx, fy, t)
            squiggleControlPoint = getSquiggle(lastPoint, currentPoint)
            draw_quadratic_bezier_curve(lastPoint,squiggleControlPoint,currentPoint,color=(0,0,0))
        lastPoint = currentPoint

def draw_circle(center, radius, circle_thickness=3):

    dist = math.pi * 2 * radius
    lower_bound = np.random.randint(200, 300)
    upper_bound = np.random.randint(400, 500)

    if (dist < lower_bound):
        dt = 0.5
    elif (dist < upper_bound):
        dt = 0.4
    else:
        dt = 0.2
    print(f'*********************dt:{dt}')
    lastAngle = 0
    t = 0
    for num in range(int(2.0 / dt) + 1):
        t += dt
        if t <= 2.0:
            print(f"----------t---------:{t}")
            currentAngle = timeToAngle(t)
            print(f'current angle: {currentAngle}')
            simulate_hand_circle_curve(center, radius, lastAngle, currentAngle, color=(0, 0, 0))
        lastAngle = currentAngle

def simulate_hand_circle_curve(center, radius, theta1=0, theta2=2 * np.pi, num_points=50, deviation=1,color=(0, 0, 0)):
    # Generate points along the circle
    theta = np.linspace(theta1, theta2, num_points)
    x = center[0] + radius * np.cos(theta)
    y = center[1] + radius * np.sin(theta)
    deviation = np.random.uniform(0.3, 0.9)
    # Add random deviation to simulate hand-drawn effect
    x += np.random.normal(0, deviation, num_points)
    y += np.random.normal(0, deviation, num_points)

    # Plot the hand-drawn circle
    plt.plot(x, y, linewidth=3, color=color)


#
# image = np.zeros((config.IMAGE_HEIGHT, config.IMAGE_WIDTH, config.IMAGE_CHANNELS), dtype=np.uint8)
# image = cv2.bitwise_not(image)
# fig, ax = plt.subplots()
# ax.imshow(image, origin='upper')
# ax.axis('off')
#
# drawLine((50, 50), (300, 600))
# drawLine((50, 50), (210, 500))
# plt.show()