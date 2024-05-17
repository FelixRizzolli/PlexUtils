"""
This module provides functionality to measure and report test coverage for a Python project.
"""

import os
import unittest

from coverage import Coverage


def test_coverage():
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

    # Generate an HTML report in the 'htmlcov' directory
    html_report_dir = os.path.join(
        current_script_dir, "..", "reports", "coverage", "html"
    )
    cov.html_report(directory=html_report_dir)

    # Optionally, you can generate an XML report
    xml_report_dir = os.path.join(
        current_script_dir, "..", "reports", "coverage", "xml", "coverage.xml"
    )
    cov.xml_report(outfile=xml_report_dir)

    # Generate an LCOV report
    lcov_report_dir = os.path.join(
        current_script_dir, "..", "reports", "coverage", "lcov", "lcov.info"
    )
    cov.lcov_report(outfile=lcov_report_dir)

    # Generate a JSON report
    json_report_dir = os.path.join(
        current_script_dir, "..", "reports", "coverage", "json", "coverage.json"
    )
    cov.json_report(outfile=json_report_dir)


# Call the test_coverage function
if __name__ == "__main__":
    test_coverage()
