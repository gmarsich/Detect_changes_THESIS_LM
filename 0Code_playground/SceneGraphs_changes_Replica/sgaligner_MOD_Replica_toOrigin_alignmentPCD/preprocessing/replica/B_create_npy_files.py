'''generate_subscans.py but for Replica.
This scripts takes in input a point cloud containing some information and creates the .npy file that will be used by SGAligner.'''

import numpy as np
import os


#
# Variables
#

base_path = "/local/home/gmarsich/Desktop/data_Replica/frl_apartment_1/"
ply_file_path = os.path.join(base_path, "Segmentation/colored_mesh_with_IDs.ply")
npy_file_path = os.path.join(base_path, "SGAligner/data.npy")  # where to save the .npy file


#
# Save the .npy file
#

def read_ply_and_convert_to_npy(ply_file_path, npy_file_path):

    with open(ply_file_path, 'r') as ply_file:
        while True: # skip the header
            line = ply_file.readline().strip()
            if line == "end_header":
                break
        
        data = []
        for line in ply_file:
            parts = line.strip().split()
            
            x, y, z = float(parts[0]), float(parts[1]), float(parts[2])
            red, green, blue = int(parts[3]), int(parts[4]), int(parts[5])
            object_id = int(parts[6])

            data.append((x, y, z, red, green, blue, object_id))

    data_array = np.array(data, dtype=[('x', 'f4'), ('y', 'f4'), ('z', 'f4'),
                                       ('red', 'i4'), ('green', 'i4'), ('blue', 'i4'), 
                                       ('objectId', 'i4')])
    
    np.save(npy_file_path, data_array)


read_ply_and_convert_to_npy(ply_file_path, npy_file_path)
