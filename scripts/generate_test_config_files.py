import shutil
import os


def generate_test_config_files(data_dir, scripts_data_dir):
    print("generate_test_config_files")
    copy_files(os.path.join(scripts_data_dir, "config"), os.path.join(data_dir, "config"))
    print("DONE!")


def copy_files(src_dir: str, dst_dir: str):
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