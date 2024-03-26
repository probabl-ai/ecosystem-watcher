import srsly 
import datetime as dt 
import requests as rq
from stamina import retry

today = str(dt.datetime.now())[:10]

# Handle all Github data

@retry(on=Exception,attempts=5)
def fetch_github_stats():
    resp_releases = rq.get("https://api.github.com/repos/Wimmics/corese/releases")
    data = []
    for release in resp_releases.json():
        for asset in release['assets']:
            d = {k: asset[k] for k in ['download_count', 'name']}
            d['today'] = today
            data.append(d)

    srsly.write_jsonl(f"data/corese/github-{today}.jsonl", data)


def _arches_downloads(entry):
    return sum(entry['arches']['x86_64'])

@retry(on=Exception, attempts=5)
def fetch_flathub_stats():
    print("fetching flathub stats")
    data = []
    for name in ['CoreseCommand', 'CoreseGui']:
        resp_flathub = rq.get(f"https://klausenbusk.github.io/flathub-stats/data/fr.inria.corese.{name}.json")
        downloads = resp_flathub.json()['stats']
        data.append({
            'today': today,
            'installs_total': None,
            'installs_last_month': sum([_arches_downloads(e) for e in downloads[-30:]]),
            'installs_last_7_days': sum([_arches_downloads(e) for e in downloads[-7:]]),
            'name': name,
        })
    srsly.write_jsonl(f"data/corese/flathub-{today}.jsonl", data)


if __name__ == "__main__":
    fetch_github_stats()
    fetch_flathub_stats()
