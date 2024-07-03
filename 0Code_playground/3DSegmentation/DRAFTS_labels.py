import open3d as o3d
import os
import numpy as np

pcd_mask3D = o3d.io.read_point_cloud(os.path.join("/local/home/gmarsich/data2TB/LabelMaker/processed_ARKitScenes/40753679/intermediate/scannet200_mask3d_1/mesh_labelled.ply")) # TODO TOSET: change the name of the point cloud to open
#o3d.visualization.draw([pcd_mask3D])


import numpy as np
import open3d as o3d
import open3d.visualization.gui as gui
import open3d.visualization.rendering as rendering


def high_level():
    app = gui.Application.instance
    app.initialize()

    points = pcd_mask3D

    vis = o3d.visualization.O3DVisualizer("Rendering of the point cloud", 1024, 768)
    vis.show_settings = True
    vis.add_geometry("Points", points)
    for idx in range(0, 1):
        vis.add_3d_label(points.points[idx], "UFFA")
    vis.reset_camera_to_default()

    app.add_window(vis)
    app.run()

if __name__ == "__main__":
    high_level()





## WORKING CODE

# import open3d as o3d
# import os
# import numpy as np

# pcd_mask3D = o3d.io.read_point_cloud(os.path.join("/local/home/gmarsich/data2TB/LabelMaker/processed_ARKitScenes/40753679/intermediate/scannet200_mask3d_1/mesh_labelled.ply")) # TODO TOSET: change the name of the point cloud to open
# #o3d.visualization.draw([pcd_mask3D])


# import numpy as np
# import open3d as o3d
# import open3d.visualization.gui as gui
# import open3d.visualization.rendering as rendering


# def high_level():
#     app = gui.Application.instance
#     app.initialize()

#     points = pcd_mask3D

#     vis = o3d.visualization.O3DVisualizer("Rendering of the point cloud", 1024, 768)
#     vis.show_settings = True
#     vis.add_geometry("Points", points)
#     for idx in range(0, 1):
#         vis.add_3d_label(points.points[idx], "UFFA")
#     vis.reset_camera_to_default()

#     app.add_window(vis)
#     app.run()

# if __name__ == "__main__":
#     high_level()







# # WORKING CODE

# ----------------------------------------------------------------------------
# -                        Open3D: www.open3d.org                            -
# ----------------------------------------------------------------------------
# Copyright (c) 2018-2023 www.open3d.org
# SPDX-License-Identifier: MIT
# ----------------------------------------------------------------------------

# import numpy as np
# import open3d as o3d
# import open3d.visualization.gui as gui
# import open3d.visualization.rendering as rendering


# def make_point_cloud(npts, center, radius):
#     pts = np.random.uniform(-radius, radius, size=[npts, 3]) + center
#     cloud = o3d.geometry.PointCloud()
#     cloud.points = o3d.utility.Vector3dVector(pts)
#     colors = np.random.uniform(0.0, 1.0, size=[npts, 3])
#     cloud.colors = o3d.utility.Vector3dVector(colors)
#     return cloud

# def high_level():
#     app = gui.Application.instance
#     app.initialize()

#     points = make_point_cloud(100, (0, 0, 0), 1.0)

#     vis = o3d.visualization.O3DVisualizer("Open3D - 3D Text", 1024, 768)
#     vis.show_settings = True
#     vis.add_geometry("Points", points)
#     for idx in range(0, len(points.points)):
#         vis.add_3d_label(points.points[idx], "{}".format(idx))
#     vis.reset_camera_to_default()

#     app.add_window(vis)
#     app.run()

# if __name__ == "__main__":
#     high_level()