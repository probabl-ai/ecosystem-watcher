from tqdm import tqdm 
from pathlib import Path
import srsly 
import requests as rq 
from tenacity import retry
from dotenv import load_dotenv
import os

load_dotenv()


@retry
def fetch_pepy_info(project):
    url = f"https://api.pepy.tech/api/v2/projects/{project}"
    headers = {"X-Api-Key": f"{os.environ.get('PEPY_TOKEN')}"}
    blob = rq.get(url, headers=headers).json()
    last_30_days = list(blob['downloads'].keys())[-30:]
    downloads_total = blob['total_downloads']
    downloads_30d = sum([sum(blob['downloads'][date].values()) for date in last_30_days])
    return {"total_downloads": downloads_total, "month_downloads": downloads_30d}

@retry
def fetch_info(repo, project):
    RELEVANT_KEYS = ["full_name", "description", "forks", "open_issues", "stargazers_count", "created_at", "pushed_at"]
    url = f"https://api.github.com/search/repositories?q={repo}"
    headers = {"Authorization": f"Bearer {os.environ.get('GH_TOKEN')}"}
    blob = rq.get(url, headers=headers).json()
    for item in blob["items"]:
        if item["full_name"] == repo:
            n_contributors = len(rq.get(item['contributors_url'], headers=headers).json())
            result = {key: item[key] for key in RELEVANT_KEYS}
            return {**result, "n_contributors": n_contributors, **fetch_pepy_info(project)}

g = tqdm(list(srsly.read_jsonl("repos.jsonl")))
out_path = Path(__file__).parent.parent / "docs" / "data.jsonl"
srsly.write_jsonl(out_path, (fetch_info(ex['repo'], ex['pypi']) for ex in g))
