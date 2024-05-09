"""
This module provides a function to compile internationalized messages.
"""
import os
import subprocess
import logging
import platform
from enum import Enum


class OS(Enum):
    """
    An enumeration representing common operating systems.

    This Enum is used to standardize the representation of the most common
    operating systems. Each operating system is represented by a string that
    `platform.system()` returns.

    Attributes:
        LINUX (str): Represents the Linux operating system.
        MACOS (str): Represents the macOS operating system.
        WINDOWS (str): Represents the Windows operating system.
    """
    LINUX = 'Linux'.upper()
    MACOS = 'Darwin'.upper()
    WINDOWS = 'Windows'.upper()


def compile_messages() -> None:
    """
    Compile the internationalized messages from .po to .mo files.

    This function traverses the 'locale' directory and for each language,
    it compiles the .po files into .mo files using the 'msgfmt' command.

    Raises:
        FileNotFoundError: If the 'locale' directory does not exist.
        PermissionError: If the script does not have the necessary permissions
                         to access the 'locale' directory.
        subprocess.CalledProcessError: If the 'msgfmt' command fails.
    """
    current_script_dir: str = os.path.dirname(os.path.realpath(__file__))
    locale_dir: str = os.path.join(current_script_dir, '../locale')

    # Check if the compiler is installed
    check_compiler()

    # Traverse through each language directory in the 'locale' directory
    for language in os.listdir(locale_dir):
        language_dir: str = os.path.join(locale_dir, language)
        lc_messages_dir: str = os.path.join(language_dir, 'LC_MESSAGES')

        # Check if the 'LC_MESSAGES' directory exists
        if os.path.isdir(lc_messages_dir):
            # Traverse through each .po file in the 'LC_MESSAGES' directory
            for po_filename in os.listdir(lc_messages_dir):
                try:
                    compile_po_file(lc_messages_dir, po_filename)
                    logging.info("Compiled %s successfully.", po_filename)
                except subprocess.CalledProcessError as e:
                    logging.error("Failed to compile %s: %s", po_filename, str(e))


def compile_po_file(po_dir: str, po_filename: str) -> None:
    """
    Compiles a .po file into a .mo file using the 'msgfmt' command.

    This function checks if the provided file has a '.po' extension.
    If it does, the function constructs the path to the .mo file that will be created, and then runs
    the 'msgfmt' command to compile the .po file into a .mo file.

    Args:
        po_dir (str): The directory path of the .po file.
        po_filename (str): The name of the .po file.

    Raises:
        subprocess.CalledProcessError: If the 'msgfmt' command fails.
    """
    name, ext = os.path.splitext(po_filename)
    if ext == '.po':
        mo_file: str = os.path.join(po_dir, name + '.mo')
        po_file: str = os.path.join(po_dir, po_filename)

        # Compile the .po file into a .mo file
        run_compile_process(mo_file, po_file)


def run_compile_process(mo_file: str, po_file: str) -> None:
    """
    Executes the compilation process for given mo and po files.

    The function uses the 'msgfmt' tool to perform the compilation.
    The operating system is checked to ensure the correct command is executed.

    Args:
        mo_file (str): The path to the output file (.mo).
        po_file (str): The path to the input file (.po).

    Raises:
        subprocess.CalledProcessError: If the compilation process fails.
    """
    operating_system: str = platform.system().upper()

    if operating_system not in [OS.WINDOWS.value, OS.MACOS.value, OS.LINUX.value]:
        print("Operating system not supported: ", operating_system, ".")
        return

    if operating_system == OS.WINDOWS.value:
        try:
            subprocess.run(
                ['pybabel', 'compile', '-d', 'locale'],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            print(f"Command executed successfully. {mo_file} created.")
        except subprocess.CalledProcessError as e:
            print(f"Command failed with error:\n{e.stderr.decode('utf-8')}")
    elif operating_system in [OS.MACOS.value, OS.LINUX.value]:
        try:
            subprocess.run(
                ['msgfmt', '-o', mo_file, po_file],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            print(f"Command executed successfully. {mo_file} created.")
        except subprocess.CalledProcessError as e:
            print(f"Command failed with error:\n{e.stderr.decode('utf-8')}")


def check_compiler() -> bool:
    """
    Checks if the necessary compiler is installed on the system.

    This function checks the operating system using platform.system() and then checks if
    the necessary compiler (pybabel for Windows, msgfmt for macOS and Linux) is installed.
    If the compiler is not installed, it prints instructions on how to install the compiler
    for the specific operating system.
    If the operating system is not supported, it prints an error message.

    Returns:
        bool: True if the necessary compiler is installed or the operating system is not supported,
              False otherwise.
    """
    operating_system: str = platform.system().upper()
    print(f"Operating system: {operating_system}")
    if operating_system == OS.WINDOWS and not is_pybabel_installed():
        print("pybabel is not installed. Please install pybabel first.")
        print("If you are using Windows, you can install it with: "
              + "pip install Babel")
        return False

    if operating_system == OS.MACOS.value and not is_msgfmt_installed():
        print("msgfmt is not installed. Please install msgfmt first.")
        print("If you are using macOS, you can install it with: "
              + "brew install gettext")
        print("Then, you might need to link gettext to make msgfmt available"
              + "brew link --force gettext")
        return False

    if operating_system == OS.LINUX.value and not is_msgfmt_installed():
        print("msgfmt is not installed. Please install msgfmt first.")
        print("If you are using Ubuntu or debian, you can install it with: "
              + "sudo apt-get install gettext")
        return False

    if operating_system not in [OS.WINDOWS.value, OS.MACOS.value,  OS.LINUX.value]:
        print(f"Operating system not supported: {platform.system()}.")

    return True


def is_msgfmt_installed() -> bool:
    """
    Checks if msgfmt is installed on the system.

    This function attempts to run the 'msgfmt --version' command using the subprocess module.
    If the command succeeds, it means msgfmt is installed. If the command fails, it means
    msgfmt is not installed.

    Returns:
        bool: True if msgfmt is installed, False otherwise.
    """
    try:
        subprocess.run(
            ['msgfmt', '--version'],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return True
    except subprocess.CalledProcessError:
        return False


def is_pybabel_installed() -> bool:
    """
    Checks if PyBabel is installed on the system.

    This function attempts to run the 'pybabel --version' command using the subprocess module.
    If the command succeeds, it means PyBabel is installed. If the command fails, it means
    PyBabel is not installed.

    Returns:
        bool: True if PyBabel is installed, False otherwise.
    """
    try:
        subprocess.run(
            ['pybabel', '--version'],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return True
    except subprocess.CalledProcessError:
        return False
