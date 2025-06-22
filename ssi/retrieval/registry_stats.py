"""
This module is responsible for fetching package statistics from various package registries
like PyPI, npm, etc. These stats are crucial for calculating the Sustainability and
Applicability scores for a given technology.

Metrics to be collected:
- Release frequency and velocity.
- Download counts and trends.
- Number of maintainers and contributors.
- Date of the last release.
"""

import requests

class RegistryFetcher:
    """A base class for fetching data from a package registry."""
    def __init__(self, base_url):
        self.base_url = base_url

    def get_package_info(self, package_name):
        raise NotImplementedError("Each fetcher must implement this method.")


class PyPIFetcher(RegistryFetcher):
    """Fetches package information from the Python Package Index (PyPI)."""
    def __init__(self):
        super().__init__("https://pypi.org/pypi")

    def get_package_info(self, package_name):
        """
        Retrieves JSON metadata for a specific package from PyPI.
        
        Args:
            package_name (str): The name of the package (e.g., 'requests').
            
        Returns:
            dict: A dictionary containing the package metadata, or None on error.
        """
        url = f"{self.base_url}/{package_name}/json"
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data for {package_name} from PyPI: {e}")
            return None

    def get_release_history(self, package_info):
        """Extracts the release history from package info."""
        if not package_info or 'releases' not in package_info:
            return {}
        
        # Returns a dictionary of version numbers to release dates
        return {
            version: releases[0].get('upload_time_iso_8601')
            for version, releases in package_info.get('releases', {}).items() if releases
        }


class PackagistFetcher(RegistryFetcher):
    """Fetches package information from Packagist (for PHP packages)."""
    def __init__(self):
        super().__init__("https://packagist.org")

    def get_package_info(self, package_name):
        """
        Retrieves JSON metadata for a specific package from Packagist.
        
        Args:
            package_name (str): The name of the package (e.g., 'laravel/framework').
            
        Returns:
            dict: A dictionary containing the package metadata, or None on error.
        """
        url = f"{self.base_url}/packages/{package_name}.json"
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data for {package_name} from Packagist: {e}")
            return None


class NpmFetcher(RegistryFetcher):
    """Fetches package information from the npm registry."""
    def __init__(self):
        super().__init__("https://registry.npmjs.org")

    def get_package_info(self, package_name):
        """
        Retrieves JSON metadata for a specific package from npm.
        
        Args:
            package_name (str): The name of the package (e.g., 'react').
            
        Returns:
            dict: A dictionary containing the package metadata, or None on error.
        """
        url = f"{self.base_url}/{package_name}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data for {package_name} from npm: {e}")
            return None


def main():
    """Example usage of the fetcher."""
    print("--- Fetching PyPI Package Statistics ---")
    pypi_fetcher = PyPIFetcher()
    
    package_name = "pandas"
    package_info = pypi_fetcher.get_package_info(package_name)
    
    if package_info:
        info = package_info.get('info', {})
        release_history = pypi_fetcher.get_release_history(package_info)
        last_release_date = next(iter(release_history.values())) if release_history else "N/A"

        print(f"Package: {info.get('name')}")
        print(f"Latest Version: {info.get('version')}")
        print(f"Author: {info.get('author')}")
        print(f"Summary: {info.get('summary')}")
        print(f"Last Release Date: {last_release_date}")
        print(f"Homepage: {info.get('home_page')}")
        print(f"Total Releases: {len(release_history)}")
    print("---------------------------------------")

    print("\n--- Fetching Packagist Package Statistics ---")
    packagist_fetcher = PackagistFetcher()
    
    package_name = "laravel/framework"
    package_info = packagist_fetcher.get_package_info(package_name)
    
    if package_info:
        # Packagist has a different structure
        package_data = package_info.get('package', {})
        versions = package_data.get('versions', {})
        # Get the first version in the dictionary
        latest_version_data = next(iter(versions.values())) if versions else {}

        print(f"Package: {package_data.get('name')}")
        print(f"Latest Version: {latest_version_data.get('version')}")
        print(f"Description: {package_data.get('description')}")
        print(f"Homepage: {package_data.get('repository')}")
        print(f"Total Downloads: {package_data.get('downloads', {}).get('total')}")
    print("---------------------------------------")

    print("\n--- Fetching NPM Package Statistics ---")
    npm_fetcher = NpmFetcher()

    package_name = "react"
    package_info = npm_fetcher.get_package_info(package_name)

    if package_info:
        latest_version = package_info.get('dist-tags', {}).get('latest', 'N/A')
        latest_version_info = package_info.get('versions', {}).get(latest_version, {})
        
        print(f"Package: {package_info.get('name')}")
        print(f"Latest Version: {latest_version}")
        print(f"Description: {package_info.get('description')}")
        print(f"Homepage: {package_info.get('homepage')}")
        print(f"License: {latest_version_info.get('license')}")
    print("---------------------------------------")


if __name__ == "__main__":
    main() 