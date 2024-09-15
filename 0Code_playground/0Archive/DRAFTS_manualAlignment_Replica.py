import open3d as o3d
import os
import numpy as np

#
# Variables
#

path_listInstances_a = "/local/home/gmarsich/Desktop/data_Replica/frl_0/list_instances.txt"
path_listInstances_b = "/local/home/gmarsich/Desktop/data_Replica/frl_1/list_instances.txt"

path_meshSemantics_a = "/local/home/gmarsich/Desktop/data_Replica/frl_0/Segmentation/"
path_meshSemantics_b = "/local/home/gmarsich/Desktop/data_Replica/frl_1/Segmentation/"

point_cloud_a = o3d.io.read_point_cloud("/local/home/gmarsich/data2TB/DATASETS/Replica/frl_apartment_0/mesh.ply")
point_cloud_b = o3d.io.read_point_cloud("/local/home/gmarsich/data2TB/DATASETS/Replica/frl_apartment_1/mesh.ply")

#o3d.visualization.draw_geometries([point_cloud_a])
#o3d.visualization.draw_geometries([point_cloud_b])


#
# Useful functions
#

def get_IDs_object(path_listInstances, name):
    with open(path_listInstances, 'r') as file:
        lines = file.readlines()

    list_IDs = []
    for line in lines:
        parts = line.split()
        if parts[1] == name:
            list_IDs.append(parts[0])

    return list_IDs


def get_pointCloud_name(path_listInstances, path_meshSemantics, name, color):
    list_IDsName = get_IDs_object(path_listInstances, name)
    list_nameMeshes = [f'mesh_semantic.ply_{i}.ply' for i in list_IDsName]

    pcd = o3d.io.read_point_cloud(os.path.join(path_meshSemantics, list_nameMeshes[0]))
    if len(list_nameMeshes) > 1:
        for name_mesh in list_nameMeshes[1:]:
            pcd_tmp = o3d.io.read_point_cloud(os.path.join(path_meshSemantics, name_mesh))
            pcd += pcd_tmp

    pcd.paint_uniform_color(color)

    return pcd


#
# Color the floor
#

pcd_floor_a = get_pointCloud_name(path_listInstances_a, path_meshSemantics_a, "floor", [0, 0, 1]) # for frl_0 139933 different values of the z coordinate
#o3d.visualization.draw_geometries([pcd_floor_a])

pcd_floor_b = get_pointCloud_name(path_listInstances_b, path_meshSemantics_b, "floor", [0, 1, 0])
#o3d.visualization.draw_geometries([pcd_floor_b])



#
# Color the walls
# the wall I am interested in has object ID: frl_0: 14, frl_1: 87
#

pcd_wall_a = get_pointCloud_name(path_listInstances_a, path_meshSemantics_a, "wall", [0, 1, 1])
#o3d.visualization.draw_geometries([pcd_wall_a])

pcd_wall_b = get_pointCloud_name(path_listInstances_b, path_meshSemantics_b, "wall", [1, 1, 0])
#o3d.visualization.draw_geometries([pcd_wall_b])

# # Find the wall I am interested in
# list_walls_a = get_IDs_object(path_listInstances_a, "wall")
# pcd_wallBase_a = o3d.io.read_point_cloud(os.path.join(path_meshSemantics_a, "mesh_semantic.ply_14.ply"))
# pcd_wallBase_a.paint_uniform_color([0.7, 0.7, 0.7])
# #o3d.visualization.draw_geometries([pcd_wallBase_a, pcd_floor_a])

pcd_wallBase_a = o3d.io.read_point_cloud(os.path.join(path_meshSemantics_a, "mesh_semantic.ply_14.ply"))
pcd_wallBase_b = o3d.io.read_point_cloud(os.path.join(path_meshSemantics_b, "mesh_semantic.ply_87.ply"))










# TODO: compute the ideal plane of the wall that I selected












#
# Computation: align the two point clouds on the same plane (i.e., floor at the same height). Consider a plane with MSE
#
# TODO: shall we find the planes with MSE (on the points on the floor) or is it ok to assume that the floor is parallel to the z plane?

# Average height of the floor for pcd_floor_a
points_a = np.asarray(pcd_floor_a.points)
z_coordinates_a = points_a[:, 2]
average_z_a = np.mean(z_coordinates_a) # for frl_0 is -1.5887081996809662

# Average height of the floor for pcd_floor_b
points_b = np.asarray(pcd_floor_b.points)
z_coordinates_b = points_b[:, 2]
average_z_b = np.mean(z_coordinates_b) # for frl_0 is -1.474548179234713

delta = average_z_b - average_z_a


def translate_z(pcd, delta):
    points = np.asarray(pcd.points)
    points[:, 2] += delta
    pcd.points = o3d.utility.Vector3dVector(points)

    return pcd

# pcd_test_b = translate_z(pcd_floor_b, -delta)
# o3d.visualization.draw_geometries([pcd_test_b, pcd_floor_a])



#
# Computation: rotation around O (to get parallel walls). Remark that there are two possibilities, and only one is right
#
# TODO: here I assume that the floor is parallel to the z plane

# [x, y, z] for frl_0: [destra-sinistra, avanti-indietro, su-giù]











'''Random'''
#
# Create a plane parallel to plane z
#

# def create_plane(width, height, center=[0, 0, 1.5], resolution=10):
#     # Create a grid of points representing the plane
#     x = np.linspace(-width / 2, width / 2, resolution)
#     y = np.linspace(-height / 2, height / 2, resolution)
#     xx, yy = np.meshgrid(x, y)
#     zz = np.zeros_like(xx)  # Plane lies on z=0

#     # Combine into point cloud
#     points = np.vstack((xx.ravel(), yy.ravel(), zz.ravel())).T

#     # Create TriangleMesh object from the grid of points
#     mesh = o3d.geometry.TriangleMesh()
#     mesh.vertices = o3d.utility.Vector3dVector(points)

#     # Define triangles connecting the points
#     triangles = []
#     for i in range(resolution - 1):
#         for j in range(resolution - 1):
#             idx = i * resolution + j
#             triangles.append([idx, idx + 1, idx + resolution])
#             triangles.append([idx + 1, idx + resolution + 1, idx + resolution])

#     mesh.triangles = o3d.utility.Vector3iVector(triangles)

#     # Optionally, translate the plane to the desired center
#     mesh.translate(center)

#     # Set a color for the plane (optional)
#     mesh.paint_uniform_color([0.7, 0.7, 0.7])  # Light gray color

#     return mesh

# # Define plane dimensions
# width = 4.0
# height = 4.0

# # Create the plane mesh
# plane_mesh = create_plane(width, height)

# # Visualize the plane
# #o3d.visualization.draw_geometries([plane_mesh])





#
# Create line given two points
#

# def create_line_set(point1, point2, color):
#     lineset = o3d.geometry.LineSet()
#     lineset.points = o3d.utility.Vector3dVector([point1, point2])
#     lineset.lines = o3d.utility.Vector2iVector([[0, 1]])
#     lineset.paint_uniform_color(color)    
#     return lineset






#
# Draw point cloud with reference point
#

# pcd_total = pcd_wall_a
# pcd_total += pcd_wall_b
# o3d.visualization.draw_geometries([pcd_total])


# # Draw and add a point
# point_cloud_1 = o3d.geometry.PointCloud()
# point = np.array([[0, 0, 0]])
# point_cloud_1.points = o3d.utility.Vector3dVector(point)
# point_cloud_1.colors = o3d.utility.Vector3dVector([[1, 0, 0]])

# point_cloud_1 += pcd_total

# o3d.visualization.draw_geometries([point_cloud_1])




#
# Computations: find the plane of the floor with MSE
#

# def fit_plane(points):
#     """
#     Fit a plane to the given points using Least Squares method.
#     """
#     points = np.asarray(points)

#     A = np.c_[points[:, 0], points[:, 1], np.ones(points.shape[0])]
#     B = points[:, 2]

#     # Solve the least squares problem to find the plane parameters
#     # A * [a, b, c] = B
#     # where plane equation is ax + by + c = z
#     plane_params, _, _, _ = np.linalg.lstsq(A, B, rcond=None)

#     a, b, c = plane_params

#     z_pred = A @ plane_params
#     mse = np.mean((B - z_pred) ** 2)

#     return a, b, c, mse

# def visualize_plane(pcd, plane_params, range_x, range_y, step):
#     """
#     Visualize the point cloud and the fitted plane.
#     """
#     a, b, c, _ = plane_params

#     # Visualize the point cloud and the plane
#     o3d.visualization.draw_geometries([pcd, plane_mesh])





#
# Computations: find the average z of the floor
#


# # Average height of the floor for pcd_floor_a
# points_a = np.asarray(pcd_floor_a.points)
# z_coordinates_a = points_a[:, 2]
# average_z_a = np.mean(z_coordinates_a) # for frl_0 is -1.5887081996809662

# # Average height of the floor for pcd_floor_b
# points_b = np.asarray(pcd_floor_b.points)
# z_coordinates_b = points_b[:, 2]
# average_z_b = np.mean(z_coordinates_b) # for frl_0 is -1.474548179234713



#
# frl_0: find nice parameters for the rotation
#

# def createPlane_parallelX(width, height, center=[2.05, -7, 1.42], resolution=10):
#     # Create a grid of points representing the plane
#     y = np.linspace(-height / 2, height / 2, resolution)
#     z = np.linspace(-width / 2, width / 2, resolution)
#     yy, zz = np.meshgrid(y, z)
#     xx = np.zeros_like(yy)  # Plane lies on x=0

#     # Combine into point cloud
#     points = np.vstack((xx.ravel(), yy.ravel(), zz.ravel())).T

#     # Create TriangleMesh object from the grid of points
#     mesh = o3d.geometry.TriangleMesh()
#     mesh.vertices = o3d.utility.Vector3dVector(points)

#     # Define triangles connecting the points
#     triangles = []
#     for i in range(resolution - 1):
#         for j in range(resolution - 1):
#             idx = i * resolution + j
#             triangles.append([idx, idx + 1, idx + resolution])
#             triangles.append([idx + 1, idx + resolution + 1, idx + resolution])

#     # Duplicate triangles for double-sided rendering
#     mesh.triangles = o3d.utility.Vector3iVector(triangles + [list(reversed(tri)) for tri in triangles])
    
#     # Compute normals and apply to both sides
#     mesh.compute_vertex_normals()
#     mesh.triangle_normals = o3d.utility.Vector3dVector(np.asarray(mesh.triangle_normals).tolist() * 2)

#     # Optionally, translate the plane to the desired center
#     mesh.translate(center)

#     # Set a color for the plane (optional)
#     mesh.paint_uniform_color([0.7, 0.7, 0.7])  # Light gray color

#     return mesh


# def createPlane_parallelY(width, height, center=[2.05, -7, 1.42], resolution=10):
#     # Create a grid of points representing the plane
#     x = np.linspace(-width / 2, width / 2, resolution)
#     z = np.linspace(-height / 2, height / 2, resolution)
#     xx, zz = np.meshgrid(x, z)
#     yy = np.zeros_like(xx)  # Plane lies on y=0

#     # Combine into point cloud
#     points = np.vstack((xx.ravel(), yy.ravel(), zz.ravel())).T

#     # Create TriangleMesh object from the grid of points
#     mesh = o3d.geometry.TriangleMesh()
#     mesh.vertices = o3d.utility.Vector3dVector(points)

#     # Define triangles connecting the points
#     triangles = []
#     for i in range(resolution - 1):
#         for j in range(resolution - 1):
#             idx = i * resolution + j
#             triangles.append([idx, idx + 1, idx + resolution])
#             triangles.append([idx + 1, idx + resolution + 1, idx + resolution])

#     # Duplicate triangles to make the plane double-sided
#     triangles += [list(reversed(tri)) for tri in triangles]

#     mesh.triangles = o3d.utility.Vector3iVector(triangles)
    
#     # Optionally, compute normals
#     mesh.compute_vertex_normals()
    
#     # Optionally, translate the plane to the desired center
#     mesh.translate(center)

#     # Set a color for the plane (optional)
#     mesh.paint_uniform_color([0.7, 0.7, 0.7])  # Light gray color

#     return mesh


# def createPlane_parallelZ(width, height, center=[2.05, -7, 1.42], resolution=10):
#     # Create a grid of points representing the plane
#     x = np.linspace(-width / 2, width / 2, resolution)
#     y = np.linspace(-height / 2, height / 2, resolution)
#     xx, yy = np.meshgrid(x, y)
#     zz = np.zeros_like(xx)  # Plane lies on z=0

#     # Combine into point cloud
#     points = np.vstack((xx.ravel(), yy.ravel(), zz.ravel())).T

#     # Create TriangleMesh object from the grid of points
#     mesh = o3d.geometry.TriangleMesh()
#     mesh.vertices = o3d.utility.Vector3dVector(points)

#     # Define triangles connecting the points
#     triangles = []
#     for i in range(resolution - 1):
#         for j in range(resolution - 1):
#             idx = i * resolution + j
#             triangles.append([idx, idx + 1, idx + resolution])
#             triangles.append([idx + 1, idx + resolution + 1, idx + resolution])
    
#     # Duplicate triangles to make the plane double-sided
#     triangles += [list(reversed(tri)) for tri in triangles]
    
#     mesh.triangles = o3d.utility.Vector3iVector(triangles)
    
#     # Optionally, compute normals
#     mesh.compute_vertex_normals()
    
#     # Optionally, translate the plane to the desired center
#     mesh.translate(center)

#     # Set a color for the plane (optional)
#     mesh.paint_uniform_color([0.7, 0.7, 0.7])  # Light gray color

#     return mesh


# x_right_a = 2.145
# x_left_a = 2.05
# z_a = 1.42
# plane_right_a = createPlane_parallelX(4, 4, [x_right_a, -9.5, 1.5])
# plane_left_a = createPlane_parallelX(4, 4, [x_left_a, -9.5, 1.5])
# plane_down_a = createPlane_parallelZ(4, 4, [2.05, -7, z_a])

# # o3d.visualization.draw_geometries([pcd_wall_a, plane_right_a, plane_left_a, plane_down_a])


# y_behind_b = 2.3
# y_front_b = 2
# z_b = 1.56
# plane_behind_b = createPlane_parallelY(4, 4, [7, y_behind_b, 1.5])
# plane_front_b = createPlane_parallelY(4, 4, [7, y_front_b, 1.5])
# plane_down_b = createPlane_parallelZ(4, 4, [7, 2, z_b])

# # o3d.visualization.draw_geometries([pcd_wall_b, plane_behind_b, plane_front_b, plane_down_b])
