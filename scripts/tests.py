import subprocess


def run_tests() -> None:
    """
    Runs unit tests in the 'tests' directory.

    This function uses Python's built-in unittest module to discover and run unit tests.
    The tests are run using the  'poetry run python -m unittest discover tests' command,
    which ensures that the tests are run in the virtual environment managed by Poetry.
    """
    subprocess.run("poetry run python -m unittest discover tests", shell=True, check=True)

