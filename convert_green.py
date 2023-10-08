import os
import cv2
import numpy as np
import random

# List of input directories
input_directories = ['SwissAIHackathon/TrainingData/Paper', 'SwissAIHackathon/TrainingData/Scissors','SwissAIHackathon/TrainingData/Rock'] #

# Output directory
output_directory = ['SwissAIHackathon/TrainingData7V5/Paper', 'SwissAIHackathon/TrainingData7V5/Scissors','SwissAIHackathon/TrainingData7V5/Rock'] #, 

# Define the green color range in HSV format
lower_green = np.array([35, 80, 80])  # Lower bound for green color in HSV
upper_green = np.array([85, 255, 255])  # Upper bound for green color in HSV

# Function to process a single directory
def process_directory(input_directory,output_directory):
    for filename in os.listdir(input_directory):
        print(filename)
        if filename.endswith('.jpg') or filename.endswith('.png'):
            input_path = os.path.join(input_directory, filename)
            output_path = os.path.join(output_directory, filename)

            # Load the green screen image
            green_screen_image = cv2.imread(input_path)

            # Convert the image to HSV color space
            hsv_image = cv2.cvtColor(green_screen_image, cv2.COLOR_BGR2HSV)

            # Create a mask for the green color
            green_mask = cv2.inRange(hsv_image, lower_green, upper_green)

            # Generate a random color (BGR format)
            random_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

            # Replace the green color with the random color
            result_image = green_screen_image.copy()
            result_image[np.where(green_mask)] = random_color

            # Save the result image in the output directory
            cv2.imwrite(output_path, result_image)

# Process all input directories
for i in range(len(input_directories)):
    process_directory(input_directories[i],output_directory[i])

