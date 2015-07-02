#####################################################################################
# Author: Tyler Austin
# Name: Lab02.py
# Date Written: 2/07/15
# Date Modified: 2/10/15
# Variables Used: filePath, outputPath, distanceField, sideType, endType, dissolveType,
# ignitions, features, month, i, featurePath, buffPath, firePath, firesInBuffer,
# result, numFires
# Purpose: script which helps you analyze fire ignitions as a function of human 
# accessibility reflected as proximity to major transportation routes and utility 
# lines in California during the 2007 fire season.
#####################################################################################

# Importing the ArcPy library
import arcpy
# Importing the OS library
import os

# Variable where data is stored
filePath = 'C:/Users/taust_000/Box Sync/GEOG376/Lab02/lab02_data/'
# Made the current directory where the data is stored
os.chdir(filePath)
# Created a directory for the output data
os.makedirs('results')
# Variable for output data
outputPath = filePath + 'results/'

# Variable for size of buffer
distanceField = "1000 METERS"
# Variable for the sideType of buffer
sideType = "FULL"
# Variable for end type of buffer
endType = "ROUND"
# Variable for the dissolve type of buffer
dissolveType = "ALL"  

# Created a list of month's numerical value to enumerate throught data
ignitions = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
# Created a list of feature types to enumerate through
features = ['roads', 'railroad', 'utilities', 'urban']
# Created a list of Month's to enumerate through in the print statement
month = ['January', 'Febuary', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 
         'October', 'November', 'December']

# For loop to enumerate through each feature in feature types
for feature in features:
    # Index is used in print statement
    i = 0 
    # Assigns the filepath of each feature to a local variable 
    featurePath = filePath + feature + '.shp'
    # Assigns the filepath for the output buffer to a local variable
    buffPath = outputPath + feature + "Buffer" + '.shp'
    # Buffers each feature 1km and saves the buffer in the output location
    arcpy.Buffer_analysis(featurePath, buffPath, distanceField, sideType, endType, dissolveType)
    # For loop to enumerate through each months ignition data
    for fire in ignitions: 
        # Assigns the filepath of each months ignition data to a local variable
        firePath = filePath + '2007_' + fire + 'ignitions.shp'
        # Assigns the filepath of the output clip data to a local variable
        firesInBuffer = outputPath + '2007_' + fire + 'ignitionsIn_' + feature + 'Buffer' + '.shp'
        # Clips each month's ignitions with in the 1 km buffer of each feature and saves it in the output folder
        arcpy.Clip_analysis(firePath, buffPath, firesInBuffer)
        # Assigns the output clip file to a local variable
        result = arcpy.GetCount_management(firesInBuffer)
        # Assigns the count of the output clip file's total ignitions to a local variable
        numFires = result.getOutput(0)
        # Prints the month, count of ingitions within 1 km of buffer of each feature
        print month[i] + ': ' + numFires + ' fire ignitions in the 1 km buffer of ' + feature
        # Increments the month index by one
        i += 1