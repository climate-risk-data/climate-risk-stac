import pystac
from pystac.extensions.scientific import ScientificExtension
from pystac.extensions.projection import ProjectionExtension
import json
import os
import pandas as pd
from datetime import datetime
import numpy as np
import sys

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

def parse_year_range(year_str):
    year_str = year_str.replace('now', '2024').replace('current', '2024')
    if '-' in year_str:
        start, end = map(int, year_str.split('-'))
        return datetime(start, 1, 1), datetime(end, 12, 31)
    else:
        year = int(year_str)
        return datetime(year, 1, 1), None

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

indicator = hazard
# indicator = expvul

row_num = 2
for row_num in range(len(indicator)):
    print(row_num)
    item = indicator.iloc[row_num]

    for column_name in indicator.columns:
        globals()[column_name] = indicator[column_name][row_num]

    try:
        collections = links_dict['stac'][catalog][category]
    except KeyError as e:
        href = links_dict['stac'][catalog]['href']
        parent_catalog = pystac.Catalog.from_file(f"{href}/catalog.json")
        
        # exp & vul type (level2)
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
        except ValueError as e:
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
    # sys.exit(0)

    # if not item['title_short'] in collections:
    if not title_short in collections:
        # Open parent catalog
        parent_catalog = pystac.Catalog.from_file(f"{href}/catalog.json")

        collection = pystac.Collection(
            id = title_short,
            title = item['title_collection'],
            description = item['description_collection'],
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
        parent_catalog.save(catalog_type=pystac.CatalogType.SELF_CONTAINED)

    collection = pystac.Collection.from_file(f"{href}/{title_short}/collection.json")

    # if not title_item in list(collection.get_items()):
    if title_item not in [i.id for i in collection.get_items()]:
        item_stac = pystac.Item(
            id = title_item,
            geometry = None,
            bbox = bbox_list,
            datetime = None,
            start_datetime = datetime.utcnow(),
            end_datetime = datetime.utcnow(),
            properties={
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
                'name_contributor': item['name_contributor'],
            },
        )
        collection.add_item(item_stac)
        # collection.save()
    if not np.nan_to_num(item['publication_link']) == 0:
        sci_ext = ScientificExtension.ext(item_stac, add_if_missing=True)
        sci_ext.doi = item['publication_link']

    # proj_ext = ProjectionExtension.ext(item_stac, add_if_missing=True)
    # proj_ext.epsg = 4326

    # sci_ext = ScientificExtension.ext(collection)