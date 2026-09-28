# LinkedIn Candidate Finder: Recruiter Sourcing

Find LinkedIn profiles matching recruiter requirements: role, skills, location, experience, and target companies. Returns name, headline, current title and company, profile URL, matched skills, and a match-confidence score per candidate. Built for sourcing, not generic profile scraping.

**Run it on Apify:** [apify.com/themineworks/linkedin-candidate-finder](https://apify.com/themineworks/linkedin-candidate-finder)
**Docs, FAQ and pricing:** [themineworks.com/actors/linkedin-candidate-finder](https://themineworks.com/actors/linkedin-candidate-finder/)

**Price:** From $1.80 per 1,000 candidates on Apify's higher plans ($3.00 on the free plan), plus a $0.005 start fee per run. Failed and empty results are never charged.

## What it returns

* Search by role, required skills, location, and experience band
* Optional target-company filtering
* Name, headline, current title/company, and profile URL
* Matched-skills list and a match-confidence score per candidate
* Searches with no match add no result charges

## Quick start

You need a free [Apify account](https://console.apify.com/sign-up) and its API token (Settings, API & Integrations).

### Python

```bash
pip install apify-client
```

```python
from apify_client import ApifyClient

client = ApifyClient("YOUR_APIFY_TOKEN")
run = client.actor("themineworks/linkedin-candidate-finder").call(run_input={
    "roleTitle": "Senior Software Engineer",
    "skills": [
        "Python",
        "AWS"
    ],
    "location": "San Francisco",
    "targetCompanies": []
})

for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    print(item)
```

### Node.js

```bash
npm install apify-client
```

```javascript
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: 'YOUR_APIFY_TOKEN' });
const run = await client.actor('themineworks/linkedin-candidate-finder').call({
    "roleTitle": "Senior Software Engineer",
    "skills": [
        "Python",
        "AWS"
    ],
    "location": "San Francisco",
    "targetCompanies": []
});
const { items } = await client.dataset(run.defaultDatasetId).listItems();
console.log(items);
```

### cURL

One request that runs the actor and returns the results in the response (for runs under 5 minutes):

```bash
curl -X POST "https://api.apify.com/v2/acts/themineworks~linkedin-candidate-finder/run-sync-get-dataset-items?token=YOUR_APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"roleTitle": "Senior Software Engineer", "skills": ["Python", "AWS"], "location": "San Francisco", "targetCompanies": []}'
```

### Command line

This repo includes ready-made clients that save results to JSON and CSV:

```bash
python3 linkedin_candidate_finder.py --token YOUR_APIFY_TOKEN --role-title "Senior Software Engineer" --skills "Python,AWS" --location "San Francisco" --target-companies ""
node linkedin_candidate_finder.mjs --token YOUR_APIFY_TOKEN --role-title "Senior Software Engineer" --skills "Python,AWS" --location "San Francisco" --target-companies ""
```

## Input

| Field | Type | Default | Description |
|---|---|---|---|
| `roleTitle` (required) | string |  | The role you are recruiting for, for example 'Senior Software Engineer', 'Product Manager', 'Data Scientist' |
| `skills` | array |  | Skills the candidate must have, for example 'Python', 'AWS', 'React' |
| `location` | string |  | City, region, or country to search in, for example 'San Francisco', 'London', 'Bengaluru' |
| `targetCompanies` | array |  | Optional list of companies to prioritise, for example 'Stripe', 'Notion' |
| `maxResults` | integer | `30` | Maximum number of candidates to return across all queries |

## Output

One row per result, as JSON, CSV, Excel or through the API.

| Field | Type | Description |
|---|---|---|
| `name` | string | Full name of the candidate |
| `headline` | string | LinkedIn headline as indexed by Google |
| `current_title` | string | Current job title, best-effort parsed from the headline |
| `current_company` | string | Current company, best-effort parsed from the headline |
| `location` | string | Candidate location, reported only when confirmed in the profile's indexed text |
| `profile_url` | string | Public LinkedIn profile URL |
| `matched_skills` | array | Which of the requested skills were found on the candidate's profile |
| `match_confidence` | string | A short note on match strength: high, medium, or low, with the reasoning (role/skills/location matched or not) |
| `scraped_at` | string | ISO timestamp when this record was captured |

## Use it from an AI agent

The actor works as a tool in Claude, Cursor or any MCP client through Apify's MCP server:

```
https://mcp.apify.com/?tools=themineworks/linkedin-candidate-finder
```

## FAQ

### What makes this different from a general LinkedIn profile scraper?

This actor is built for sourcing: you describe the role and requirements, and it returns ranked candidates with a match-confidence score, not a raw profile dump.

### What is the price?

Pay per result: from $1.80 per 1,000 candidates on Apify's higher plans, $3.00 on the free plan, plus a $0.005 start fee per run. Failed results are never charged.

### Can I export the results to CSV or Excel?

Yes. Every run saves to an Apify dataset you can download as JSON, CSV, Excel or XML, or read through the API. The Python and Node clients in this repo also write the results to local files.

### Can I run it on a schedule?

Yes. Save your input as a task on Apify and attach a schedule, or call the API from your own cron job. Scheduled runs are billed the same way as manual ones.

## Related scrapers

* [Foundit Jobs Scraper](https://themineworks.com/actors/foundit-jobs-scraper/): Foundit.in (Monster India): 20 fields, monitor mode
* [Hirist Jobs Scraper](https://themineworks.com/actors/hirist-jobs-scraper/): India IT jobs across 147 locations, 19 fields
* [Naukri Jobs Scraper](https://themineworks.com/actors/naukri-jobs/): India's largest job board structured as clean JSON

Part of [The Mine Works](https://themineworks.com/): 151 pay-per-result scrapers with no login and no browser setup on your side.

## License

MIT © The Mine Works
