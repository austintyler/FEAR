#####################################################################################
# Author: Tyler Austin
# Name: Lab05.py
# Date Written: 3/26/15
# Date Modified: 3/26/15
# Variables Used: sourcePath, filePath, shpName, projection, projShpFile, rfeMerged, 
#     groupOne, groupTwo, groupThree, field, cursor, totalSize, grpOnePercent, 
#     grpTwoPercent, grpThreePercent
# Purpose: To provide the breakdown of satellite active fire detection for
#     2007 in the Russian Far East by detection confidence level.
#####################################################################################

# Importing the ArcPy library
import arcpy

# Set workspace
sourcePath = 'R:/376/Spring15/Lab05/lab05_data/'
# sourcePath = 'C:/Users/taust_000/Box Sync/GEOG376/Lab05/lab05_data_source/'
filePath = 'S:/376/Spring15/tea/lab05_data/'
# filePath = 'C:/Users/taust_000/Box Sync/GEOG376/Lab05/lab05_data/'

# List of shapefile names
shpName = ['200701_rfe.shp', '200702_rfe.shp', '200703_rfe.shp', '200704_rfe.shp', '200705_rfe.shp', '200706_rfe.shp',
           '200707_rfe.shp', '200708_rfe.shp', '200709_rfe.shp', '200710_rfe.shp', '200711_rfe.shp', '200712_rfe.shp']

# GCS 'WGS 1984' used to define projection 
projection = arcpy.SpatialReference(4326)

# Output list
projShpFile = []

# Loop to copy shapefiles, define their projection and append to the output list
for shape in shpName:
    # Copy data into student folder
    arcpy.CopyFeatures_management(sourcePath + shape, filePath + shape)
    # Define projection
    arcpy.DefineProjection_management(filePath + shape, projection)
    # Append to output file
    projShpFile.append(filePath + shape)

# Variable for merge output file
rfeMerged = filePath + '2007_rfe_merged.shp'

# Merge all shapefiles into one
arcpy.Merge_management ([projShpFile[0], projShpFile[1], projShpFile[2], projShpFile[3], projShpFile[4], projShpFile[5],
                         projShpFile[6], projShpFile[7], projShpFile[8], projShpFile[9], projShpFile[10], 
                         projShpFile[11]], rfeMerged)

# lists for different confidence levels
groupOne = []
groupTwo = []
groupThree = []

# variable for field queried
field = "CONF"

# variable to create cursor to loop through each feature in shapefile
cursor = arcpy.SearchCursor(rfeMerged)

# loops through each feature in shapefile and then queries the confidence field to
# determine which group it sound be appended to
for feature in cursor:
    if feature.getValue(field) > 85:
        groupOne.append(feature)
    elif feature.getValue(field) <= 85 and feature.getValue(field) >= 60:
        groupTwo.append(feature)
    else:
        groupThree.append(feature)

# calculates total amount of features in shapefile
totalSize = float(len(groupOne) + len(groupTwo) + len(groupThree))

# calculates group percent of total features rounded to the nearest integer
grpOnePercent = int(round((len(groupOne)/totalSize)*100, -1))
grpTwoPercent = int(round((len(groupTwo)/totalSize)*100, -1))
grpThreePercent = int(round((len(groupThree)/totalSize)*100, -1))

# print statements
print 'In 2007 ' + str(grpOnePercent) +'% of fires were detected within the 81% to 100% confidence range.'
print 'In 2007 ' + str(grpTwoPercent) +'% of fires were detected within the 60% to 80% confidence range.'
print 'In 2007 ' + str(grpThreePercent) +'% of fires were detected within the 0% to 59% confidence range.'

# The End
print 'Processing Completed'
