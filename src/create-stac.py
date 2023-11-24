#%%
import pystac
import json
import os
from tempfile import TemporaryDirectory
from datetime import datetime

tmp_dir = TemporaryDirectory()
#tmp_dir.name = 'C:/Users/lrn238/Documents/GitHub/climate-risk-stac/'

#%%
root_url = r'https://raw.githubusercontent.com/DirkEilander/climate-risk-stac/main/stac'
stac_extensions=[]

#%% create catalog folder structure %%#

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
catalog_h11 = pystac.Catalog(
    id="coastal-flood",
    title="Coastal flooding",
    description="Coastal flooding datasets",
    stac_extensions=stac_extensions,
)
catalog_h1.add_child(catalog_h11)

catalog_h12 = pystac.Catalog(
    id="fluvial-flood",
    title="Fluvial flooding",
    description="Fluvial flooding datasets",
    stac_extensions=stac_extensions,
)
catalog_h1.add_child(catalog_h12)

#catalog_h13 = pystac.Catalog(
#    id="pluvial-flood",
#    title="Pluvial flooding",
#    description="Pluvial flood datasets",
#    stac_extensions=stac_extensions,
#)
#catalog_h1.add_child(catalog_h13)


catalog_h2 = pystac.Catalog(
    id="precipitation",
    title="Precipitation",
    description="Precipitation-related datasets",
    stac_extensions=stac_extensions,
)
catalog_h.add_child(catalog_h2)

catalog_h21 = pystac.Catalog(
    id="drought",
    title="Drought",
    description="Drought datasets",
    stac_extensions=stac_extensions,
)
catalog_h2.add_child(catalog_h21)

catalog_h22 = pystac.Catalog(
    id="snow",
    title="Heavy snowfall",
    description="Heavy snowfall datasets",
    stac_extensions=stac_extensions,
)
catalog_h2.add_child(catalog_h22)


catalog_h3 = pystac.Catalog(
    id="temperature",
    title="Temperature",
    description="Temperature-related datasets",
    stac_extensions=stac_extensions,
)
catalog_h.add_child(catalog_h3)

catalog_h31 = pystac.Catalog(
    id="heat-wave",
    title="Heat wave",
    description="Heat wave datasets",
    stac_extensions=stac_extensions,
)
catalog_h3.add_child(catalog_h31)

catalog_h32 = pystac.Catalog(
    id="cold-wave",
    title="Cold wave",
    description="Cold wave datasets",
    stac_extensions=stac_extensions,
)
catalog_h3.add_child(catalog_h32)


catalog_h4 = pystac.Catalog(
    id="wind",
    title="Wind",
    description="Wind-related datasets",
    stac_extensions=stac_extensions,
)
catalog_h.add_child(catalog_h4)

catalog_h41 = pystac.Catalog(
    id="tropical-cyclone",
    title="Tropical cyclone",
    description="Tropical cyclone datasets",
    stac_extensions=stac_extensions,
)
catalog_h4.add_child(catalog_h41)

catalog_h42 = pystac.Catalog(
    id="extratropical-cyclone",
    title="Extratropical cyclone",
    description="Extratropical cyclone datasets",
    stac_extensions=stac_extensions,
)
catalog_h4.add_child(catalog_h42)


catalog_h5 = pystac.Catalog(
    id="environment",
    title="Environmental degradation",
    description="Environmental degradation datasets",
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
collection = pystac.Collection(
    id="aqueduct",
    title="Aqueduct flood hazard maps",
    description="Aqueduct flood hazard maps for different return periods ...",
    extent=pystac.Extent(
        spatial=pystac.SpatialExtent([[-180, -90, 180, 90]]),
        temporal=pystac.TemporalExtent([[datetime.utcnow(), None]]),
    ),
)
catalog_h12.add_child(collection)


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

#  exp  (level3)
catalog_ev11 = pystac.Catalog(
    id="number",
    title="Population number",
    description="Population number datasets",
    stac_extensions=stac_extensions,
)
catalog_ev1.add_child(catalog_ev11)

# add dataset collections
collection = pystac.Collection(
    id="ghs-pop",
    title="Global Human Settlement Layer Population",
    description="The Global Human Settlement Layer Population (GHS-POP) datasets are available in two different coordinate systems and two spatial resolutions each for the years 1975-2030 in 5-year time intervals.",
    extent=pystac.Extent(
        spatial=pystac.SpatialExtent([[-180, -90, 180, 90]]),
        temporal=pystac.TemporalExtent([[datetime.utcnow(), None]]),
    ),
)
catalog_ev11.add_child(collection)

# add item (Timothy :))





# %%
catalog.normalize_hrefs(os.path.join(tmp_dir.name, "stac"))
catalog.save(catalog_type=pystac.CatalogType.SELF_CONTAINED)
