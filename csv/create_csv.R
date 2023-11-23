##################################
##  create csvs with attributes ##
##################################
# by Lena Reimann
# Nov 20, 2023

## goal: create a first setup of the csvs needed for STAC
# harmonized with/mapped to STAC and RDLS terminologies (* = stac; @ = rdls)

rm(list=ls())

# define directory
wd = "C:/Users/lrn238/OneDrive - Vrije Universiteit Amsterdam/Global_data_repository_paper/catalog/STAC"

## collection (here: every row represents one collection, i.e. datasets from the same category and provider)
# produce collection df with GHS-POP used as sample data
collection = data.frame( 
  catalog1 = "Exposure and Vulnerability",
  catalog2 = "Social", #depends on catalog1
  category = "Population", #@
  risk_data_type = "Exposure", #@; use as label  
  title = "Global Human Settlement Layer Population", #@
  title_short = "GHS-POP", #collection name that items refer to
  item_ids = 1, #vector of items that belong to the collection 
  description = "The Global Human Settlement Layer Population (GHS-POP) datasets are available in two different coordinate systems and two spatial resolutions each for the years 1975-2030 in 5-year time intervals.", #*
  data_type = "raster", #raster, vector, tabular (not in any of the specs -> remove?)
  format = "GeoTIFF", #@; e.g. GeoTIFF, NetCDF, shapefile, csv 
  bbox = "-180, -90, 180, 90", #*, @; extent coordinates --> more elegant way to get this in the stac format
  spatial_scale = "global", #@ (only 'scale'); for now global as the default
  reference_period = "current and future", #@; use as label
  temporal_resolution = "1975-2030", #*, @; to be added in ISO8601
  time_interval = "5-yearly", #(e.g. years, decades); not necessarily needed, but can be derived from the items
  scenarios = "N/A", #if future
  data_calculation_type = "simulated", #@; Inferred, observed, simulated; not so suitable for E/V?
  calculation_approach = "dasymetric", #if applicable, determined by data calculation type
  underlying_data = "Gridded Population of the World (GPW) v4, GHS built-up land (GHS-BUILT)", #related to data calculation type
  provider = "JRC Data Catalogue", #*
  provider_role = "licensor, producer", #*
  license = "CC BY 4.0", #*
  code_link = "N/A", #e.g. doi to code related to the data
  code_type = "N/A", #e.g. download, processing
  publication_link = "https://doi.org/10.2760/098587", #e.g. doi; rephrase to accommodate scientific extension
  publication_type = "report", #e.g. report, article, policy brief
  usage_notes = "any relevant information or cautions for using the data"
)

name = "collection.csv"
write.csv(collection, file = paste(wd, name, sep = "/"), row.names = F)

# export variable/attribute names
vars = colnames(collection)
name = "attributes_collection.csv"
write.csv(vars, file = paste(wd, name, sep = "/"), row.names = F)


## item (here: each row in the csv represents one item in stac)
# produce item df with GHS-POP used as sample data -> 4 different spatial resolutions
item = data.frame(
  id = 1, 
  #catalog1 = "Exposure and Vulnerability", #first division
  #catalog2 = "Social", # second division
  #category = "Population", # third division
  collection_name = "GHS-POP", #collection name that items refer to
  title = "GHS-POP WGS84 3 arc seconds", #*
  description = "GHS-POP in WGS84 coordinates and a spatial resolution of 3 arc seconds.", #*
  bbox = "-180, -90, 180, 90", #extent coordinates --> more elegant solution for STAC
  crs_name = "WGS84", # Coordinate Reference System; rephrase to accommodate projection extensions
  crs_code = 4326, #EPSG code
  spatial_resolution = 3, #@; value
  spatial_resolution_unit = "arc seconds", #unit
  #reference_period = "future", #@; historical, future
  #year = 2030, 
  #scenario_name = "extrapolation", #if future
  resources = "https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_POP_GLOBE_R2023A/GHS_POP_E1975_GLOBE_R2023A_4326_3ss/V1-0/GHS_POP_E1975_GLOBE_R2023A_4326_3ss_V1_0.zip" 
  #* == STAC asset; example file for 1975
)


## make it a function ##
make_item = function(
    id,
    collection_name,
    title,
    description,
    bbox,
    crs_name,
    crs_code,
    spatial_resolution,
    spatial_resolution_unit,
    resources) {
  
  item = data.frame(
    id,
    collection_name,
    title,
    description,
    bbox,
    crs_name,
    crs_code,
    spatial_resolution,
    spatial_resolution_unit,
    resources
  )
  
  return(item)
}

# prep input for 'make item' function
id = c(1,2,3,4)
collection_name = rep("GHS_POP", length(id))
title = c("GHS-POP WGS84 3 arc seconds", 
          "GHS-POP WGS84 30 arc seconds",
          "GHS-POP Mollweide 100 meters",
          "GHS-POP Mollweide 1 kilometer")
description =  c("GHS-POP in WGS84 coordinates and a spatial resolution of 3 arc seconds.", 
                 "GHS-POP in WGS84 coordinates and a spatial resolution of 30 arc seconds.",
                 "GHS-POP in Mollweide coordinates and a spatial resolution of 100 meters.",
                 "GHS-POP in Mollweide coordinates and a spatial resolution of 1 kilometer.")
bbox = rep("-180, -90, 180, 90", length(id))
crs_name = c("WGS84", "WGS84", "Mollweide", "Mollweide")
crs_code = c(4326, 4326, 54009, 54009)
spatial_resolution = c(3, 30, 100, 1000)
spatial_resolution_unit = c("arc seconds", "arc seconds", "meters", "meters")
resources = c("https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_POP_GLOBE_R2023A/GHS_POP_E1975_GLOBE_R2023A_4326_3ss/V1-0/GHS_POP_E1975_GLOBE_R2023A_4326_3ss_V1_0.zip",
              "https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_POP_GLOBE_R2023A/GHS_POP_E1975_GLOBE_R2023A_4326_30ss/V1-0/GHS_POP_E1975_GLOBE_R2023A_4326_30ss_V1_0.zip",
              "https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_POP_GLOBE_R2023A/GHS_POP_E1975_GLOBE_R2023A_54009_100/V1-0/GHS_POP_E1975_GLOBE_R2023A_54009_100_V1_0.zip",
              "https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_POP_GLOBE_R2023A/GHS_POP_E1975_GLOBE_R2023A_54009_1000/V1-0/GHS_POP_E1975_GLOBE_R2023A_54009_1000_V1_0.zip"
)

# run 'make item' function
item = make_item(
  id,
  collection_name,
  title,
  description,
  bbox,
  crs_name,
  crs_code,
  spatial_resolution,
  spatial_resolution_unit,
  resources
  )

name = "item.csv"
write.csv(item, file = paste(wd, name, sep = "/"), row.names = F)

# export variable/attribute names
vars = colnames(item)
name = "attributes_item.csv"
write.csv(vars, file = paste(wd, name, sep = "/"), row.names = F)







