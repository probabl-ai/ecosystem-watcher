import srsly
from jinja2 import Template
from pathlib import Path 

template_path = Path(__file__).parent.parent / "site" / "template.html"
template = Template(template_path.read_text())
data_path = Path(__file__).parent.parent / "site" / "data.jsonl"
items = srsly.read_jsonl(data_path)
print(template.render(items=items))
