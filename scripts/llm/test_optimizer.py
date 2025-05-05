"""
Test script for the Free Resume Optimizer.

This script allows you to test the Resume Optimizer with different resumes
and job types to see the optimization suggestions, using free/open-source models.
"""

import argparse
import os
import json
import time
from pathlib import Path
from scripts import ResumeOptimizer


def main():
    """Main function to test the resume optimizer."""
    parser = argparse.ArgumentParser(description="Test the Resume Optimizer")

    parser.add_argument("--resume", "-r", type=str, required=True,
                        help="Path to the resume file (txt format)")

    parser.add_argument("--job-type", "-j", type=str, default=None,
                        help="Job type to target (e.g., 'software intern')")

    parser.add_argument("--job-data", "-d", type=str,
                        default="data/job_data/software_intern_data.json",
                        help="Path to the job data JSON file")

    parser.add_argument("--output", "-o", type=str, default=None,
                        help="Path to save the optimization results (JSON format)")

    parser.add_argument("--huggingface-token", "-t", type=str, default=None,
                        help="HuggingFace API token (optional)")

    # ADD THESE NEW ARGUMENTS HERE
    parser.add_argument("--generate-optimized-resume", "-g", action="store_true",
                        help="Generate an optimized version of the resume text")

    parser.add_argument("--optimized-output", "-oo", type=str, default=None,
                        help="Path to save the optimized resume text")
    # END OF NEW ARGUMENTS

    args = parser.parse_args()

    # Check if resume file exists
    if not os.path.exists(args.resume):
        print(f"Error: Resume file not found: {args.resume}")
        return

    # Check if job data file exists
    if not os.path.exists(args.job_data):
        print(f"Error: Job data file not found: {args.job_data}")
        return

    # Read resume content
    with open(args.resume, 'r', encoding='utf-8') as f:
        resume_text = f.read()

    # Initialize the optimizer
    try:
        print(f"Initializing Resume Optimizer with job data: {args.job_data}")
        optimizer = ResumeOptimizer(
            job_data_path=args.job_data,
            huggingface_token=args.huggingface_token
        )
        print("Optimizer initialized successfully")
    except Exception as e:
        print(f"Error initializing the optimizer: {e}")
        return

    # Run the optimization
    print(f"\nOptimizing resume for job type: {args.job_type or 'any'}")
    print("This may take a minute...\n")

    start_time = time.time()

    try:
        results = optimizer.optimize_resume(resume_text, job_type=args.job_type)

        if "error" in results:
            print(f"Error: {results['error']}")
            return
    except Exception as e:
        print(f"Error during optimization: {e}")
        return

    end_time = time.time()
    duration = end_time - start_time

    print(f"Optimization completed in {duration:.2f} seconds\n")

    # Save results to file if specified
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2)

        print(f"Results saved to {args.output}")

    # Print results
    print("="*80)
    print("RESUME OPTIMIZATION RESULTS")
    print("="*80 + "\n")

    print("RELEVANT JOBS:")
    for i, job in enumerate(results["relevant_jobs"]):
        print(f"{i+1}. {job['title']} at {job['company']} ({job['location']})")

    print("\nKEYWORD ANALYSIS:")

    print("\nPresent Keywords:")
    present_keywords = results["keyword_analysis"]["present_keywords"]
    for i in range(0, len(present_keywords), 5):
        print(", ".join(present_keywords[i:i+5]))

    print("\nMissing Keywords:")
    missing_keywords = results["keyword_analysis"]["missing_keywords"]
    for i in range(0, len(missing_keywords), 5):
        print(", ".join(missing_keywords[i:i+5]))

    print("\nOPTIMIZATION SUGGESTIONS:")
    print(results["optimization_suggestions"])

    # ADD THIS NEW SECTION HERE
    # Generate optimized resume text if requested
    if args.generate_optimized_resume:
        print("\nGenerating optimized resume text...")
        optimized_resume = optimizer.generate_optimized_resume(resume_text, job_type=args.job_type)

        # Save optimized resume to file
        if args.optimized_output:
            output_path = Path(args.optimized_output)
            output_path.parent.mkdir(parents=True, exist_ok=True)

            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(optimized_resume)

            print(f"Optimized resume saved to {args.optimized_output}")
        else:
            print("\n" + "="*80)
            print("OPTIMIZED RESUME")
            print("="*80 + "\n")
            print(optimized_resume)
    # END OF NEW SECTION


if __name__ == "__main__":
    main()