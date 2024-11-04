import logging
import datetime as dt 
from tqdm import tqdm 
from pathlib import Path
import srsly 
import requests as rq 
from tenacity import retry
from dotenv import load_dotenv
import os
import sys
import datetime as dt

load_dotenv()
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
logger = logging.getLogger(__name__)


@retry(logging.DEBUG)
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
    print(f"Fetching for {repo=} {project=} {dt.datetime.now()}")
    RELEVANT_KEYS = ["full_name", "description", "forks", "open_issues", "stargazers_count", "created_at", "pushed_at"]
    url = f"https://api.github.com/search/repositories?q={repo}"
    headers = {"Authorization": f"Bearer {os.environ.get('GH_TOKEN')}"}
    blob = rq.get(url, headers=headers).json()
    for item in blob["items"]:
        if item["full_name"] == repo:
            n_contributors = len(rq.get(item['contributors_url'], headers=headers).json())
            result = {key: item[key] for key in RELEVANT_KEYS}
            return {**result, "repo": repo, "pip": project, "n_contributors": n_contributors, **fetch_pepy_info(project)}


if __name__ == "__main__":
    # Progress bar will also show print statements to help us debug in hindsight
    today = str(dt.datetime.now())[:10]
    g = tqdm(list(srsly.read_jsonl("repos.jsonl")))
    site_out_path = Path(__file__).parent.parent / "docs" / "data.jsonl"
    data_out_path = Path(__file__).parent.parent / "data" / f"{today}.jsonl"

    # We want the most recent data on the site, but also a historical stamp
    fetched_info = [fetch_info(ex['repo'], ex['pypi']) for ex in g]
    srsly.write_jsonl(site_out_path, fetched_info)
    srsly.write_jsonl(data_out_path, fetched_info)
