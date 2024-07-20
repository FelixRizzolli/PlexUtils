"""
This module is used to generate the documentation for a project using Sphinx.
"""

import subprocess


def generate_docs() -> None:
    """
    Generates the documentation for a project using Sphinx.
    :return: None
    """

    # Generate the API documentation
    subprocess.run(
        ["poetry", "run", "sphinx-apidoc", "-f", "-o", "docs/source", "plexutils"],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    print("✅ API documentation generated.")

    # Generate the HTML documentation
    subprocess.run(
        ["poetry", "run", "sphinx-build", "-M", "html", "docs/source", "docs/build"],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    print("✅ HTML documentation generated.")
