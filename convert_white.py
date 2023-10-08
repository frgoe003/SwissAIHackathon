import os
import cv2
import numpy as np
import random

# List of input directories
input_directories = ['SwissAIHackathon/TrainingData2/Paper', 'SwissAIHackathon/TrainingData2/Rock', 'SwissAIHackathon/TrainingData2/Scissors']

# Output directory
output_directory = ['SwissAIHackathon/TrainingData7V5/Paper', 'SwissAIHackathon/TrainingData7V5/Rock', 'SwissAIHackathon/TrainingData7V5/Scissors']

# Directory containing background images
background_directory = 'SwissAIHackathon/backgrounds2'


# Function to load a random background image
def load_random_background(background_dir):
    background_files = os.listdir(background_dir)
    random_background_file = random.choice(background_files)

    print(random_background_file)
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
            output_path = os.path.join(output_directory, filename)

            # Load the image with the white background
            white_background_image = cv2.imread(input_path)

            # Load a random background image
            background = load_random_background(background_directory)

            # Resize the background image to match the white background image's size
            background = cv2.resize(background, (white_background_image.shape[1], white_background_image.shape[0]))

            # Create a mask for the white background
            white_mask = cv2.inRange(white_background_image, (230, 230, 230), (255, 255, 255))

            # Invert the white mask to select the subject
            subject_mask = cv2.bitwise_not(white_mask)

            # Composite the subject and background
            result_image = cv2.bitwise_and(white_background_image, white_background_image, mask=subject_mask)
            result_image += cv2.bitwise_and(background, background, mask=white_mask)

            # Save the result image in the output directory
            cv2.imwrite(output_path, result_image)

# Process all input directories
for i in range(len(input_directories)):
    process_directory(input_directories[i],output_directory[i])

