import h5py
import os


# See the matrices representing the images

# Print the current working directory
print("Current working directory:", os.getcwd())

# Verify that the file exists
file_path = '/local/home/gmarsich/Desktop/Thesis/0Code_playground/pointClouds/pointClouds_ChatGPT/frame.0000.color.hdf5'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
else:
    # Open the HDF5 file
    with h5py.File(file_path, 'r') as file:
        # Print all root level groups
        print("Keys: %s" % list(file.keys()))
        # Get a specific dataset
        dataset = 'dataset'  # replace with the actual dataset name
        if dataset in file:
            dataset = file[dataset]
            
            # Print dataset attributes
            print("Shape of dataset:", dataset.shape)
            print("Data type of dataset:", dataset.dtype)
            
            # Read the data from the dataset
            data = dataset[:]
            
            # Print the data
            print(data)
        else:
            print(f"Dataset '{dataset}' not found in the file.")




# See the image got from the matrices
# WARNING: the brightness is strange

import h5py
import numpy as np
import matplotlib.pyplot as plt
import os

# Correct file path
file_path = '/local/home/gmarsich/Desktop/Thesis/0Code_playground/pointClouds/pointClouds_ChatGPT/frame.0000.color.hdf5'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
else:
    # Open the HDF5 file
    with h5py.File(file_path, 'r') as file:
        # Access the specific dataset
        dataset_name = 'dataset'  # replace with the actual dataset name
        if dataset_name in file:
            dataset = file[dataset_name]
            
            # Print dataset attributes
            print("Shape of dataset:", dataset.shape)
            print("Data type of dataset:", dataset.dtype)
            
            # Read the data from the dataset
            data = dataset[:]
            
            # Convert data type to float32 for compatibility with matplotlib
            data = data.astype(np.float32)
            
            # Display the image using matplotlib
            plt.imshow(data)
            plt.title('Image from HDF5 Dataset')
            plt.axis('off')  # Turn off axis numbers and ticks
            
            # Save the plot to a file
            output_file = 'image_from_hdf5_CORRECT.png'
            plt.savefig(output_file)
            print(f"Image saved as '{output_file}'")
        else:
            print(f"Dataset '{dataset_name}' not found in the file.")
