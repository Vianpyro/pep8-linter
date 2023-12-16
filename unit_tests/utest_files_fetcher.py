"""
Unit Tests for File Fetcher Module

This script contains unit tests to verify the functionality of the 'fetch_github_files' function \
    defined in the 'files_fetcher' module.
It uses Python's 'unittest' framework to create test cases for success and failure scenarios of \
    file fetching, as well as for validating the parsing of command-line arguments.

Example Usage:
    python -m unit_tests.utest_files_fetcher

Test Cases:
- 'test_fetch_github_files_success': Mocks a successful response and checks if the \
    'fetch_github_files' function returns the expected list of file download URLs.
- 'test_fetch_github_files_failure': Mocks a failed response and asserts that the \
    'fetch_github_files' function raises a 'ConnectionError' when unable to fetch files.
"""
import unittest
from unittest.mock import patch
from files_fetcher import fetch_github_files


class TestFileFetcher(unittest.TestCase):
    """
    Test case for the File Fetcher module.

    This class contains unit tests to validate the functionality of the 'fetch_github_files' \
        function within the 'files_fetcher' module.

    Test Cases:
    - 'test_fetch_github_files_success': Validates the successful fetching of files by mocking \
      a successful response from the API and checking the expected output.
    - 'test_fetch_github_files_failure': Tests the handling of a failed response from the API \
      by mocking a failure scenario and verifying that it raises a 'ConnectionError'.
    """

    def test_fetch_github_files_success(self):
        """
        Test the 'fetch_github_files' function for successful file fetching.

        This test case mocks a successful API response and checks if the 'fetch_github_files'
        function returns the expected list of file download URLs.
        """
        # Mocking requests.get() to return a predefined response
        with patch("files_fetcher.requests.get") as mocked_get:
            mocked_response = mocked_get.return_value
            mocked_response.status_code = 200
            mocked_response.json.return_value = [
                {
                    "type": "file",
                    "name": "example.pep",
                    "download_url": "http://example.com/example.pep",
                }
                # Add more mocked data as needed
            ]

            # Testing the fetch_github_files function with mock data
            result = fetch_github_files("owner", "repo", "branch", "*.pep")

            # Asserting that the result contains expected data
            self.assertEqual(result, ["http://example.com/example.pep"])

    def test_fetch_github_files_failure(self):
        """
        Test the 'fetch_github_files' function for handling a failed API response.

        This test case mocks a failed API response and verifies that the 'fetch_github_files' \
            function correctly raises a 'ConnectionError' when unable to fetch files.
        """
        # Mocking requests.get() to simulate a failed response
        with patch("files_fetcher.requests.get") as mocked_get:
            mocked_response = mocked_get.return_value
            mocked_response.status_code = 404  # Simulating failure status code

            # Testing the fetch_github_files function with failed response
            with self.assertRaises(ConnectionError):
                fetch_github_files("owner", "repo", "branch", "*.pep")


if __name__ == "__main__":
    unittest.main()
