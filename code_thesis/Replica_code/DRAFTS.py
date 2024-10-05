import open3d as o3d

colored_point_cloud = o3d.io.read_point_cloud('/local/home/gmarsich/Desktop/data_Replica/frl_apartment_3/frl_apartment_3_withIDs_LabelMaker.ply')
colored_point_cloud_2 = o3d.io.read_point_cloud('/local/home/gmarsich/Desktop/data_Replica/frl_apartment_1/frl_apartment_1_withIDs_LabelMaker.ply')
o3d.visualization.draw_geometries([colored_point_cloud, colored_point_cloud_2])

# # print(f"First point: {colored_point_cloud.points[0]}")


# # from plyfile import PlyData

# # n_lines = 10

# # # Path to your PLY file
# file_path = '/local/home/gmarsich/Desktop/data_Replica/frl_apartment_1/scannet200_mask3d_1/mesh_labelled.ply'
# # with open(file_path, 'rb') as ply_file:  # Open the file in binary mode
# #     plydata = PlyData.read(ply_file)

# # # Print the header information
# # print(plydata)


# colored_point_cloud = o3d.io.read_point_cloud(file_path)
# print(len(colored_point_cloud.points))

# # Path to your text file
# file_path = '/local/home/gmarsich/Desktop/data_Replica/frl_apartment_1/scannet200_mask3d_1/pred_mask/000.txt'

# # Initialize a counter for the number of lines
# line_count = 0

# # Open the file in read mode and count the lines
# with open(file_path, 'r') as file:
#     for line in file:
#         line_count += 1

# print(f'The file contains {line_count} lines.')

