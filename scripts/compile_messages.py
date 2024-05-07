"""
This module provides a function to compile internationalized messages.
"""
import os
import subprocess
import logging


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
        subprocess.run(['msgfmt', '-o', mo_file, po_file], check=True)
