import open3d as o3d
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import KDTree


pcd_a = o3d.io.read_point_cloud('/local/home/gmarsich/data2TB/DATASETS/Replica/frl_apartment_1/mesh.ply')
o3d.visualization.draw_geometries([pcd_a])




# import open3d as o3d

# transformation_matrix = [[ 0.93039052 , 0.10583947, -0.35095796 ,0], 
#                          [ 0.23923753 , 0.55008223 , 0.80010933 ,0],
#                          [ 0.27773888 ,-0.82837645 , 0.48647052, 0],
#                          [ 0.    ,      0.       ,   0.    ,      1.        ]]

# print(transformation_matrix[:3][:3])

# pcd_a = o3d.io.read_point_cloud('/local/home/gmarsich/Desktop/data_Replica/frl_apartment_0/Segmentation/mesh_semantic.ply_4.ply')
# pcd_b = o3d.io.read_point_cloud('/local/home/gmarsich/Desktop/data_Replica/frl_apartment_0/Segmentation/mesh_semantic.ply_4.ply')
# o3d.visualization.draw_geometries([pcd_a, pcd_b])

# points = np.asarray(pcd_a.points)
# centroid = np.mean(points, axis=0)
# pcd_a.translate(-centroid)
# pcd_b.translate(-centroid)

# pcd_b.transform(transformation_matrix)
# o3d.visualization.draw_geometries([pcd_a, pcd_b])

# print(np.rad2deg(np.arccos((np.trace(transformation_matrix[:3][:3]) - 1) / 2)))
# o3d.visualization.draw_geometries([colored_point_cloud_2])






# colored_point_cloud = o3d.io.read_point_cloud('/local/home/gmarsich/Desktop/Thesis/0Code_playground/SceneGraphs_changes_Replica/withPCA/preprocessing/results/frl_apartment_0_withIDs.ply')
# colored_point_cloud_2 = o3d.io.read_point_cloud('/local/home/gmarsich/Desktop/Thesis/0Code_playground/SceneGraphs_changes_Replica/withPCA/preprocessing/results/frl_apartment_1_withIDs.ply')
# o3d.visualization.draw_geometries([colored_point_cloud, colored_point_cloud_2])



# distances = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
# distances = np.delete(distances, 1, axis=1)
# print(distances)


# color = '#87CEFA'
# fig, ax = plt.subplots()
# ax.set_facecolor(color)
# ax.set_xticks([])
# ax.set_yticks([])
# plt.show()

# color = color.lstrip('#')

# # Split into RGB components
# r_hex = color[0:2]  # Red
# g_hex = color[2:4]  # Green
# b_hex = color[4:6]  # Blue

# # Convert hex to decimal
# r = int(r_hex, 16)
# g = int(g_hex, 16)
# b = int(b_hex, 16)

# # Print the RGB values
# print(f'R: {r}, G: {g}, B: {b}')


# colored_point_cloud = o3d.io.read_point_cloud('/local/home/gmarsich/data2TB/DATASETS/Replica/frl_apartment_0/mesh.ply')
# o3d.visualization.draw_geometries([colored_point_cloud])



