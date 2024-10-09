# environment: thesisPlayground_pointClouds_env

import h5py
import numpy as np
import matplotlib.pyplot as plt
import os

# Print the current working directory
print("Current working directory:", os.getcwd())

# Verify that the file exists
basis_path = '/local/home/gmarsich/data2TB/DATASETS/Hypersim/evermotion_dataset/scenes/ai_007_008/images/scene_cam_00_geometry_hdf5'  # TODO TOSET: change the path to the folder of the file to render
file_name = 'frame.0000.depth_meters.hdf5'  # TODO TOSET: change the file to render
file_path = os.path.join(basis_path, file_name)

if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
else:
    # Open the HDF5 file
    with h5py.File(file_path, 'r') as file:

        # Print all root level groups
        print("Keys: %s" % list(file.keys()))

        # Access the specific dataset
        dataset_name = 'dataset'  # TODO TOSET: change depending on your hdf5 file
        if dataset_name in file:
            dataset = file[dataset_name]
            
            # Print dataset attributes
            print("Shape of dataset:", dataset.shape)
            print("Data type of dataset:", dataset.dtype)
            
            # Read the data from the dataset
            data = dataset[:]
            
            # Convert data type to float32 for compatibility with matplotlib
            data = data.astype(np.float32)
            
            # Create a figure and axis for the plot
            fig, ax = plt.subplots()
            
            # Display the image using matplotlib with a colormap
            cax = ax.imshow(data, cmap='viridis')  # You can change 'viridis' to other colormaps, e.g., 'plasma', 'inferno', etc.
            plt.axis('off')  # Turn off axis numbers and ticks
            
            # Add a colorbar to indicate the scale
            cbar = fig.colorbar(cax, ax=ax)
            cbar.set_label('Depth (meters)', rotation=270, labelpad=15)  # Adjust the label and padding as necessary
            
            # Save the plot to a file
            output_file = os.path.join(basis_path, 'tonemapped_' + file_name + '.png')
            plt.savefig(output_file)
            print(f"Image saved as '{output_file}\n'")
        else:
            print(f"Dataset '{dataset_name}' not found in the file.\n")
