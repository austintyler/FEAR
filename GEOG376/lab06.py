#####################################################################################
# Author: Tyler Austin
# Name: Lab06.py
# Date Written: 4/10/15
# Date Modified: 4/10/15
# Variables Used: sourcePath, filePath, projection, polygonList, array, point1, 
#                 point2, point3, point4, polygon, merged, world, inFeatures, 
#                 intersectOutput, dissolveOutput, calcAreaOutput
# Purpose: Created a shapefile of 10 degree grid (lat/lon) for northern hemisphere 
#          and geospatially analyze land areas within the 10 degree grid to develop
#          skills to create and modify geometries of geospatial data.
#####################################################################################

# import arcypy library
import arcpy

sourcePath = 'C:/Users/taust_000/Box Sync/GEOG376/Lab06/lab06_data_source/'
# sourcePath = 'R:/376/Spring15/Lab05/lab06_data/'

filePath = 'C:/Users/taust_000/Box Sync/GEOG376/Lab06/lab06_data/'
# filePath = 'S:/376/Spring15/tea/lab06_data/'

# copy over world.shp
arcpy.CopyFeatures_management(sourcePath + 'world.shp', filePath + 'world.shp')

# world.shp used to define projection 
projection = arcpy.SpatialReference(filePath + 'world.prj')

# polygon list
polygonList = []

# double for loop creates grid polygons of nothern hemishpere by 10 degrees
for y in range(0, 91, 10):
    for x in range(-180, 181, 10):
        # create an empty array
        array = arcpy.Array()        
        # create an empty point variable
        point1 = arcpy.Point(x, y)
        point2 = arcpy.Point(x + 10, y)
        point3 = arcpy.Point(x + 10, y + 10)
        point4 = arcpy.Point(x, y + 10)
        # add that point to empty array
        array.add(point1)
        array.add(point2)
        array.add(point3)
        array.add(point4)
        # polygon from the array
        polygon = arcpy.Polygon(array, projection)
        polygonList.append(polygon)

# variable for merge output file   
merged = filePath + 'polygons_merged.shp'
# merge all polygons into one shapefile
arcpy.CopyFeatures_management(polygonList, merged)

# add 'UID' field
arcpy.AddField_management(merged, "UID", "LONG")
# calculate 'UID' field
arcpy.CalculateField_management(merged, "UID", '!FID! + 1', "PYTHON_9.3")

# variable for world shapefile
world = filePath + 'world.shp'

# intersect
inFeatures = [merged, world]
intersectOutput = filePath + 'area_per_gridSquare.shp'   
arcpy.Intersect_analysis(inFeatures, intersectOutput)

# dissolve
dissolveOutput = filePath + 'area_per_gridSquare_dissolved.shp'
arcpy.Dissolve_management(intersectOutput, dissolveOutput, 'UID')

# Calculate Area
calcAreaOutput = filePath + 'calculatedArea_per_gridSquare.shp'
arcpy.CalculateAreas_stats(dissolveOutput, calcAreaOutput)

# add 'Land_fr' field
arcpy.AddField_management(calcAreaOutput, "Land_fr", "DOUBLE")
# calculate 'Land_fr' field
arcpy.CalculateField_management(calcAreaOutput, "Land_fr", '!F_AREA!', "PYTHON_9.3")
# delete 'F_AREA' field
arcpy.DeleteField_management(calcAreaOutput, 'F_AREA')


# Final shapefile is called 'calculatedArea_per_gridSquare.shp'