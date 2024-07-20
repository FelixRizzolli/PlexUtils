"""
This module provides functions to run unit tests and generate coverage reports.

It includes functions to run unit tests in the 'tests' directory using Python's built-in
unittest module. It also provides functions to generate coverage reports in multiple
formats (HTML, XML, LCOV, JSON) using the Coverage.py library.

Functions:
    run_tests: Runs unit tests in the 'tests' directory.
    run_test_coverage: Executes test coverage analysis for the project and generates
                       detailed reports.
    create_html_report: Creates an HTML coverage report.
    create_xml_report: Creates an XML coverage report.
    create_lcov_report: Creates an LCOV coverage report.
    create_json_report: Creates a JSON coverage report.
"""

import os
import subprocess
import unittest

from coverage import Coverage


def run_tests() -> None:
    """
    Runs unit tests in the 'tests' directory.

    This function uses Python's built-in unittest module to discover and run unit tests.
    The tests are run using the  'poetry run python -m unittest discover tests' command,
    which ensures that the tests are run in the virtual environment managed by Poetry.

    :return: None
    """
    subprocess.run(
        "poetry run python -m unittest discover tests", shell=True, check=True
    )


def run_test_coverage() -> None:
    """
    Execute test coverage analysis for the project.

    This function starts the coverage measurement, discovers all tests in the 'tests' directory,
    runs them, and then stops the coverage. It reports the coverage data to the console and
    generates detailed reports in multiple formats including HTML, XML, LCOV, and JSON.

    Reports:
        - Console: Displays a summary of the coverage analysis.
        - HTML: Generates a directory 'htmlcov' with an interactive HTML report.
        - XML: Creates a file 'coverage.xml' with the coverage report in XML format.
        - LCOV: Generates an LCOV report file 'lcov.info'.
        - JSON: Creates a JSON report file 'coverage.json'.

    :return: None
    """
    # Get the absolute path of the current script
    current_script_dir: str = os.path.dirname(os.path.realpath(__file__))

    # Start the coverage measurement
    sources_dir = os.path.join(current_script_dir, "../plexutils")
    cov = Coverage(source=[sources_dir])
    cov.start()

    # Discover and run tests
    tests_dir = os.path.join(current_script_dir, "../tests")
    loader = unittest.TestLoader()
    suite = loader.discover(tests_dir)
    runner = unittest.TextTestRunner()
    runner.run(suite)

    # Stop the coverage measurement and save
    cov.stop()
    cov.save()

    # Report the results to the console
    cov.report()

    # Generate detailed reports
    report_dir: str = os.path.join(current_script_dir, "..", "reports", "coverage")
    create_html_report(cov, report_dir)
    create_xml_report(cov, report_dir)
    create_lcov_report(cov, report_dir)
    create_json_report(cov, report_dir)


def create_html_report(cov: Coverage, report_dir: str) -> None:
    """
    Creates an HTML coverage report.

    :param cov: The coverage object.
    :type cov: Coverage
    :param report_dir: The directory where the report will be saved.
    :type report_dir: str

    :return: None
    """
    html_report_dir: str = os.path.join(report_dir, "html")
    cov.html_report(directory=html_report_dir)


def create_xml_report(cov: Coverage, report_dir: str) -> None:
    """
    Creates an XML coverage report.

    :param cov: The coverage object.
    :type cov: Coverage
    :param report_dir: The directory where the report will be saved.
    :type report_dir: str

    :return: None
    """
    xml_report_dir: str = os.path.join(report_dir, "xml", "coverage.xml")
    cov.xml_report(outfile=xml_report_dir)


def create_lcov_report(cov: Coverage, report_dir: str) -> None:
    """
    Creates an LCOV coverage report.

    :param cov: The coverage object.
    :type cov: Coverage
    :param report_dir: The directory where the report will be saved.
    :type report_dir: str

    :return: None
    """
    lcov_report_dir: str = os.path.join(report_dir, "lcov", "lcov.info")
    cov.lcov_report(outfile=lcov_report_dir)


def create_json_report(cov: Coverage, report_dir: str) -> None:
    """
    Creates a JSON coverage report.

    :param cov: The coverage object.
    :type cov: Coverage
    :param report_dir: The directory where the report will be saved.
    :type report_dir: str

    :return: None
    """
    json_report_dir: str = os.path.join(report_dir, "json", "coverage.json")
    cov.json_report(outfile=json_report_dir)
