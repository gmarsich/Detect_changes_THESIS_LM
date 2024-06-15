# environment: thesisPlayground_pointClouds_env

'''
The point cloud generated starting from depths is in asset units and with the following system of camera coordinates:

"Our convention for storing camera orientations is that the camera's positive x-axis points right,
the positive y-axis points up, and the positive z-axis points away from where the camera is looking."
(https://github.com/apple/ml-hypersim)

However, in world coordinates the z axis points up (i.e., inverse of gravity)
'''

import numpy as np
import open3d as o3d
import pandas as pd



# path_metadata_camera_parameters example: '/local/home/gmarsich/Desktop/Thesis/0Code_playground/pointClouds_Hypersim/withDepths/metadata_camera_parameters.csv'
# scene example: 'ai_022_006'
# cam_xx example: 'cam_00'
# path_point_cloud example: "/local/home/gmarsich/data2TB/Hypersim/MyThings/point_cloud_DEPTHS_TONEMAP_ai_001_001_cam_00_ASSETS.ply"

def convert_to_meters(path_metadata_camera_parameters, scene, cam_xx, path_point_cloud):

    df_camera_parameters = pd.read_csv(path_metadata_camera_parameters, index_col="scene_name")
    df_ = df_camera_parameters.loc[scene]
    factor_assets_to_meters = df_["settings_units_info_meters_scale"]

    # Load and make a copy of the point cloud
    pcd_assets = o3d.io.read_point_cloud(path_point_cloud)

    pcd_meters = o3d.geometry.PointCloud()
    pcd_meters.points = o3d.utility.Vector3dVector(np.asarray(pcd_assets.points))
    pcd_meters.colors = o3d.utility.Vector3dVector(np.asarray(pcd_assets.colors))
    pcd_meters.normals = o3d.utility.Vector3dVector(np.asarray(pcd_assets.normals))

    # Apply conversion from asset units to meters
    points = np.asarray(pcd_meters.points)
    points *= factor_assets_to_meters
    pcd_meters.points = o3d.utility.Vector3dVector(points)

    # o3d.visualization.draw_geometries([pcd_meters]) # to visualise the point cloud
    o3d.io.write_point_cloud("point_cloud_DEPTHS_TONEMAP_" + scene + "_" + cam_xx + "_METERS" + ".ply", pcd_meters) # to save the point cloud as .ply file # TODO TOSET: change the name of the point cloud, in case



#
# The following two methods are to visualise the point cloud together with the reference axes. The spheres represent units on the axis
#

def create_marker(position, color=[1, 0, 0]):
    sphere = o3d.geometry.TriangleMesh.create_sphere(radius=0.05)
    sphere.paint_uniform_color(color)
    sphere.translate(position)
    return sphere


# path_point_cloud example: "/local/home/gmarsich/data2TB/Hypersim/MyThings/point_cloud_DEPTHS_TONEMAP_ai_001_001_cam_00_METERS.ply"

def render_pcd_and_axes(path_point_cloud, n_points):

    # Load the point cloud
    pcd_assets = o3d.io.read_point_cloud(path_point_cloud)

    # Create a coordinate frame
    coordinate_frame = o3d.geometry.TriangleMesh.create_coordinate_frame(size=1.0, origin=[0, 0, 0])

    # Create markers for units along each axis
    x_markers = [create_marker([i, 0, 0], [1, 0, 0]) for i in range(1, n_points + 1)]
    y_markers = [create_marker([0, i, 0], [0, 1, 0]) for i in range(1, n_points + 1)]
    z_markers = [create_marker([0, 0, i], [0, 0, 1]) for i in range(1, n_points + 1)]

    # Combine all geometries for visualization
    all_geometries = [pcd_assets, coordinate_frame] + x_markers + y_markers + z_markers

    # Visualize the point cloud, coordinate frame, and unit markers
    o3d.visualization.draw_geometries(all_geometries,
                                    zoom=0.5,
                                    front=[0.0, 0.0, -1.0],
                                    lookat=[0.0, 0.0, 0.0],
                                    up=[0.0, -1.0, 0.0])

