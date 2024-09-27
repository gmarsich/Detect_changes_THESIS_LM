import open3d as o3d

colored_point_cloud = o3d.io.read_point_cloud('/local/home/gmarsich/Desktop/Thesis/0Code_playground/SceneGraphs_changes_Replica/withPCA/preprocessing/results/frl_apartment_0_withIDs.ply')
colored_point_cloud_2 = o3d.io.read_point_cloud('/local/home/gmarsich/Desktop/Thesis/0Code_playground/SceneGraphs_changes_Replica/withPCA/preprocessing/results/frl_apartment_1_withIDs.ply')
o3d.visualization.draw_geometries([colored_point_cloud, colored_point_cloud_2])