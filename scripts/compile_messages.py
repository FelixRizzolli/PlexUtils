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
            for file in os.listdir(lc_messages_dir):
                if file.endswith('.po'):
                    po_file = os.path.join(lc_messages_dir, file)
                    mo_file = os.path.join(lc_messages_dir, file[:-3] + '.mo')

                    # Compile the .po file into a .mo file
                    subprocess.run(['msgfmt', '-o', mo_file, po_file], check=True)
