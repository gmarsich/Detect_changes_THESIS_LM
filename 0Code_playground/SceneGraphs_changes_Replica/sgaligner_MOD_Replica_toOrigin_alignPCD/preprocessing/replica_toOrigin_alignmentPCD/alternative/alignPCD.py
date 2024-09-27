'''This script tries to perform an alignment of two objects (coming from different scenes of the Replica dataset).
"Tries" because it is not granted that two objects are the same. The script will provide the transformation matrix.'''

'''This script was inspired by this tutorial: https://www.open3d.org/docs/release/tutorial/pipelines/global_registration.html'''

# environment: sgm


import open3d as o3d
import os
import numpy as np
import copy


def get_transformationMatrix(point_cloud_target, point_cloud_source, seeRenderings):

    def draw_registrationResult(source, target, transformation):
        source_temp = copy.deepcopy(source)
        target_temp = copy.deepcopy(target)
        source_temp.paint_uniform_color([1, 0.706, 0])
        target_temp.paint_uniform_color([0, 0.651, 0.929])
        source_temp.transform(transformation)
        o3d.visualization.draw_geometries([source_temp, target_temp])
        
    if seeRenderings:
        draw_registrationResult(point_cloud_source, point_cloud_target, np.identity(4)) # visualise the initial setup


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


    def prepare_dataset(voxel_size, point_cloud_target, point_cloud_source):
        print(":: Load two point clouds and disturb initial pose.")

        target = point_cloud_target
        source = point_cloud_source

        source_down, source_fpfh = preprocess_pointCloud(source, voxel_size)
        target_down, target_fpfh = preprocess_pointCloud(target, voxel_size)
        return source, target, source_down, target_down, source_fpfh, target_fpfh


    voxel_size = 0.05  # means 5cm for this dataset
    source, target, source_down, target_down, source_fpfh, target_fpfh = prepare_dataset(voxel_size, point_cloud_target, point_cloud_source)


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

    return result_refinement.transformation



#
#
# Tests
#
#

#
# Variables to set
#

path_target_pcd = "/local/home/gmarsich/Desktop/data_Replica/frl_apartment_0/Segmentation/mesh_semantic.ply_4.ply" # its reference system will be used as world reference system; scene 0
path_source_pcd = "/local/home/gmarsich/Desktop/data_Replica/frl_apartment_1/Segmentation/mesh_semantic.ply_103.ply" # to be moved according to the world reference system; scene 1

point_cloud_target = o3d.io.read_point_cloud(path_target_pcd)
point_cloud_source = o3d.io.read_point_cloud(path_source_pcd)

seeRenderings = True # do you want to see the renderings step by step?

# o3d.visualization.draw_geometries([point_cloud_target])
# o3d.visualization.draw_geometries([point_cloud_source])

o3d.visualization.draw_geometries([point_cloud_target, point_cloud_source])

matrix = get_transformationMatrix(point_cloud_target, point_cloud_source, seeRenderings)

o3d.visualization.draw_geometries([point_cloud_source, point_cloud_target])
o3d.visualization.draw_geometries([point_cloud_source.transform(matrix), point_cloud_target])

