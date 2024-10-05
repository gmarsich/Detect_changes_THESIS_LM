In this folder I enquired on how to render the point cloud of a scene in the Hypersim dataset, given the images and other information.
The environment that has been used is `thesisPlayground_pointClouds_env`.

In a first case, positions of the points in the image were directly given (folder `withPositions`), in the second case the depth were given (folder `withDepths`). Enter the two folders to render the point cloud you need.

`apply_tonemap.py` is a file used as support to transform the given `.hdf5` files (RGB images) to `.hdf5` files with the right tonemap. It is used internally by the files in `withPositions` and `withDepths`.
`open_hdf5_files.py` is to visualise a `.hdf5` file and to save it in `.png`.