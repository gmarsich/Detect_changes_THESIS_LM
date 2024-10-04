import open3d as o3d


colored_point_cloud = o3d.io.read_point_cloud('/local/home/gmarsich/Desktop/data_Replica/frl_apartment_0/frl_apartment_0_withIDs.ply')
colored_point_cloud_2 = o3d.io.read_point_cloud('/local/home/gmarsich/Desktop/data_Replica/frl_apartment_5/frl_apartment_5_withIDs.ply')
o3d.visualization.draw_geometries([colored_point_cloud, colored_point_cloud_2])


