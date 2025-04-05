"""
Simple script to prepare job data for the Resume Optimizer.

This script formats the scraped LinkedIn job data into a structure
that can be used by the resume optimizer.
"""

import json
import os
import argparse
from pathlib import Path


def prepare_job_data(input_file, output_file):
    """
    Prepare the job data for the Resume Optimizer.

    Args:
        input_file: Path to the raw job data file
        output_file: Path to save the processed job data
    """
    print(f"Processing job data from {input_file}")

    # Create output directory if it doesn't exist
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        # Read input data
        with open(input_file, 'r', encoding='utf-8') as f:
            raw_data = json.load(f)

        # Process the data - keeping the original format
        processed_data = {}

        for key, job in raw_data.items():
            if isinstance(job, dict):
                processed_data[key] = job

        # Write processed data
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(processed_data, f, indent=2)

        print(f"Processed {len(processed_data)} job postings")
        print(f"Saved to {output_file}")

    except Exception as e:
        print(f"Error processing job data: {e}")


def main():
    """Main function to run the script."""
    parser = argparse.ArgumentParser(description="Prepare job data for Resume Optimizer")

    parser.add_argument("--input", "-i", type=str, required=True,
                        help="Path to the raw job data JSON file")

    parser.add_argument("--output", "-o", type=str, required=True,
                        help="Path to save the processed job data")

    args = parser.parse_args()

    prepare_job_data(args.input, args.output)


if __name__ == "__main__":
    main()