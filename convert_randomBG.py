import os
import cv2
import numpy as np
import random


# List of input directories
input_directories = ['SwissAIHackathon/TrainingData/Paper', 'SwissAIHackathon/TrainingData/Rock', 'SwissAIHackathon/TrainingData/Scissors']#['SwissAIHackathon/TrainingData/Scissors','SwissAIHackathon/TrainingData/Paper'] #

# Output directory
output_directory = ['SwissAIHackathon/TrainingData7V5/Paper', 'SwissAIHackathon/TrainingData7V5/Rock', 'SwissAIHackathon/TrainingData7V5/Scissors']#['SwissAIHackathon/TrainingData7V5/Scissors','SwissAIHackathon/TrainingData7V5/Paper'] 

# Directory containing background images
background_directory = 'SwissAIHackathon/backgrounds2'

# Define the green color range in HSV format
lower_green = np.array([35, 80, 80])  # Lower bound for green color in HSV
upper_green = np.array([85, 255, 255])  # Upper bound for green color in HSV

# Function to load a random background image
def load_random_background(background_dir):
    background_files = os.listdir(background_dir)
    random_background_file = random.choice(background_files)

    #print(random_background_file)
    if random_background_file.endswith('.jpg') or random_background_file.endswith('.png'):

        background_path = os.path.join(background_dir, random_background_file)
        return cv2.imread(background_path)
    else:
        return load_random_background(background_dir)
    

# Function to process a single directory
def process_directory(input_directory,output_directory):
    for filename in os.listdir(input_directory):
        if filename.endswith('.jpg') or filename.endswith('.png'):
            input_path = os.path.join(input_directory, filename)

            filename = filename[:-4]+'BACK1'+'.png'
            output_path = os.path.join(output_directory, filename)

            print(filename)
            # Load the green screen image
            green_screen_image = cv2.imread(input_path)


            # Convert the image to HSV color space
            hsv_image = cv2.cvtColor(green_screen_image, cv2.COLOR_BGR2HSV)

            # Create a mask for the green color
            green_mask = cv2.inRange(hsv_image, lower_green, upper_green)

            # Load a random background image
            background = load_random_background(background_directory)

            # Resize the background image to match the green screen image's size
            background = cv2.resize(background, (green_screen_image.shape[1], green_screen_image.shape[0]))

            # Composite the green screen image and background
            result_image = cv2.bitwise_and(green_screen_image, green_screen_image, mask=~green_mask)
            result_image += cv2.bitwise_and(background, background, mask=green_mask)

            # Save the result image in the output directory
            cv2.imwrite(output_path, result_image)

# Process all input directories
for i in range(len(input_directories)):
    process_directory(input_directories[i],output_directory[i])
