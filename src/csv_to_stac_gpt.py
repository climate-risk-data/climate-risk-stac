import pystac
from pystac.extensions.scientific import ScientificExtension
from pystac.extensions.projection import ProjectionExtension
import json
import os
import pandas as pd
from datetime import datetime
import numpy as np
import sys

# Directory for (reading &) writing the catalog
dir = 'C:/Users/lrn238/OneDrive - Vrije Universiteit Amsterdam/Documents/GitHub/climate-risk-stac/'

# Create the main catalog
catalog_main = pystac.Catalog(
    id="climate-risk-data",
    title="Climate Risk Data",
    description="Community catalog containing datasets for the three risk drivers Hazard, Exposure, and Vulnerability."
)

# Reformat temporal resolution to adjust to STAC requirements
def parse_year_range(year_str):
    year_str = year_str.replace('now', '2024').replace('current', '2024')
    if '-' in year_str:
        start, end = map(int, year_str.split('-'))
        return datetime(start, 1, 1), datetime(end, 12, 31)
    else:
        year = int(year_str)
        return datetime(year, 1, 1), None

# Read data sheets
hazard = pd.read_csv('csv/hazard.csv', encoding='utf-8')
expvul = pd.read_csv('csv/expvul.csv', encoding='utf-8')

# Preprocessing of data sheets: replace all blank cells with "not available"
hazard = hazard.fillna('not available')
expvul = expvul.fillna('not available')

# Initialize the dictionary to store links
links_dict = {}

# Manually include the parent folder for the main catalog
parent_folder = "stac"
links_dict[parent_folder] = {"href": f"./{parent_folder}/catalog.json"}

# Process links recursively
def process_links(catalog, links_dict, parent_folder):
    for link in catalog.links:
        if link.rel == 'child':
            target_path = link.target.replace('./', f'{parent_folder}/')
            if 'collection' in link.target:
                linked_catalog = pystac.Collection.from_file(target_path)
                links_dict[linked_catalog.id] = {"href": f"{parent_folder}/{linked_catalog.id}"}
            elif 'catalog' in link.target:
                linked_catalog = pystac.Catalog.from_file(target_path)
                links_dict[linked_catalog.id] = {"href": f"{parent_folder}/{linked_catalog.id}"}
                process_links(linked_catalog, links_dict[linked_catalog.id], os.path.join(parent_folder, os.path.split(link.target[2:])[0]))

# Process links in the main catalog
process_links(catalog_main, links_dict[parent_folder], parent_folder)

# Determine catalog/excel tab to be used and loop through both
for indicator in [hazard, expvul]:
    for row_num in range(len(indicator)):
        item = indicator.iloc[row_num]

        for column_name in indicator.columns:
            globals()[column_name] = indicator[column_name][row_num]

        try:
            collections = links_dict['stac'][catalog][category]
        except KeyError:
            href = links_dict['stac'][catalog]['href']
            parent_catalog = pystac.Catalog.from_file(f"{href}/catalog.json")

            catalog_ev1 = pystac.Catalog(
                id=category,
                title=category,
                description=category,
            )
            parent_catalog.add_child(catalog_ev1)
            links_dict['stac'][catalog][category] = {"href": f"stac/{catalog}/{category}"}
            parent_catalog.save(catalog_type=pystac.CatalogType.SELF_CONTAINED)

            collections = links_dict['stac'][catalog][category]

        href = collections['href']

        if pd.isna(title_short):
            if pd.isna(title_collection):
                print('This we should discuss: probably title is NaN')
                continue
            else:
                title_short = title_collection

        if not np.nan_to_num(item['bbox']) == 0:
            try:
                bbox_list = [float(coord.strip()) for coord in item['bbox'].split(',')]
            except ValueError:
                print(f'Check bbox: {item["bbox"]}')
                bbox_list = item['bbox']
        else:
            bbox_list = np.nan

        if not np.nan_to_num(item['temporal_resolution']) == 0:
            year_start, year_end = parse_year_range(str(item['temporal_resolution']))
        else:
            year_start, year_end = np.nan, np.nan
            print('This we should discuss: cannot create collection, because of no input for temporal_resolution')
            continue

        if title_short not in collections:
            parent_catalog = pystac.Catalog.from_file(f"{href}/catalog.json")

            collection = pystac.Collection(
                id=title_short,
                title=item['title_collection'],
                description=item['description_collection'],
                extent=pystac.Extent(
                    spatial=pystac.SpatialExtent([bbox_list]),
                    temporal=pystac.TemporalExtent([[year_end, year_start]]),
                ),
                extra_fields={
                    'data_type': item['data_type'],
                    'data_format': item['format'],
                    'spatial_scale': item['spatial_scale'],
                    'coordinate_system': item['coordinate_system'],
                },
            )
            parent_catalog.add_child(collection)
            parent_catalog.normalize_hrefs(os.path.join(dir, "stac"))
            parent_catalog.save(catalog_type=pystac.CatalogType.SELF_CONTAINED)

        collection = pystac.Collection.from_file(f"{href}/{title_short}/collection.json")

        if title_item not in [i.id for i in collection.get_items()]:
            item_stac = pystac.Item(
                id=item['title_item'],
                geometry=None,
                bbox=bbox_list,
                datetime=None,
                properties={
                    'title': item['title_item'],
                    'description': item['description_item'],
                    'data_type': item['data_type'],
                    'data_format': item['format'],
                    'spatial_scale': item['spatial_scale'],
                    'coordinate_system': item['coordinate_system'],
                    'reference_period': item['reference_period'],
                    'temporal_resolution': item['temporal_resolution'],
                    'temporal_interval': item['temporal_interval'],
                    'scenarios': item['scenarios'],
                    'data_calculation_type': item['data_calculation_type'],
                    'analysis_type': item['analysis_type'],
                    'underlying_data': item['underlying_data'],
                    'provider': item['provider'],
                    'provider_role': item['provider_role'],
                    'license': item['license'],
                    'link_website': item['link_website'],
                    'publication_link': item['publication_link'],
                    'publication_type': item['publication_type'],
                    'code_link': item['code_link'],
                    'code_type': item['code_type'],
                    'usage_notes': item['usage_notes'],
                    'assets': item['assets'],
                },
            )
            collection.add_item(item_stac)

            if not np.nan_to_num(item['publication_link']) == 0:
                sci_ext = ScientificExtension.ext(item_stac, add_if_missing=True)
                sci_ext.doi = item['publication_link']

    catalog_main.normalize_hrefs(os.path.join(dir, "stac"))
    catalog_main.save(catalog_type=pystac.CatalogType.SELF_CONTAINED)
