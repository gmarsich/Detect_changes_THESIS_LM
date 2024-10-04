'''This script performs an alignment of the frl apartments in the Replica dataset, because frl apartments don't have a common reference system even
if the six scenes basically represent the same room. It will provide the transformation matrix.'''

'''This script was inspired by this tutorial: https://www.open3d.org/docs/release/tutorial/pipelines/global_registration.html'''

# environment: sceneGraphs_groundTruth_Replica DONE


import open3d as o3d
import os
import numpy as np
import copy


#
# Variables to set
#

target_name = "frl_apartment_0" # its reference system will be used as world reference system
source_name = "frl_apartment_1" # to be moved according to the world reference system

seeRenderings = False # do you want to see the renderings step by step?

basePath = "/local/home/gmarsich/Desktop/data_Replica"



#
# Automatic variable: they should be ok like that
#

folder_results = basePath # where should the results be stored?

name_listInstances = "list_instances.txt"
name_folderSegmentation = "Segmentation"

path_listInstances_a = os.path.join(basePath, target_name, name_listInstances) # path to a file generated with another script, where data on the pcd was collected
path_listInstances_b = os.path.join(basePath, source_name, name_listInstances) # path to a file generated with another script, where data on the pcd was collected

path_meshSemantics_a = os.path.join(basePath, target_name, name_folderSegmentation) # path to the folder containing the meshes of the instances of the target
path_meshSemantics_b = os.path.join(basePath, source_name, name_folderSegmentation) # path to the folder containing the meshes of the instances of the source

# point_cloud_a = o3d.io.read_point_cloud(os.path.join("/local/home/gmarsich/data2TB/DATASETS/Replica/", target_name, "mesh.ply"))
# point_cloud_b = o3d.io.read_point_cloud(os.path.join("/local/home/gmarsich/data2TB/DATASETS/Replica/", source_name, "mesh.ply"))

os.makedirs(folder_results, exist_ok=True)



#
# Get the point clouds of some interesting instances
#

# TODO: one may try to take a subset in {ceiling, wall, floor, stair} (or a subset of specific walls) and see if the alignment is better.
    # An assessment metric would be required

def get_IDs_object(path_listInstances, name):
    '''Given the name in English, return the list of the IDs
    of the corresponding instances'''

    with open(path_listInstances, 'r') as file:
        lines = file.readlines()

    list_IDs = []
    for line in lines:
        parts = line.split()
        if parts[1] == name:
            list_IDs.append(parts[0])

    return list_IDs


def get_pointCloud_fromName(path_listInstances, path_meshSemantics, name, color = None):
    '''Given the name in English, return the pcd of the instance(s)'''

    list_IDs = get_IDs_object(path_listInstances, name)
    list_nameMeshes = [f'mesh_semantic.ply_{i}.ply' for i in list_IDs]

    pcd = o3d.io.read_point_cloud(os.path.join(path_meshSemantics, list_nameMeshes[0]))
    if len(list_nameMeshes) > 1:
        for name_mesh in list_nameMeshes[1:]:
            pcd_tmp = o3d.io.read_point_cloud(os.path.join(path_meshSemantics, name_mesh))
            pcd += pcd_tmp

    if color != None:
        pcd.paint_uniform_color(color)

    return pcd


pcd_ceiling_a = get_pointCloud_fromName(path_listInstances_a, path_meshSemantics_a, "ceiling")
pcd_ceiling_b = get_pointCloud_fromName(path_listInstances_b, path_meshSemantics_b, "ceiling")

pcd_wall_a = get_pointCloud_fromName(path_listInstances_a, path_meshSemantics_a, "wall") # all the walls in the scene
pcd_wall_b = get_pointCloud_fromName(path_listInstances_b, path_meshSemantics_b, "wall") # all the walls in the scene

pcd_floor_a = get_pointCloud_fromName(path_listInstances_a, path_meshSemantics_a, "floor")
pcd_floor_b = get_pointCloud_fromName(path_listInstances_b, path_meshSemantics_b, "floor")

pcd_stair_a = get_pointCloud_fromName(path_listInstances_a, path_meshSemantics_a, "stair")
pcd_stair_b = get_pointCloud_fromName(path_listInstances_b, path_meshSemantics_b, "stair")


pcd_references_a = pcd_ceiling_a # pcd_references_a is the pcd with the instances that will be used to get the transformation matrix
pcd_references_a += pcd_wall_a
pcd_references_a += pcd_floor_a
pcd_references_a += pcd_stair_a
# o3d.visualization.draw_geometries([pcd_references_a])

pcd_references_b = pcd_ceiling_b # pcd_references_b is the pcd with the instances that will be used to get the transformation matrix
pcd_references_b += pcd_wall_b
pcd_references_b += pcd_floor_b
pcd_references_b += pcd_stair_b
# o3d.visualization.draw_geometries([pcd_references_b])



#
# Get the transformation matrix
#


def draw_registrationResult(source, target, transformation):
    source_temp = copy.deepcopy(source)
    target_temp = copy.deepcopy(target)
    source_temp.paint_uniform_color([1, 0.706, 0])
    target_temp.paint_uniform_color([0, 0.651, 0.929])
    source_temp.transform(transformation)
    o3d.visualization.draw_geometries([source_temp, target_temp],
                                      zoom=0.4559,
                                      front=[0.6452, -0.3036, -0.7011],
                                      lookat=[1.9892, 2.0208, 1.8945],
                                      up=[-0.2779, -0.9482, 0.1556])
    
if seeRenderings:
    draw_registrationResult(pcd_references_a, pcd_references_b, np.identity(4)) # visualise the initial setup


def preprocess_pointCloud(pcd, voxel_size):
    print(":: Downsample with a voxel size %.3f." % voxel_size)
    pcd_down = pcd.voxel_down_sample(voxel_size)

    radius_normal = voxel_size * 2
    print(":: Estimate normal with search radius %.3f." % radius_normal)
    #pcd_down.estimate_normals(o3d.geometry.KDTreeSearchParamHybrid(radius=radius_normal, max_nn=30))

    radius_feature = voxel_size * 5
    print(":: Compute FPFH feature with search radius %.3f." % radius_feature)
    pcd_fpfh = o3d.pipelines.registration.compute_fpfh_feature(
        pcd_down,
        o3d.geometry.KDTreeSearchParamHybrid(radius=radius_feature, max_nn=100))
    return pcd_down, pcd_fpfh


def prepare_dataset(voxel_size, pcd_references_a, pcd_references_b):
    print(":: Load two point clouds and disturb initial pose.")

    target = pcd_references_a
    source = pcd_references_b

    source_down, source_fpfh = preprocess_pointCloud(source, voxel_size)
    target_down, target_fpfh = preprocess_pointCloud(target, voxel_size)
    return source, target, source_down, target_down, source_fpfh, target_fpfh


voxel_size = 0.05  # means 5cm for this dataset
source, target, source_down, target_down, source_fpfh, target_fpfh = prepare_dataset(voxel_size, pcd_references_a, pcd_references_b) # source is pcd_references_a, target is pcd_references_b


def execute_fastGlobalRegistration(source_down, target_down, source_fpfh, target_fpfh, voxel_size):
    distance_threshold = voxel_size * 0.5
    print(":: Apply fast global registration with distance threshold %.3f" \
            % distance_threshold)
    result = o3d.pipelines.registration.registration_fgr_based_on_feature_matching(
        source_down, target_down, source_fpfh, target_fpfh,
        o3d.pipelines.registration.FastGlobalRegistrationOption(
            maximum_correspondence_distance=distance_threshold))
    return result

result_fast = execute_fastGlobalRegistration(source_down, target_down, source_fpfh, target_fpfh, voxel_size)

if seeRenderings:
    draw_registrationResult(source_down, target_down, result_fast.transformation) # visualise the result after the global registration


def refine_registration(source, target, voxel_size):
    distance_threshold = voxel_size * 0.4
    print(":: Point-to-plane ICP registration is applied on original point")
    print("   clouds to refine the alignment. This time we use a strict")
    print("   distance threshold %.3f." % distance_threshold)
    result_refinement = o3d.pipelines.registration.registration_icp(
        source, target, distance_threshold, result_fast.transformation,
        o3d.pipelines.registration.TransformationEstimationPointToPlane())
    return result_refinement

result_refinement = refine_registration(source, target, voxel_size)

if seeRenderings:
    draw_registrationResult(source, target, result_refinement.transformation) # visualise the result after the refinement



#
# Create a folder where to store the results and save the transformation matrix
#

name_results = source_name + "_to_"+ target_name
path_results = os.path.join(folder_results, "results_alignment", name_results)
os.makedirs(path_results, exist_ok=True)
np.savetxt(os.path.join(path_results, name_results + ".txt"), result_refinement.transformation, fmt='%.18e')
