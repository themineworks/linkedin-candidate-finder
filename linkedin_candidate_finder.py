#!/usr/bin/env python3
"""Recruiter sourcing. Find LinkedIn profiles matching role, skills, and location. Python, Node.js and cURL clients for the LinkedIn Candidate Finder on Apify, pay per result.

Command-line client for the themineworks/linkedin-candidate-finder actor on Apify: runs it, waits for it
to finish and saves every result as JSON and CSV. Flags map 1:1 to the actor's input.
Free Apify account and API token: https://console.apify.com/sign-up
Docs and pricing: https://themineworks.com/actors/linkedin-candidate-finder/
"""
import argparse, csv, json, os, sys
from apify_client import ApifyClient

ACTOR = "themineworks/linkedin-candidate-finder"


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--token", default=os.environ.get("APIFY_TOKEN"), help="Apify API token (or set APIFY_TOKEN)")
    ap.add_argument("--out", default="results", help="Output basename, writes .json and .csv")
    ap.add_argument("--role-title", help="The role you are recruiting for, for example 'Senior Software Engineer', 'Product…")
    ap.add_argument("--skills", help="Comma-separated. Skills the candidate must have, for example 'Python', 'AWS', 'React'")
    ap.add_argument("--location", help="City, region, or country to search in, for example 'San Francisco', 'London', 'Bengaluru'")
    ap.add_argument("--target-companies", help="Comma-separated. Optional list of companies to prioritise, for example 'Stripe', 'Notion'")
    ap.add_argument("--max-results", type=int, help="Maximum number of candidates to return across all queries")
    a = ap.parse_args()
    if not a.token:
        sys.exit("Provide --token or set APIFY_TOKEN. Free token: https://console.apify.com/sign-up")

    run_input = {}
    if a.role_title is not None: run_input["roleTitle"] = a.role_title
    if a.skills: run_input["skills"] = [s.strip() for s in a.skills.split(",") if s.strip()]
    if a.location is not None: run_input["location"] = a.location
    if a.target_companies: run_input["targetCompanies"] = [s.strip() for s in a.target_companies.split(",") if s.strip()]
    if a.max_results is not None: run_input["maxResults"] = a.max_results

    client = ApifyClient(a.token)
    print(f"Running {ACTOR} ...")
    run = client.actor(ACTOR).call(run_input=run_input)
    items = list(client.dataset(run["defaultDatasetId"]).iterate_items())

    with open(a.out + ".json", "w", encoding="utf-8") as f:
        json.dump(items, f, indent=2, ensure_ascii=False)
    keys = []
    for it in items:
        keys += [k for k in it if k not in keys]
    if items:
        with open(a.out + ".csv", "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=keys, extrasaction="ignore")
            w.writeheader()
            for it in items:
                w.writerow({k: json.dumps(v, ensure_ascii=False) if isinstance(v, (list, dict)) else v for k, v in it.items()})
    print(f"Done: {len(items)} results saved to {a.out}.json and {a.out}.csv")


if __name__ == "__main__":
    main()
