##################################
##  create csvs with attributes ##
##################################
# by Lena Reimann
# Nov 30, 2023

## goal: create a first setup of the csv needed for STAC
#         a) one csv independent from item or collection
#         b) two separate csvs (kept for reference)
# harmonized with/mapped to STAC and RDLS terminologies (* = stac; @ = rdls)

rm(list=ls())

# define directory
wd = "C:/Users/lrn238/Documents/GitHub/climate-risk-stac/"

#----------------#
#### Option a ####
#----------------#

## make one csv from which items and collections are derived
csv = data.frame(
  
  # catalog ('folder') location
  catalog1 = "exposure-vulnerability",
  catalog2 = "population", #'category' according to RDLs
  catalog3 = "population-number", 
  risk_data_type = "exposure", #@; use as label  
  data_type_category = "social", # use as label; maybe not needed?
  
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
  format = "GeoTIFF", #@; e.g. GeoTIFF, NetCDF, shapefile, csv 
  
  # spatial details
  spatial_scale = "global", #@ (only 'scale'); for now global as the default
  crs_name = c("WGS84", "WGS84", "Mollweide", "Mollweide"), # Coordinate Reference System; rephrase to accommodate projection extensions
  crs_code = c(4326, 4326, 54009, 54009), #EPSG code
  spatial_resolution = c(3, 30, 100, 1000), #@; value
  spatial_resolution_unit = c("arc seconds", "arc seconds", "meters", "meters"), #unit
  
  # temporal details
  reference_period = "historical and future", #@; use as label
  temporal_resolution = "1975-2030", #*, @; to be added in ISO8601
  time_interval = "5-yearly", #(e.g. years, decades); not necessarily needed, but can be derived from the items
  #year = seq(1975, 2030, by = 5),
  scenarios = "extrapolation", #if future
  
  # data calculation
  data_calculation_type = "simulated", #@; Inferred, observed, simulated; not so suitable for E/V?
  calculation_approach = "dasymetric", #if applicable, determined by data calculation type
  underlying_data = "Gridded Population of the World (GPW) v4, GHS built-up land (GHS-BUILT)",
  
  # data provision
  provider = "JRC Data Catalogue", #*
  provider_role = "licensor, producer", #*
  license = "CC BY 4.0", #*
  link_website = "https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_POP_GLOBE_R2023A/",
  
  # code
  code_link = "N/A", #e.g. doi to code related to the data
  code_type = "N/A", #e.g. download, processing
  
  # publication
  publication_link = "https://doi.org/10.2760/098587", #e.g. doi; rephrase to accommodate scientific extension
  publication_type = "report", #e.g. report, article, policy brief
  
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
             )#*
)

name = "csv.csv"
#write.csv(csv, file = paste(wd, "csv", name, sep = "/"), row.names = F)

# export variable/attribute names
vars = colnames(csv)
name = "attributes_csv.csv"
#write.csv(vars, file = paste(wd, "csv", name, sep = "/"), row.names = F)




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







