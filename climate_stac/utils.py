from datetime import datetime
import logging
import numpy as np
import pystac
import rasterio
from shapely import box, unary_union
from shapely.geometry import Polygon, mapping


__all__ = [
    'compute_overall_bbox',
    'get_bbox_and_footprint',
    'parse_year_range',
    'generate_keywords',
    'update_keywords',
    'providers_are_equal'
]

# Configure the logger
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("climate_stac")


def get_bbox_and_footprint(raster_uri):
    with rasterio.open(raster_uri) as ds:
        bounds = ds.bounds
        bbox = [bounds.left, bounds.bottom, bounds.right, bounds.top]
        footprint = Polygon(
            [
                [bounds.left, bounds.bottom],
                [bounds.left, bounds.top],
                [bounds.right, bounds.top],
                [bounds.right, bounds.bottom],
            ]
        )

        return bbox, mapping(footprint)

def compute_overall_bbox(items: list[pystac.Item]) -> None | list[float]:
    """Return the overall spatial extent of all collection items."""
    bboxes = []
    for item in items:
        if item.bbox:
            minx, miny, maxx, maxy = item.bbox
            bboxes.append(box(minx, miny, maxx, maxy))
    if not bboxes:
        return None
    overall_bbox = unary_union(bboxes).bounds
    return list(overall_bbox)

# Function to parse year range
def parse_year_range(year_str: str) -> tuple[datetime, datetime]:
    # If the string contains a dash, it's a range
    if "-" in year_str:
        start, end = year_str.split("-")

        # Determine the length of the start and end strings to parse correctly
        if len(start) == 4 and len(end) == 4:
            start_year, end_year = int(start), int(end)
            return datetime(start_year, 1, 1), datetime(end_year, 12, 31)
        # if YYYY-now:
        elif len(start) == 4 and len(end) == 3:
            start_year = int(start)
            end_year = datetime.now().year
            end_month = datetime.now().month
            end_day = datetime.now().day
            # other option: end = None, but it creates some issues when creating the items
            return datetime(start_year, 1, 1), datetime(end_year, end_month, end_day)
        # if start date BC (can handle any year until 10000 BC, but not year 0):
        elif len(start) > 4 and len(end) == 4:
            start_year = (
                int(start.replace("BC", "")) - 1
            )  # 1 BC is year 0; 2 BC is year 1 etc.
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


# Function to generate keywords
def generate_keywords(item: pystac.Item) -> list:
    # Determine risk data type if not 'hazard'
    risk_data = item['risk_data_type'] if item['risk_data_type'] != 'hazard' else None
    
    # Subcategory: a) replace subcategory with string with commas, b) split the string if it contains commas
    if item['category'] == 'flood' and item['subcategory'] == 'flood type not specified':
        item['subcategory'] = "coastal flood,fluvial flood,pluvial flood"
    subcategories = item['subcategory'].split(',') if ',' in item['subcategory'] else [item['subcategory']]
    
    # Extract other attributes
    spatial_scale = item['spatial_scale']
    reference_period = item['reference_period']
    
    # Add 'code' keyword if 'code_link' is provided
    code_keyword = "code available" if np.nan_to_num(item['code_link']) else None
    
    # Filter out None or empty values and flatten lists into keywords
    keywords = [
        keyword for keyword in [risk_data, *subcategories, spatial_scale, reference_period, code_keyword]
        if keyword
    ]
    logger.info(f"keywords: {keywords}")
    return keywords

# Function to update existing keywords
def update_keywords(ext_key, keywords, categories):
    # Combine existing keywords and additional keywords into a set to avoid duplicates
    new_key = set(ext_key) | set(keywords)

    # Check for the presence of 'historical & future'
    if 'historical & future' in new_key:
        new_key.update(['historical', 'future'])
        new_key.discard('historical & future')

    # Sort the keywords based on categories
    sorted_keywords = []
    for categories, cat_keywords in categories.items():
        sorted_keywords.extend([kw for kw in cat_keywords if kw in new_key])

    # Add any remaining keywords that are not in the categories
    remaining_keywords = new_key - set(sorted_keywords)
    sorted_keywords.extend(remaining_keywords)
    return sorted_keywords

# Function to compare two pystac.Provider objects
def providers_are_equal(provider1: pystac.Provider, provider2: pystac.Provider) -> bool:
    name_equal = provider1.name == provider2.name
    roles_equal = set(provider1.roles) == set(provider2.roles)
    url_equal = provider1.url == provider2.url
    return name_equal and roles_equal and url_equal