import h5py
import numpy as np
import open3d as o3d
import pandas as pd

def get_intrinsics(path_metadata, scene):
    """
    This code takes as input the data from the provided file metadata_camera_parameters.csv (the path of it) and the scene that one wants to analyse.
    The output is the matrix of intrinsics for that scene.
    
    Parameters:
        path_metadata (str): Path to the metadata_camera_parameters.csv file.
        scene (str): The scene to analyse
    
    Returns:
        np.ndarray: The intrinsic matrix for the specified scene.
    """

    # Load the metadata CSV file
    df = pd.read_csv(path_metadata)
    
    # Filter the DataFrame to get the row corresponding to the specified scene
    scene_row = df[df['scene'] == scene]
    
    if scene_row.empty:
        raise ValueError(f"Scene '{scene}' not found in the metadata.")
    
    # Extract the projection matrix elements
    M_proj = np.array([
        [scene_row["M_proj_00"].values[0], scene_row["M_proj_01"].values[0], scene_row["M_proj_02"].values[0], scene_row["M_proj_03"].values[0]],
        [scene_row["M_proj_10"].values[0], scene_row["M_proj_11"].values[0], scene_row["M_proj_12"].values[0], scene_row["M_proj_13"].values[0]],
        [scene_row["M_proj_20"].values[0], scene_row["M_proj_21"].values[0], scene_row["M_proj_22"].values[0], scene_row["M_proj_23"].values[0]],
        [scene_row["M_proj_30"].values[0], scene_row["M_proj_31"].values[0], scene_row["M_proj_32"].values[0], scene_row["M_proj_33"].values[0]]
    ])
    
    # Normalize the matrix by M_proj_33 to ensure the bottom-right value is 1
    M_proj = M_proj / M_proj[3, 3]
    
    # Extract the 3x3 intrinsic matrix from the projection matrix
    intrinsic_matrix = M_proj[:3, :3]
    
    return intrinsic_matrix


# # Example usage
# path_metadata = 'path/to/metadata_camera_parameters.csv'
# scene = 'example_scene'
# intrinsics = get_intrinsics(path_metadata, scene)
# print("Intrinsic Matrix for the scene:")
# print(intrinsics)


def load_hdf5_data(image_file, depth_file):
    """
    Load images and depth data from HDF5 files.
    
    Parameters:
        image_file (str): Path to the HDF5 file containing images.
        depth_file (str): Path to the HDF5 file containing depth maps.
    
    Returns:
        images (np.ndarray): Array of images.
        depths (np.ndarray): Array of depth maps.
    """
    with h5py.File(image_file, 'r') as f:
        images = np.array(f['images'])  # Adjust the key according to your HDF5 structure
    
    with h5py.File(depth_file, 'r') as f:
        depths = np.array(f['depths'])  # Adjust the key according to your HDF5 structure

    return images, depths



def generate_point_cloud(images, depths, intrinsic_matrix):
    """
    Generate point clouds from images and depth maps.
    
    Parameters:
        images (np.ndarray): Array of images.
        depths (np.ndarray): Array of depth maps.
        intrinsic_matrix (np.ndarray): Intrinsic matrix of the camera.
    
    Returns:
        point_clouds (list): List of Open3D PointCloud objects.
    """
    point_clouds = []

    for i in range(len(images)):
        image = images[i]
        depth = depths[i]

        # Create an empty point cloud
        points = []

        # Get the image dimensions
        h, w = depth.shape

        # Create a mesh grid of pixel coordinates
        u, v = np.meshgrid(np.arange(w), np.arange(h))
        u = u.flatten()
        v = v.flatten()

        # Get the corresponding depth values
        z = depth.flatten()

        # Filter out points with zero depth
        valid = z > 0
        u = u[valid]
        v = v[valid]
        z = z[valid]

        # Convert pixel coordinates to normalized image coordinates
        x = (u - intrinsic_matrix[0, 2]) / intrinsic_matrix[0, 0]
        y = (v - intrinsic_matrix[1, 2]) / intrinsic_matrix[1, 1]

        # Create 3D points in the camera coordinate system
        x = x * z
        y = y * z

        # Stack the coordinates into a single array
        points = np.vstack((x, y, z)).T

        # Create Open3D PointCloud object and add it to the list
        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(points)
        point_clouds.append(pcd)

    return point_clouds



def merge_point_clouds(point_clouds):
    """
    Merge multiple point clouds into a single point cloud.
    
    Parameters:
        point_clouds (list): List of Open3D PointCloud objects.
    
    Returns:
        combined_pcd (open3d.geometry.PointCloud): Combined point cloud.
    """
    combined_pcd = o3d.geometry.PointCloud()
    for pcd in point_clouds:
        combined_pcd += pcd
    return combined_pcd