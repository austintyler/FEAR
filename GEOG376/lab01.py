#####################################################################################
# Author: Tyler Austin
# Name: Lab01.py
# Date Written: 1/30/15
# Date Modified: N/A
# Variables Used: desc_wwf, desc_sa, sr_wwf, sr_sa, pcs_wwf, gcs_wwf, pcs_sa, gcs_sa
# This program explores dataset properties and prints to screen selected parameters.
#####################################################################################

# Importing the ArcPy library
import arcpy

# Variables
# Opening shapefile and assigning it to a varibale
desc_wwf = arcpy.Describe("S:/376/Spring15/tea/lab01_data/wwf_terr_ecos.shp")
# Opening Raster Image and assigning it to a varibale
desc_sa = arcpy.Describe("S:/376/Spring15/tea/lab01_data/forests_sa")
# Assigned spatial reference of shapefile to a variable
sr_wwf = desc_wwf.spatialReference
# Assigned spatial reference of raster image to a variable
sr_sa = desc_sa.spatialReference
# Assigned projected coordinate system name of spatial reference shpfile to a variable
pcs_wwf = sr_wwf.PCSname
# Assigned geographic coordinate system name of spatial reference shpfile to a variable
gcs_wwf = sr_wwf.GCSname
# Assigned projected coordinate system name of spatial reference raster image to a variable
pcs_sa = sr_sa.PCSname
# Assigned geographic coordinate system name of spatial reference raster image to a variable
gcs_sa = sr_sa.GCSname

# Print shapefile name
print desc_wwf.name
# Print header
print "Dataset Properties:"
# Print dataset type of shp
print "Dataset Type: " + desc_wwf.datasetType
# Print feature type of shp
print "Feature Type: " + desc_wwf.featureType
# Print shape type of shp
print "Shape Type: " + desc_wwf.shapeType

# Determines if shp has a projected or geographic coordinate system and prints
# the repsective Projection Name
if (len(pcs_wwf) > len(gcs_wwf)):
    print "Projection Name: " + pcs_wwf
else:
    print "Projection Name: " + gcs_wwf

# Prints the extent of the shp
# XMin, XMax, YMin, YMax
print("Extent: {0}, {1}, {2}, {3}".format(desc_wwf.extent.XMin, desc_wwf.extent.XMax, desc_wwf.extent.YMin, desc_wwf.extent.YMax))

# Blank Spaces
print "\n"
print "\n"

# Print raster image name
print "Dataset " + desc_sa.name + " Properties: "
# Print dataset type of raster
print "Dataset Type: " + desc_sa.datasetType
# Print grid format of raster
print "Grid Format: " + desc_sa.format
# Print the number of bands in raster
print "Number of Bands: " + str(desc_sa.bandCount)

# Determines if Raster has a projected or geographic coordinate system and prints
# the repsective Projection Name
if (len(pcs_sa) > len(gcs_sa)):
    print "Projection Name: " + pcs_sa
else:
    print "Projection Name: " + gcs_sa

# Prints the extent of the Raster
# XMin, XMax, YMin, YMax
print("Extent: {0}, {1}, {2}, {3}".format(desc_sa.extent.XMin, desc_sa.extent.XMax, desc_sa.extent.YMin, desc_sa.extent.YMax))

# Blank Spaces and closing remarks
print "\n"
print "\n"
print "End of Dataset Description"



