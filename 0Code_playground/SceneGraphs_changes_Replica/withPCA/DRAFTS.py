import open3d as o3d
import numpy as np
#import matplotlib.pyplot as plt
from scipy.spatial import KDTree

# colored_point_cloud = o3d.io.read_point_cloud('/local/home/gmarsich/Desktop/Thesis/0Code_playground/SceneGraphs_changes_Replica/withPCA/preprocessing/results/frl_apartment_0_withIDs.ply')
# colored_point_cloud_2 = o3d.io.read_point_cloud('/local/home/gmarsich/Desktop/Thesis/0Code_playground/SceneGraphs_changes_Replica/withPCA/preprocessing/results/frl_apartment_1_withIDs.ply')
# o3d.visualization.draw_geometries([colored_point_cloud, colored_point_cloud_2])

aaaa = np.array([[1, 2], [2, 3]])
if isinstance(aaaa, np.ndarray):
    forse = aaaa.tolist()

    print(type(forse))







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

