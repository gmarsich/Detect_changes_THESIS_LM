import open3d as o3d
import os
import numpy as np

import pickle

# point_cloud_a = o3d.io.read_point_cloud("/local/home/gmarsich/Desktop/steps_3RScan/3RScan_original_allScenes/scenes/4acaebcc-6c10-2a2a-858b-29c7e4fb410d/labels.instances.annotated.v2.ply")
# point_cloud_b = o3d.io.read_point_cloud("/local/home/gmarsich/Desktop/steps_3RScan/3RScan_original_allScenes/scenes/754e884c-ea24-2175-8b34-cead19d4198d/labels.instances.align.annotated.v2.ply")
# pcd = o3d.io.read_point_cloud("/local/home/gmarsich/Desktop/data_Replica/frl_apartment_0/Segmentation/colored_mesh.ply")

# print(pcd)
# o3d.visualization.draw_geometries([pcd])



# # Load the .npy file
# file_path = '/local/home/gmarsich/Desktop/3RScan/out/scenes/754e884c-ea24-2175-8b34-cead19d4198d_5/data.npy'
# data = np.load(file_path)

# # Check the type of the data
# print(f"Data type: {type(data)}")

# # Check the dtype of the data
# print(f"Data dtype: {data.dtype}")

# # Check the shape of the array
# print(f"Data shape: {data.shape}")

# # Print a small portion of the data to inspect
# print("Sample of the data:")
# print(data[:5])






# Load the .pkl file
file_path = '/local/home/gmarsich/Desktop/3RScan/out/files/orig/data/754e884c-ea24-2175-8b34-cead19d4198d_5.pkl'
with open(file_path, 'rb') as file:
    data = pickle.load(file)

# Check the type of the data
print(f"Data type: {type(data)}")

# If it's a dictionary, print the keys
if isinstance(data, dict):
    print(f"Keys: {list(data.keys())}")

# If it's a list or array, check its length and contents
elif isinstance(data, list):
    print(f"List length: {len(data)}")
    print(f"First few entries: {data[:5]}")
    
# For any other types, print a small part of the data
else:
    print("Sample of the data:", data)

