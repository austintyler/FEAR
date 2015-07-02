#####################################################################################
# Author: Tyler Austin
# Name: Lab08b.py
# Date Written: 4/24/15
# Date Modified: 4/24/15
# Variables Used: filePath, locations, header, out_file, contents, temp
# Purpose: Join all data in from the different files created in lab08a.py into one 
#          file and replace missing data with -999
#####################################################################################


filePath = 'C:/Users/taust_000/Box Sync/GEOG376/Lab08/lab08_data/'
# filePath = 'S:/376/Spring15/tea/lab08_data/'

# list of airports used for weather collection
locations = ['KFDK', 'KBWI', 'KGAI', 'KCGS', 'KIAD']

# variable used for header of finished document
header = 'Date,THighF,TAvgF,TLowF,DPHighF,DPAvgF,DPLowF,RHHigh,RHAvg,RHLow,PMaxIn,PAvgIn,PMinIn,VMaxMi,VAvgMi,VMinMi,WSMaxMPH,WSAvgMPH,GSMaxMPH,PrSumIn,CloudCover,Events,WindDirDeg,lat,lon\n'

# creates an output file called janToMar2001.txt
out_file = open(filePath + 'janToMar2001.txt', 'w')

# writes the header to the file
out_file.write(header)

# for loop for months of Jan, Feb, Mar which are 1, 2, 3 respectively
for month in range(1,4):
    # for loop to iterate over locations in list
    for location in locations:
        # opens input file for each location's month's data 
        with open(filePath + location + str(month) + '_latlon.txt', 'r') as in_file:
            # loop iterates over each line in input file
            for line in in_file:
                # splits the contents of the line that are seperated by commas into string objects in a list
                contents = line.split(',')
                # loop creates index and iterates over the string objects in the list
                for i, content in enumerate(contents):
                    # if the string object is empty
                    if content == '':
                        # replace string object with -999
                        contents[i] = '-999'
                # joins all string objects in list in to a single string
                temp = ','.join(contents)
                # writes string to output file
                out_file.write(temp)
# closes output file                
out_file.close()

print 'lab08b.py finished'