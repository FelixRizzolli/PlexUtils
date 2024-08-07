"""
This module automates the code formatting and linting process for a Python project.

It uses the `isort` tool to sort import statements, `black` to enforce consistent
code formatting,and `pylint` to identify coding errors and enforce coding standards.
The script is designed to be run from the command line and will process the specified
directories: 'plexutils', 'scripts', and 'tests'.
"""

import os
import subprocess
import tempfile

import mypy.api

from scripts.changelog import get_current_version as get_version_from_changelog
from scripts.changelog import get_version_from_pyproject


def lint() -> None:
    """
    Run formatting and linting tools on the project's directories.

    This function retrieves the absolute paths for the 'plexutils', 'scripts', and
    'tests' directories, and sequentially runs `isort`, `black`, and `pylint` on them.
    It ensures that the code adheres to Python's PEP 8 style guide and is free from
    common coding issues.

    The function assumes that `isort`, `black`, and `pylint` are installed in the
    current environment.

    :return: None
    """
    # Get the absolute path of the current script
    current_script_dir: str = os.path.dirname(os.path.realpath(__file__))

    # Define the project directory
    project_dir: str = os.path.join(current_script_dir, "..")

    # Define the directories to lint
    source_dir: str = os.path.join(project_dir, "plexutils")
    scripts_dir: str = os.path.join(project_dir, "scripts")
    tests_dir: str = os.path.join(project_dir, "tests")
    directories: str = f"{source_dir} {scripts_dir} {tests_dir}"

    # Run the formatting and linting tools
    run_isort(directories)
    run_black(directories)
    run_pylint(directories)
    run_mypy(directories)
    check_version()


def run_isort(directories: str) -> None:
    """
    Runs the isort tool on the specified directories.

    isort is a Python utility / library to sort imports alphabetically, and
    automatically separated into sections.

    :param directories: The directories to run isort on.
    :type directories: str

    :return: None
    """
    print("Running isort...")
    subprocess.run(f"isort {directories}", shell=True, check=True)


def run_black(directories: str) -> None:
    """
    Runs the black tool on the specified directories.

    Black is the uncompromising Python code formatter. By using it, you agree
    to cede control over minutiae of hand-formatting.

    :param directories: The directories to run black on.
    :type directories: str

    :return: None
    """
    print("Running black...")
    subprocess.run(f"black {directories}", shell=True, check=True)


def run_pylint(directories: str) -> None:
    """
    Runs the pylint tool on the specified directories.

    Pylint is a tool that checks for errors in Python code, tries to enforce
    a coding standard and looks for code smells.

    :param directories: The directories to run pylint on.
    :type directories: str

    :return: None
    """
    print("Running pylint...")
    subprocess.run(f"pylint {directories}", shell=True, check=True)


def run_mypy(directories: str) -> None:
    """
    Runs the mypy tool on the specified directories.

    Mypy is an optional static type checker for Python. You can add type hints
    to your Python programs using the standard Python type hint syntax and
    then use mypy to type check them.

    :param directories: The directories to run mypy on.
    :type directories: str

    :return: None
    """
    print("Running mypy...")

    # Create a temporary mypy.ini file
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as temp:
        temp.write("[mypy]\n")
        temp.write(f"files = {', '.join(directories.split(' '))}\n")
        temp.write("check_untyped_defs = True\n")
        temp.write("[mypy-tvdb_v4_official.*]\n")
        temp.write("ignore_missing_imports = True\n")

    # The mypy options you want to use
    mypy_options = ["--config-file", temp.name]

    # Run mypy and capture the result
    result = mypy.api.run(mypy_options)

    # If the result contains any output, print it
    if result[0]:  # stdout
        print(result[0])

    # If the result contains any error messages, print them
    if result[1]:  # stderr
        print(result[1])

    # Delete the temporary mypy.ini file
    os.unlink(temp.name)


def check_version() -> None:
    """
    Compares the version number from the changelog and the pyproject.toml file.

    This function retrieves the version number from the changelog and the pyproject.toml file.
    It then compares these two version numbers and prints a message indicating whether they
    match or not.

    :return: None
    """
    print("Comparing versions...")

    # Get the version from the changelog and pyproject.toml
    version_changelog: str = get_version_from_changelog()
    version_pyproject: str = get_version_from_pyproject()

    if version_changelog == version_pyproject:
        print("Versions match.")
    else:
        print(f"Changelog version: {version_changelog}")
        print(f"Pyproject version: {version_pyproject}")
        print("Versions do not match!")


if __name__ == "__main__":
    lint()
