#%% NOTES %%#
#

import pystac
from pystac.extensions.scientific import ScientificExtension
import pandas as pd
from datetime import datetime
import numpy as np
import os

# Directory for (reading &) writing the catalog
dir = 'C:/Users/lrn238/OneDrive - Vrije Universiteit Amsterdam/Documents/GitHub/climate-risk-stac/'

# Function to parse year range
def parse_year_range(year_str):
     # If the string contains a dash, it's a range
    if '-' in year_str:
        start, end = year_str.split('-')
        
        # Determine the length of the start and end strings to parse correctly
        if len(start) == 4 and len(end) == 4:
            start_year, end_year = int(start), int(end)
            return datetime(start_year, 1, 1), datetime(end_year, 12, 31)
        elif len(start) == 4 and len(end) == 0:
            start_year = int(start)
            end_year = datetime.now().year
            end_month = datetime.now().month
            end_day = datetime.now().day
            return datetime(start_year, 1, 1), datetime(end_year, end_month, end_day)
        # if start date BC (can handle any year until 10000 BC, but not year 0):
        elif len(start) > 4 and len(end) == 4:
            start_year = int(start.replace('BC', '')) - 1 # 1 BC is year 0; 2 BC is year 1 etc.
            end_year = int(end)
            return datetime(start_year, 1, 1), datetime(end_year, 12, 31)
        else:
            raise ValueError("Invalid year range format")
    
    # If there's no dash, it's a single year
    else:
        if len(year_str) == 4:
            year = int(year_str)
            return datetime(year, 1, 1), datetime(year, 12, 31)
        else:
            raise ValueError("Invalid year format")
        

# Read data sheets
hazard = pd.read_csv('csv/hazard.csv', encoding='utf-8')
expvul = pd.read_csv('csv/expvul.csv', encoding='utf-8')

# Preprocessing of data sheets: replace all blank cells with "not available" --> do this only for the 'property' columns!
#hazard = hazard.fillna('not available')
#expvul = expvul.fillna('not available')

# Create the main catalog
catalog_main = pystac.Catalog(
    id="climate-risk-data",
    title="Climate Risk Data",
    description="Community catalog containing datasets for the three risk drivers Hazard, Exposure, and Vulnerability."
)

# Function to create collections and items
def create_catalog_from_csv(indicator, catalog_main, dir):
    for row_num in range(len(indicator)-1):
        item = indicator.iloc[row_num]
        
        # Extract values from the row
        catalog_id = item['catalog']
        category_id = item['category']
        
        # bbox and temp resolution
        bbox = item['bbox']
        temporal_resolution = item['temporal_resolution']
        
        ## CATALOGS ##
        # Create or retrieve the first-level catalog
        if catalog_id not in [cat.id for cat in catalog_main.get_children()]:
            catalog1 = pystac.Catalog(id=catalog_id, 
                                      title=catalog_id.capitalize(), 
                                      description=catalog_id) #adjust here once it works
            catalog_main.add_child(catalog1)
        else:
            catalog1 = catalog_main.get_child(catalog_id)

        # Create or retrieve the second-level catalog
        if category_id not in [cat.id for cat in catalog1.get_children()]:
            catalog2 = pystac.Catalog(id=category_id, 
                                      title=category_id.capitalize(), 
                                      description=category_id) #adjust here once it works
            catalog1.add_child(catalog2)
        else:
            catalog2 = catalog1.get_child(category_id)   
        
        ## COLLECTIONS ##
        # Use item titles if necessary
        title_collection = (item['title_short'] if not pd.isna(item['title_short'])
                    else (item['title_collection'] if not pd.isna(item['title_collection'])
                          else item['title_item']))
        # collection description
        #description_collection = item['description_collection'] if not pd.isna(item['description_collection']) else ''                                                                               

        # Create or retrieve the collection 
        if title_collection not in [col.id for col in catalog2.get_children()]:
            # Process bbox
            if not np.nan_to_num(bbox) == 0:
                try:
                    bbox_list = [float(coord.strip()) for coord in bbox.split(',')]
                except ValueError:
                    print(f'Check bbox: {bbox}')
                    bbox_list = bbox
            else:
                bbox_list = np.nan

            # Process temporal resolution ## this needs to be changed to account for the total range of all items ##
            if not np.nan_to_num(temporal_resolution) == 0:
                year_start, year_end = parse_year_range(str(temporal_resolution))
            else:
                year_start, year_end = np.nan, np.nan
                print('Cannot create collection, because of no input for temporal_resolution')
                continue

            #keywords = item['keywords'].split(',') if 'keywords' in item else [] ## check for proper formatting of keywords
            
            # create basic collection
            collection = pystac.Collection(
                id=title_collection,
                title=title_collection,
                description= str(item['description_collection']),#description_collection,
                extent=pystac.Extent(
                    spatial=pystac.SpatialExtent([bbox_list]), # needs to be updated based on all items in the collection
                    temporal=pystac.TemporalExtent([[year_start, year_end]]), # needs to be updated based on all items in the collection
                ),
                license=item['license'],
                keywords=['Subcategory:' + '' + str(item['subcategory']), item['risk_data_type']], #remove str() again once subcategory fixed; change to only use risk data type for E+V
                extra_fields={
                    'subcategory': str(item['subcategory']), #remove str() again once subcategory fixed
                    'risk data type': item['risk_data_type']
                }
            )

            # Create and add a Provider
            provider = pystac.Provider(
                 name=item['provider'],
                 roles=item['provider_role'],
                 url=item['link_website']
                )
            collection.providers = [provider]
            
            catalog2.add_child(collection)

        else:
            collection = catalog2.get_child(title_collection)
        

        ## ITEMS ##
        
        # #datetime
        #year_start, year_end = parse_year_range(str(temporal_resolution))
        #datetime_value = year_start if year_start else datetime.now()
        
        #Create the item
        # item_stac = pystac.Item(
        #     id=item['title_item'],
        #     geometry=None,  # Add geometry if available
        #     bbox=bbox_list,
        #     datetime=datetime.now(),
        #     #start_datetime = year_start,
        #     #end_datetime = year_end,
        #     properties={
        #         'title': item['title_item'],
        #         'description': item['description_item'],
        #         'data_type': item['data_type'],
        #         'data_format': str(item['format']),
        #         'spatial_scale': item['spatial_scale'],
        #         'coordinate_system': str(item['coordinate_system']),
        #         'reference_period': item['reference_period'],
        #         #'temporal_resolution': item['temporal_resolution'], #change here
        #         'temporal_interval': str(item['temporal_interval']),
        #         'scenarios': str(item['scenarios']),
        #         'data_calculation_type': item['data_calculation_type'],
        #         'analysis_type': str(item['analysis_type']),
        #         'underlying_data': str(item['underlying_data']),
        #         'provider': item['provider'],
        #         'provider_role': item['provider_role'],
        #         'license': item['license'],
        #         'link_website': item['link_website'],
        #         'publication_link': str(item['publication_link']),
        #         'publication_type': str(item['publication_type']),
        #         'code_link': str(item['code_link']),
        #         'code_type': str(item['code_type']),
        #         'usage_notes': str(item['usage_notes']),
        #     },
        # )
        
        # # Add scientific extension if DOI is present
        # # if item['publication_link'].startswith('10.'):
        # #     sci_ext = ScientificExtension.ext(item_stac, add_if_missing=True)
        # #     sci_ext.doi = item['publication_link'] # adjust condition here for link that are not dois
        # # else:
        # #     return "The string does not start with '10'."

        # # if not pd.isna(item['publication_link']):
        # #     sci_ext = ScientificExtension.ext(item_stac, add_if_missing=True)
        # #     sci_ext.doi = item['publication_link'] # adjust condition here for link that are not dois

        # code to add a web link (for the publication as well as the website link)
        #item.add_link(pystac.Link(rel="related", target="https://www.openai.com", title="OpenAI"))

        
        # # Add item to collection
        # collection.add_item(item_stac)

    # Normalize hrefs and save the catalog
    catalog_main.normalize_hrefs(os.path.join(dir, "stac"))
    catalog_main.save(catalog_type=pystac.CatalogType.SELF_CONTAINED)

# Create catalogs from both hazard and exposure-vulnerability CSVs
create_catalog_from_csv(hazard, catalog_main, dir)
create_catalog_from_csv(expvul, catalog_main, dir)
