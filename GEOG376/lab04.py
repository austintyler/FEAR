#####################################################################################
# Author: Tyler Austin
# Name: Lab04.py
# Date Written: 2/26/15
# Date Modified: 2/26/15
# Variables Used: sourcePath, filePath, in_features, azRoadShp, azRoad, azRailShp, 
# azRail, caRoadShp, caRoad, caRailShp, caRail, expression, codeblock, numRoadAZ, 
# numRailAZ, numRoadCA, numRailCA
# Purpose: Selects features by attributes in this case by state and type of feature 
# and then creates new shapefiles of selected features.
#####################################################################################

# Importing the ArcPy library
import arcpy
from arcpy import env

# Set workspace
sourcePath = 'R:/376/Spring15/Lab04/lab04_data/'
filePath = 'S:/376/Spring15/tea/lab04_data/'
# filePath = 'C:/Users/taust_000/Box Sync/GEOG376/Lab04/lab04_data'
env.workspace = filePath

# Set local variables
in_features = "line_features.shp"

azRoadShp = "azRoad.shp"
azRoad = '"{0}" = {1}'.format('SOURCETHM','\'Azrdlines\'')

azRailShp = "azRail.shp"
azRail = '"{0}" = {1}'.format('SOURCETHM','\'Azrrlines\'')

caRoadShp = "caRoad.shp"
caRoad = '"{0}" = {1}'.format('SOURCETHM','\'Cardlines\'')

caRailShp = "caRail.shp"
caRail = '"{0}" = {1}'.format('SOURCETHM','\'Carrlines\'')

# Copy data into student folder
arcpy.CopyFeatures_management(sourcePath + in_features, filePath + in_features)

# Add fields to in_feature
arcpy.AddField_management(in_features, "state_AB", "TEXT")
arcpy.AddField_management(in_features, "state_name", "TEXT")

# Calculate new fields
arcpy.CalculateField_management(in_features, "state_AB", '!SOURCETHM![:2].upper()', "PYTHON_9.3")

# uses below code to write the state name from its abbreviation
expression = "nameState(!SOURCETHM![:2])"
# function to determine state name
codeblock = """
def nameState(abbrev):
    if abbrev == 'Az':
        return 'Arizona'
    if abbrev == 'Ca':
        return 'California'
    else:
        return 'DontCare'
"""

arcpy.CalculateField_management(in_features, "state_name", expression, "PYTHON_9.3", codeblock)

# Execute Select
arcpy.Select_analysis(in_features, azRoadShp, azRoad)
arcpy.Select_analysis(in_features, azRailShp, azRail)
arcpy.Select_analysis(in_features, caRoadShp, caRoad)
arcpy.Select_analysis(in_features, caRailShp, caRail)

# Delete added fields from input file
arcpy.DeleteField_management (in_features, "state_AB")
arcpy.DeleteField_management (in_features, "state_name")

# Count number of records and print count in each shapefile
numRoadAZ = arcpy.GetCount_management(azRoadShp).getOutput(0)
numRailAZ = arcpy.GetCount_management(azRailShp).getOutput(0)
numRoadCA = arcpy.GetCount_management(caRoadShp).getOutput(0)
numRailCA = arcpy.GetCount_management(caRailShp).getOutput(0)

print 'There are {0} number of records for roads in Arizona.'.format(numRoadAZ)
print 'There are {0} number of records for railroads in Arizona.'.format(numRailAZ)
print 'There are {0} number of records for roads in California.'.format(numRoadCA)
print 'There are {0} number of records for railroads in California.'.format(numRailCA)



