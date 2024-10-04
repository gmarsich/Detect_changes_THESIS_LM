import open3d as o3d

colored_point_cloud = o3d.io.read_point_cloud('/local/home/gmarsich/Desktop/data_Replica/frl_apartment_0/scannet200_mask3d_1/mesh_labelled.ply')
o3d.visualization.draw_geometries([colored_point_cloud])

print(f"First point: {colored_point_cloud.points[0]}")