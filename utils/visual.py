import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm
import imageio.v2 as imageio
import os
import argparse
import logging
import json
import hashlib


def setup_logger(log_file):
    # Create a logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    # Create a file handler
    fh = logging.FileHandler(log_file)
    fh.setLevel(logging.DEBUG)

    # Create a console handler that outputs only ERROR level logs and above
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)

    # Create a formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # Add handlers to the logger
    if not logger.handlers:
        logger.addHandler(fh)
        logger.addHandler(ch)

    return logger

def plot_first_frame_from_npy(npy_file_path, img_file_path, axis=0, logger=None):
    # Load 3D data
    data = np.load(npy_file_path)

    # Check the validity of the axis
    if axis < 0 or axis > 2:
        raise ValueError("Axis must be 0, 1, or 2")

    # Determine the global minimum and maximum values of the data
    data_min = min(-0.1, np.min(data))
    data_max = max(0.1, np.max(data))

    # Use TwoSlopeNorm to fix 0 values to the middle color of the coolwarm colormap
    norm = TwoSlopeNorm(vmin=data_min, vcenter=0, vmax=data_max)

    # Plot the first slice image
    plt.figure()

    # Plot the slice image with a fixed colorbar range
    if axis == 0:
        plt.imshow(data[0, :, :], cmap='coolwarm', origin='lower', norm=norm)
    elif axis == 1:
        plt.imshow(data[:, 0, :], cmap='coolwarm', origin='lower', norm=norm)
    else:
        plt.imshow(data[:, :, 0], cmap='coolwarm', origin='lower', norm=norm)

    plt.colorbar()  # Add colorbar
    plt.axis('off')  # Hide axes

    # Add title indicating the time step
    plt.title('Initial Condition')  # Title set as "Initial Condition"

    # Save the plot as a PNG image
    plt.savefig(img_file_path, bbox_inches='tight', pad_inches=0)
    plt.close('all')

    if logger:
        logger.info(f"PNG image has been successfully saved to {img_file_path}")

def create_gif_from_npy(npy_file_path, gif_file_path, temp_dir='temp_gif_frames', axis=0, duration=0.1, max_frames=40, logger=None):
    # Create output directory
    os.makedirs(os.path.dirname(gif_file_path), exist_ok=True)

    # Load 3D data
    data = np.load(npy_file_path)

    # Check the validity of the axis
    if axis < 0 or axis > 2:
        raise ValueError("Axis must be 0, 1, or 2")

    # Get the number of slices along the specified axis
    num_slices = data.shape[axis]

    # If the number of slices is greater than max_frames, downsample to max_frames
    if num_slices > max_frames:
        idx_map = np.arange(0, num_slices, num_slices // max_frames)
        idx_map = idx_map[:max_frames]
    else:
        idx_map = np.arange(num_slices)

    # Determine the global minimum and maximum values of the data
    data_min = min(-0.1, np.min(data))
    data_max = max(0.1, np.max(data))

    # Use TwoSlopeNorm to fix 0 values to the middle color of the coolwarm colormap
    norm = TwoSlopeNorm(vmin=data_min, vcenter=0, vmax=data_max)

    # Create a temporary directory to store slice images
    os.makedirs(temp_dir, exist_ok=True)

    # Save each slice as a PNG image
    filenames = []
    for idx in idx_map:
        plt.figure()

        # Plot the slice image with a fixed colorbar range
        if axis == 0:
            plt.imshow(data[idx, :, :], cmap='coolwarm', origin='lower', norm=norm)
        elif axis == 1:
            plt.imshow(data[:, idx, :], cmap='coolwarm', origin='lower', norm=norm)
        else:
            plt.imshow(data[:, :, idx], cmap='coolwarm', origin='lower', norm=norm)

        plt.colorbar()  # Add colorbar
        plt.axis('off')  # Hide axes

        # Add title indicating the time step
        plt.title(f'Time Step {idx+1}')  # Title set as "Time Step k"

        temp_filename = os.path.join(temp_dir, f'slice_{idx}.png')
        plt.savefig(temp_filename, bbox_inches='tight', pad_inches=0)
        plt.close('all')
        filenames.append(temp_filename)

    # Create GIF file
    temp_gif_file_path = os.path.join(temp_dir, 'temp.gif')
    with imageio.get_writer(temp_gif_file_path, mode='I', duration=duration, loop=0) as writer:
        for filename in filenames:
            image = imageio.imread(filename)
            writer.append_data(image)

    os.move(temp_gif_file_path, gif_file_path)
    # Delete temporary files
    for filename in filenames:
        os.remove(filename)
    os.rmdir(temp_dir)

    if logger:
        logger.info(f"GIF file has been successfully saved to {gif_file_path}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Create GIF files from CFDBench 3D data")
    parser.add_argument('--name', type=str, help="Name of the CFDBench subdataset")
    parser.add_argument('--dir', type=str, help="Root directory of the CFDBench subdataset")
    parser.add_argument('--log_dir', type=str, default='log', help="Directory to save log files")
    parser.add_argument('--temp_dir', type=str, default='temp_gif_frames', help="Temporary directory to save PNG files")
    parser.add_argument('--out_dir', type=str, default='gif', help="Output subdirectory to save GIF files")
    parser.add_argument('--vars', type=str, nargs='+', help="Variable names to create GIF files for")
    parser.add_argument('--types', type=str, nargs='+', help="Data types to create GIF files for")
    parser.add_argument('--cases_start', type=int, nargs='+', help="Start index of different types of cases")
    parser.add_argument('--cases_end', type=int, nargs='+', help="End index of different types of cases")
    parser.add_argument('--axis', type=int, default=0, help="Axis to slice the 3D data along")
    parser.add_argument('--duration', type=float, default=0.1, help="Duration of each frame in the GIF file")
    parser.add_argument('--max_frames', type=int, default=40, help="Maximum number of frames of the GIF file")
    args = parser.parse_args()

    # check the validity of the arguments
    if args.axis < 0 or args.axis > 2:
        raise ValueError("Axis must be 0, 1, or 2")
    if args.duration <= 0:
        raise ValueError("Duration must be positive")
    if len(args.types) != len(args.cases_start) or len(args.cases_start) != len(args.cases_end):
        raise ValueError("Length of types, cases_start, and cases_end must be the same")

    # create directories
    dir = args.dir
    out_dir = os.path.join(args.out_dir, args.name)
    log_dir = args.log_dir
    # generate identifier based on args
    args_dict = vars(args).copy()
    args_json = json.dumps(args_dict, sort_keys=True)
    hash_object = hashlib.sha256(args_json.encode())
    temp_dir = os.path.join(args.temp_dir, hash_object.hexdigest())
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(args.log_dir, exist_ok=True)

    # create GIF files for each variable and data type
    for type_str, cases_start, cases_end in zip(args.types, args.cases_start, args.cases_end):
        logger = setup_logger(os.path.join(log_dir, f'{args.name}_{type_str}.log'))
        for case in range(cases_start, cases_end):
            case_str = f"{case:04d}"
            for var_str in args.vars:
                npy_file_path = os.path.join(dir, type_str, f'case{case_str}', f'{var_str}.npy')
                img_file_path = os.path.join(out_dir, type_str, f'case{case_str}', f'{var_str}_ic.png')
                gif_file_path = os.path.join(out_dir, type_str, f'case{case_str}', f'{var_str}.gif')
                if not os.path.exists(img_file_path):
                    plot_first_frame_from_npy(npy_file_path, img_file_path, axis=args.axis, logger=logger)
                if not os.path.exists(gif_file_path):
                    create_gif_from_npy(npy_file_path, gif_file_path, temp_dir=temp_dir, axis=args.axis, duration=args.duration, logger=logger, max_frames=args.max_frames)
