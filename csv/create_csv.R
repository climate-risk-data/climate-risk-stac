##################################
##  create csvs with attributes ##
##################################
# by Lena Reimann
# Dec 11, 2023

## goal: create a first setup of the csv needed for STAC
#         a) one csv independent from item or collection
#         b) two separate csvs (kept for reference)
# harmonized with/mapped to STAC and RDLS terminologies (* = stac; @ = rdls)

rm(list=ls())

#lib = "C:/Users/lrn238/AppData/Local/RLIB" 
# load packages
#library(dplyr, lib.loc = lib)

# define directory
wd = "C:/Users/lrn238/Documents/GitHub/climate-risk-stac/"

#----------------#
#### Option a ####
#----------------#

## make one csv from which items and collections are derived
csv = data.frame(
  
  # catalog ('folder') location
  catalog = "exposure-vulnerability",
  category = "population",
  subcategory = "population-number", 
  risk_data_type = "exposure", #@; use as label  
  #data_type_category = "social", # use as label; maybe not needed?
  
  # collection-specific attributes
  title_collection = "Global Human Settlement Layer Population", #
  title_short = "GHS-POP", #not needed unless used as 'folder title'
  description_collection = "The Global Human Settlement Layer Population (GHS-POP) datasets 
  are available in two different coordinate systems and two spatial resolutions each 
  for the years 1975-2030 in 5-year time intervals.", #*
  
  # item-specific attributes
  title_item = c("GHS-POP WGS84 3 arc seconds", 
                 "GHS-POP WGS84 30 arc seconds",
                 "GHS-POP Mollweide 100 meters",
                 "GHS-POP Mollweide 1 kilometer"),
  description_item = c("GHS-POP in WGS84 coordinates and a spatial resolution of 3 arc seconds.", 
                       "GHS-POP in WGS84 coordinates and a spatial resolution of 30 arc seconds.",
                       "GHS-POP in Mollweide coordinates and a spatial resolution of 100 meters.",
                       "GHS-POP in Mollweide coordinates and a spatial resolution of 1 kilometer."),
  item_id = 1:4, #if several datasets listed from the same overall dataset (i.e. collection)
  
  # extent
  bbox = rep("-180, -90, 180, 90", 4), #*, @; extent coordinates --> more elegant way to get this in the stac format

  # data type
  data_type = "raster", #raster, vector, tabular (not in any of the specs -> remove?)
  format = "geotiff", #@; e.g. geotiff, netcdf, shapefile, csv 
  
  # spatial details
  spatial_scale = "global", #@; for now global as the default
  crs_name = c("WGS84", "WGS84", "Mollweide", "Mollweide"), # Coordinate Reference System; rephrase to accommodate projection extensions
  crs_code = c(4326, 4326, 54009, 54009), #EPSG code
  spatial_resolution = c(3, 30, 100, 1000), #@; value
  spatial_resolution_unit = c("arc seconds", "arc seconds", "meters", "meters"), #unit
  
  # temporal details
  reference_period = "historical & future", #@; use as label
  temporal_resolution = "1975-2030", #*, @; to be added in ISO8601
  temporal_interval = "5-yearly", #(e.g. years, decades); not necessarily needed, but can be derived from the items
  #year = seq(1975, 2030, by = 5),
  scenarios = "extrapolation", #if future
  
  # data calculation
  data_calculation_type = "simulated", #@; Inferred, observed, simulated; not so suitable for E/V?
  analysis_type = "dasymetric modeling",
  underlying_data = "Gridded Population of the World (GPW) v4, GHS built-up land (GHS-BUILT)",
  
  # data provision
  provider = "JRC Data Catalogue", #*
  provider_role = "licensor", #*
  license = "CC-BY-4.0", #*
  link_website = "https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_POP_GLOBE_R2023A/",
  
  # publication
  publication_link = "https://doi.org/10.2760/098587", #e.g. doi; rephrase to accommodate scientific extension
  publication_type = "report", #e.g. report, article, policy brief  
  
  # code
  code_link = " ", #e.g. doi to code related to the data
  code_type = " ", #e.g. download, processing
  
  # usage notes
  usage_notes = "GHS-POP may underestimate population in sparsely populated locations where settlements are not detected by the satellite; 
  it may therefore overconcentrate population in those locations where settlements are detected.",
  
  # links to specific datasets
  assets = c(paste("GHS_POP_E1975_GLOBE_R2023A_4326_3ss/V1-0/GHS_POP_E1975_GLOBE_R2023A_4326_3ss_V1_0.zip",
                   "GHS_POP_E1980_GLOBE_R2023A_4326_3ss/V1-0/GHS_POP_E1980_GLOBE_R2023A_4326_3ss_V1_0.zip", 
                   "GHS_POP_E1985_GLOBE_R2023A_4326_3ss/V1-0/GHS_POP_E1985_GLOBE_R2023A_4326_3ss_V1_0.zip", 
                   "GHS_POP_E1990_GLOBE_R2023A_4326_3ss/V1-0/GHS_POP_E1990_GLOBE_R2023A_4326_3ss_V1_0.zip", 
                   "GHS_POP_E1995_GLOBE_R2023A_4326_3ss/V1-0/GHS_POP_E1995_GLOBE_R2023A_4326_3ss_V1_0.zip", 
                   "GHS_POP_E2000_GLOBE_R2023A_4326_3ss/V1-0/GHS_POP_E2000_GLOBE_R2023A_4326_3ss_V1_0.zip", 
                   "GHS_POP_E2005_GLOBE_R2023A_4326_3ss/V1-0/GHS_POP_E2005_GLOBE_R2023A_4326_3ss_V1_0.zip", 
                   "GHS_POP_E2010_GLOBE_R2023A_4326_3ss/V1-0/GHS_POP_E2010_GLOBE_R2023A_4326_3ss_V1_0.zip",
                   "GHS_POP_E2015_GLOBE_R2023A_4326_3ss/V1-0/GHS_POP_E2015_GLOBE_R2023A_4326_3ss_V1_0.zip",
                   "GHS_POP_E2020_GLOBE_R2023A_4326_3ss/V1-0/GHS_POP_E2020_GLOBE_R2023A_4326_3ss_V1_0.zip",
                   "GHS_POP_E2025_GLOBE_R2023A_4326_3ss/V1-0/GHS_POP_E2025_GLOBE_R2023A_4326_3ss_V1_0.zip",
                   "GHS_POP_E2030_GLOBE_R2023A_4326_3ss/V1-0/GHS_POP_E2030_GLOBE_R2023A_4326_3ss_V1_0.zip",
                   sep = ";"),
             paste("GHS_POP_E1975_GLOBE_R2023A_4326_30ss/V1-0/GHS_POP_E1975_GLOBE_R2023A_4326_30ss_V1_0.zip",
                   "GHS_POP_E1980_GLOBE_R2023A_4326_30ss/V1-0/GHS_POP_E1980_GLOBE_R2023A_4326_30ss_V1_0.zip", 
                   "GHS_POP_E1985_GLOBE_R2023A_4326_30ss/V1-0/GHS_POP_E1985_GLOBE_R2023A_4326_30ss_V1_0.zip", 
                   "GHS_POP_E1990_GLOBE_R2023A_4326_30ss/V1-0/GHS_POP_E1990_GLOBE_R2023A_4326_30ss_V1_0.zip", 
                   "GHS_POP_E1995_GLOBE_R2023A_4326_30ss/V1-0/GHS_POP_E1995_GLOBE_R2023A_4326_30ss_V1_0.zip", 
                   "GHS_POP_E2000_GLOBE_R2023A_4326_30ss/V1-0/GHS_POP_E2000_GLOBE_R2023A_4326_30ss_V1_0.zip", 
                   "GHS_POP_E2005_GLOBE_R2023A_4326_30ss/V1-0/GHS_POP_E2005_GLOBE_R2023A_4326_30ss_V1_0.zip", 
                   "GHS_POP_E2010_GLOBE_R2023A_4326_30ss/V1-0/GHS_POP_E2010_GLOBE_R2023A_4326_30ss_V1_0.zip",
                   "GHS_POP_E2015_GLOBE_R2023A_4326_30ss/V1-0/GHS_POP_E2015_GLOBE_R2023A_4326_30ss_V1_0.zip",
                   "GHS_POP_E2020_GLOBE_R2023A_4326_30ss/V1-0/GHS_POP_E2020_GLOBE_R2023A_4326_30ss_V1_0.zip",
                   "GHS_POP_E2025_GLOBE_R2023A_4326_30ss/V1-0/GHS_POP_E2025_GLOBE_R2023A_4326_30ss_V1_0.zip",
                   "GHS_POP_E2030_GLOBE_R2023A_4326_30ss/V1-0/GHS_POP_E2030_GLOBE_R2023A_4326_30ss_V1_0.zip",
                   sep = ";"),
             paste("GHS_POP_E1975_GLOBE_R2023A_54009_100/V1-0/GHS_POP_E1975_GLOBE_R2023A_54009_100_V1_0.zip",
                   "GHS_POP_E1980_GLOBE_R2023A_54009_100/V1-0/GHS_POP_E1980_GLOBE_R2023A_54009_100_V1_0.zip", 
                   "GHS_POP_E1985_GLOBE_R2023A_54009_100/V1-0/GHS_POP_E1985_GLOBE_R2023A_54009_100_V1_0.zip", 
                   "GHS_POP_E1990_GLOBE_R2023A_54009_100/V1-0/GHS_POP_E1990_GLOBE_R2023A_54009_100_V1_0.zip", 
                   "GHS_POP_E1995_GLOBE_R2023A_54009_100/V1-0/GHS_POP_E1995_GLOBE_R2023A_54009_100_V1_0.zip", 
                   "GHS_POP_E2000_GLOBE_R2023A_54009_100/V1-0/GHS_POP_E2000_GLOBE_R2023A_54009_100_V1_0.zip", 
                   "GHS_POP_E2005_GLOBE_R2023A_54009_100/V1-0/GHS_POP_E2005_GLOBE_R2023A_54009_100_V1_0.zip", 
                   "GHS_POP_E2010_GLOBE_R2023A_54009_100/V1-0/GHS_POP_E2010_GLOBE_R2023A_54009_100_V1_0.zip",
                   "GHS_POP_E2015_GLOBE_R2023A_54009_100/V1-0/GHS_POP_E2015_GLOBE_R2023A_54009_100_V1_0.zip",
                   "GHS_POP_E2020_GLOBE_R2023A_54009_100/V1-0/GHS_POP_E2020_GLOBE_R2023A_54009_100_V1_0.zip",
                   "GHS_POP_E2025_GLOBE_R2023A_54009_100/V1-0/GHS_POP_E2025_GLOBE_R2023A_54009_100_V1_0.zip",
                   "GHS_POP_E2030_GLOBE_R2023A_54009_100/V1-0/GHS_POP_E2030_GLOBE_R2023A_54009_100_V1_0.zip",
                   sep = ";"),
             paste("GHS_POP_E1975_GLOBE_R2023A_54009_1000/V1-0/GHS_POP_E1975_GLOBE_R2023A_54009_1000_V1_0.zip",
                   "GHS_POP_E1980_GLOBE_R2023A_54009_1000/V1-0/GHS_POP_E1980_GLOBE_R2023A_54009_1000_V1_0.zip", 
                   "GHS_POP_E1985_GLOBE_R2023A_54009_1000/V1-0/GHS_POP_E1985_GLOBE_R2023A_54009_1000_V1_0.zip", 
                   "GHS_POP_E1990_GLOBE_R2023A_54009_1000/V1-0/GHS_POP_E1990_GLOBE_R2023A_54009_1000_V1_0.zip", 
                   "GHS_POP_E1995_GLOBE_R2023A_54009_1000/V1-0/GHS_POP_E1995_GLOBE_R2023A_54009_1000_V1_0.zip", 
                   "GHS_POP_E2000_GLOBE_R2023A_54009_1000/V1-0/GHS_POP_E2000_GLOBE_R2023A_54009_1000_V1_0.zip", 
                   "GHS_POP_E2005_GLOBE_R2023A_54009_1000/V1-0/GHS_POP_E2005_GLOBE_R2023A_54009_1000_V1_0.zip", 
                   "GHS_POP_E2010_GLOBE_R2023A_54009_1000/V1-0/GHS_POP_E2010_GLOBE_R2023A_54009_1000_V1_0.zip",
                   "GHS_POP_E2015_GLOBE_R2023A_54009_1000/V1-0/GHS_POP_E2015_GLOBE_R2023A_54009_1000_V1_0.zip",
                   "GHS_POP_E2020_GLOBE_R2023A_54009_1000/V1-0/GHS_POP_E2020_GLOBE_R2023A_54009_1000_V1_0.zip",
                   "GHS_POP_E2025_GLOBE_R2023A_54009_1000/V1-0/GHS_POP_E2025_GLOBE_R2023A_54009_1000_V1_0.zip",
                   "GHS_POP_E2030_GLOBE_R2023A_54009_1000/V1-0/GHS_POP_E2030_GLOBE_R2023A_54009_1000_V1_0.zip",
                   sep = ";")
             ),#*
  name_contributor = "Lena Reimann"
)

name = "csv.csv"
write.csv(csv, file = paste(wd, "csv", name, sep = "/"), row.names = F)


## create table with attribute descriptions and mappings to stac & RDLS
# export attribute names
column_name = colnames(csv)

description = c("id of catalog (i.e. hazard or exposure-vulnerability)",
                "category of data type",
                "subcategory of data type",
                "risk driver (i.e. hazard, exposure, vulnerability)",
                #"category of the risk driver (e.g. hydrological, meterological; social, physical)",
                "dataset (collection) name",
                "short name of dataset (if applicable)",
                "short description of dataset (collection)",
                "name of specific dataset item",
                "short description of dataset item",
                "dataset item id",
                "bounding box coordinates (WGS coordinates)",
                "data type (i.e. raster, vector, tabular)",
                "data format (i.e. geotiff, geopackage, shapefile, geodatabase, csv)",
                "spatial scale (i.e. global, regional, national, subnational; for now global only)",
                "name of the coordinate reference system (CRS) (e.g. WGS84, Mollweide)",
                "numerical code of CRS (e.g. 4326, 54009)",
                "spatial resolution (numeric or administrative unit level)",
                "spatial resolution unit (i.e. arc seconds, arc minutes, decimal degrees, meters, kilometers)",
                "reference period for which the data are available (i.e. historical, future, historical & future)",
                "temporal resolution of the data (YYYY or YYYY-YYYY)",
                "temporal intervals of the data (i.e. hourly, daily, monthly, yearly, 5-yearly, 10-yearly, irregular)",
                "name of scenarios used (if future) (e.g. RCPs, SSPs, warming levels)",
                "method used for data calculation (i.e. inferred, observed, simulated)",
                "method used for calculating the data (i.e. probabilistic, deterministic, empirical for hazards; e.g. dasymetric modeling, random forest modeling for exposure & vulnerability)",
                "data underlying the calculation type and approach (if applicable)",
                "name of data provider",
                "role of data provider (i.e. licensor, producer, processor, host)",
                "data distribution license (e.g CC0-1.0, CC-BY-4.0, CC-BY-SA-4.0)",
                "link to the website where the data can be accessed",
                "link to publication (e.g. doi)",
                "type of publication (e.g. report, article, documentation)",
                "link to available code (e.g. doi)",
                "type of available code (e.g. for data download, processing, application)",
                "any relevant information for using the data",
                "links to specific data files, separated by ';'",
                "name of person who added the dataset to the sheet (for possible follow-ups)"
                )
# make df
csv_readme = data.frame(column_name, description)

# add columns for the rdls and stac specs
csv_readme$rdls = NA
csv_readme$stac = NA

# add rdls equivalents (not necessarily complete)
csv_readme[which(csv_readme$column_name == "catalog"), "rdls"] <- "category"
csv_readme[which(csv_readme$column_name == "category"), "rdls"] <- "category"
csv_readme[which(csv_readme$column_name == "subcategory"), "rdls"] <- "category"
csv_readme[which(csv_readme$column_name == "risk_data_type"), "rdls"] <- "risk_data_type"
#csv_readme[which(csv_readme$column_name == "data_type_category"), "rdls"] <- paste("exposure_category", "hazard_type", sep = "; ")
csv_readme[which(csv_readme$column_name == "bbox"), "rdls"] <- "bbox"
csv_readme[which(csv_readme$column_name == "format"), "rdls"] <- "format"
csv_readme[which(csv_readme$column_name == "spatial_scale"), "rdls"] <- "spatial_scale"
csv_readme[which(csv_readme$column_name == "crs_code"), "rdls"] <- "coordinate_system"
csv_readme[which(csv_readme$column_name == "spatial_resolution"), "rdls"] <- "spatial_resolution"
#csv_readme[which(csv_readme$column_name == "reference_period"), "rdls"] <- "reference_period" #can't find this any more
csv_readme[which(csv_readme$column_name == "temporal_resolution"), "rdls"] <- "temporal_resolution"
csv_readme[which(csv_readme$column_name == "data_calculation_type"), "rdls"] <- "data_calculation_type"
csv_readme[which(csv_readme$column_name == "analysis_type"), "rdls"] <- "analysis_type"
csv_readme[which(csv_readme$column_name == "provider"), "rdls"] <- "publisher"
csv_readme[which(csv_readme$column_name == "provider_role"), "rdls"] <- "entity"
csv_readme[which(csv_readme$column_name == "license"), "rdls"] <- "license"
csv_readme[which(csv_readme$column_name == "link_website"), "rdls"] <- "access_url"
csv_readme[which(csv_readme$column_name == "publication_link"), "rdls"] <- "doi"
csv_readme[which(csv_readme$column_name == "assets"), "rdls"] <- "download_url"
csv_readme[which(csv_readme$column_name == "name_contributor"), "rdls"] <- "contact_point"

# add stac equivalents (not necessarily complete)
csv_readme[which(csv_readme$column_name == "catalog"), "stac"] <- "catalog"
csv_readme[which(csv_readme$column_name == "category"), "stac"] <- "catalog"
csv_readme[which(csv_readme$column_name == "subcategory"), "stac"] <- "catalog"
csv_readme[which(csv_readme$column_name == "title_collection"), "stac"] <- "title"
csv_readme[which(csv_readme$column_name == "description_collection"), "stac"] <- "description"
csv_readme[which(csv_readme$column_name == "title_item"), "stac"] <- "title"
csv_readme[which(csv_readme$column_name == "description_item"), "stac"] <- "description"
csv_readme[which(csv_readme$column_name == "item_id"), "stac"] <- "id (not numeric)"
csv_readme[which(csv_readme$column_name == "bbox"), "stac"] <- "bbox"
csv_readme[which(csv_readme$column_name == "crs_code"), "stac"] <- "proj:epsg (projection extension)"
csv_readme[which(csv_readme$column_name == "temporal_resolution"), "stac"] <- "datetime"
csv_readme[which(csv_readme$column_name == "provider"), "stac"] <- "provider"
csv_readme[which(csv_readme$column_name == "provider_role"), "stac"] <- "roles"
csv_readme[which(csv_readme$column_name == "license"), "stac"] <- "license"
csv_readme[which(csv_readme$column_name == "publication_link"), "stac"] <- "sci:doi (scientific citation extension)"
csv_readme[which(csv_readme$column_name == "assets"), "stac"] <- "assets"


# rearrange columns
# column_name = csv_readme$column_name
# stac = csv_readme$stac
# rdls = csv_readme$rdls
# description = csv_readme$description

# csv_readme =  data.frame(column_name, stac, rdls, description)

name = "mapping_attributes.csv"
write.csv(csv_readme, file = paste(wd, "csv", name, sep = "/"), row.names = F)




#----------------------#
#### Option b (OLD) ####
#----------------------#

## collection (here: every row represents one collection, i.e. datasets from the same category and provider)
# produce collection df with GHS-POP used as sample data
# collection = data.frame( 
#   # catalog ('folder') location
#   catalog1 = "Exposure and Vulnerability",
#   catalog2 = "Social", 
#   catalog3 = "Population", #'category' according to RDLs
#   risk_data_type = "Exposure", #@; use as label  
#   
#   # collection-specific attributes
#   title = "Global Human Settlement Layer Population", #
#   title_short = "GHS-POP", #not needed unless used as 'folder title'
#   description = "The Global Human Settlement Layer Population (GHS-POP) datasets 
#   are available in two different coordinate systems and two spatial resolutions each 
#   for the years 1975-2030 in 5-year time intervals.", #*
# 
#   # extent
#   bbox = "-180, -90, 180, 90", #*, @; extent coordinates --> more elegant way to get this in the stac format
#   
#   # data type
#   data_type = "raster", #raster, vector, tabular (not in any of the specs -> remove?)
#   format = "GeoTIFF", #@; e.g. GeoTIFF, NetCDF, shapefile, csv 
#   
#   # spatial details
#   spatial_scale = "global", #@ (only 'scale'); for now global as the default
#   
#   # temporal details
#   reference_period = "current and future", #@; use as label
#   temporal_resolution = "1975-2030", #*, @; to be added in ISO8601
#   time_interval = "5-yearly", #(e.g. years, decades); not necessarily needed, but can be derived from the items
#   scenarios = "N/A", #if future
#   
#   # data calculation
#   data_calculation_type = "simulated", #@; Inferred, observed, simulated; not so suitable for E/V?
#   calculation_approach = "dasymetric", #if applicable, determined by data calculation type
#   underlying_data = "Gridded Population of the World (GPW) v4, GHS built-up land (GHS-BUILT)", #related to data calculation type
#   
#   # data provision
#   provider = "JRC Data Catalogue", #*
#   provider_role = "licensor, producer", #*
#   license = "CC BY 4.0", #*
#   link_website = "link to overall website where the data can be accessed",
#   
#   # code
#   code_link = "N/A", #e.g. doi to code related to the data
#   code_type = "N/A", #e.g. download, processing
#   
#   # publication
#   publication_link = "https://doi.org/10.2760/098587", #e.g. doi; rephrase to accommodate scientific extension
#   publication_type = "report", #e.g. report, article, policy brief
#   
#   # usage notes
#   usage_notes = "any relevant information or cautions for using the data"
# )
# 
# name = "collection.csv"
# #write.csv(collection, file = paste(wd, "csv", name, sep = "/"), row.names = F)
# 
# # export variable/attribute names
# vars = colnames(collection)
# name = "attributes_collection.csv"
# #write.csv(vars, file = paste(wd, "csv", name, sep = "/"), row.names = F)
# 
# 
# ## item (here: each row in the csv represents one item in stac)
# # produce item df with GHS-POP used as sample data -> 4 different spatial resolutions
# ## make it a function ##
# make_item = function(
#     id,
#     collection_name,
#     title,
#     description,
#     bbox,
#     crs_name,
#     crs_code,
#     spatial_resolution,
#     spatial_resolution_unit,
#     assets) {
#   
#   item = data.frame(
#     id,
#     collection_name,
#     title,
#     description,
#     bbox,
#     crs_name,
#     crs_code,
#     spatial_resolution,
#     spatial_resolution_unit,
#     assets
#   )
#   
#   return(item)
# }
# 
# # prep input for 'make item' function
# id = c(1,2,3,4)
# collection_name = rep("GHS_POP", length(id))
# title = c("GHS-POP WGS84 3 arc seconds", 
#           "GHS-POP WGS84 30 arc seconds",
#           "GHS-POP Mollweide 100 meters",
#           "GHS-POP Mollweide 1 kilometer")
# description =  c("GHS-POP in WGS84 coordinates and a spatial resolution of 3 arc seconds.", 
#                  "GHS-POP in WGS84 coordinates and a spatial resolution of 30 arc seconds.",
#                  "GHS-POP in Mollweide coordinates and a spatial resolution of 100 meters.",
#                  "GHS-POP in Mollweide coordinates and a spatial resolution of 1 kilometer.")
# bbox = rep("-180, -90, 180, 90", length(id))
# crs_name = c("WGS84", "WGS84", "Mollweide", "Mollweide")
# crs_code = c(4326, 4326, 54009, 54009)
# spatial_resolution = c(3, 30, 100, 1000)
# spatial_resolution_unit = c("arc seconds", "arc seconds", "meters", "meters")
# assets = c("https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_POP_GLOBE_R2023A/GHS_POP_E1975_GLOBE_R2023A_4326_3ss/V1-0/GHS_POP_E1975_GLOBE_R2023A_4326_3ss_V1_0.zip",
#               "https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_POP_GLOBE_R2023A/GHS_POP_E1975_GLOBE_R2023A_4326_30ss/V1-0/GHS_POP_E1975_GLOBE_R2023A_4326_30ss_V1_0.zip",
#               "https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_POP_GLOBE_R2023A/GHS_POP_E1975_GLOBE_R2023A_54009_100/V1-0/GHS_POP_E1975_GLOBE_R2023A_54009_100_V1_0.zip",
#               "https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_POP_GLOBE_R2023A/GHS_POP_E1975_GLOBE_R2023A_54009_1000/V1-0/GHS_POP_E1975_GLOBE_R2023A_54009_1000_V1_0.zip"
# )
# 
# # run 'make item' function
# item = make_item(
#   id,
#   collection_name,
#   title,
#   description,
#   bbox,
#   crs_name,
#   crs_code,
#   spatial_resolution,
#   spatial_resolution_unit,
#   assets
#   )
# 
# name = "item.csv"
# #write.csv(item, file = paste(wd, "csv", name, sep = "/"), row.names = F)
# 
# # export variable/attribute names
# vars = colnames(item)
# name = "attributes_item.csv"
# #write.csv(vars, file = paste(wd, "csv", name, sep = "/"), row.names = F)







