"""
GitHub PEP8 File Fetcher

This Python script fetches Pep8-asm files from a GitHub repository using the GitHub API.
It takes command-line arguments for repository details such as owner, repository name, branch, and \
     file model, allowing users to specify the criteria for file retrieval.

The script uses the requests library to interact with the GitHub API and fetches files that match \
    a specified file model (pattern).
It traverses the repository contents recursively, identifying files that match the given model.
Upon successful retrieval, it displays the content of each `.pep` file found.

To execute, run the script providing optional command-line arguments:
    -o/--owner: Repository owner name (default: 'lbajolet')
    -r/--repo: Repository name (default: 'PEP8-examples')
    -b/--branch: Repository branch to select (default: 'master')
    -f/--file-model: Model of files to load (default: '*.pep')

Example Usage:
    python files_fetcher.py -o owner_name -r repository_name -b branch_name -f file_model
"""
from typing import Any
from fnmatch import fnmatchcase
import requests

# GitHub repository details
DEFAULT_OWNER = "lbajolet"
DEFAULT_REPO = "PEP8-examples"
DEFAULT_BRANCH = "master"
DEFAULT_FILE_MODEL = "*.pep"  # File_model of the files to search for


def fetch_file(url: str, **params) -> Any:
    """
    Fetches data from a specified URL using the requests library.

    Args:
    - url (str): The URL to fetch data from.
    - params: Additional parameters to be passed to the request.

    Returns:
    - Any: The fetched data (response content).

    Raises:
    - ConnectionError: If the request to the specified URL fails.
    """
    response = requests.get(url, **params)

    if response.status_code == 200:
        return response.json()

    raise ConnectionError("Failed to fetch repository contents")


def fetch_github_files(owner: str, repo: str, branch: str, file_model: str) -> list:
    """
    Fetches files matching the specified file model within the given GitHub repository.

    Args:
    - owner (str): Repository owner's username or organization.
    - repo (str): Name of the repository.
    - branch (str): Repository branch name to fetch files from.
    - file_model (str): File model (pattern) to match files.

    Returns:
    - list: A list containing download URLs of files that match the file model.
    """
    api_url = f"https://api.github.com/repos/{owner}/{repo}/contents"
    params = {"ref": branch}

    repo_contents = fetch_file(api_url, params=params)
    files = []

    # Function to recursively fetch files
    def fetch_files_recursive(contents):
        for item in contents:
            if item["type"] == "file" and fnmatchcase(item["name"], file_model):
                files.append(item["download_url"])
            elif item["type"] == "dir":
                sub_directory_url = item["url"]
                sub_directory_contents = requests.get(sub_directory_url).json()
                fetch_files_recursive(sub_directory_contents)

    fetch_files_recursive(repo_contents)

    return files


if __name__ == "__main__":
    import argparse

    # Command line argument parser configuration
    def parse_arguments():
        """
        Parses and retrieves command-line arguments provided by the user.

        Returns:
        - Namespace: An object containing parsed argument values.
        """
        parser = argparse.ArgumentParser(description="Pep8 files fetcher")
        parser.add_argument("-o", "--owner", default=DEFAULT_OWNER, help="Repository owner name")
        parser.add_argument("-r", "--repo", default=DEFAULT_REPO, help="Repository name")
        parser.add_argument("-b", "--branch", default=DEFAULT_BRANCH, help="Repository branch to select")
        parser.add_argument("-f", "--file-model", default=DEFAULT_FILE_MODEL, help="Model of files to load")
        return parser.parse_args()

    args = parse_arguments()

    pep_files = fetch_github_files(
        args.owner or None,
        args.repo or None,
        args.branch or None,
        args.file_model or None
    )

    # Display the .pep files
    for file_url in pep_files:
        pep_file_content = requests.get(file_url).text
