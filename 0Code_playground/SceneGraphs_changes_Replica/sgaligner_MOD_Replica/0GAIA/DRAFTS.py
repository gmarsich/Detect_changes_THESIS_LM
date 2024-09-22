import open3d as o3d
import os
import numpy as np
import matplotlib.pyplot as plt
import pickle

# #
# # Verify that two scenes overlap and that colors in object.json are the colors of the instances
# #

# point_cloud_a = o3d.io.read_point_cloud("/local/home/gmarsich/Desktop/data_Replica/frl_apartment_0/Segmentation/colored_mesh_with_IDs.ply")
# point_cloud_b = o3d.io.read_point_cloud("/local/home/gmarsich/Desktop/data_Replica/frl_apartment_1/Segmentation/colored_mesh_with_IDs.ply")

# o3d.visualization.draw_geometries([point_cloud_a, point_cloud_b])
# o3d.visualization.draw_geometries([point_cloud_b])

# color = '#02c442'
# fig, ax = plt.subplots()
# ax.set_facecolor(color)
# ax.set_xticks([])
# ax.set_yticks([])
# plt.show()





# #
# # Verify that the .npy files that I generated are ok
# #

# # Load the .npy file
# file_path = '/local/home/gmarsich/Desktop/3RScan/out/scenes/754e884c-ea24-2175-8b34-cead19d4198d_5/data.npy'
# file_path = '/local/home/gmarsich/Desktop/data_Replica/frl_apartment_1/SGAligner/data.npy'
# data = np.load(file_path, allow_pickle=True)

# print(f"Data type: {type(data)}")

# print(f"Data dtype: {data.dtype}")

# print(f"Data shape: {data.shape}")

# print("Sample of the data:")
# print(data[-1])





# #
# # Verify that the .pkl files that I generated are ok
# #

# # Load the .pkl file
# file_path = '/local/home/gmarsich/Desktop/3RScan/out/files/orig/data/754e884c-ea24-2175-8b34-cead19d4198d_5.pkl'
# file_path = '/local/home/gmarsich/Desktop/data_Replica/frl_apartment_1/SGAligner/data_dict.pkl'

# with open(file_path, 'rb') as file:
#     data = pickle.load(file)

# print(f"Data type: {type(data)}")

# # If it's a dictionary, print the keys
# if isinstance(data, dict):
#     print(f"Keys: {list(data.keys())}")


# print(data['obj_points'].keys())
# #print(data['obj_points'][64][:4])
# #print(len(data['obj_points'][64]))
# #print(len(data['ei']))
# print(data['ei'][152])


# points_np = np.array(data['obj_points'][256*2][152])
# pcd = o3d.geometry.PointCloud()
# pcd.points = o3d.utility.Vector3dVector(points_np)
# axis = o3d.geometry.TriangleMesh.create_coordinate_frame(
#                 size=1.0,  # Size of the axis
#                 origin=[0, 0, 0]  # Origin point of the axis
#             )
# o3d.visualization.draw_geometries([pcd, axis])



# point_cloud = o3d.io.read_point_cloud("/local/home/gmarsich/Desktop/data_Replica/frl_apartment_1/Segmentation/colored_mesh_with_IDs.ply")
# o3d.visualization.draw_geometries([point_cloud, axis])


# point_cloud = o3d.io.read_point_cloud("/local/home/gmarsich/Desktop/data_Replica/frl_apartment_1/Segmentation/mesh_semantic.ply_154.ply")
# o3d.visualization.draw_geometries([point_cloud, axis])






# #
# # Test a side function that gets only certain instances
# #

# # side function
# def get_newObjectPoints(objectIDs):
#     ei_array = np.array([200, 201, 345, 289])
#     positions = [np.where(ei_array == obj_id)[0] for obj_id in objectIDs]
#     flat_positions = np.concatenate(positions)

#     object_points = np.array([4, 3, 2, 1])
#     new_object_points = object_points[flat_positions]

#     return new_object_points


# print(get_newObjectPoints([200, 289, 345]))




