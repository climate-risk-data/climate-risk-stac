#%%
import pystac
import json
import os
from tempfile import TemporaryDirectory
from datetime import datetime

tmp_dir = TemporaryDirectory()

#%%
root_url = r'https://raw.githubusercontent.com/DirkEilander/climate-risk-stac/main/stac'
stac_extensions=[]

catalog = pystac.Catalog(
    id="climate-risk-data", 
    title="Climate Risk Data",
    description="Community catalog containing datasets for all risk drivers.",
    stac_extensions=stac_extensions,
)

#%%
# add child collections

collection_h = pystac.Collection(
    id="hazard",
    title="Hazard",
    description="Hazard datasets",
    extent=pystac.Extent(
        spatial=pystac.SpatialExtent([[-180, -90, 180, 90]]),
        temporal=pystac.TemporalExtent([[datetime.utcnow(), None]]),
    ),
)
catalog.add_child(collection_h)

collection_ev = pystac.Collection(
    id="exposure-vulnerability",
    title="Exposure and Vulnerability",
    description="Exposure and Vulnerability datasets",
    extent=pystac.Extent(
        spatial=pystac.SpatialExtent([[-180, -90, 180, 90]]),
        temporal=pystac.TemporalExtent([[datetime.utcnow(), None]]),
    ),
)
catalog.add_child(collection_ev)

#

# %%
catalog.normalize_hrefs(os.path.join(tmp_dir.name, "stac"))
catalog.save(catalog_type=pystac.CatalogType.SELF_CONTAINED)