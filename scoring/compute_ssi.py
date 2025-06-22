import json
import pandas as pd
from pathlib import Path

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

def calculate_ssi(data):
    """Calculates the Software Stability Index (SSI) from raw scores."""
    records = []
    for item in data:
        scores = item['scores']
        fss = (
            scores.get('learnability', 0) * WEIGHTS['learnability'] +
            scores.get('applicability', 0) * WEIGHTS['applicability'] +
            scores.get('sustainability', 0) * WEIGHTS['sustainability']
        )
        
        record = {
            "Technology": item['name'],
            "Version": item['version_or_year'],
            "Learnability": scores.get('learnability', 0),
            "Applicability": scores.get('applicability', 0),
            "Sustainability": scores.get('sustainability', 0),
            "SSI Score": round(fss, 2)
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

    df = calculate_ssi(sample_data)
    df['Stability Band'] = df['SSI Score'].apply(get_stability_band)
    
    # Set display options for pandas
    pd.set_option('display.width', 1000)
    pd.set_option('display.max_columns', 10)
    
    print("--- Software Stability Index (SSI) ---")
    print(df.to_string(index=False))
    print("--------------------------------------")


if __name__ == "__main__":
    main()
