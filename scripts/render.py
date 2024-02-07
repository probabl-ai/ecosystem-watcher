import datetime as dt 
import srsly
from jinja2 import Template
import humanize
from pathlib import Path 


if __name__ == "__main__":
    template_path = Path(__file__).parent.parent / "docs" / "template.html"
    template = Template(template_path.read_text())
    data_path = Path(__file__).parent.parent / "docs" / "data.jsonl"

    items = list(srsly.read_jsonl(data_path))
    items = sorted(items, key=lambda d: -d['month_downloads'])
    
    # Loop over items, printing so hindsight debugging is easier
    for item in items:
        print(f"Generating stats for {item['full_name']=}")
        item['age'] = humanize.naturaldelta(dt.datetime.now() - dt.datetime.fromisoformat(item['created_at'][:10]))
        item['age_days'] = (dt.datetime.now() - dt.datetime.fromisoformat(item['created_at'][:10])).days
        item['since_update'] = humanize.naturaldelta(dt.datetime.now() - dt.datetime.fromisoformat(item['pushed_at'][:10]))
        item['since_update_days'] = (dt.datetime.now() - dt.datetime.fromisoformat(item['pushed_at'][:10])).days
        item["total_downloads"] = humanize.intcomma(item["total_downloads"])
        item["month_downloads"] = humanize.intcomma(item["month_downloads"])


    out_path = template_path.parent / "index.html" 
    out_path.write_text(template.render(items=items))
