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
    LINUX = 'Linux'
    MACOS = 'Darwin'
    WINDOWS = 'Windows'


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
    if platform.system() == OS.WINDOWS:
        subprocess.run(['pybabel', 'compile', '-d', 'locale'], check=True)
    elif platform.system() == OS.MACOS:
        subprocess.run(['msgfmt', '-o', mo_file, po_file], check=True)
    elif platform.system() == OS.LINUX:
        subprocess.run(['msgfmt', '-o', mo_file, po_file], check=True)
    else:
        print(f"Operating system not supported: {platform.system()}.")
