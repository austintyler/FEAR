#####################################################################################
# Author: Tyler Austin
# Name: Lab09.py
# Date Written: 5/15/15
# Date Modified: 5/15/15
# Variables Used: 
# Purpose: 
#####################################################################################

# import libraries
import arcpy
import time
import numpy
from collections import Counter
import sys 
import traceback
import os

# creating custom exception class for checking validity of directory
arcpy.AddMessage('creating custom exception class for checking validity of directory\n')
class NoWorkspace (Exception):
    pass

# creating custom exception class for checking year validity
arcpy.AddMessage('creating custom exception class for checking year validity\n')
class InvalidYear (Exception):
    pass

# try catch to determine if directory is valid
arcpy.AddMessage('try catch to determine if directory is valid\n')
try:
    filePath = raw_input('Provide File Directory: ')
    # C:/Users/taust_000/Box Sync/GEOG376/Final_Project/project_data/
    if not os.path.isdir(filePath):
        raise NoWorkspace
    print 'File Directory Valid \n'
except NoWorkspace:
    print 'File Directory is Invalid!'
    arcpy.AddMessage('File Directory is Invalid!\n')
    arcpy.AddError('File Directory is Invalid!!!\n')
except:
    tb = sys.exc_info()[2]
    tbinfo = traceback.format_tb(tb)[0]
    pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nErrorInfo:\n" + str(sys.exc_info()[1])
    msgs = "ArcPy ERRORS:\n" + arcpy.GetMessages(2) + "\n"
    arcpy.AddError(pymsg + '\n')
    arcpy.AddError(msgs + '\n')
    print pymsg + "\n"
    print msgs + "\n"

# creating log file that will be found in given directory
logfile = filePath + 'log.txt'
log1 = open(logfile, 'a')
    
# try catch to check if year is valid
try:
    yearRequested = int(raw_input('Provide a year between 2001 and 2010: '))
    if yearRequested > 2010 or yearRequested < 2001:
        raise InvalidYear
    print >> log1, 'Valid Year \n'
    arcpy.AddMessage('Valid Year\n')
except InvalidYear:
    print >> log1, 'Invalid Year!!!'
    arcpy.AddMessage('Invalid Year!!!\n')
    arcpy.AddError('Invalid Year!!!\n')
except:
    tb = sys.exc_info()[2]
    tbinfo = traceback.format_tb(tb)[0]
    pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nErrorInfo:\n" + str(sys.exc_info()[1])
    msgs = "ArcPy ERRORS:\n" + arcpy.GetMessages(2) + "\n"
    arcpy.AddError(pymsg + '\n')
    arcpy.AddError(msgs + '\n')
    print >> log1, pymsg + "\n"
    print >> log1, msgs + "\n"

# variable for fire point shapefile
inFires = filePath + str(yearRequested) + '_af.shp'

# variable for perimeters polygon shapefile
inBurnScars = filePath + str(yearRequested) + 'perimeters.shp'

# variable for ecosystem polygon shapefile
ecoSHP = filePath + 'wwf_terr_ecos.shp'

# variable for first date of fire season
firstDate = None

# variable for last date of fire season
lastDate = None

# variable for year of fire season
year = None

# variable for peak date of fire season
peakDate = None

# variable for number of burn scars in fire season
numBurnScars = None

# variable for total area burned in fire season
areaBurned = None

# variable for a list of the five largest burn scars of the fire season
fiveLargestScars = None

# variable for a list of tuples of affected ecosystems and respective area burned
scarAreaPerEcosystem = None

def setCommonProjections():
    """
    This method sets the projection of the Ecosystems shapefile so that it can be used for spatial analysis.
    """
    # projecting the ecosystem polygon shapefile to NAD_1983_Alaska_Albers
    arcpy.AddMessage('projecting the ecosystem polygon shapefile to NAD_1983_Alaska_Albers\n')
    arcpy.Project_management(ecoSHP, ecoSHP[:-4] + '_projected.shp', "PROJCS['NAD_1983_Alaska_Albers',GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Albers'],PARAMETER['False_Easting',0.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',-154.0],PARAMETER['Standard_Parallel_1',55.0],PARAMETER['Standard_Parallel_2',65.0],PARAMETER['Latitude_Of_Origin',50.0],UNIT['Meter',1.0]]", "WGS_1984_(ITRF00)_To_NAD_1983", "GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]")
    # setting global varibal for ecosystem shapefile to projected shapefile
    arcpy.AddMessage('setting global varibal for ecosystem shapefile to projected shapefile\n')
    global ecoSHP
    ecoSHP = ecoSHP[:-4] + '_projected.shp'
    
def getDates(shp):
    """
    This method takes in the paramter of a fires point shapefile and uses the feild YYYYMMDD to sort
    the features by thier date. It uses the first four characters to assign the year, assigns the first
    date by using the feature at the top of the list and assigns the last date by taking the last feature
    of the sorted list. It then finds the mode of the dates to assign the peak date (if there is one) or
    it will use the first date as the peak.
    """
    # search field YYYYMMDD
    arcpy.AddMessage('search field YYYYMMDD\n')
    field = 'YYYYMMDD'
    # sorting dates in assending order
    arcpy.AddMessage('sorting dates in assending order\n')
    assending = sorted(arcpy.da.SearchCursor(shp, field))
    # setting global variable year
    arcpy.AddMessage('setting global variable year\n')
    global year
    year = str(assending[0][0])[:4]
    # setting global variable of first date
    arcpy.AddMessage('setting global variable of first date\n')
    global firstDate 
    firstDate = int(assending[0][0])
    # setting gloabl variable of last date
    arcpy.AddMessage('setting gloabl variable of last date\n')
    global lastDate
    lastDate = int(assending[-1][0])
    # setting gloabl variable peak date
    arcpy.AddMessage('setting gloabl variable peak date\n')
    global peakDate
    # creates dictionary of objects in parameter lst as key and count of objects in list as value
    modeList = Counter(assending)
    # assign peakDate (most events in one day)
    peakDate = int(modeList.most_common(1)[0][0][0])  

def getNumEvents(shp):
    """
    This method takes the parameter of a burn scar perimeters polygon shapefile. It then dissolves the shapefile
    by the Fire_ID file so that each fire that make consist of seperate polygons can be combined to find the
    actual total number of events. It also sums the size of the combined polygons so that the area of a single 
    fire event is one feature to be used later.
    """
    # creating local variable for dissolved burn scar dissolved shapefile
    arcpy.AddMessage('creating local variable for dissolved burn scar dissolved shapefile\n')
    outSHP = inBurnScars[:-4] + '_dissolved.shp'
    # dissolving perimeters by Fire_ID
    arcpy.AddMessage('dissolving perimeters by Fire_ID\n')
    arcpy.Dissolve_management(shp, outSHP, "Fire_ID", "Area SUM;Fire_Name FIRST")
    # creating a temporary dBase to store burn scar dissolved shapefile attributes for quick access
    arcpy.AddMessage('creating a temporary dBase to store burn scar dissolved shapefile attributes for quick acces\n')
    tempTable = filePath + 'tempTable.dbf'
    arcpy.MakeTableView_management(outSHP, tempTable)
    # updating global variable for number of burn scars by counting amount of features in table
    arcpy.AddMessage('updating global variable for number of burn scars by counting amount of features in table\n')
    global numBurnScars
    numBurnScars = int(arcpy.GetCount_management(tempTable).getOutput(0))
    # deleting temp table
    arcpy.AddMessage('deleting temp table\n')
    arcpy.Delete_management(tempTable)
    # overwiting global variable with dissolved burn scar events for future procces
    arcpy.AddMessage('overwiting global variable with dissolved burn scar events for future procces\n')
    global inBurnScars
    inBurnScars = outSHP
    
def getHectares(shp):
    """
    This method takes in the new dissolved shapefile of burn scar polygons and converts the area
    into Hectares from Square Meters.
    """
    # converting parameter area in to hectares
    arcpy.AddMessage('converting parameter area in to hectares\n')
    arcpy.CalculateField_management(shp, 'SUM_Area', '!shape.area@hectares!', 'PYTHON')
    # creating a NumPy array of areas for each feature
    arcpy.AddMessage('creating a NumPy array of areas for each feature\n')
    col = arcpy.da.TableToNumPyArray(shp, 'SUM_Area', skip_nulls=True)
    # updating global variable of total area burn in fire season
    arcpy.AddMessage('updating global variable of total area burn in fire season\n')
    global areaBurned
    # uses sum of all features areas and then rounds to 3 decimal places
    areaBurned = round(col['SUM_Area'].sum(), 3)
    
def getFiveLargestEvents(shp):
    """
    This method takes in the dissolved burn scar polygon shapefile in order to find the 5 largest burn 
    scars by area. Else if less than five burn scars are present then the user will be notified and it will
    list all scars present. This is achieved by sorting the features in a list by desending order of thier 
    area and assigning the first 5 (or less) features to a list.
    """
    # checking to see if there is less than 5 burn scars in fire season
    arcpy.AddMessage('checking to see if there is less than 5 burn scars in fire season\n')
    if numBurnScars < 5:
        # letting user know how many burn scars are present if less than 5
        arcpy.AddMessage('Only ' + str(numBurnScars) + ' fire event(s) in year.\n')
    # fields to sort SUM_Area, FIRST_Fire
    arcpy.AddMessage('fields to sort SUM_Area, FIRST_Fire\n')
    field = ['SUM_Area', 'FIRST_Fire']
    # sorting dates in dessending order to get largest
    arcpy.AddMessage('sorting dates in dessending order to get largest\n')
    dessending = sorted(arcpy.da.SearchCursor(shp, field), reverse=True)
    # creating empty list for 5 largest fires
    arcpy.AddMessage('creating empty list for 5 largest fires\n')
    largest = []
    # looping thru 5 largest fires and appending to list
    arcpy.AddMessage('looping thru 5 largest fires and appending to list\n')
    for event in dessending[:5]:
        largest.append(event[1])
    # updating gloabl variable of the five largest burn scars in fire season
    arcpy.AddMessage('updating gloabl variable of the five largest burn scars in fire season\n')
    global fiveLargestScars
    fiveLargestScars = largest

def getScarAreaPerEcosystem(shp):
    """
    This method takes the parameter of the dissolved burn scar polygon shapefile and determines the area of burn
    scars in each ecosystem. First an intersect analysis is performed on the parameter and the ecosystem polygon
    shapefile. All fields are joined in this operation. Next the intersected burn scar shapefile is then dissolved 
    by the ecosystem name field (ECO_NAME) and the total area for each feature is summed to create a total burn scar
    area for each ecosystem. A list is made of tuples consisting of the ecosystem as the zero index and  the total
    area burned as the first index. The list is created alphabetically by ecosystems.
    """
    # creating local variable for intersect output
    arcpy.AddMessage('creating local variable for intersect output\n')
    intersectedFires = filePath + 'intersectedFires.shp'
    # intersecting input variable with ecosystem shapefile and joining all fields
    arcpy.AddMessage('intersecting input variable with ecosystem shapefile and joining all fields\n')
    arcpy.Intersect_analysis([shp, ecoSHP], intersectedFires, "ALL", "", "INPUT")
    # creating local variable for dissolving intersected output
    arcpy.AddMessage('creating local variable for dissolving intersected output\n')
    intersectedFiresDissolved = filePath + 'intersectedFires_dissolved.shp'
    # dissolving intersected output by ecosystem name (ECO_NAME)
    arcpy.AddMessage('dissolving intersected output by ecosystem name (ECO_NAME)\n')
    arcpy.Dissolve_management(intersectedFires, intersectedFiresDissolved, "ECO_NAME", "SUM_Area SUM", "MULTI_PART", "DISSOLVE_LINES")
    # making feature layer of intersected dissolved shapefile
    arcpy.AddMessage('making feature layer of intersected dissolved shapefile\n')
    arcpy.MakeFeatureLayer_management(intersectedFiresDissolved, "intersectedFiresDissolved")
    # adding area attributes of feature layer in hectares
    arcpy.AddMessage('adding area attributes of feature layer in hectares\n')
    arcpy.AddGeometryAttributes_management('intersectedFiresDissolved', "AREA", "", "HECTARES", "")
    # fields for sorting ECO_NAME, POLY_AREA
    arcpy.AddMessage('fields for sorting ECO_NAME, POLY_AREA\n')
    field = ['ECO_NAME', 'POLY_AREA']
    # sorting ecosystems in alphabetical order
    arcpy.AddMessage('sorting ecosystems in alphabetical order\n')
    assending = sorted(arcpy.da.SearchCursor("intersectedFiresDissolved", field))
    # creating empty list for tuples of consisting of ecosystems and total area burn in ecosystem
    arcpy.AddMessage('creating empty list for tuples of consisting of ecosystems and total area burn in ecosystem\n')
    ecosystems = []
    # creating said tuples from sorted cursor
    arcpy.AddMessage('creating said tuples from sorted cursor\n')
    for event in assending:
        ecosystems.append(event)
    # updating global variable for total burn scar area per ecosystem in fire season
    arcpy.AddMessage('updating global variable for total burn scar area per ecosystem in fire season\n')
    global scarAreaPerEcosystem
    # deleting temporary processing files
    arcpy.AddMessage('deleting temporary processing files\n')
    scarAreaPerEcosystem = ecosystems
    arcpy.Delete_management(intersectedFires)
    arcpy.Delete_management(intersectedFiresDissolved)
    arcpy.Delete_management("intersectedFiresDissolved")

# executing above functions
print >> log1, 'Setting Common Projections \n'
arcpy.AddMessage('Setting Common Projections \n')
setCommonProjections()
print >> log1, 'Projections Achieved \n'
arcpy.AddMessage('Projections Achieved \n')
print >> log1, 'Getting dates of importance to fire season \n'
arcpy.AddMessage('Getting dates of importance to fire season \n')
getDates(inFires)
print >> log1, 'Fire Season Year: ' + str(year) + ' \n'
arcpy.AddMessage('Fire Season Year: ' + str(year) + ' \n')
print >> log1, 'Beginning Date of Fire Season: ' + str(firstDate) + ' \n'
arcpy.AddMessage('Beginning Date of Fire Season: ' + str(firstDate) + ' \n')
print >> log1, 'Ending Date of Fire Season: ' + str(lastDate) + ' \n'
arcpy.AddMessage('Ending Date of Fire Season: ' + str(lastDate) + ' \n')
print >> log1, 'Peak Date of Fire Season: ' + str(peakDate) + ' \n'
arcpy.AddMessage('Peak Date of Fire Season: ' + str(peakDate) + ' \n')
print >> log1, 'Calculating number of burn scars for ' + str(year) + ' \n'
arcpy.AddMessage('Calculating number of burn scars for ' + str(year) + ' \n')
getNumEvents(inBurnScars)
print >> log1, 'Total Number of Burn Scars during Fire Season: ' + str(numBurnScars) + ' \n'
arcpy.AddMessage('Total Number of Burn Scars during Fire Season: ' + str(numBurnScars) + ' \n')
print >> log1, 'Calculating total area of burn scars in ' + str(year) + ' \n'
arcpy.AddMessage('Calculating total area of burn scars in ' + str(year) + ' \n')
getHectares(inBurnScars)
print >> log1, 'Total Area Burned during Fire Season: ' + str(areaBurned) + ' \n'
arcpy.AddMessage('Total Area Burned during Fire Season: ' + str(areaBurned) + ' \n')
print >> log1, 'Finding the largest 5 events in ' + str(year) + ' \n'
arcpy.AddMessage('Finding the largest 5 events in ' + str(year) + '\n')
getFiveLargestEvents(inBurnScars)
arcpy.AddMessage('Largest 5 events in ' + str(year) + ':')
print >> log1, fiveLargestScars
arcpy.AddMessage(fiveLargestScars)
arcpy.AddMessage('\n')
print >> log1, 'Finding total area burned per ecosystem in ' + str(year) + ' \n'
arcpy.AddMessage('Finding total area burned per ecosystem in ' + str(year) + ' \n')
getScarAreaPerEcosystem(inBurnScars)
arcpy.AddMessage('Total area burned per ecosystem in ' + str(year) + ':')
print >> log1, scarAreaPerEcosystem
arcpy.AddMessage(scarAreaPerEcosystem)
arcpy.AddMessage('\n')
# deleting dissolved burn scars file used for processing
arcpy.AddMessage('deleting dissolved burn scars file used for processing\n')
arcpy.Delete_management(inBurnScars)

# writing report text file
arcpy.AddMessage('writing report text file\n')
out_file = open(filePath + str(yearRequested) + '_report.txt', 'w')
out_file.write('Fire Season Year: ' + str(year) + '\n')
out_file.write('Beginning Date of Fire Season: ' + str(firstDate) + '\n')
out_file.write('Ending Date of Fire Season: ' + str(lastDate) + '\n')
out_file.write('Peak Date of Fire Season: ' + str(peakDate) + '\n')
out_file.write('Total Number of Burn Scars during Fire Season: ' + str(numBurnScars) + '\n')
out_file.write('Total Area Burned during Fire Season: ' + str(areaBurned) + '\n')
out_file.write('Five Largest Burn Scars: \n')
index = 1
for scar in fiveLargestScars:
    out_file.write('\t' + str(index) + '. ' + scar + '\n')
    index += 1
out_file.write('Total Area Burned in Affected Ecosystems: \n')
for ecosystem in scarAreaPerEcosystem:
    out_file.write('\t' + ecosystem[0] + ': ' + str(round(ecosystem[1], 3)) + ' hectares \n')  
out_file.close()

print >> log1, 'Execution Complete!'
arcpy.AddMessage('Execution Complete!\n')
log1.close()
