import cv2
import numpy as np
import os

def change_background_folder(input_folder, output_folder, new_background_color):
    # Make sure the output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Loop through all files in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith(('.jpg', '.jpeg', '.png')):  # Check for image file extensions
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)

            change_background(input_path, output_path)

def change_background(image_path, output_path):
    # Read the image
    image = cv2.imread(image_path)

    # Convert the image to HSV color space
    # hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    left_corner = gray[0][0]
    print(left_corner)
    # Define the lower and upper bounds for the color you want to replace
    lower_bound = max(0, left_corner - 10) # Adjust these values based on your image
    upper_bound = min(255, left_corner + 10)
    print(lower_bound)
    print(upper_bound)

    # Create a mask using inRange to identify pixels within the specified color range
    mask = cv2.inRange(gray, 150, 255)

    # Invert the mask to select the background
    background_mask = cv2.bitwise_not(mask)

    # # Create an all-white image
    white_background = np.full_like(gray, 255, dtype=np.uint8)

    # # Use the mask to combine the original image with the white background
    result = cv2.bitwise_and(gray, gray, mask=background_mask)
    result += cv2.bitwise_and(white_background, white_background, mask=mask)

    # Threshold the image to obtain a binary image with lines
    _, thresh = cv2.threshold(result, 170, 255, cv2.THRESH_BINARY)

    # Set the pixels corresponding to the lines to black
    result[thresh == 0] = 0
    # result = cv2.GaussianBlur(result, (5, 5), 0)

    # Save the result
    cv2.imwrite(output_path, result)
# Example usage
input_folder_path = '/content/drive/MyDrive/data/handdrawn/original'
output_folder_path = '/content/drive/MyDrive/data/handdrawn/processed'
new_background_color = [255, 255, 255]  # White color in BGR format

change_background_folder(input_folder_path, output_folder_path, new_background_color)