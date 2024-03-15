import srsly 
import datetime as dt 
import requests as rq
from tenacity import retry

today = str(dt.datetime.now())[:10]

# Handle all Github data

@retry
def fetch_github_stats():
    resp_releases = rq.get("https://api.github.com/repos/Wimmics/corese/releases")
    data = []
    for release in resp_releases.json():
        for asset in release['assets']:
            d = {k: asset[k] for k in ['download_count', 'name']}
            d['today'] = today
            data.append(d)

    srsly.write_jsonl(f"data/corese/github-{today}.jsonl", data)


@retry
def fetch_flathub_stats():
    data = []
    for name in ['CoreseCommand', 'CoreseGui']:
        resp_flathub = rq.get(f"https://flathub.org/_next/data/60a2786bb9d4c2b2b30a218033e961157168c0a4/en/apps/fr.inria.corese.{name}.json?appDetails=fr.inria.corese.CoreseGui")
        downloads = resp_flathub.json()['pageProps']['stats']
        data.append({
            'today': today,
            'installs_total': downloads['installs_total'],
            'installs_last_month': downloads['installs_last_month'],
            'installs_last_7_days': downloads['installs_last_7_days'],
            'name': name,
        })
    srsly.write_jsonl(f"data/corese/flathub-{today}.jsonl", data)


if __name__ == "__main__":
    fetch_github_stats()
    fetch_github_stats()
