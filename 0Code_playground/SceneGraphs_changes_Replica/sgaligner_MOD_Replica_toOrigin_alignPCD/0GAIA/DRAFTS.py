import open3d as o3d
import os
import numpy as np
import matplotlib.pyplot as plt
import pickle

#
# Verify that two scenes overlap and that colors in object.json are the colors of the instances
#

# point_cloud_a = o3d.io.read_point_cloud("/local/home/gmarsich/Desktop/data_Replica/frl_apartment_0/Segmentation/colored_mesh_with_IDs.ply")
# point_cloud_b = o3d.io.read_point_cloud("/local/home/gmarsich/Desktop/data_Replica/frl_apartment_1/Segmentation/colored_mesh_with_IDs.ply")

# o3d.visualization.draw_geometries([point_cloud_a, point_cloud_b])
# o3d.visualization.draw_geometries([point_cloud_a.paint_uniform_color([1, 0.706, 0]), point_cloud_b.paint_uniform_color([0, 0.651, 0.929])])
# o3d.visualization.draw_geometries([point_cloud_a])

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
# #file_path = '/local/home/gmarsich/Desktop/data_Replica/frl_apartment_1/SGAligner/data.npy'
# data = np.load(file_path, allow_pickle=True)

# print(f"Data type: {type(data)}")

# print(f"Data dtype: {data.dtype}")

# print(f"Data shape: {data.shape}")

# print("Sample of the data:")
# print(data[:4])





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





# #
# # Number of points in a point cloud
# #

# point_clouddd = o3d.io.read_point_cloud("/local/home/gmarsich/Desktop/data_Replica/frl_apartment_0/Segmentation/mesh_semantic.ply_4.ply")
# print(len(point_clouddd.points))





# #
# # Visualise the set of instances that are taken into account
# #

# # Variables
# path_meshSemantics_ref = "/local/home/gmarsich/Desktop/data_Replica/frl_apartment_0/Segmentation" # folder containing the mesh_semantic.ply_i.ply
# path_meshSemantics_src = "/local/home/gmarsich/Desktop/data_Replica/frl_apartment_1/Segmentation"
# path_transformationMatrix = "/local/home/gmarsich/Desktop/Thesis/0Code_playground/SceneGraphs_changes_Replica/sgaligner_MOD_Replica/0GAIA/alignment_Replica/results_alignment/frl_apartment_1_to_frl_apartment_0/frl_apartment_1_to_frl_apartment_0.txt"
# objectIDs_src = [27, 89, 130, 13, 2] # 1: ceiling, stair, tv-screen 130, 13, floor
# objectIDs_ref = [10, 120, 231, 45, 32, 8] # 0: ceiling, stair, tv-screen 231, 45, table, floor

# # Doing the important stuff
# transformation_matrix = np.loadtxt(path_transformationMatrix)

# def load_and_color_point_clouds(path_meshSemantics, objectIDs, transformation_matrix = None, color = None):
#     combined_point_clouds = []

#     for value in objectIDs:
#         filename = f'mesh_semantic.ply_{value}.ply'
#         filepath = os.path.join(path_meshSemantics, filename)
        
#         if os.path.exists(filepath):
#             pcd = o3d.io.read_point_cloud(filepath)
#             if transformation_matrix is not None:
#                 pcd.transform(transformation_matrix)
#             combined_point_clouds.append(pcd)

#     if combined_point_clouds:
#         full_point_cloud = combined_point_clouds[0]
#         for pcd in combined_point_clouds[1:]:
#             full_point_cloud += pcd
            
#     if color is not None:
#         full_point_cloud.paint_uniform_color(color)
        
#     return full_point_cloud


# pcd_ref = load_and_color_point_clouds(path_meshSemantics_ref, objectIDs_ref, transformation_matrix = None)
# pcd_src = load_and_color_point_clouds(path_meshSemantics_src, objectIDs_src, transformation_matrix)

# o3d.visualization.draw_geometries([pcd_src, pcd_ref])

# o3d.visualization.draw_geometries([pcd_src])






#
# Render the set of the subscans (npy files) in the same rendering
#

base_path = '/local/home/gmarsich/Desktop/steps_3RScan/3RScan_original_allScenes/out/scenes'

list_path_subscans = [os.path.join(base_path, '754e884c-ea24-2175-8b34-cead19d4198d_0/data.npy'),
                      os.path.join(base_path, '754e884c-ea24-2175-8b34-cead19d4198d_1/data.npy'),
                      os.path.join(base_path, '754e884c-ea24-2175-8b34-cead19d4198d_2/data.npy'),
                      os.path.join(base_path, '754e884c-ea24-2175-8b34-cead19d4198d_3/data.npy'),
                      os.path.join(base_path, '754e884c-ea24-2175-8b34-cead19d4198d_4/data.npy'),
                      os.path.join(base_path, '754e884c-ea24-2175-8b34-cead19d4198d_5/data.npy'),
                      os.path.join(base_path, '754e884c-ea24-2175-8b34-cead19d4198d_6/data.npy'),
                      ]

combined_pcd = o3d.geometry.PointCloud()

for path_subscan in list_path_subscans:
    data = np.load(path_subscan, allow_pickle=True)
    
    points = np.vstack((data['x'], data['y'], data['z'])).T  # Shape (N, 3)
    colors = np.vstack((data['red'], data['green'], data['blue'])).T / 255.0  # Shape (N, 3), normalized to [0, 1]

    pcd = o3d.geometry.PointCloud()

    pcd.points = o3d.utility.Vector3dVector(points)
    pcd.colors = o3d.utility.Vector3dVector(colors)

    combined_pcd += pcd

o3d.visualization.draw_geometries([combined_pcd])






# #
# # Render the set of the subscans (in pkl files) in the same rendering
# #

# base_path = '/local/home/gmarsich/Desktop/steps_3RScan/3RScan_original_allScenes/out/files/orig/data'

# list_path_subscans = [os.path.join(base_path, '754e884c-ea24-2175-8b34-cead19d4198d_0.pkl'),
#                       os.path.join(base_path, '754e884c-ea24-2175-8b34-cead19d4198d_1.pkl'),
#                       os.path.join(base_path, '754e884c-ea24-2175-8b34-cead19d4198d_2.pkl'),
#                       os.path.join(base_path, '754e884c-ea24-2175-8b34-cead19d4198d_3.pkl'),
#                       os.path.join(base_path, '754e884c-ea24-2175-8b34-cead19d4198d_4.pkl'),
#                       os.path.join(base_path, '754e884c-ea24-2175-8b34-cead19d4198d_5.pkl'),
#                       ]

# complete_pcd = o3d.geometry.PointCloud()

# for path_subscan in list_path_subscans:
#     with open(path_subscan, 'rb') as handle:
#         data_dict = pickle.load(handle)

#     obj_points = data_dict['obj_points'][128]

#     combined_pcd = o3d.geometry.PointCloud()

#     for obj in obj_points:
#         points = obj  # Shape (128, 3)
#         random_color = np.random.rand(3)  # Random RGB color (values between 0 and 1)

#         colors = np.tile(random_color, (points.shape[0], 1))  # Shape (128, 3)

#         pcd = o3d.geometry.PointCloud()
#         pcd.points = o3d.utility.Vector3dVector(points)
#         pcd.colors = o3d.utility.Vector3dVector(colors)
        
#         # Add this object's point cloud to the combined point cloud
#         combined_pcd += pcd

#     complete_pcd += combined_pcd

# o3d.visualization.draw_geometries([complete_pcd])




