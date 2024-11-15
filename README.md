# Thesis: "Editable 3D scene graphs: detecting changes between two scenes in the Replica dataset" ([Master's degree in Data Science and Scientific Computing](https://dssc.units.it/))

### [Marsich Gaia](https://github.com/gmarsich)

This work tackles the problem of detecting changes in indoor 3D environments by making use of point cloud
 representations and of an organisation of the information relying on scene graphs. The research focuses on
 examining variations in different temporal snapshots of the same scene. Two main methods, one using
 SGAligner and the other relying on PCA, are exploited and compared to detect changes in object
 configurations: the instances can be added, removed, moved or left still.
 
 The study began with a preliminary analysis of point cloud reconstruction, useful for understanding the
 basic framework for the manipulation of point clouds and related data. As segmentation plays a key role in
 being able to recognise changes occurring in an environment, in the following some first segmentation and
 labelling tests were performed.
 
 The idea of the core pipeline consists of three main steps. First,
 the point clouds of both the initial and the updated scenes are segmented to group the datapoints into distinct
 instances, each one associated to a class label. Next, a scene graph is created for each snapshot. Finally,
 changes are detected by comparison using either the approach exploiting SGAligner or the one relying
 on PCA, allowing for the identification of added, removed, moved or stationary objects. The results
 show that both methods, albeit with their limitations, successfully recognise a certain amount of instances
 and changes.



Contents of the repository:

| Element      | Description |
| :---        |    :----:   |
| 0Code_playground      | Tests and drafts       |
| code_thesis   | Final version of the useful code |

## Characteristics of the computer that was used
The code has been run on a machine with:

- OS: Ubuntu 22.04.4 LTS

- GPU: NVIDIA Corporation GP102 [GeForce GTX 1080 Ti]

Different environments were used: the related information is stored in `code_thesis/envs`. The specific environment that was employed for a certain code is indicated in the files themselves.
