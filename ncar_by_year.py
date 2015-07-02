#####################################################################################
# Author(s): Tyler Austin, Josh Hyde
# Name: ncar_by_year.py
# Date Written: 7/1/15
# Date Modified: 7/1/15
# Purpose: Tool to find climate variable mean by year by country
#####################################################################################

# import libraries
import arcpy
from arcpy.da import *
print "arcpy imported"

# directories
sourcePath = 'C:/Users/576643/NCAR/'
filePath = 'C:/Users/576643/NCAR/working/'
resultPath = 'C:/Users/576643/NCAR/results/'

# code variables
ccVar = filePath + 'tas_1950_1999.shp'
countries = filePath + 'countries.shp'
masterTable = filePath + 'varMeanByYear.dbf'
grid = filePath + 'ncar_polygons.shp'
varName = raw_input("Provide variable name (ex. air_temp): ")
startYr = int(raw_input("Provide Start Year (YYYY): "))
endYr = int(raw_input("Provide End Year (YYYY): ")) + 1

# copying features into working folder
arcpy.CopyFeatures_management(sourcePath + 'tas_1950_1999.shp', ccVar)
arcpy.CopyFeatures_management(sourcePath + 'countries.shp', countries)
arcpy.Copy_management(sourcePath + 'ncar_polygons.shp', grid)
print "files copied to working folder"

# creating master output table
arcpy.CreateTable_management(filePath, 'varMeanByYear.dbf')
arcpy.AddField_management(masterTable, 'FREQUENCY', 'TEXT')
arcpy.DeleteField_management(masterTable, 'Field1')
for y in range(startYr, endYr, 1):
    arcpy.AddField_management(masterTable, 'MEAN_' + str(y), 'DOUBLE')
arcpy.AddField_management(masterTable, 'sov_a3', 'TEXT')
print 'master output table created'

# joining climate variable point to grid polygons
ccVarGrid = filePath + "variables_by_grid.shp"
arcpy.SpatialJoin_analysis(grid, ccVar, ccVarGrid)
print "created variable grid"

# making feature layers of shapfiles
arcpy.MakeFeatureLayer_management(countries, "cntyLyr")
arcpy.MakeFeatureLayer_management(ccVarGrid, "ccVarLyr")
print "feature layers created"

# iterating over each country to find mean of climate variable per year
with arcpy.da.SearchCursor(countries, ["FID", "sov_a3"]) as cursor:    
    for row in cursor:  
        # select by country by attribute  
        arcpy.SelectLayerByAttribute_management("cntyLyr", "NEW_SELECTION", "FID = {}".format(row[0]))
        print row[1] + "selected"
        
        # select by grids by location    
        arcpy.SelectLayerByLocation_management("ccVarLyr", "WITHIN_A_DISTANCE", "cntyLyr", "1 CENTIMETERS", "NEW_SELECTION")
        print "grid polygons selected by location for " + row[1]
        
        # local variable for selected grids
        selCCVar = filePath + 'tempPoints.shp'
        
        # export data to shapefile
        arcpy.CopyFeatures_management("ccVarLyr", selCCVar)
        
        # summary statistics
        outTable = filePath + 'temp_table.dbf'
        yrs = []
        for yr in range(startYr, endYr, 1):
            yrs.append([str(yr) + '12', 'MEAN'])        
        arcpy.Statistics_analysis(selCCVar, outTable, yrs)
        print row[1] + "stats computed"
        
        # add field
        arcpy.AddField_management(outTable, "sov_a3", "TEXT")
        
        # populate new field
        cur = arcpy.UpdateCursor(outTable)
        for r in cur:
            r.setValue('sov_a3', row[1])
            cur.updateRow(r)        
        del cur
        
        # add to master table
        with arcpy.da.SearchCursor(outTable, "*") as statTable:
            masterCursor = arcpy.da.InsertCursor(masterTable, "*")            
            for r in statTable:        
                masterCursor.insertRow(r)  
        
        # delete search and insert cursors       
        del statTable
        del masterCursor
        
        # delete temp shapefiles
        arcpy.Delete_management(selCCVar)
        arcpy.Delete_management(outTable)
        print row[1] + " complete!"

# delete search cursor        
del cursor

# join and export country/table to shp
arcpy.JoinField_management(countries, "sov_a3", masterTable, "sov_a3")
exportShp = resultPath + "cntyByVarMean.shp"
arcpy.CopyFeatures_management(countries, exportShp)
arcpy.DeleteField_management(exportShp, 'FID_1')

# export to excel
arcpy.TableToExcel_conversion(exportShp, resultPath + varName + '_' + str(startYr) + '_' + str(endYr) + '.xls')

# Delete feature layers
arcpy.Delete_management("cntyLyr")        
arcpy.Delete_management("ccVarLyr")
arcpy.Delete_management(ccVar)
arcpy.Delete_management(countries)
arcpy.Delete_management(grid)
arcpy.Delete_management(ccVarGrid)

