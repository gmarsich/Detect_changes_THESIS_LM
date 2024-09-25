'''Random visualisations and tests'''


# #
# # Visualise a scene in Replica
# #

# import open3d as o3d

# point_cloud = o3d.io.read_point_cloud("/local/home/gmarsich/data2TB/DATASETS/Replica/frl_apartment_0/mesh.ply")
# o3d.visualization.draw_geometries([point_cloud])





# #
# # Sadly remark that there is no common coordinate system in the frl apartments in Replica
# #

# import open3d as o3d

# point_cloud_0 = o3d.io.read_point_cloud("/local/home/gmarsich/data2TB/DATASETS/Replica/frl_apartment_0/mesh.ply")
# point_cloud_1 = o3d.io.read_point_cloud("/local/home/gmarsich/data2TB/DATASETS/Replica/frl_apartment_1/mesh.ply")
# point_cloud_2 = o3d.io.read_point_cloud("/local/home/gmarsich/data2TB/DATASETS/Replica/frl_apartment_2/mesh.ply")
# point_cloud_3 = o3d.io.read_point_cloud("/local/home/gmarsich/data2TB/DATASETS/Replica/frl_apartment_3/mesh.ply")
# point_cloud_4 = o3d.io.read_point_cloud("/local/home/gmarsich/data2TB/DATASETS/Replica/frl_apartment_4/mesh.ply")
# point_cloud_5 = o3d.io.read_point_cloud("/local/home/gmarsich/data2TB/DATASETS/Replica/frl_apartment_5/mesh.ply")

# point_cloud_0.paint_uniform_color([1, 0, 0])
# point_cloud_1.paint_uniform_color([0, 1, 0])
# point_cloud_2.paint_uniform_color([0, 0, 1])
# point_cloud_3.paint_uniform_color([1, 1, 0]) # yellow
# point_cloud_4.paint_uniform_color([0, 1, 1])
# point_cloud_5.paint_uniform_color([1, 0, 1]) # fucsia

# full_point_cloud = point_cloud_0
# full_point_cloud += point_cloud_1
# # full_point_cloud += point_cloud_2
# # full_point_cloud += point_cloud_3
# # full_point_cloud += point_cloud_4
# # full_point_cloud += point_cloud_5

# o3d.visualization.draw_geometries([full_point_cloud])







#
# Observe that the subscenes in 3RScan have a common coordinate system
#

# import numpy as np
# import open3d as o3d

# Load the .npy file (your file path may vary)
# point_cloud_data = np.load('/local/home/gmarsich/Desktop/steps_3RScan/3RScan_original/out/scenes/754e884c-ea24-2175-8b34-cead19d4198d_6/data.npy')
# points = np.array([(x, y, z) for x, y, z, *_ in point_cloud_data])
# colors = np.array([(r/255, g/255, b/255) for _, _, _, r, g, b, *_ in point_cloud_data])
# pcd = o3d.geometry.PointCloud()
# pcd.points = o3d.utility.Vector3dVector(points)
# pcd.colors = o3d.utility.Vector3dVector(colors)

# o3d.visualization.draw_geometries([pcd], window_name='3D Point Cloud')

# point_cloud_data = np.load('/local/home/gmarsich/Desktop/steps_3RScan/3RScan_original/out/scenes/754e884c-ea24-2175-8b34-cead19d4198d_5/data.npy')
# points = np.array([(x, y, z) for x, y, z, *_ in point_cloud_data])
# colors = np.array([(r/255, g/255, b/255) for _, _, _, r, g, b, *_ in point_cloud_data])
# pcd_2 = o3d.geometry.PointCloud()
# pcd_2.points = o3d.utility.Vector3dVector(points)
# pcd_2.colors = o3d.utility.Vector3dVector(colors)

# o3d.visualization.draw_geometries([pcd_2], window_name='3D Point Cloud')

# final = pcd
# final += pcd_2


# point_cloud_data = np.load('/local/home/gmarsich/Desktop/steps_3RScan/3RScan_original/out/scenes/754e884c-ea24-2175-8b34-cead19d4198d_5/data.npy')
# points = np.array([(x, y, z) for x, y, z, *_ in point_cloud_data])
# colors = np.array([(r/255, g/255, b/255) for _, _, _, r, g, b, *_ in point_cloud_data])
# pcd_3 = o3d.geometry.PointCloud()
# pcd_3.points = o3d.utility.Vector3dVector(points)
# pcd_3.colors = o3d.utility.Vector3dVector(colors)

# o3d.visualization.draw_geometries([pcd_3], window_name='3D Point Cloud')

# final += pcd_3
# o3d.visualization.draw_geometries([final], window_name='3D Point Cloud')

