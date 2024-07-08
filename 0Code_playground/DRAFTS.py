import open3d as o3d
import os
import numpy as np

# Show the segmentation with Mask3D (computed by LabelMaker)
pcd_mask3D = o3d.io.read_point_cloud("/local/home/gmarsich/data2TB/LabelMaker/processed_ARKitScenes/40753679/intermediate/scannet200_mask3d_1/mesh_labelled.ply") # TODO TOSET: change the name of the point cloud to open
o3d.visualization.draw_geometries([pcd_mask3D])