from pathlib import Path
from climate_stac.parse_form import parse_md_to_dict
from climate_stac.data_model import HazardDataModel

if __name__ == '__main__':
    with open('csv/test_form.md', 'r') as f:
        md_content = f.read()

    parsed_form = parse_md_to_dict(md_content)
    item = HazardDataModel(**parsed_form)
    path = Path('json', item.catalog, item.category, f"{item.id}.json")
    item.to_json(path)