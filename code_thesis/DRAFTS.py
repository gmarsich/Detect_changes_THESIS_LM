import open3d as o3d
import numpy as np
#import matplotlib.pyplot as plt
from scipy.spatial import KDTree


import open3d as o3d

colored_point_cloud = o3d.io.read_point_cloud('/local/home/gmarsich/Desktop/data_Replica/frl_apartment_3/frl_apartment_3_withIDs_LabelMaker.ply')
# colored_point_cloud_2 = o3d.io.read_point_cloud('/local/home/gmarsich/Desktop/data_Replica/frl_apartment_1/frl_apartment_1_withIDs_LabelMaker.ply')
points = np.asarray(colored_point_cloud.points)
print(points[0])
# o3d.visualization.draw_geometries([colored_point_cloud, colored_point_cloud_2])





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


colored_point_cloud = o3d.io.read_point_cloud('/local/home/gmarsich/data2TB/DATASETS/Replica/frl_apartment_0/mesh.ply')
o3d.visualization.draw_geometries([colored_point_cloud])

