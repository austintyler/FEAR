#####################################################################################
# Author: Tyler Austin
# Name: Lab07.py
# Date Written: 4/16/15
# Date Modified: 4/16/15
# Variables Used: sourcePath, filePath, tenDegGrid, landAreaShp, areaPerGrid, 
#                 projection, uid, landArea
# Purpose: Use cursor objects for aspects of geospatial relationship analysis to 
#          determine land percentage of the northern hemisphere in 10 x 10 degree 
#          grids
#####################################################################################

# import arcypy library
import arcpy

sourcePath = 'C:/Users/taust_000/Box Sync/GEOG376/Lab07/lab07_data_source/'
# sourcePath = 'R:/376/Spring15/Lab05/lab07_data/'

filePath = 'C:/Users/taust_000/Box Sync/GEOG376/Lab07/lab07_data/'
# filePath = 'S:/376/Spring15/tea/lab07_data/'

# variables for shapefiles
tenDegGrid = filePath + 'ten_deg_grid.shp'
landAreaShp = filePath + 'world_ten_deg_area.shp'
areaPerGrid = filePath + 'area_per_grid.shp'

# copy over world_ten_deg_area.shp and ten_deg_grid.shp
# arcpy.CopyFeatures_management(sourcePath + 'ten_deg_grid.shp', tenDegGrid)
# arcpy.CopyFeatures_management(sourcePath + 'world_ten_deg_area.shp', landArea)

# Define projection GCS_WGS_1984 to world_ten_deg_area.shp and ten_deg_grid.shp and place in working folder
projection = arcpy.SpatialReference(4326)

arcpy.Project_management(sourcePath + 'ten_deg_grid.shp', tenDegGrid, projection)
print 1
arcpy.Project_management(sourcePath + 'world_ten_deg_area.shp', landAreaShp, projection)
print 2
# Calculate Area
arcpy.CalculateAreas_stats(tenDegGrid, areaPerGrid)
print 3

# add fields 'lat, 'lon', 'land' and 'Percentage'
arcpy.AddField_management(areaPerGrid, "lat", "DOUBLE")
arcpy.AddField_management(areaPerGrid, "lon", "DOUBLE")
arcpy.AddField_management(areaPerGrid, "land", "DOUBLE")
arcpy.AddField_management(areaPerGrid, "Percentage", "DOUBLE")

# populate lat, lon, and default land and percent fields using curcsor:
with arcpy.da.UpdateCursor(areaPerGrid, ['Shape', 'lat', 'lon', 'land', 'Percentage']) as cursor:
    for row in cursor:
        row[1] = row[0][0] # lat equals Y value
        row[2] = row[0][1] # lon equals X value
        row[3] = 0 # default value for land
        row[4] = 0 # default value for Percentage
        cursor.updateRow(row) # updates row in cursor

# deleting cursors
del row
del cursor

# calculating land percentage in each grid
# opens search cursor to go through calculated land areas
with arcpy.da.SearchCursor(landAreaShp, ['UID', 'Land_fr']) as cursor1:
    for row in cursor1:
        # gets UID
        uid = row[0]
        # gets fractional value of land
        landArea = row[1]
        # opens update cursor to iterate over the ten degree grid 
        with arcpy.da.UpdateCursor(areaPerGrid, ['UID', 'land', 'Percentage', 'F_AREA']) as cursor2:
            for r in cursor2:
                # if UIDs match
                if r[0] == uid:
                    # assigns fractional value of land
                    r[1] = landArea
                    # assigns fractional value of land percentage of grid area
                    r[2] = round((landAreaShp/r[3]) * 100)
                    # updates row in update cursor
                    cursor2.updateRow(r)

# deleting cursors                
del r
del cursor2
del row
del cursor1

