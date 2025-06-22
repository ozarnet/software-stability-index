import json
import pandas as pd
from pathlib import Path
import sys

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

# Assuming the retrieval modules are in the ssi/retrieval directory
from ssi.retrieval.registry_stats import PyPIFetcher
from ssi.retrieval.issue_tracker_scanner import GitHubIssueScanner

# --- Normalization Functions ---

def normalize_issue_count(count, max_issues=1000):
    """Normalizes the open issue count. Lower is better."""
    if count is None:
        return 5.0 # Return a neutral score if data is unavailable
    # Score is 10 if count is 0, and decreases to 0 as it approaches max_issues
    return max(0, 10 * (1 - (min(count, max_issues) / max_issues)))

def normalize_mttr(mttr_str, max_days=90):
    """Normalizes the Mean Time to Resolution. Lower is better."""
    if mttr_str is None or mttr_str == "N/A":
        return 5.0 # Neutral score
    
    # Extract days from timedelta string representation
    try:
        # Handles strings like "184 days, 14:45:34.235294"
        days_str = mttr_str.split(' ')[0]
        days = int(days_str)
    except (ValueError, IndexError):
        return 5.0 # Return neutral score if parsing fails
        
    return max(0, 10 * (1 - (min(days, max_days) / max_days)))


# Define weights for the scoring categories
WEIGHTS = {
    "learnability": 0.30,
    "applicability": 0.25,
    "sustainability": 0.45
}

# Define stability bands based on the final score
STABILITY_BANDS = {
    (0.0, 4.0): "Hazardous",
    (4.0, 6.0): "Low",
    (6.0, 7.5): "Moderate",
    (7.5, 9.0): "Stable",
    (9.0, 10.0): "Ultra-stable"
}

def get_stability_band(score):
    """Determines the stability band for a given score."""
    for (lower, upper), band in STABILITY_BANDS.items():
        if lower <= score < upper:
            return band
    return "N/A"

def calculate_ssi(data, live_data=None):
    """Calculates the Software Stability Index (SSI) from raw scores."""
    live_data = live_data or {}
    records = []
    for item in data:
        scores = item['scores']
        tech_live_data = live_data.get(item['name'], {})

        # --- Calculate Sustainability Score with Live Data ---
        s_manual = scores.get('sustainability', 0)
        
        # Normalize live metrics
        s_issue_backlog = normalize_issue_count(tech_live_data.get('open_issues'))
        s_mttr = normalize_mttr(tech_live_data.get('mttr'))
        
        # Combine manual and live sustainability scores
        # We'll give the manual score 70% weight, and the two live metrics 15% each
        if tech_live_data: # Only apply live data if it was fetched
             s_final = (s_manual * 0.7) + (s_issue_backlog * 0.15) + (s_mttr * 0.15)
        else:
            s_final = s_manual

        fss = (
            scores.get('learnability', 0) * WEIGHTS['learnability'] +
            scores.get('applicability', 0) * WEIGHTS['applicability'] +
            s_final * WEIGHTS['sustainability']
        )
        
        record = {
            "Technology": item['name'],
            "Version": item['version_or_year'],
            "Learnability": scores.get('learnability', 0),
            "Applicability": scores.get('applicability', 0),
            "Sustainability": round(s_final, 2),
            "SSI Score": round(fss, 2),
            "Open Issues": tech_live_data.get('open_issues', 'N/A'),
            "MTTR": tech_live_data.get('mttr', 'N/A')
        }
        records.append(record)
    
    return pd.DataFrame(records)

def main():
    """Main function to load data, compute SSI, and print results."""
    # Construct path to the data file relative to this script
    script_dir = Path(__file__).parent
    data_file = script_dir.parent / 'examples' / 'sample_scores.json'

    try:
        with open(data_file, 'r') as f:
            sample_data = json.load(f)
    except FileNotFoundError:
        print(f"Error: The data file was not found at {data_file}")
        return
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {data_file}")
        return

    # --- Fetch Live Data ---
    print("Fetching live data... (this may take a moment)")
    github_scanner = GitHubIssueScanner()
    live_data_results = {}

    for item in sample_data:
        tech_name = item['name']
        
        # Fetch from GitHub if repo info is present
        if 'github_repo' in item:
            owner, repo = item['github_repo'].split('/')
            open_issues = github_scanner.get_repository_issues(owner, repo)
            mttr = github_scanner.get_mean_time_to_resolution(owner, repo)
            live_data_results[tech_name] = {
                'open_issues': open_issues,
                'mttr': str(mttr) if mttr else None
            }

    df = calculate_ssi(sample_data, live_data_results)
    df['Stability Band'] = df['SSI Score'].apply(get_stability_band)
    
    # Set display options for pandas
    pd.set_option('display.width', 1000)
    pd.set_option('display.max_columns', 10)
    
    print("\n--- Software Stability Index (SSI) ---")
    print(df.to_string(index=False))
    print("--------------------------------------")


if __name__ == "__main__":
    main()
