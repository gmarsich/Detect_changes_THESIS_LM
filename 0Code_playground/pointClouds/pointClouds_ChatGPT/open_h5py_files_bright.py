import h5py
import numpy as np
import matplotlib.pyplot as plt
import os

# Function to adjust and invert the brightness
def adjust_and_invert_brightness(data):
    # Normalize the data
    data_min = data.min()
    data_max = data.max()
    print(f"Data range before normalization: [{data_min}..{data_max}]")
    normalized_data = (data - data_min) / (data_max - data_min)
    print(f"Data range after normalization: [{normalized_data.min()}..{normalized_data.max()}]")
    
    # Invert the normalized data
    inverted_data = 1.0 - normalized_data
    print(f"Data range after inversion: [{inverted_data.min()}..{inverted_data.max()}]")
    
    return inverted_data

# Correct file path
file_path = '/local/home/gmarsich/Desktop/Thesis/0Code_playground/pointClouds/pointClouds_ChatGPT/frame.0000.color.hdf5'  # Update this to your correct path if necessary
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
else:
    # Open the HDF5 file
    with h5py.File(file_path, 'r') as file:
        # Access the specific dataset
        dataset_name = 'tonemapped_rgb'  # replace with the actual dataset name
        if dataset_name in file:
            dataset = file[dataset_name]
            
            # Print dataset attributes
            print("Shape of dataset:", dataset.shape)
            print("Data type of dataset:", dataset.dtype)
            
            # Read the data from the dataset
            data = dataset[:]
            
            # Adjust and invert the brightness
            adjusted_data = adjust_and_invert_brightness(data)
            
            # Convert data type to float32 for compatibility with matplotlib
            adjusted_data = adjusted_data.astype(np.float32)
            
            # Display the image using matplotlib
            plt.imshow(adjusted_data, cmap='gray')  # You can use 'gray' colormap to ensure black-to-white scale
            plt.title('Inverted Image from HDF5 Dataset')
            plt.axis('off')  # Turn off axis numbers and ticks
            
            # Save the plot to a file
            output_file = 'image_from_hdf5_bright.png'
            plt.savefig(output_file)
            print(f"Image saved as '{output_file}'")
        else:
            print(f"Dataset '{dataset_name}' not found in the file.")
