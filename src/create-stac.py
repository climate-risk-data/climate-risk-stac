#%%
import pystac
import json
import os
from tempfile import TemporaryDirectory
from datetime import datetime

tmp_dir = TemporaryDirectory()
#tmp_dir.name = 'C:/Users/lrn238/OneDrive - Vrije Universiteit Amsterdam/Documents/GitHub/climate-risk-stac/'

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
  
# add item (Timothy :))


# %%
catalog.normalize_hrefs(os.path.join(tmp_dir.name, "stac"))
catalog.save(catalog_type=pystac.CatalogType.SELF_CONTAINED)
