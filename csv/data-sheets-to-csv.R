###############################################
##  fill csv with datasets already collected ## # do it manually??
###############################################
# by Lena Reimann
# Dec 6, 2023

## goal: reformat data sheets to fit csv requirements
#         a) own data sheet of E+V data
#         b) WCR data sheet of H, E, V data
#         c) Lindersson et al. 2020 data sheet


rm(list=ls())


# load packages
lib = "C:/Users/lrn238/AppData/Local/RLIB" 
library(readxl, lib.loc = lib)

# define directory
wd = "C:/Users/lrn238/Documents/GitHub/climate-risk-stac/"


#-------------------------#
#### a) own data sheet ####
#-------------------------#

# load sheet
path = "C:/Users/lrn238/OneDrive - Vrije Universiteit Amsterdam/Global_data_repository_paper/catalog/STAC/"
file = "LR_Subnational exposure & vulnerability data.xlsx"

hist = read_excel(paste0(path, file), sheet = "Observed")
proj = read_excel(paste0(path, file), sheet = "Projections") 
# also load hazard sheet!!!

cols = colnames(hist)
# select global
hist = subset(hist, coverage_sp == "global")






