import cv2
import numpy as np

# Function to calculate distance between two points
def calculate_distance(point1, point2):
    return np.sqrt((point2[0] - point1[0])**2 + (point2[1] - point1[1])**2)
# Load the image in grayscale
image_path = 'standard.png'
image = cv2.imread(image_path)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# Apply Gaussian blur to reduce noise
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# Apply adaptive thresholding to handle varying line thickness
thresh_img = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
inverted_image = cv2.bitwise_not(thresh_img)
thin_image = cv2.ximgproc.thinning(inverted_image)

# Detect corners using Shi-Tomasi
corners = cv2.goodFeaturesToTrack(thin_image, maxCorners=200, qualityLevel=0.1, minDistance=10)

# Convert corners to integer coordinates
corners = np.int0(corners)

# Draw corners on the original image
image_with_corners = image.copy()
for corner in corners:
    x, y = corner.ravel()
    cv2.circle(image_with_corners, (x, y), 3, 255, -1)
    if x >= 100:
      print(f"({x}, {y})")
      cv2.putText(image_with_corners, f"({x}, {y})", (x, y), cv2.FONT_HERSHEY_PLAIN, 1, (0,0,255), 1, cv2.LINE_AA)
# for corner1 in corners:
#   for corner2 in corners:
#     if corner1.all == corner2.all:
#       continue
#     elif calculate_distance(corner1.ravel(), corner2.ravel()) < 100:
#       cv2.line(image_with_corners, corner1.ravel(), corner2.ravel(), (0, 255, 0), 2)
#       print("one line")
#     else:
#       continue
# Display the original and marked images
# cv2_imshow(image)
# cv2_imshow(thin_image)
cv2.imshow("image", image_with_corners)
