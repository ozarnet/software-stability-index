"""
This module is responsible for scanning issue trackers like GitHub and GitLab
to gather metrics related to project health and sustainability.

Metrics to be collected:
- Unresolved issue backlog (S2)
- Community support resolution time (S5)
- Bug regression rate
"""

import requests
import os
from datetime import datetime, timedelta

class GitHubIssueScanner:
    """A scanner for fetching issue data from GitHub repositories."""

    def __init__(self, token=None):
        """
        Initializes the scanner with an optional GitHub personal access token.
        
        Args:
            token (str, optional): A GitHub PAT to authenticate and get higher rate limits.
                                   If not provided, will try to use GITHUB_TOKEN env var.
        """
        self.base_url = "https://api.github.com"
        self.search_url = f"{self.base_url}/search/issues"
        self.repo_url = f"{self.base_url}/repos"
        self.token = token or os.getenv("GITHUB_TOKEN")
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
        }
        if self.token:
            self.headers["Authorization"] = f"token {self.token}"

    def _search_issues(self, query):
        """Helper function to perform a search query."""
        try:
            response = requests.get(self.search_url, headers=self.headers, params={'q': query})
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error searching issues with query '{query}': {e}")
            return None

    def get_unresolved_issue_backlog(self, repo_owner, repo_name, days=365):
        """
        Calculates the percentage of unresolved issues created in the last N days.

        Args:
            repo_owner (str): The owner of the repository.
            repo_name (str): The name of the repository.
            days (int): The period in days to look back.

        Returns:
            float: The percentage of unresolved issues, or None on error.
        """
        since_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        repo_qualifier = f"repo:{repo_owner}/{repo_name}"

        # Query for total issues created in the period
        total_query = f"{repo_qualifier} is:issue created:>{since_date}"
        total_result = self._search_issues(total_query)
        if not total_result:
            return None
        total_count = total_result.get('total_count', 0)
        if total_count == 0:
            return 0.0

        # Query for open issues created in the period
        open_query = f"{repo_qualifier} is:issue is:open created:>{since_date}"
        open_result = self._search_issues(open_query)
        if not open_result:
            return None
        open_count = open_result.get('total_count', 0)

        return (open_count / total_count) * 100

    def get_mean_time_to_resolution(self, repo_owner, repo_name, sample_size=100):
        """
        Calculates the Mean Time To Resolution (MTTR) for recently closed issues.

        Args:
            repo_owner (str): The owner of the repository.
            repo_name (str): The name of the repository.
            sample_size (int): The number of recent issues to sample.

        Returns:
            timedelta: The average time to resolve an issue, or None on error.
        """
        url = f"{self.repo_url}/{repo_owner}/{repo_name}/issues"
        params = {
            'state': 'closed',
            'per_page': sample_size,
            'sort': 'updated',
            'direction': 'desc'
        }
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            closed_issues = response.json()

            total_resolution_time = timedelta(0)
            resolved_count = 0

            for issue in closed_issues:
                # Consider only issues that are not pull requests
                if 'pull_request' not in issue and issue.get('closed_at'):
                    created_at = datetime.fromisoformat(issue['created_at'].replace('Z', '+00:00'))
                    closed_at = datetime.fromisoformat(issue['closed_at'].replace('Z', '+00:00'))
                    total_resolution_time += closed_at - created_at
                    resolved_count += 1
            
            if resolved_count == 0:
                return None
                
            return total_resolution_time / resolved_count

        except requests.exceptions.RequestException as e:
            print(f"Error fetching closed issues for {repo_owner}/{repo_name}: {e}")
            return None

    def get_repository_issues(self, repo_owner, repo_name):
        """
        Fetches the total count of open issues for a given repository.
        
        Args:
            repo_owner (str): The owner of the repository (e.g., 'facebook').
            repo_name (str): The name of the repository (e.g., 'react').
            
        Returns:
            int: The count of open issues, or None on error.
        """
        # For this example, we'll just get the count of open issues.
        # A full implementation would handle pagination.
        url = f"{self.repo_url}/{repo_owner}/{repo_name}"
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            repo_data = response.json()
            return repo_data.get('open_issues_count', 0)
        except requests.exceptions.RequestException as e:
            print(f"Error fetching issue data for {repo_owner}/{repo_name}: {e}")
            return None

def main():
    """Example usage of the scanner."""
    print("--- Fetching GitHub Issue Statistics ---")
    # To run this, you may need a GitHub Personal Access Token (PAT)
    # set as the GITHUB_TOKEN environment variable to avoid rate limiting.
    scanner = GitHubIssueScanner()
    
    repo_owner = "facebook"
    repo_name = "react"
    
    open_issues = scanner.get_repository_issues(repo_owner, repo_name)
    
    if open_issues is not None:
        print(f"Repository: {repo_owner}/{repo_name}")
        print(f"Total Open Issues: {open_issues}")

    backlog_percentage = scanner.get_unresolved_issue_backlog(repo_owner, repo_name)
    if backlog_percentage is not None:
        print(f"Unresolved Backlog (Last Year): {backlog_percentage:.2f}%")

    mttr = scanner.get_mean_time_to_resolution(repo_owner, repo_name)
    if mttr is not None:
        print(f"Mean Time To Resolution (MTTR): {mttr}")
    
    print("---------------------------------------")

if __name__ == "__main__":
    main() 