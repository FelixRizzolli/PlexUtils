"""
This module automates the code formatting and linting process for a Python project.

It uses the `isort` tool to sort import statements, `black` to enforce consistent code formatting,
and `pylint` to identify coding errors and enforce coding standards. The script is designed to be
run from the command line and will process the specified directories: 'plexutils', 'scripts', and 'tests'.
"""

import os
import subprocess

def lint():
    """
    Run formatting and linting tools on the project's directories.

    This function retrieves the absolute paths for the 'plexutils', 'scripts', and 'tests' directories,
    and sequentially runs `isort`, `black`, and `pylint` on them. It ensures that the code adheres to
    Python's PEP 8 style guide and is free from common coding issues.

    The function assumes that `isort`, `black`, and `pylint` are installed in the current environment.
    """
    # Get the absolute path of the current script
    current_script_dir: str = os.path.dirname(os.path.realpath(__file__))

    # Define the project directory
    project_dir: str = os.path.join(current_script_dir, "..")

    # Define the directories to lint
    source_dir = os.path.join(project_dir, "plexutils")
    scripts_dir = os.path.join(project_dir, "scripts")
    tests_dir = os.path.join(project_dir, "tests")
    directories: str = f"{source_dir} {scripts_dir} {tests_dir}"

    # Run isort
    print("Running isort...")
    subprocess.run(f"isort {directories}", shell=True, check=True)

    # Run black
    print("Running black...")
    subprocess.run(f"black {directories}", shell=True, check=True)

    # Run pylint
    print("Running pylint...")
    subprocess.run(f"pylint {directories}", shell=True, check=True)


if __name__ == "__main__":
    lint()
