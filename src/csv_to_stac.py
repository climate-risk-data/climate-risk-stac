#############################################################################
# suggestions made by Lena as comments starting with '#%%' -----------------#
# see create-stac.py for script I have run to add example items to catalogs #
#############################################################################

import pystac
from pystac.extensions.scientific import ScientificExtension
from pystac.extensions.projection import ProjectionExtension
import json
import os
import pandas as pd
from datetime import datetime
import numpy as np
import sys

#%% directory for (reading &) writing the catalog (change accordingly)
dir = 'C:/Users/lrn238/OneDrive - Vrije Universiteit Amsterdam/Documents/GitHub/climate-risk-stac/'

#%% create first catalog manually
#catalog_main = pystac.Catalog.from_file("stac/catalog.json")
catalog_main = pystac.Catalog(
    id="climate-risk-data", 
    title="Climate Risk Data",
    description="Community catalog containing datasets for the three risk drivers Hazard, Expousre, and Vulnerability.",
    # stac_extensions=stac_extensions,
)

#%% not needed anymore when building catalog directly from csvs?
# establish folder structure (better to build the catalog directly from the xls --> next step)
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

# reformat temporal resolution to adjust to stac requirements
def parse_year_range(year_str):
    year_str = year_str.replace('now', '2024').replace('current', '2024')
    if '-' in year_str:
        start, end = map(int, year_str.split('-'))
        return datetime(start, 1, 1), datetime(end, 12, 31)
    else:
        year = int(year_str)
        return datetime(year, 1, 1), None


#%% read data sheets (needs to be changed)
hazard = pd.read_csv('csv/hazard.csv', encoding='utf-8')
expvul = pd.read_csv('csv/expvul.csv', encoding='utf-8')
# sys.exit(0)

#%% # preprocessing of data sheets, two options (option a. much easier?): 
# a. replace all blank cells with "not available" (my favorite)
# b. in loop adding items: make condition for properties to leave out certain properties if na
hazard = hazard.fillna('not available')
expvul = expvul.fillna('not available')


#%% create catalog folder structure %%# --> make a function that does this based on the (sub)categories in the csvs?
# first level catalogs based on column 'catalog': ids "hazard"; "exposure-vulnerability"
# second level based on column 'category': 
## hazard ids "flooding"; "extreme-precipitation"; "extreme-heat"; "windstorm"; "wildfire"; "multi-hazard"
## expvul ids "population"; "buildings"; "infrastructure"; "environment"
# idea: 
## make condition in loop: if catalog already created, add collection+item; else create catalog
# (see create-stac.py for the folders/catalogs as implemented manually now)


#%% commented out because not needed any more? -->>> We need it because that is now how the code also works to create a digital copy of the stac folder structure
# Initialize the dictionary to store links
links_dict = {}

# Manually include the parent folder for the main catalog
parent_folder = "stac"
links_dict[parent_folder] = {"href": f"./{parent_folder}/catalog.json"}

# Process links recursively
process_links(catalog_main, links_dict[parent_folder], parent_folder)

# Print the resulting dictionary
print(links_dict)


# determine catalog/excel tab to be used #%% loop through both?
for indicator in [hazard, expvul]:
    # go over the table rows #%% add catalogs in this process: check whether catalog already created, otherwise create
    row_num = 2
    for row_num in range(len(indicator)):
        print(row_num)
        # Get item metadata
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

        # if not item['title_short'] in collections #%% not sure whether this is needed, but:
        #%% always create a collection, even if only one item in it 
        if not title_short in collections:
            # Open parent catalog 
            parent_catalog = pystac.Catalog.from_file(f"{href}/catalog.json") #% not sure whether this is actually needed, but rather determine catalog that this collection should go into (this can be done when building the entire catalog)

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

            parent_catalog.normalize_hrefs(os.path.join(dir, "stac")) #%% not 100% sure if needed
            parent_catalog.save(catalog_type=pystac.CatalogType.SELF_CONTAINED) #%% only save at the end?

        collection = pystac.Collection.from_file(f"{href}/{title_short}/collection.json")

        # if not title_item in list(collection.get_items()):
        if title_item not in [i.id for i in collection.get_items()]:
            item_stac = pystac.Item(
                id = title_item,
                geometry = None,
                bbox = bbox_list,
                datetime = None, #%% should be replaced by temporal_resolution
                #start_datetime = datetime.utcnow(), #%% not needed
                #end_datetime = datetime.utcnow(), #%% not needed
                properties={
                    'title': item['title_item'], #%% added
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

        # %%

    #%% write catalog --> entire catalog with all subcatalogs, collections, and items
    catalog_main.normalize_hrefs(os.path.join(dir, "stac"))
    catalog_main.save(catalog_type=pystac.CatalogType.SELF_CONTAINED)
