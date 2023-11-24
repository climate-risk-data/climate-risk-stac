#%%
import pystac
import json
import os
from tempfile import TemporaryDirectory
from datetime import datetime

tmp_dir = TemporaryDirectory()

tmp_dir.name = 'C:/Users/lrn238/Documents/GitHub/climate-risk-stac/'

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
    description="Hazard dataset",
    stac_extensions=stac_extensions,
)
catalog.add_child(catalog_h)

# subcatalogs hazard profile (level2)
catalog_h1 = pystac.Catalog(
    id="flood",
    title="Flood",
    description="Flooding datasets",
    stac_extensions=stac_extensions,
)
catalog_h.add_child(catalog_h1)

catalog_h2 = pystac.Catalog(
    id="precipitation",
    title="Precipitation",
    description="Precipitation-related datasets",
    stac_extensions=stac_extensions,
)
catalog_h.add_child(catalog_h2)

catalog_h3 = pystac.Catalog(
    id="temperature",
    title="Temperature",
    description="Temperature-related datasets",
    stac_extensions=stac_extensions,
)
catalog_h.add_child(catalog_h3)

catalog_h4 = pystac.Catalog(
    id="pressure-wind",
    title="Pressure and Wind",
    description="Pressure- and Wind-related datasets",
    stac_extensions=stac_extensions,
)
catalog_h.add_child(catalog_h4)

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

# subcatalogs hazard type (level3)
catalog_h11 = pystac.Catalog(
    id="coastal-flood",
    title="Coastal flood flood",
    description="Coastal flood datasets",
    stac_extensions=stac_extensions,
)
catalog_h1.add_child(catalog_h11)

catalog_h12 = pystac.Catalog(
    id="fluvial-flood",
    title="Fluvial flood",
    description="Fluvial flood datasets",
    stac_extensions=stac_extensions,
)
catalog_h1.add_child(catalog_h12)

catalog_h13 = pystac.Catalog(
    id="pluvial-flood",
    title="Pluvial flood",
    description="Pluvial flood datasets",
    stac_extensions=stac_extensions,
)
catalog_h1.add_child(catalog_h13)




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



# %%
catalog.normalize_hrefs(os.path.join(tmp_dir.name, "stac"))
catalog.save(catalog_type=pystac.CatalogType.SELF_CONTAINED)