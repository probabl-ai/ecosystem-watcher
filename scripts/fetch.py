from pathlib import Path
import srsly 
import requests as rq 

def fetch_github_search_info(repo):
    RELEVANT_KEYS = ["full_name", "description", "forks", "open_issues", "stargazers_count", "created_at", "updated_at"]
    url = f"https://api.github.com/search/repositories?q={repo}"
    blob = rq.get(url).json()
    if not blob.get("items", None):
        print(blob)
    for item in blob["items"]:
        if item["full_name"] == repo:
            n_contributors = len(rq.get(item['contributors_url']).json())
            result = {**item, "n_contributors": n_contributors}
            return {key: result[key] for key in RELEVANT_KEYS}

g = srsly.read_jsonl("repos.jsonl")
out_path = Path(__file__).parent.parent / "site" / "data.jsonl"
srsly.write_jsonl(out_path, (fetch_github_search_info(ex['repo']) for ex in g))
