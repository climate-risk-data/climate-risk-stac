#%%
import pystac
from pystac.extensions.scientific import ScientificExtension
from pystac.extensions.projection import ProjectionExtension
import json
import os
#from tempfile import TemporaryDirectory
from datetime import datetime
import pandas as pd
from datetime import datetime
import numpy as np
import sys

#tmp_dir = TemporaryDirectory()
dir = 'C:/Users/lrn238/OneDrive - Vrije Universiteit Amsterdam/Documents/GitHub/climate-risk-stac/'

#%%
root_url = r'https://raw.githubusercontent.com/DirkEilander/climate-risk-stac/main/stac'
stac_extensions=[]

# Read the data sheet
hazard = pd.read_excel('csv/xls.xlsx', 'hazard')
expvul = pd.read_excel('csv/xls.xlsx', 'exposure-vulnerability')

# determine catalog/excel tab to be used
#indicator = hazard
indicator = expvul

# preprocessing, two options (option a. much easier?): 
# a. replace all na with "not available"
# b. make condition for properties to leave out certain properties if na


#%% create catalog folder structure %%# --> make a function that does this based on the (sub)categories in the xls

# create main catalog (level0)
catalog = pystac.Catalog(
    id="climate-risk-data", 
    title="Climate Risk Data",
    description="Community catalog containing datasets for all risk drivers.",
    stac_extensions=stac_extensions,
)

# subcatalog hazard (level1)
catalog_h = pystac.Catalog(
    id="hazard",
    title="Hazard",
    description="Hazard datasets",
    stac_extensions=stac_extensions,
)
catalog.add_child(catalog_h)

# hazard profile (level2)
catalog_h1 = pystac.Catalog(
    id="flooding",
    title="Flooding",
    description="Flooding datasets",
    stac_extensions=stac_extensions,
)
catalog_h.add_child(catalog_h1)

# hazard type (level3)
#catalog_h11 = pystac.Catalog(
#    id="coastal-flood",
#    title="Coastal flooding",
#    description="Coastal flooding datasets",
#    stac_extensions=stac_extensions,
#)
#catalog_h1.add_child(catalog_h11)

#catalog_h12 = pystac.Catalog(
#    id="fluvial-flood",
#    title="Fluvial flooding",
#    description="Fluvial flooding datasets",
#    stac_extensions=stac_extensions,
#)
#catalog_h1.add_child(catalog_h12)

#catalog_h13 = pystac.Catalog(
#    id="pluvial-flood",
#    title="Pluvial flooding",
#    description="Pluvial flood datasets",
#    stac_extensions=stac_extensions,
#)
#catalog_h1.add_child(catalog_h13)


catalog_h2 = pystac.Catalog(
    id="extreme-precipitation",
    title="Extreme precipitation",
    description="Extreme precipitation-related datasets",
    stac_extensions=stac_extensions,
)
catalog_h.add_child(catalog_h2)

#catalog_h21 = pystac.Catalog(
#    id="drought",
#    title="Drought",
#    description="Drought datasets",
#    stac_extensions=stac_extensions,
#)
#catalog_h2.add_child(catalog_h21)

#catalog_h22 = pystac.Catalog(
#    id="snow",
#    title="Heavy snowfall",
#    description="Heavy snowfall datasets",
#    stac_extensions=stac_extensions,
#)
#catalog_h2.add_child(catalog_h22)


catalog_h3 = pystac.Catalog(
    id="extreme-temperature",
    title="Extreme temperature",
    description="Extreme temperature-related datasets",
    stac_extensions=stac_extensions,
)
catalog_h.add_child(catalog_h3)

#catalog_h31 = pystac.Catalog(
#    id="heat-wave",
#    title="Heat wave",
#    description="Heat wave datasets",
#    stac_extensions=stac_extensions,
#)
#catalog_h3.add_child(catalog_h31)

#catalog_h32 = pystac.Catalog(
#    id="cold-wave",
#    title="Cold wave",
#    description="Cold wave datasets",
#    stac_extensions=stac_extensions,
#)
#catalog_h3.add_child(catalog_h32)


catalog_h4 = pystac.Catalog(
    id="windstorm",
    title="Windstorm",
    description="Windstorm-related datasets",
    stac_extensions=stac_extensions,
)
catalog_h.add_child(catalog_h4)

#catalog_h41 = pystac.Catalog(
#    id="tropical-cyclone",
#    title="Tropical cyclone",
#    description="Tropical cyclone datasets",
#    stac_extensions=stac_extensions,
#)
#catalog_h4.add_child(catalog_h41)

#catalog_h42 = pystac.Catalog(
#    id="extratropical-cyclone",
#    title="Extratropical cyclone",
#    description="Extratropical cyclone datasets",
#    stac_extensions=stac_extensions,
#)
#catalog_h4.add_child(catalog_h42)


catalog_h5 = pystac.Catalog(
    id="wildfire",
    title="Wildfire",
    description="Wildfire datasets",
    stac_extensions=stac_extensions,
)
catalog_h.add_child(catalog_h5)


catalog_h6 = pystac.Catalog(
    id="multi-hazard",
    title="Multi-hazard",
    description="Multi-hazard datasets",
    stac_extensions=stac_extensions,
)
catalog_h.add_child(catalog_h6)


#%%
# add dataset collections
collection1 = pystac.Collection(
    id="aqueduct",
    title="Aqueduct flood hazard maps",
    description="Aqueduct flood hazard maps for different return periods ...",
    extent=pystac.Extent(
        spatial=pystac.SpatialExtent([[-180, -90, 180, 90]]),
        temporal=pystac.TemporalExtent([[datetime.utcnow(), None]]),
    ),
    #keywords = "Fluvial flooding", # or similar?
)
catalog_h1.add_child(collection1)



#%%
# exposure & vulnerability
catalog_ev = pystac.Catalog(
    id="exposure-vulnerability",
    title="Exposure and Vulnerability",
    description="Exposure and Vulnerability datasets",
    stac_extensions=stac_extensions,
)
catalog.add_child(catalog_ev)

# exp & vul type (level2)
catalog_ev1 = pystac.Catalog(
    id="population",
    title="Population",
    description="Population datasets",
    stac_extensions=stac_extensions,
)
catalog_ev.add_child(catalog_ev1)

#  exp (level3)
#catalog_ev11 = pystac.Catalog(
#    id="population-number",
#    title="Population number",
#    description="Datasets of population numbers",
#    stac_extensions=stac_extensions,
#)
#catalog_ev1.add_child(catalog_ev11)

#  vul (level3)
#catalog_ev12 = pystac.Catalog(
#    id="demographics",
#    title="Demographics",
#    description="Datasets of demographic characteristics",
#    stac_extensions=stac_extensions,
#)
#catalog_ev1.add_child(catalog_ev12)

#catalog_ev13 = pystac.Catalog(
#    id="socioeconomic",
#    title="Socioeconomic status",
#    description="Datasets of socioeconomic status",
#    stac_extensions=stac_extensions,
#)
#catalog_ev1.add_child(catalog_ev13)

#catalog_ev14 = pystac.Catalog(
#    id="adaptive-capacity",
#    title="Adaptive capacity",
#    description="Datasets of adaptive capacity",
#    stac_extensions=stac_extensions,
#)
#catalog_ev1.add_child(catalog_ev14)


catalog_ev2 = pystac.Catalog(
    id="buildings",
    title="Buildings",
    description="Buildings datasets",
    stac_extensions=stac_extensions,
)
catalog_ev.add_child(catalog_ev2)

#catalog_ev21 = pystac.Catalog(
#    id="building-footprints",
#    title="Building footprints",
#    description="Datasets of building footprints",
#    stac_extensions=stac_extensions,
#)
#catalog_ev2.add_child(catalog_ev21)

#catalog_ev22 = pystac.Catalog(
#    id="building-characteristics",
#    title="Building characteristics",
#    description="Datasets of building characteristics (e.g. use type, material, heritage)",
#    stac_extensions=stac_extensions,
#)
#catalog_ev2.add_child(catalog_ev22)


catalog_ev3 = pystac.Catalog(
    id="infrastructure",
    title="Infrastructure",
    description="Infrastructure datasets",
    stac_extensions=stac_extensions,
)
catalog_ev.add_child(catalog_ev3)

#catalog_ev31 = pystac.Catalog(
#    id="infrastructure-footprints",
#    title="Infrastructure footprints",
#    description="Datasets of infrastructure footprints",
#    stac_extensions=stac_extensions,
#)
#catalog_ev3.add_child(catalog_ev31)

#catalog_ev32 = pystac.Catalog(
#    id="infrastructure-characteristics",
#    title="Infrastructure characteristics",
#    description="Datasets of infrastructure characteristics (e.g. type, accessibility)",
#    stac_extensions=stac_extensions,
#)
#catalog_ev3.add_child(catalog_ev32)


catalog_ev4 = pystac.Catalog(
    id="environment",
    title="Environment",
    description="Datasets of environmental variables",
    stac_extensions=stac_extensions,
)
catalog_ev.add_child(catalog_ev4)

#catalog_ev41 = pystac.Catalog(
#    id="urban-built",
#    title="Urban, built-up land",
#    description="Datasets of urban landuse and built-up land",
#    stac_extensions=stac_extensions,
#)
#catalog_ev4.add_child(catalog_ev41)

#catalog_ev42 = pystac.Catalog(
#    id="lulc",
#    title="Land use and land cover",
#    description="Land use and land cover datasets (e.g. forests, agriculture, protected land)",
#    stac_extensions=stac_extensions,
#)
#catalog_ev4.add_child(catalog_ev42)


# add dataset collections
collection1 = pystac.Collection(
    id="ghs-pop",
    title="Global Human Settlement Layer Population",
    description="The Global Human Settlement Layer Population (GHS-POP) datasets are available in two different coordinate systems and two spatial resolutions each for the years 1975-2030 in 5-year time intervals.",
    extent=pystac.Extent(
        spatial=pystac.SpatialExtent([[-180, -90, 180, 90]]),
        temporal=pystac.TemporalExtent([[datetime.utcnow(), None]]),
    ),
    #keywords = "Population number", # or similar?
)
catalog_ev1.add_child(collection1)
  
# add example item (Timothy :))

# loop through the sheet (right now only one line)
#row_num = 2 # for hazard data test item
row_num = 20 # for expvul data test item

# Get item metadata
item = indicator.iloc[row_num]

# determine catalog to place this item into (create catalog?) --> determine this based on 'catalog' and 'category' attributes from xls
#catalogX = catalog_h3 # for hazard data test item
catalogX = catalog_ev1 # for expvul data test item

# determine bbox list
bbox_list = [float(coord.strip()) for coord in item['bbox'].split(',')]

# find a way to determine the geometry
#footprint = Polygon([ 
#            [bbox_list[1], bbox_list[2]],
#            [bbox_list[1], bbox_list[4]],
#            [bbox_list[3], bbox_list[4]],
#            [bbox_list[3], bbox_list[2]]
#            ])

item_stac = pystac.Item(
            id = 'test',
            geometry = None,
            bbox = bbox_list,
            datetime = datetime.utcnow(),
            #start_datetime = datetime.utcnow(),
            #end_datetime = datetime.utcnow(),
            properties={
                'title': item['title_item'], #added
                'description': item['description_item'],
                'data_type': item['data_type'],
                'data_format': item['format'],
                'spatial_scale': item['spatial_scale'],
                #'coordinate_system': item['coordinate_system'],
                'reference_period': item['reference_period'],
                'temporal_resolution': item['temporal_resolution'],
                'temporal_interval': item['temporal_interval'], #expvul test: json just changed to "not available" (fix later!)
                #'scenarios': item['scenarios'],
                'data_calculation_type': item['data_calculation_type'],
                'analysis_type': item['analysis_type'],
                'underlying_data': item['underlying_data'],
                'provider': item['provider'],
                'provider_role': item['provider_role'],
                'license': item['license'],
                'link_website': item['link_website'],
                'publication_link': item['publication_link'],
                'publication_type': item['publication_type'],
                #'code_link': item['code_link'],
                #'code_type': item['code_type'],
                #'usage_notes': item['usage_notes'],
                #'assets': item['assets'],
                'name_contributor': item['name_contributor'],
            },
        )
catalogX.add_item(item_stac) # my change

#collection.add_item(item_stac)
# collection.save()
if not np.nan_to_num(item['publication_link']) == 0:
    sci_ext = ScientificExtension.ext(item_stac, add_if_missing=True)
    sci_ext.doi = item['publication_link']

# %%
catalog.normalize_hrefs(os.path.join(dir, "stac"))
catalog.save(catalog_type=pystac.CatalogType.SELF_CONTAINED)
