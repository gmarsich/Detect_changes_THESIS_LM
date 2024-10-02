import open3d as o3d
import numpy as np
import matplotlib.pyplot as plt

# colored_point_cloud = o3d.io.read_point_cloud('/local/home/gmarsich/Desktop/Thesis/0Code_playground/SceneGraphs_changes_Replica/withPCA/preprocessing/results/frl_apartment_0_withIDs.ply')
# colored_point_cloud_2 = o3d.io.read_point_cloud('/local/home/gmarsich/Desktop/Thesis/0Code_playground/SceneGraphs_changes_Replica/withPCA/preprocessing/results/frl_apartment_1_withIDs.ply')
# o3d.visualization.draw_geometries([colored_point_cloud, colored_point_cloud_2])

def farthest_point_sampling(pcd, n_samples):

    points = np.asarray(pcd.points)
    colors = np.asarray(pcd.colors)
    n_points = points.shape[0]
    
    sampled_indices = np.zeros(n_samples, dtype=int)
    sampled_indices[0] = np.random.randint(n_points) # randomly select the first point

    distances = np.full(n_points, np.inf)

    for i in range(1, n_samples):
        current_point = points[sampled_indices[i - 1]]
        distances = np.minimum(distances, np.linalg.norm(points - current_point, axis=1))
        sampled_indices[i] = np.argmax(distances) # select the farthest point

    # Create a new point cloud from the sampled points
    sampled_points = points[sampled_indices]
    sampled_colors = colors[sampled_indices]
    sampled_pcd = o3d.geometry.PointCloud()
    sampled_pcd.points = o3d.utility.Vector3dVector(sampled_points)
    sampled_pcd.colors = o3d.utility.Vector3dVector(sampled_colors)

    return sampled_pcd

colored_point_cloud = o3d.io.read_point_cloud('/local/home/gmarsich/Desktop/data_Replica BKP/frl_apartment_0/Segmentation/mesh_semantic.ply_60.ply')
o3d.visualization.draw_geometries([colored_point_cloud])

new = farthest_point_sampling(colored_point_cloud, round(len(colored_point_cloud.points)/50))
o3d.visualization.draw_geometries([new])
print(len(colored_point_cloud.points))







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

