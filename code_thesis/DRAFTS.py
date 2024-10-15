import open3d as o3d
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import KDTree
import os
from Replica_code.SceneGraph import SceneGraph
import pickle

path_a = '/local/home/gmarsich/Desktop/data_Replica/frl_apartment_4/Scene_Graphs/sceneGraph_GT'
sceneGraph_a = SceneGraph()
sceneGraph_a.load_SceneGraph(path_a)

pcd_a = sceneGraph_a.get_pointCloud('148')
pcd_complete_a = sceneGraph_a.complete_pointCloud.paint_uniform_color([1, 0, 0])
o3d.visualization.draw_geometries([pcd_complete_a, pcd_a])



# path_a = '/local/home/gmarsich/Desktop/data_Replica/frl_apartment_0/Scene_Graphs/sceneGraph_GT'
# sceneGraph_a = SceneGraph()
# sceneGraph_a.load_SceneGraph(path_a)

# pcd_a = sceneGraph_a.get_pointCloud('4')
# pcd_complete_a = sceneGraph_a.complete_pointCloud.paint_uniform_color([1, 0, 0])
# o3d.visualization.draw_geometries([pcd_complete_a, pcd_a])



# path_b = '/local/home/gmarsich/Desktop/data_Replica/frl_apartment_0/Scene_Graphs/sceneGraph_LabelMaker'
# sceneGraph_b = SceneGraph()
# sceneGraph_b.load_SceneGraph(path_b)

# pcd_b = sceneGraph_b.get_pointCloud('124')
# pcd_complete_b = sceneGraph_b.complete_pointCloud.paint_uniform_color([1, 0, 0])
# o3d.visualization.draw_geometries([pcd_complete_b, pcd_b])












# path_0 = '/local/home/gmarsich/Desktop/data_Replica/frl_apartment_0/Scene_Graphs/sceneGraph_LabelMaker'
# path_save = '/local/home/gmarsich/Desktop/data_Replica/frl_apartment_0/Scene_Graphs'
# list_IDs_0 = [x for x in range(128)]

# graph_0 = SceneGraph()
# graph_0.load_SceneGraph(path_0)
# list_vertices, list_centroids, list_colors_vertices, list_labels, PCDs, list_pairs_edges = graph_0.get_visualisation_SceneGraph(list_IDs_0, threshold=1, color = 'absoluteColor')
# graph_0.draw_SceneGraph_PyViz3D(list_centroids, list_colors_vertices, list_labels, list_pairs_edges, PCDs, path_save, wantLabels = False)





# path = '/local/home/gmarsich/Desktop/steps_3RScan/3RScan_original_allScenes/out/files/orig/data/754e884c-ea24-2175-8b34-cead19d4198d_0.pkl'

# with open(path, 'rb') as file:
#     data = pickle.load(file)

# # Print or work with the data
# print(data.keys())





# pcd_a = o3d.io.read_point_cloud('/local/home/gmarsich/Desktop/DATA/3RScan/4acaebcc-6c10-2a2a-858b-29c7e4fb410d/labels.instances.annotated.v2.ply')
# o3d.visualization.draw_geometries([pcd_a])




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



