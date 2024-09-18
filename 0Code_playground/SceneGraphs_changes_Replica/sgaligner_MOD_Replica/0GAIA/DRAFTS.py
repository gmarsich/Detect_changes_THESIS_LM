import open3d as o3d
import os

point_cloud_a = o3d.io.read_point_cloud("/local/home/gmarsich/Desktop/steps_3RScan/3RScan_original_allScenes/scenes/4acaebcc-6c10-2a2a-858b-29c7e4fb410d/labels.instances.annotated.v2.ply")
point_cloud_b = o3d.io.read_point_cloud("/local/home/gmarsich/Desktop/steps_3RScan/3RScan_original_allScenes/scenes/754e884c-ea24-2175-8b34-cead19d4198d/labels.instances.align.annotated.v2.ply")
pcd = o3d.io.read_point_cloud("/local/home/gmarsich/Desktop/data_Replica/frl_apartment_0/Segmentation/colored_mesh.ply")

print(pcd)
o3d.visualization.draw_geometries([pcd])
