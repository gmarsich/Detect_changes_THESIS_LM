STEPS:

- use get_transformationMatrix.py to get the transformation matrix
- use create_ply_withSegmentation.py to get colored_mesh_with_IDs.ply (that is aligned with a target scene) and objects.json
- use create_npy_files.py to get the .npy files (each .npy file basically contains a point cloud)
- use create_pkl_files.py to get the .pkl files (each .pkl file contains a dictionary)
- use create_new_dictionary.py to get the new_dict_that will be used as input for SGAligner


PPT:
- what is in .npy, .pkl and anchors_val.json
- facciamo un data_dict senza avere un dataloader
- no GAT perche' ha bisogno di un grafico in input



TESTS:
objectIDs_src = [34, 39, 27, 103, 38, 164] # bike, bike, ceiling, sofa, cup, sink
objectIDs_ref = [77, 93, 10, 4, 66, 59] # bike, bike, ceiling, sofa, mat, book

objectIDs_src = [27, 89, 130, 13] # 1: ceiling, stair, tv-screen, tv-screen
objectIDs_ref = [10, 120, 231, 45, 32] # 0: ceiling, stair, tv-screen, tv-screen, table

objectIDs_src = [27, 89, 130, 13, 2] # 1: ceiling, stair, tv-screen 130, 13, floor
objectIDs_ref = [10, 120, 231, 45, 32, 8] # 0: ceiling, stair, tv-screen 231, 45, table, floor

objectIDs_src = [25, 62, 160] # 1: chair (round), chair (tall), chair
objectIDs_ref = [48, 52] # 0: chair (round), chair (tall)

