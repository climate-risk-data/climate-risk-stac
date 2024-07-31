#%% NOTES %%#
#

import pystac
from pystac.extensions.scientific import ScientificExtension
import pandas as pd
from datetime import datetime
import numpy as np
import os
#import json

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
        elif len(start) == 4 and len(end) == 3:
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
        
# Function to make keywords based on subcategory and risk data type
def parse_keywords(subc, rdata):
    # separate strings
    subc = subc.split(',') if ',' in subc else subc
    # use rdata if expvul
    keywords = subc if rdata == 'hazard' else [subc, rdata]
    print(f"new keywords: {keywords}")
    return keywords


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
    for row_num in range(len(indicator)):
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

            # make keywords
            keyw = parse_keywords(item['subcategory'], item['risk_data_type'])
         
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
                keywords=keyw, # add further if needed
                extra_fields={
                    'subcategory': item['subcategory'],
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
        
        print('collection ', row_num, ' ', title_collection, ' successful')

        ## ITEMS ##
        
        # datetime and bbox
        year_start, year_end = parse_year_range(str(temporal_resolution))
        bbox_list = [float(coord.strip()) for coord in bbox.split(',')]
        
        # Create basic item
        item_stac = pystac.Item(
            id=item['title_item'],
            geometry=None,  # Add geometry if available
            bbox=bbox_list,
            datetime=datetime.now(),
            #start_datetime = year_start,
            #end_datetime = year_end,
            properties={
                'title': item['title_item'],
                'description': item['description_item'],
                'risk data type': item['risk_data_type'],
                'subcategory': str(item['subcategory']),
                'spatial scale': item['spatial_scale'],
                'reference period': item['reference_period'],
                'temporal resolution': str(item['temporal_resolution']) +' ('+ str(item['temporal_interval']) + ')',
                #'temporal interval': str(item['temporal_interval']),
                'scenarios': str(item['scenarios']),
                'data type': item['data_type'],
                'data format': str(item['format']),
                'coordinate system': str(item['coordinate_system']),
                'spatial resolution': str(item['spatial_resolution']) +' '+ str(item['spatial_resolution_unit']),
                'data calculation type': item['data_calculation_type'],
                'analysis type': str(item['analysis_type']),
                'underlying data': str(item['underlying_data']),
                'publication link': str(item['publication_link']),
                'publication type': str(item['publication_type']),
                'code link': str(item['code_link']),
                'code type': str(item['code_type']),
                'usage notes': str(item['usage_notes'])
            }
            # extra_fields={ # are part of the json, but not shown in the browser
            #         'subcategory': str(item['subcategory']), #remove str() again once subcategory fixed
            #         'risk data type': item['risk_data_type']
            #     }
        )

        # add keywords --> not available for items

        # add projection extension!

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
        #item_stac.add_link(pystac.Link(rel="related", target="https://www.openai.com", title="OpenAI"))

        
        # Add item to collection
        collection.add_item(item_stac)

    	# get paths of item
        #for item_stac in catalog_main.get_all_items():
        #    print(item_stac.get_self_href())
        
        # confirmation item added
        print('item ', row_num, ' ', item['title_item'], ' successful')

    #print(json.dumps(item_stac.to_dict(), indent=4))
    catalog_main.describe()

    # Normalize hrefs and save the catalog
    catalog_main.normalize_hrefs(os.path.join(dir, "stac"))
    catalog_main.save(catalog_type=pystac.CatalogType.SELF_CONTAINED)
    #catalog_main.save(catalog_type=pystac.CatalogType.RELATIVE_PUBLISHED)
   

# Create catalogs from both hazard and exposure-vulnerability CSVs
create_catalog_from_csv(hazard, catalog_main, dir)
create_catalog_from_csv(expvul, catalog_main, dir)


# # Function to ensure directory exists
# def ensure_dir(file_path):
#     directory = os.path.dirname(file_path)
#     if not os.path.exists(directory):
#         os.makedirs(directory)

# # Ensure the directory exists
# ensure_dir(dir)


# # Ensure directories for all items
# for item in catalog_main.get_all_items():
#     item_href = item.get_self_href()
#     ensure_dir(item_href)

# # Save all items
# for item in catalog_main.get_all_items():
#     item.save_object(include_self_link=False)