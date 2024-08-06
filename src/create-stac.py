#%% NOTES %%#
#

import pystac
#from pystac import RelType
from pystac.extensions.scientific import ScientificExtension
from pystac.extensions.projection import ProjectionExtension
import pandas as pd
from datetime import datetime
import numpy as np
import os
#import json

# File paths
dir = 'C:/Users/lrn238/OneDrive - Vrije Universiteit Amsterdam/Documents/GitHub/climate-risk-stac/'
haz = 'csv/hazard_test.csv' # use test set which also includes expvul
exv = 'csv/expvul.csv' # can both be combined into one csv, but: some attributes are slightly different

# Read data sheets
hazard = pd.read_csv(haz, encoding='utf-8')
expvul = pd.read_csv(exv, encoding='utf-8')

# Mapping formats to media types (for assets)
format_to_media_type = {
    "geotiff": pystac.MediaType.GEOTIFF,
    "FlatGeobuf": pystac.MediaType.FLATGEOBUF,
    "netcdf": "application/x-netcdf",
    "geopackage": pystac.MediaType.GEOPACKAGE,
    "shapefile": "application/x-shapefile",
    "geodatabase": "application/x-filegdb",
    "csv": "text/csv",
    "excel": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "GeoParquet": pystac.MediaType.PARQUET,
    "GRIB": "application/grib",
    "GRIB2": "application/grib2",
    "txt": pystac.MediaType.TEXT,
    "pbf": "application/x-protobuf",
    "ascii": "text/plain"
}

# Categories for keywords
cat_keywords = {
    "risk_data_type": ["hazard", "exposure", "vulnerability"],
    "subcategory": ["coastal flood", "fluvial flood", "pluvial flood", "drought", "snowstorm/blizzard", "heat wave", "cold wave", "tropical cyclone", "extratropical cyclone",
                    "wildfire", "multi hazard",
                    "population number", "demographics", "socioeconomic status", "adaptive capacity", "building footprints", "building characteristics", 
                    "infrastructure footprints", "infrastructure characteristics", "urban/built-up", "land use/land cover", "population vulnerability"
                    ],
    "spatial_scale": ["(near-)global", "regional", "national", "subnational"],
    "reference_period": ["historical", "future", "historical & future"],
    "code": ["code"]
}

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
        
# Function to update existing keywords
def update_keywords(ext_key, keywords, categories):
    new_key = set(ext_key)
    # Add missing keywords from the existing keywords list
    for keyword in keywords:
        new_key.add(keyword)

    # Check for the presence of 'historical & future'
    if 'historical & future' in new_key:
        new_key.add('historical')
        new_key.add('future')
        new_key.discard('historical & future')

    # elif 'historical' in new_key and 'future' in new_key:
    #     new_key.discard('historical')
    #     new_key.discard('future')
    #     new_key.add('historical & future')

    # Sort the keywords based on categories
    sorted_keywords = []
    for categories, cat_keywords in categories.items():
        for keyword in cat_keywords:
            if keyword in new_key:
                sorted_keywords.append(keyword)

    # Add any remaining keywords that are not in the categories
    remaining_keywords = new_key - set(sorted_keywords)
    sorted_keywords.extend(remaining_keywords)
    return sorted_keywords

# Function to update providers ## DOES NOT WORK YET ##
def update_providers(provider1, provider2):
    # check whether both providers are equal
    print(provider1)
    print(provider2)
    check=(
        provider1 == provider2 #and
        #provider1[1] == provider2[1] and
        #provider1[2] == provider2[2]
    )
    if not check:
        providers = [provider1, provider2]
    else:
        providers = provider1
    return providers

# Create the main catalog
catalog_main = pystac.Catalog(
    id="climate-risk-data",
    title="Climate Risk Data",
    description="This is a community catalog containing datasets for the three risk drivers Hazard, Exposure, and Vulnerability. The catalog in its current form conforms with the risk framework of the IPCC's 5th Assessment Report (AR5) where risk results from the interaction of hazards, the elements exposed to these hazards as well as the vulnerability of the exposed elements. The catalog structure has been defined following a variety of standards for provisioning of risk data (please see 'LINK TO FIGURE WITH CATALOG STRUCTURE'). The catalog allows for the integration of other risk drivers, such as adaptation responses as defined in IPCC AR6 when such data are available. \n The first version of the catalog (released in XXXX) focusses on global-scale datasets that can be used as input in climate risk assessments (CRA) with as little preprocessing as possible. It has been developed as part of the Horizon Europe project CLIMAAX, which ... (see link to website/handbook below). \n The development of the catalog is described in detail in the publication referenced below. The catalog is designed under Open Science and FAIR Data Principles, with the idea to be a community-led endeavor. We encourage anyone working with risk data at different spatial scales (i.e. local to global) to add datasets to this catalog, thereby creating growing knowledge base for further potential users. Please use GitHub Actions (see link below) to suggest new datasets."
)

# Function to create collections and items
def create_catalog_from_csv(indicator, catalog_main, dir):
    for row_num in range(len(indicator)):
        item = indicator.iloc[row_num]
        
        # Extract values from the row
        catalog_id = item['catalog']
        category_id = item['category']
        
      
        ## CATALOGS ##
        # Create or retrieve the first-level catalog
        if catalog_id not in [cat.id for cat in catalog_main.get_children()]:
            catalog1 = pystac.Catalog(id=catalog_id, 
                                      title=catalog_id.capitalize(), 
                                      description= f"{catalog_id.capitalize()} datasets" 
                                      )
            catalog_main.add_child(catalog1)
        else:
            catalog1 = catalog_main.get_child(catalog_id)

        # Create or retrieve the second-level catalog

        if category_id not in [cat.id for cat in catalog1.get_children()]:
            catalog2 = pystac.Catalog(id=category_id, 
                                      title=category_id.capitalize(), 
                                      description=f"{category_id.capitalize()} datasets")
            catalog1.add_child(catalog2)
        else:
            catalog2 = catalog1.get_child(category_id)   
        

        # Process bbox (needed for collections and items)
        bbox = item['bbox']
        bbox_list = [float(coord.strip()) for coord in bbox.split(',')]

        # Process temporal resolution ## this needs to be changed to account for the total range of all items ##
        start, end = parse_year_range(str(item['temporal_resolution']))

        ## COLLECTIONS ##
        # combine title and short title
        title_collection = (item['title_collection'] + ' (' + item['title_short'] + ')' if not pd.isna(item['title_short'])
                            else (item['title_collection'])
                            )

        # make keywords
        # Function to make keywords based on subcategory and risk data type
        # use rdata if expvul
        rdata = item['risk_data_type'] if item['risk_data_type'] != 'hazard' else None
        # separate strings
        subc = item['subcategory'].split(',') if ',' in item['subcategory'] else item['subcategory']
        # add further keywords
        scale = item['spatial_scale']
        ref = item['reference_period']
        # add code keyword if provided
        code = 'code' if np.nan_to_num(item['code_link']) else None
        # filter out empty values
        keywords = []
        for keyword in [rdata, subc, scale, ref, code]:
            if keyword:
                if isinstance(keyword, list):
                    keywords = keywords + keyword
                else:
                    keywords.append(keyword)   
        print(f"keywords: {keywords}")

        # Create or retrieve the collection 
        if title_collection not in [col.id for col in catalog2.get_children()]:
                    
            # create basic collection
            collection = pystac.Collection(
                id=title_collection,
                title=title_collection,
                description= item['description_collection'],
                extent=pystac.Extent(
                    spatial=pystac.SpatialExtent([bbox_list]), # needs to be updated based on all items in the collection
                    temporal=pystac.TemporalExtent([[start, end]]), # needs to be updated based on all items in the collection
                ),
                license=item['license'],
                keywords=keywords, # add further if needed
                extra_fields={
                    'risk data type': item['risk_data_type'],
                    'subcategory': item['subcategory']                    
                }
            )

            # Create and add a Provider         
            provider = pystac.Provider(
                 name=item['provider'],
                 roles= [item['provider_role']], # change role: pystac.provider.ProviderRole.HOST ## DOES NOT WORK ##
                 url=item['link_website']
                )
            collection.providers = [provider]
            
            print(pystac.ProviderRole(item['provider_role']))
            
            catalog2.add_child(collection)

            print(f"collection {row_num} {title_collection} successfully added")

        else:
            # retrieve collection
            collection = catalog2.get_child(title_collection)
            
            # Update keywords
            # retrieve existing keywords
            key_col = collection.keywords
            # update keywords
            new_key = update_keywords(key_col, keywords, cat_keywords)
            # add to collection
            collection.keywords = new_key
            print(f"updated and sorted keywords: {new_key}")

            # # Update providers -> relevant when more than one weblink per collection provided: needs to be fixed to account for the option that several providers are already present. These need to be compared one by one
            # # retrieve existing provider
            # provider1 = collection.providers
            # # create potential new provider from current row
            # provider2 = pystac.Provider(
            #      name=item['provider'],
            #      roles=item['provider_role'],
            #      url=item['link_website']
            #     )
            # new_pro = update_providers(provider1, provider2)
            # # add to collection
            # collection.providers = new_pro
            print(f"collection {row_num} {title_collection} successfully updated")

        ## ITEMS ##
        # Create new item if not present yet
        if item['title_item'] not in [col.id for col in collection.get_items()]:
       
            # define item attributes that can deviate per item
            temporal_resolution = f"{item['temporal_resolution']} ({item['temporal_interval']})" if np.nan_to_num(item['temporal_interval']) else f"{item['temporal_resolution']}"
            scenarios = item['scenarios'] if np.nan_to_num(item['scenarios']) else None
            analysis_type = item['analysis_type'] if np.nan_to_num(item['analysis_type']) else None
            underlying_data = item['underlying_data'] if np.nan_to_num(item['underlying_data']) else None
            code =  f"{item['code_type']} (see Code link)" if np.nan_to_num(item['code_link']) else None
            usage_notes = item['usage_notes'] if np.nan_to_num(item['usage_notes']) else None
            
            # condition for spatial resolution
            if np.nan_to_num(item['spatial_resolution_unit']):
                if item['spatial_resolution'] == 'administrative units':
                    spatial_resolution = f"{item['spatial_resolution']} ({item['spatial_resolution_unit']})"
                else:
                    spatial_resolution = f"{item['spatial_resolution']} {item['spatial_resolution_unit']}"
            else:
                spatial_resolution = f"{item['spatial_resolution']}"

            # condition for publication
            if str(item['publication_link']).startswith('10.'):
                publication = f"{item['publication_type']} (see DOI)" 
            elif np.nan_to_num(item['publication_link']): 
                publication = f"{item['publication_type']} (see Publication link)"
            else:
                publication = None

            # Create basic item
            item_stac = pystac.Item(
                id=item['title_item'],
                geometry=None,  # Add geometry if available
                bbox=bbox_list,
                datetime=None, #datetime.now(),
                start_datetime=start,
                end_datetime=end,
                properties={
                    'title': item['title_item'],
                    'description': item['description_item'],
                    'risk data type': item['risk_data_type'],
                    'subcategory': item['subcategory'],
                    'spatial scale': item['spatial_scale'],
                    'reference period': item['reference_period'],
                    'temporal resolution': temporal_resolution, # combination of resolution and interval
                    'scenarios': scenarios,
                    'data type': item['data_type'],
                    'data format': item['format'],
                    'spatial resolution': spatial_resolution, # combination of resolution and unit
                    'data calculation type': item['data_calculation_type'],
                    'analysis type': analysis_type,
                    'underlying data': underlying_data,
                    'publication type': publication,
                    'code type': code,
                    'usage notes': usage_notes
                }
                # extra_fields={ # are part of the json, but not shown in the browser
                #         'subcategory': str(item['subcategory']), #remove str() again once subcategory fixed
                #         'risk data type': item['risk_data_type']
                #     }
            )

            # add projection extension
            proj_ext = ProjectionExtension.ext(item_stac, add_if_missing=True)
            # Add projection properties
            proj_ext.epsg = int(item['coordinate_system'])

            # Publication: Add scientific extension if DOI is present
            if str(item['publication_link']).startswith('10.'):
                print("doi available")
                sci_ext = ScientificExtension.ext(item_stac, add_if_missing=True)
                sci_ext.doi = item['publication_link'] # adjust condition here for links that are not dois
            elif np.nan_to_num(item['publication_link']):
                print("weblink available")
                link = pystac.Link(
                    rel="cite-as",  # Relationship of the link
                    target=item['publication_link'],  # Target URL
                    title="Publication link",  # Optional title
                    )
                item_stac.add_link(link)

            # Code: add link if available
            if code != None:
                print("code available")
                link = pystac.Link(
                    rel="cite-as",  # Relationship of the link
                    target=item['code_link'],  # Target URL
                    title="Code link",  # Optional title
                    )
                item_stac.add_link(link)

            # ADD ASSETS        
            # establish the number of assets
            asset_str = item['assets']
            if np.nan_to_num(asset_str):
                print('at least one asset provided; use asset link')
                assets = asset_str.split(';') if ';' in asset_str else [asset_str]
                roles = ["data"]
            else:
                assets = [item['link_website']] # change here once asset link updated
                roles = ["overview"]
                print('no assets provided; use website link instead')

            # loop through all assets
            counter = 1
            for asset in assets:
                # Determine the media type based on the format attribute
                media_type = format_to_media_type.get(item['format'].lower(), "application/octet-stream")  # Default to binary stream

                # Define the asset
                asset_stac = pystac.Asset(
                        href=asset,
                        media_type=media_type,
                        roles=roles,
                        title=f"Data Link {counter}"
                )
                # Add the asset to the item
                key = f"data-file_{counter}"
                item_stac.add_asset(key, asset_stac)
                counter +=1

            # Add item to collection
            collection.add_item(item_stac)
            
            # confirmation item added
            print(f"item {row_num} {item['title_item']} successfully added")
        else:
            print(f"item {row_num} already present. Compare items and remove duplicates.")
    
    # update collection properties based on all items belonging to the collection ## NOT FINISHED YET ##
    #collection_interval = sorted([collection_item.datetime, collection_item2.datetime])
    #temporal_extent = pystac.TemporalExtent(intervals=[collection_interval])

    catalog_main.describe()

    # Normalize hrefs and save the catalog
    catalog_main.normalize_hrefs(os.path.join(dir, "stac"))
    catalog_main.save(catalog_type=pystac.CatalogType.SELF_CONTAINED)
    #catalog_main.save(catalog_type=pystac.CatalogType.RELATIVE_PUBLISHED)
   

# Create catalogs from both hazard and exposure-vulnerability CSVs
create_catalog_from_csv(hazard, catalog_main, dir)
#create_catalog_from_csv(expvul, catalog_main, dir)