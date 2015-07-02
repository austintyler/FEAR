#####################################################################################
# Author: Tyler Austin
# Name: Lab08a.py
# Date Written: 4/24/15
# Date Modified: 4/24/15
# Variables Used: filePath, locations, url, openUrl, output, temp, latLonUrl, 
#                 latLonFile, lines, lat, lon, line, next_line 
# Purpose: Scape historical weather data from weather underground and latitudes and
#          longitutes and create a output file for each locations for each month
#####################################################################################

# import urllib and regex library
import urllib, re

filePath = 'C:/Users/taust_000/Box Sync/GEOG376/Lab08/lab08_data/'
# filePath = 'S:/376/Spring15/tea/lab08_data/'

# list of airports used for weather collection
locations = ['KFDK', 'KBWI', 'KGAI', 'KCGS', 'KIAD']

# weather underground url for pulling historic data. {0} is for airport and {1} is for month
url = 'http://www.wunderground.com/history/airport/{0}/2011/{1}/1/MonthlyHistory.html?req_city=&req_state=&_reqdb.zip=&reqdb.magic=&reqdb.wmo=99999&format=1'

# for loop for months of Jan, Feb, Mar which are 1, 2, 3 respectively
for month in range(1,4):
    # for loop to iterate over locations in list
    for location in locations: 
        # opens url with location and month formatted in
        openUrl = urllib.urlopen(url.format(location, month))
        # creates file for output data
        output = open(filePath + location + str(month) + '.txt','wb')
        # for loop to iterate over each line on website
        for line in openUrl.readlines():
            # if statement to only pull data and not header
            if '2011' in line:
                # strips html markup from line
                temp = re.sub('<[^<]+?>', '', line)
                # writes line to output file
                output.write(temp)
        # closes output file
        output.close()
        # closes website html file
        openUrl.close()
    
# for loop for months of Jan, Feb, Mar which are 1, 2, 3 respectively
for month in range(1,4):
    # for loop to iterate over locations in list
    for location in locations:
        
        # url to html file where each weather stations lat and lon are stored
        latLonUrl = 'http://www.wunderground.com/cgi-bin/findweather/getForecast?query='
        # open url for each location
        latLonFile = urllib.urlopen(latLonUrl+ location)
        # reads the file and puts each line in to a string and into a list
        lines = latLonFile.read().splitlines()
        
        # default lat value
        lat = 0
        # default lon value
        lon = 0
        # creates an idex that iterates thru the length of the lines list
        for i in range(len(lines)):
            # if statement that prevents loop from going out of bounds
            if i + 1 < len(lines):
                # variable for current line
                line = lines[i]
                # variable for the line after the current line
                next_line = lines[i + 1]
                # if line contains the words station.latitude
                if 'station.latitude' in line: 
                    # updates lat value for location by splicing
                    lat = (next_line[(next_line.find('wx-value') + 10):(next_line.find('wx-value') + 15)])
                # if line contains the words station.longitute
                if 'station.longitude' in line: 
                    # updates lon value for location by splicing
                    lon = ('-' + next_line[(next_line.find('wx-value') + 10):(next_line.find('wx-value') + 15)])
        # creates an output file        
        with open(filePath + location + str(month) + '_latlon.txt', 'w') as out_file:
            # opens location's month's text file with data that is comma seperated as the in_file
            with open(filePath + location + str(month) + '.txt', 'r') as in_file:
                # loop to iterate over each line in the in_file 
                for line in in_file:
                    # appends lat and lon to each line
                    out_file.write(line.rstrip('\n') + ',' + lat + ',' + lon + '\n')

print 'lab08a.py finished'