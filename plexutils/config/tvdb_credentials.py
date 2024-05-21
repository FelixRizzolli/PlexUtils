"""
This module contains the TVDBCredentials class which is used to store and retrieve
TVDB API credentials.
"""


class TVDBCredentials:
    """
    A class used to represent TVDB API credentials.
    """

    def __init__(self, api_key: str, api_pin: str):
        """
        Constructs all the necessary attributes for the TVDBCredentials object.

        Args:
            api_key(str): The TVDB API key.
            api_pin(str): The TVDB API pin.
        """
        self._api_key: str = api_key
        self._api_pin: str = api_pin

    @property
    def api_key(self) -> str:
        """
        Returns the TVDB API key.

        Returns:
            str: The TVDB API key.
        """
        return self._api_key

    @property
    def api_pin(self) -> str:
        """
        Returns the TVDB API pin.

        Returns:
            str: The TVDB API pin.
        """
        return self._api_pin
