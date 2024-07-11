#%% NOTES %%#
# also includes keywords (via 'extra_fields') --> needs to be changed to combine attributes from several columns into a list instead of a "keywords" col

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
        title_short = item['title_short'] if not pd.isna(item['title_short']) else item['title_collection']
        bbox = item['bbox']
        temporal_resolution = item['temporal_resolution']
        
        # Create or retrieve the catalog
        if catalog_id not in [cat.id for cat in catalog_main.get_children()]:
            new_catalog = pystac.Catalog(id=catalog_id, title=catalog_id, description=catalog_id)
            catalog_main.add_child(new_catalog)
        else:
            new_catalog = catalog_main.get_child(catalog_id)
        
        # Create or retrieve the collection
        if category_id not in [col.id for col in new_catalog.get_children()]:
            # Process bbox
            if not np.nan_to_num(bbox) == 0:
                try:
                    bbox_list = [float(coord.strip()) for coord in bbox.split(',')]
                except ValueError:
                    print(f'Check bbox: {bbox}')
                    bbox_list = bbox
            else:
                bbox_list = np.nan

            # Process temporal resolution
            if not np.nan_to_num(temporal_resolution) == 0:
                year_start, year_end = parse_year_range(str(temporal_resolution))
            else:
                year_start, year_end = np.nan, np.nan
                print('Cannot create collection, because of no input for temporal_resolution')
                continue

            keywords = item['keywords'].split(',') if 'keywords' in item else []
            
            collection = pystac.Collection(
                id=category_id,
                title=category_id,
                description=category_id,
                extent=pystac.Extent(
                    spatial=pystac.SpatialExtent([bbox_list]),
                    temporal=pystac.TemporalExtent([[year_end, year_start]]),
                ),
                extra_fields={
                    'data_type': item['data_type'],
                    'data_format': item['format'],
                    'spatial_scale': item['spatial_scale'],
                    'coordinate_system': item['coordinate_system'],
                    'keywords': keywords
                },
            )
            new_catalog.add_child(collection)
        else:
            collection = new_catalog.get_child(category_id)
        
        # Create the item
        item_stac = pystac.Item(
            id=item['title_item'],
            geometry=None,  # Add geometry if available
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
        
        # Add scientific extension if publication link is present
        if not pd.isna(item['publication_link']):
            sci_ext = ScientificExtension.ext(item_stac, add_if_missing=True)
            sci_ext.doi = item['publication_link']
        
        # Add item to collection
        collection.add_item(item_stac)

    # Normalize hrefs and save the catalog
    catalog_main.normalize_hrefs(os.path.join(dir, "stac"))
    catalog_main.save(catalog_type=pystac.CatalogType.SELF_CONTAINED)

# Create catalogs from both hazard and exposure-vulnerability CSVs
create_catalog_from_csv(hazard, catalog_main, dir)
create_catalog_from_csv(expvul, catalog_main, dir)
