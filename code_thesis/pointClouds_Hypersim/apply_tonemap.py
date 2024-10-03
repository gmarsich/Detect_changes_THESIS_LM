# the hints for the tonemap to apply were taken from here: https://github.com/apple/ml-hypersim/blob/main/code/python/tools/scene_generate_images_tonemap.py

import h5py
import glob
import os
import numpy as np
from matplotlib import image as mpimg

def apply_tonemapping(rgb_color):
    gamma = 1.0 / 2.2   # standard gamma correction exponent
    inv_gamma = 1.0 / gamma
    percentile = 90        # we want this percentile brightness value in the unmodified image...
    brightness_nth_percentile_desired = 0.8       # ...to be this bright after scaling

    brightness = 0.3 * rgb_color[:, :, 0] + 0.59 * rgb_color[:, :, 1] + 0.11 * rgb_color[:, :, 2]  # "CCIR601 YIQ" method for computing brightness

    brightness_nth_percentile_current = np.percentile(brightness, percentile)

    scale = np.power(brightness_nth_percentile_desired, inv_gamma) / brightness_nth_percentile_current

    rgb_color_tm = np.power(np.maximum(scale * rgb_color, 0), gamma)
    return rgb_color_tm

def apply_tonemapping_to_hdf5(in_hdf5_file, out_hdf5_file):
    try:
        with h5py.File(in_hdf5_file, "r") as f:
            rgb_color = f["dataset"][:].astype(np.float32)
    except Exception as e:
        print(f"WARNING: Could not load HDF5 file: {in_hdf5_file} - {e}")
        return

    # Apply tonemapping to the RGB data
    tonemapped_rgb = apply_tonemapping(rgb_color)

    # Save tonemapped data to new HDF5 file
    with h5py.File(out_hdf5_file, "w") as f:
        f.create_dataset("tonemapped_rgb", data=tonemapped_rgb)

def apply_tonemapping_to_directory(in_dir, out_dir):
    # Create output directory if it doesn't exist
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    # Find all HDF5 files in the input directory
    in_hdf5_files = glob.glob(os.path.join(in_dir, "*.color.hdf5"))

    for in_hdf5_file in in_hdf5_files:
        # Construct output HDF5 file path
        out_hdf5_file = os.path.join(out_dir, os.path.basename(in_hdf5_file))

        # Apply tonemapping to the input HDF5 file and save tonemapped data to the output HDF5 file
        apply_tonemapping_to_hdf5(in_hdf5_file, out_hdf5_file)

def main():
    # Specify input and output directories
    in_dir = "/path/to/input_directory" # TODO TOSET: should modify the path
    out_dir = "/path/to/output_directory" # TODO TOSET: should modify the path

    # Apply tonemapping to all HDF5 files in the input directory and save tonemapped data to new HDF5 files in the output directory
    apply_tonemapping_to_directory(in_dir, out_dir)

if __name__ == "__main__":
    main()
