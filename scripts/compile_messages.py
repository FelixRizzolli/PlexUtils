"""
This module provides a function to compile internationalized messages.
"""
import os
import subprocess


def compile_messages() -> None:
    """
    Compile the internationalized messages from .po to .mo files.

    This function traverses the 'locale' directory and for each language,
    it compiles the .po files into .mo files using the 'msgfmt' command.
    """
    current_script_dir = os.path.dirname(os.path.realpath(__file__))
    locale_dir = os.path.join(current_script_dir, '../locale')

    # Traverse through each language directory in the 'locale' directory
    for language in os.listdir(locale_dir):
        language_dir = os.path.join(locale_dir, language)
        lc_messages_dir = os.path.join(language_dir, 'LC_MESSAGES')

        # Check if the 'LC_MESSAGES' directory exists
        if os.path.isdir(lc_messages_dir):
            # Traverse through each .po file in the 'LC_MESSAGES' directory
            for po_file in os.listdir(lc_messages_dir):
                compile_po_file(lc_messages_dir, po_file)


def compile_po_file(po_dir: str, po_file: str) -> None:
    """
    Compiles a .po file into a .mo file using the 'msgfmt' command.

    This function checks if the provided directory path ends with '.po', indicating it's a .po file.
    If it is, the function constructs the path to the .mo file that will be created, and then runs
    the 'msgfmt' command to compile the .po file into a .mo file.

    Args:
        po_dir (str): The directory path of the .po file.
        po_file (str): The name of the .po file.

    Raises:
        CalledProcessError: If the 'msgfmt' command fails.
    """
    if po_dir.endswith('.po'):
        mo_file: str = os.path.join(po_dir, po_file[:-3] + '.mo')

        # Compile the .po file into a .mo file
        subprocess.run(['msgfmt', '-o', mo_file, po_file], check=True)

