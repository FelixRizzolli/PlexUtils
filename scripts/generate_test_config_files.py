"""
This module contains functions to generate test configuration files.
"""

import os
import shutil


def generate_test_config_files(data_dir, scripts_data_dir):
    """
    Generate test configuration files.

    This function copies configuration files from a source directory
    to a destination directory for testing purposes.

    Parameters:
        data_dir (str): The destination directory where the configuration files will be copied to.
        scripts_data_dir (str): The source directory where the configuration files are located.

    Returns:
        None
    """
    print("generate_test_config_files")
    copy_files(
        os.path.join(scripts_data_dir, "config"), os.path.join(data_dir, "config")
    )
    print("DONE!")


def copy_files(src_dir: str, dst_dir: str):
    """
    Copy files from a source directory to a destination directory.

    This function checks if the destination directory exists, if not, it creates it.
    Then it iterates over all files in the source directory and copies each file to the
    destination directory.

    Parameters:
        src_dir (str): The source directory where the files are located.
        dst_dir (str): The destination directory where the files will be copied to.

    Returns:
        None
    """
    # Check if destination directory exists, if not, create it
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)

    # Iterate over all files in source directory
    for filename in os.listdir(src_dir):
        # Construct full file path
        src_file = os.path.join(src_dir, filename)
        dst_file = os.path.join(dst_dir, filename)

        # Copy file to destination directory
        shutil.copy(src_file, dst_file)
