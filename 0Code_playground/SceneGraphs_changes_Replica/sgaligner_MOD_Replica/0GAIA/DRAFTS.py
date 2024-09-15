import open3d as o3d
import os

point_cloud_b = o3d.io.read_point_cloud("/local/home/gmarsich/Desktop/Thesis/0Code_playground/SceneGraphs_changes_Replica/sgaligner_MOD_Replica/0GAIA/alignment_Replica/results_alignment/frl_apartment_1_to_frl_apartment_0/frl_apartment_1_ALIGNED_to_frl_apartment_0.ply")
o3d.visualization.draw_geometries([point_cloud_b])