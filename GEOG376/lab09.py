#####################################################################################
# Author: Tyler Austin
# Name: Lab09.py
# Date Written: 5/1/15
# Date Modified: 5/1/15
# Variables Used: sourcePath, filePath, inSHP, inDBF, inJulianStart, inYearStart,
#                 inJulianEnd, inYearEnd, startDay, endDay, totalDays, tempQuery,
#                 joinTable, result, count, outSHP, shpJoinField, dbfJoinField, 
#                 fieldList
# Purpose: practice incorporating your custom code into the user friendly ArcGIS
#          toolbox format and using IDW analysis.
#####################################################################################

# Importing the ArcPy library
import arcpy
from arcpy.sa import *
from arcpy import env

# Set workspace
#sourcePath = 'R:/376/Spring15/Lab09/lab09_data/'
sourcePath = 'C:/GEOG376/lab09_data_source/'
# filePath = 'S:/376/Spring15/tea/lab09_data/'
filePath = 'C:/GEOG376/lab09_data/'
env.workspace = filePath

# boolean for valid inputs
validInputs = True

#input shapefile
#inSHP = raw_input("Input Shapefile: ")
inSHP = arcpy.GetParameterAsText(0)

#input dBase table
#inDBF = raw_input("Input DBF: ")
inDBF = arcpy.GetParameterAsText(1)

# input start year
#inYearStart = raw_input("Beginning Year: ")
inYearStart = int(arcpy.GetParameterAsText(2))

# input julian start date
#inJulianStart =  raw_input("Beginning Julian Day: ")
inJulianStart = int(arcpy.GetParameterAsText(3))

# input end year
#inYearEnd = raw_input("Ending Year: ")
inYearEnd = int(arcpy.GetParameterAsText(4))

# input end julian date
#inJulianEnd = raw_input("Ending Julian Day: ")
inJulianEnd = int(arcpy.GetParameterAsText(5))

# ensures start year is valid
if inYearStart < 2001 or inYearStart > 2010:
    validInputs = False
    arcpy.AddMessage('invalid start year, enter value between 2001 and 2010 inclusively')
    
# ensures end year is valid
if inYearEnd < 2001 or inYearEnd > 2010:
    validInputs = False
    arcpy.AddMessage('invalid end year, enter value between 2001 and 2010 inclusively')

# ensures start julian day is valid:
if inYearStart % 4 == 0 and (inJulianStart > 366 or inJulianStart < 1):
    validInputs = False
    arcpy.AddMessage('invalid start julian day')
elif inYearStart % 4 != 0 and (inJulianStart > 365 or inJulianStart < 1):
    validInputs = False
    arcpy.AddMessage('invalid start julian day')
    
# ensures end julian day is valid:
if inYearEnd % 4 == 0 and (inJulianEnd > 366 or inJulianEnd < 1):
    validInputs = False
    arcpy.AddMessage('invalid end julian day')
elif inYearEnd % 4 != 0 and (inJulianEnd > 365 or inJulianEnd < 1):
    validInputs = False
    arcpy.AddMessage('invalid end julian day')

# ensures start julian day is 3 digits
if len(str(inJulianStart)) == 1:
    inJulianStart = '00' + str(inJulianStart)
elif len(str(inJulianStart)) == 2:
    inJulianStart = '0' + str(inJulianStart)

# ensures end julian day is 3 digits
if len(str(inJulianEnd)) == 1:
    inJulianEnd = '00' + str(inJulianEnd)
elif len(str(inJulianStart)) == 2:
    inJulianEnd = '0' + str(inJulianEnd)

# continues processes if input values are valid
if validInputs:
    # concatonates start date
    startDay = int(str(inYearStart) + str(inJulianStart))
    
    # concatonates end date
    endDay = int(str(inYearEnd) + str(inJulianEnd))
    
    # Make a layer from the DBF
    arcpy.Copy_management(inDBF, filePath + "temp.dbf") 
    arcpy.AddMessage('Created copy of input DBF')
    
    # create new field for concatonating year and julian
    arcpy.AddField_management(filePath + "temp.dbf", "YR_JD", "LONG")
    arcpy.AddMessage('Added field YR_JD to concatonate year and julian day')
    
    # calculate field concatonate year and julian day YYYYDDD
    arcpy.CalculateField_management(filePath + "temp.dbf", "YR_JD", 'int("%d%d" % (!YEAR!, !JD!))', "PYTHON_9.3")
    arcpy.AddMessage('Calculating Field for YR_JD')
    
    # start loop for join weather data to shapefile
    while startDay <= endDay:
        
        # SQL query to find rows in table based on date
        tempQuery = '"{0}" = {1}'.format('YR_JD', startDay)
        
        # variable for table used to join data
        joinTable = filePath + "queryDBF.dbf"
        
        # Select all rows date range and write to joinTable
        arcpy.TableSelect_analysis(filePath + "temp.dbf", joinTable, tempQuery)     
        
        # counts how many rows were copied to joinTable
        result = arcpy.GetCount_management(joinTable)
        count = int(result.getOutput(0))
        
        arcpy.AddMessage('There are ' + str(count) + ' records for ' + str(startDay))
        
        # only continues join if data exists to be joined
        if count > 0:
            # new shapefile name
            outSHP = inSHP[2:-5] + str(startDay) + '.shp'    
            
            # copy input shapefile
            arcpy.CopyFeatures_management(inSHP, outSHP)
            arcpy.AddMessage('Created shapefile ' + outSHP)
            
            # Set the local parameters for join
            shpJoinField = "ST_ID"
            dbfJoinField = "STA"
            fieldList = ["TC", "RH", "WSms", "PR"]
            
            # Join feature class and table by stations
            arcpy.JoinField_management (outSHP, shpJoinField, joinTable, dbfJoinField, fieldList)  
            arcpy.AddMessage('Joining fields TC, RH, WSms, and PR from from input database to output shapefile')
            
            # loop over each field for IDW analysis
            for field in fieldList:
                # Set local variables for IDW
                zField = field
                cellSize = 0.02864
                power = 2
                
                # Execute IDW
                outIDW = Idw(outSHP, zField, cellSize, power)
                arcpy.AddMessage('Performing IDW analysis for ' + outSHP + ' using ' + field + ' as magnitude value for each point.')
                
                # Save the output 
                outIDW.save(outSHP[-9:-4] + 'idw' + field) 
                arcpy.AddMessage('Output saved as ' + outSHP[-9:-4] + 'idw' + field)
        
        # deleted joinTable
        arcpy.Delete_management(joinTable)
        
        # incremente day
        yr = int(str(startDay)[:4])
        jDay = int(str(startDay)[4:])
        
        # if leap year
        if yr % 4 == 0:
            # if julian day is at max for year (366)
            if jDay == 366:
                # start next year
                startDay += 635
            # days remain in year
            else:
                # increment to next day
                startDay += 1
        # if not a leap year
        else:
            # if julian day is at max for year (365)
            if jDay == 365:
                # start next year
                startDay += 636
            # days remain in year
            else:
                # increment to next day
                startDay += 1
    
    
    # delete temporary dBase file
    arcpy.Delete_management(filePath + "temp.dbf")
    # The End
    arcpy.AddMessage('Processing Complete!')
    
# if input parameters are invalid
else:
    arcpy.AddMessage('Processing Aborted Invlaid Inputs!')