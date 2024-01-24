import pystac
import json
import os
import pandas as pd
from datetime import datetime

catalog_main = pystac.Catalog.from_file("stac/catalog.json")

def process_links(catalog, links_dict, parent_folder):
    for link in catalog.links:
        if link.rel == 'child':
            print(link.target.replace('./', f'{parent_folder}/'))
            if 'collection' in link.target:
                linked_catalog = pystac.Collection.from_file(link.target.replace('./', f'{parent_folder}/'))
                links_dict[linked_catalog.id] = {"href": f"{parent_folder}/{linked_catalog.id}"}
            elif 'catalog' in link.target:
                linked_catalog = pystac.Catalog.from_file(link.target.replace('./', f'{parent_folder}/'))
                # Include the parent folder in the href for sub-catalogs
                links_dict[linked_catalog.id] = {"href": f"{parent_folder}/{linked_catalog.id}"}
                process_links(linked_catalog, links_dict[linked_catalog.id], os.path.join( parent_folder, os.path.split(link.target[2:])[0]))


# Initialize the dictionary to store links
links_dict = {}

# Manually include the parent folder for the main catalog
parent_folder = "stac"
links_dict[parent_folder] = {"href": f"./{parent_folder}/catalog.json"}

# Process links recursively
process_links(catalog_main, links_dict[parent_folder], parent_folder)

# Print the resulting dictionary
print(links_dict)

# Read the data sheet
hazard = pd.read_excel('csv/xls.xlsx', 'hazard')
expvul = pd.read_excel('csv/xls.xlsx', 'exposure-vulnerability')

# Get item metadata
item = hazard.iloc[0]
for column_name in hazard.columns:
    globals()[column_name] = hazard[column_name][0]

links_dict['stac'][catalog][category]['fluvial-flood'].keys()

collections = links_dict['stac'][catalog][category]['fluvial-flood']
href = collections['href']

# if not item['title_short'] in collections:
if not 'JRC' in collections:
    # Open parent catalog
    parent_catalog = pystac.Catalog.from_file(f"{href}/catalog.json")

    bbox_list = [float(coord.strip()) for coord in item['bbox'].split(',')]

    collection = pystac.Collection(
        # id = item['title_short'],
        id = 'JRC',
        title = item['title_collection'],
        description = item['description_collection'],
        extent=pystac.Extent(
            spatial=pystac.SpatialExtent([bbox_list]),
            # temporal=pystac.TemporalExtent([item['temporal_resolution']]),
            temporal=pystac.TemporalExtent([[datetime.utcnow(), None]]),
        ),
        extra_fields={
            'data_type': item['data_type'],
            'data_format': item['format'],
            'spatial_scale': item['spatial_scale'],
            'crs_name': item['crs_name'],
            'crs_code': int(item['crs_code']),
        },
    )
    parent_catalog.add_child(collection)
    parent_catalog.save(catalog_type=pystac.CatalogType.SELF_CONTAINED)



