"""
This module provides functions to extract changelog information from a markdown file.
"""

import os
import re
import sys
from re import Match
from typing import Any, Optional

import toml


def print_current_version() -> None:
    """
    Prints the version number of the latest/next release in the changelog.

    Returns:
        None
    """
    print(f"Changelog version: {get_current_version()}")
    print(f"Pyproject version: {get_version_from_pyproject()}")


def get_current_version() -> str:
    """
    Returns the version number of the latest release in the changelog.

    :return: The version number of the latest release.
    :rtype: str
    """
    current_script_dir: str = os.path.dirname(os.path.realpath(__file__))
    changelog_file: str = os.path.join(current_script_dir, "..", "CHANGELOG.md")

    # Read the changelog from the file
    with open(changelog_file, "r", encoding="utf-8") as file:
        changelog_file_content: str = file.read()

    # Parse and sort the changelog
    changelog: list = sort_changelog(parse_changelog(changelog_file_content))

    # Get the current version
    return changelog[0]["version"]


def get_version_from_pyproject() -> str:
    """
    Extracts the version number from a pyproject.toml file.

    This function loads the pyproject.toml file, navigates to the 'version' field
    under 'tool.poetry', and returns the version number.

    :return: The version number as a string. If the version number is not found, an empty string is
             returned.
    :rtype: str
    """
    current_script_dir: str = os.path.dirname(os.path.realpath(__file__))
    pyproject_file: str = os.path.join(current_script_dir, "..", "pyproject.toml")

    # Load the pyproject.toml file
    pyproject = toml.load(pyproject_file)

    # Get the version number
    version: str = pyproject.get("tool", {}).get("poetry", {}).get("version", "")

    return version


def print_change(ver: str = "") -> None:
    """
    Prints the changes made in a specific version or the latest version.

    :param ver: The version to print the changes for.
    :type ver: str

    :return: None
    """
    current_script_dir: str = os.path.dirname(os.path.realpath(__file__))
    changelog_file: str = os.path.join(current_script_dir, "..", "CHANGELOG.md")

    # Get the version number from the command line arguments, if provided
    version: str = ""
    if len(ver) == 0:
        version = str(sys.argv[1]) if len(sys.argv) > 1 else ""
    else:
        version = ver

    # Read the changelog from the file
    with open(changelog_file, "r", encoding="utf-8") as file:
        changelog_file_content: str = file.read()

    # Parse and sort the changelog
    changelog: list = sort_changelog(parse_changelog(changelog_file_content))

    # Get the changes for the specified version or the latest version
    if version is None:
        version = changelog[0]["version"]
    change: dict = get_change(changelog, version)

    # Print the title
    if change["version"] == "unreleased":
        print("Unreleased Changes:")
    else:
        print(f"Version: {change['version']} ({change['date']})")

    # Print the changes for each category
    for category in change["changes"]:
        print(f"\n{category['category']}:")
        for item in category["changes"]:
            print(f"- {item}")


def parse_changelog(changelog_file_content: str) -> list:
    """
    Parses the content of a changelog file and returns a list of changes.

    :param changelog_file_content: The content of the changelog file as a string.
    :type changelog_file_content: str

    :return: A list of dictionaries, each representing a change.
    :rtype: list
    """

    lines: list = changelog_file_content.split("\n")
    current_version: str = ""
    current_change_category: str = ""
    changelog: list = []
    for line in lines:
        uh_current_version = read_unreleased_headline(line, changelog)
        if uh_current_version:
            current_version = uh_current_version

        vh_current_version = read_version_headline(line, changelog)
        if vh_current_version:
            current_version = vh_current_version

        ch_current_change_category = read_category_headline(
            line, current_version, changelog
        )
        if ch_current_change_category:
            current_change_category = ch_current_change_category

        read_change_item(line, current_version, current_change_category, changelog)

    return changelog


def read_unreleased_headline(line: str, changelog: list) -> Optional[str]:
    """
    Reads a line from the changelog and checks if it starts with "## [Unreleased]".

    :param line: The line to check.
    :type line: str
    :param changelog: The current changelog list.
    :type changelog: list

    :return: The version if the line starts with "## [Unreleased]", None otherwise.
    :rtype: Optional[str]
    """

    match: bool = line.startswith("## [Unreleased]")

    if match:
        change = {"version": "unreleased", "changes": []}
        changelog.append(change)
        current_version = str(change["version"])
        return current_version

    return None


def read_version_headline(line: str, changelog: list) -> Optional[str]:
    """
    Reads a line from the changelog and checks if it matches the version headline pattern.

    :param line: The line to check.
    :type line: str
    :param changelog: The current changelog list.
    :type changelog: list

    :return: The version if the line matches the pattern, None otherwise.
    :rtype: Optional[str]
    """

    match: Optional[Match[str]] = re.search(
        r"^## \[(\d+)\.(\d+)\.(\d+)\] - (\d{4})-(\d{2})-(\d{2})", line
    )

    if match:
        change: dict[str, Any] = build_change(line)
        changelog.append(change)
        current_version = str(change["version"])
        return current_version

    return None


def read_category_headline(
    line: str, current_version: str, changelog: list
) -> Optional[str]:
    """
    Reads a line from the changelog and checks if it matches the category headline pattern.

    :param line: The line to check.
    :type line: str
    :param current_version: The current version.
    :type current_version: str
    :param changelog: The current changelog list.
    :type changelog: list

    :return: The category if the line matches the pattern, None otherwise.
    :rtype: Optional[str]
    """

    match: Optional[Match[str]] = re.search(r"^### (.+)", line)

    if match:
        current_change_category = match.group(1)
        cc_change: dict = get_change(changelog, current_version)

        if not isinstance(cc_change["changes"], list):
            cc_change["changes"] = []

        cc_change["changes"].append(
            {"category": current_change_category, "changes": []}
        )
        return current_change_category

    return None


def read_change_item(
    line: str, current_version: str, current_change_category: str, changelog: list
) -> None:
    """
    Reads a line from the changelog and checks if it matches the change item pattern.

    :param line: The line to check.
    :type line: str
    :param current_version: The current version.
    :type current_version: str
    :param current_change_category: The current change category.
    :type current_change_category: str
    :param changelog: The current changelog list.
    :type changelog: list

    :return: None
    """

    ci_match: Optional[Match[str]] = re.search(r"^- (.+)", line)

    if ci_match:
        change_item: str = ci_match.group(1)
        ci_change: dict = get_change(changelog, current_version)
        change_category: dict = get_change_category(ci_change, current_change_category)

        if not isinstance(change_category["changes"], list):
            change_category["changes"] = []

        change_category["changes"].append(change_item)


def build_change(title: str) -> dict[str, Any]:
    """
    Builds a change dictionary from a title line.

    :param title: The title line.
    :type title: str

    :return: A dictionary representing a change.
    :rtype: dict[str, Any]
    """
    match: Optional[Match[str]] = re.search(
        r"^## \[(\d+)\.(\d+)\.(\d+)\] - (\d{4})-(\d{2})-(\d{2})", title
    )

    if match:
        major: str = match.group(1)
        minor: str = match.group(2)
        bugfix: str = match.group(3)
        year: str = match.group(4)
        month: str = match.group(5)
        day: str = match.group(6)

        return {
            "version": f"{major}.{minor}.{bugfix}",
            "date": f"{year}-{month}-{day}",
            "changes": [],
        }

    return {}


def get_change(changelog: list, version: str) -> dict:
    """
    Gets a change from the changelog by version.

    :param changelog: The changelog.
    :type changelog: list
    :param version: The version to get the change for.
    :type version: str

    :return: The change for the given version, or the first change if version is None.
    :rtype: dict
    """
    if version is None:
        return changelog[0]
    return next((c for c in changelog if c["version"] == version), {})


def get_change_category(change: dict, category: str) -> dict:
    """
    Gets a change category from a change.

    :param change: The change.
    :type change: dict
    :param category: The category to get.
    :type category: str

    :return: The change category for the given category.
    :rtype: dict
    """
    return next((c for c in change["changes"] if c["category"] == category), {})


def sort_changelog(changelog: list) -> list:
    """
    Sorts the changelog list by version number in descending order.
    The "unreleased" version, if it exists, is always placed at the beginning of the list.

    :param changelog: The changelog list to sort.
    :type changelog: list

    :return: The sorted changelog list.
    :rtype: list
    """
    unreleased: list = [
        change for change in changelog if change["version"] == "unreleased"
    ]
    released: list = [
        change for change in changelog if change["version"] != "unreleased"
    ]

    released.sort(
        key=lambda change: list(map(int, change["version"].split("."))), reverse=True
    )

    return unreleased + released
