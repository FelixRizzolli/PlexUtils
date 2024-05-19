"""
This module automates the code formatting and linting process for a Python project.

It uses the `isort` tool to sort import statements, `black` to enforce consistent
code formatting,and `pylint` to identify coding errors and enforce coding standards.
The script is designed to be run from the command line and will process the specified
directories: 'plexutils', 'scripts', and 'tests'.
"""

import os
import subprocess


def lint():
    """
    Run formatting and linting tools on the project's directories.

    This function retrieves the absolute paths for the 'plexutils', 'scripts', and
    'tests' directories, and sequentially runs `isort`, `black`, and `pylint` on them.
    It ensures that the code adheres to Python's PEP 8 style guide and is free from
    common coding issues.

    The function assumes that `isort`, `black`, and `pylint` are installed in the
    current environment.
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

    # Run the formatting and linting tools
    run_isort(directories)
    run_black(directories)
    run_pylint(directories)


def run_isort(directories):
    """
    Runs the isort tool on the specified directories.

    isort is a Python utility / library to sort imports alphabetically, and
    automatically separated into sections.

    Args:
        directories (str): The directories to run isort on.
    """
    print("Running isort...")
    subprocess.run(f"isort {directories}", shell=True, check=True)


def run_black(directories):
    """
    Runs the black tool on the specified directories.

    Black is the uncompromising Python code formatter. By using it, you agree
    to cede control over minutiae of hand-formatting.

    Args:
        directories (str): The directories to run black on.
    """
    print("Running black...")
    subprocess.run(f"black {directories}", shell=True, check=True)


def run_pylint(directories):
    """
    Runs the pylint tool on the specified directories.

    Pylint is a tool that checks for errors in Python code, tries to enforce
    a coding standard and looks for code smells.

    Args:
        directories (str): The directories to run pylint on.
    """
    print("Running pylint...")
    subprocess.run(f"pylint {directories}", shell=True, check=True)


if __name__ == "__main__":
    lint()
