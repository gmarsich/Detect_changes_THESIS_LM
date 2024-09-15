'''Random visualisations and tests'''


# #
# # Visualise the point cloud from the npy file
# #

# import numpy as np
# import open3d as o3d

# # Load the .npy file (your file path may vary)
# point_cloud_data = np.load('/local/home/gmarsich/Desktop/3RScan_original/out/scenes/754e884c-ea24-2175-8b34-cead19d4198d_6/data.npy')

# # Extract point cloud coordinates (x, y, z)
# points = np.array([(x, y, z) for x, y, z, *_ in point_cloud_data])

# # Extract RGB values (normalized to range 0-1 for Open3D)
# colors = np.array([(r/255, g/255, b/255) for _, _, _, r, g, b, *_ in point_cloud_data])

# # Create Open3D point cloud object
# pcd = o3d.geometry.PointCloud()
# pcd.points = o3d.utility.Vector3dVector(points)
# pcd.colors = o3d.utility.Vector3dVector(colors)

# # Visualize the point cloud
# o3d.visualization.draw_geometries([pcd], window_name='3D Point Cloud')







# #
# # Visualise the point cloud from the point clouds of objects in the pkl file
# #

# import open3d as o3d
# import numpy as np
# import pickle

# # Load the .pkl file
# with open('/local/home/gmarsich/Desktop/3RScan/out/files/orig/data/754e884c-ea24-2175-8b34-cead19d4198d_6.pkl', 'rb') as f:
#     data_dict = pickle.load(f)

# print(data_dict.keys())

# obj_points = data_dict['obj_points'][256] # possibilities for the resolution: 64, 128, 256, 512

# # # Convert point cloud to Open3D format and visualize the single objects
# # for obj_pcl in obj_points:
# #     pcd = o3d.geometry.PointCloud()
# #     pcd.points = o3d.utility.Vector3dVector(obj_pcl)
# #     o3d.visualization.draw_geometries([pcd])

# print(len(obj_points))

# # See the entire point cloud
# combined_pcd = o3d.geometry.PointCloud()

# for obj_pcl in obj_points:
#     pcd = o3d.geometry.PointCloud()
#     pcd.points = o3d.utility.Vector3dVector(obj_pcl)
#     combined_pcd += pcd

# o3d.visualization.draw_geometries([combined_pcd])








# #
# # IDs in the pkl file
# #

# import common
# import os.path as osp

# ref_data_dict = common.load_pkl_data(osp.join("/local/home/gmarsich/Desktop/3RScan/out/files/orig/data/754e884c-ea24-2175-8b34-cead19d4198d_5.pkl"))
# print(ref_data_dict['objects_id'])
# src_data_dict = common.load_pkl_data(osp.join("/local/home/gmarsich/Desktop/3RScan/out/files/orig/data/754e884c-ea24-2175-8b34-cead19d4198d_6.pkl"))
# print(src_data_dict['objects_id'])







# #
# # See a color given by objects_subscenes_val.json
# #

# import matplotlib.pyplot as plt

# color = '#b24c4c'
# fig, ax = plt.subplots()
# ax.set_facecolor(color)
# ax.set_xticks([])
# ax.set_yticks([])
# plt.show()








'''Miscellaneous'''

# #
# # Visualise the ugly point cloud of an object (code to be put in eval_step in the /local/home/gmarsich/Desktop/sgaligner_MOD_3RScan/src/inference/sgaligner/inference_align_reg.py file)
# #

# import open3d as o3d
# import numpy as np

# # First point cloud
# point = data_dict['tot_obj_pts'][3]
# point_cloud_np = np.vstack(point)
# pcd = o3d.geometry.PointCloud()
# pcd.points = o3d.utility.Vector3dVector(point_cloud_np)

# # Set all points to black
# black_color = np.zeros((point_cloud_np.shape[0], 3))  # (number of points, 3) for RGB
# pcd.colors = o3d.utility.Vector3dVector(black_color)

# # Visualize the first point cloud
# o3d.visualization.draw_geometries([pcd])

# # Second point cloud
# point = data_dict['tot_obj_pts'][10]
# point_cloud_np = np.vstack(point)
# pcd = o3d.geometry.PointCloud()
# pcd.points = o3d.utility.Vector3dVector(point_cloud_np)

# # Set all points to black
# black_color = np.zeros((point_cloud_np.shape[0], 3))  # (number of points, 3) for RGB
# pcd.colors = o3d.utility.Vector3dVector(black_color)

# # Visualize the second point cloud
# o3d.visualization.draw_geometries([pcd])