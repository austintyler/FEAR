#####################################################################################
# Author: Tyler Austin
# Name: Final.py
# Date Written: 5/16/15
# Date Modified: 5/16/15
# Variables Used: again, Tdb, RH, THI, system, goAgain
# Purpose: Calculate THI using Temp and RH.
#####################################################################################

# import libraries
import os, sys, traceback

# creating custom exception class for checking 
class InvalidTemp (Exception):
    pass

# creating custom exception class for checking 
class InvalidRH (Exception):
    pass

# boolean for user to decide to continue program
again = True

# While loop to let the user continue until they are satisfied
while validTemp and validRH and again:

    # dry bulb temperature (*F)
    Tdb = float(raw_input("Provide a dry bulb temperature above 80 degrees F or 26 degrees C: "))
    
    # Fahrenheit or Celsius
    system = raw_input("Is this temperature in Fahrenheit or Celsius? Enter F or C respectively: ")
    
    # Convert if celsius (°C * 9/5 + 32 = °F)
    if (system.lower() == 'c'):
        Tdb = ((Tdb * 9) / 5.0) + 32
    
    # Check if over 80*F (error handle)
    try:
        if int(Tdb) < 80:
            raise InvalidTemp
        print 'Temperature is Valid \n'
    except InvalidTemp:
        print 'Temperature is Invalid! Must be over 80°F'
        break
    except:
        tb = sys.exc_info()[2]
        tbinfo = traceback.format_tb(tb)[0]
        pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nErrorInfo:\n" + str(sys.exc_info()[1])
        print pymsg + "\n"
    
    # relative humidity (as a Percent)
    RH = raw_input("Enter relative humidity as a percent: ")
    
    # Remove percent symbol if present
    if RH[-1] == '%':
        RH = float(RH[:-1])
    
    # divide RH by 100 if fraction to convert to decimal
    if '/' in str(RH):
        fraction = RH.split('/')
        RH = float(fraction[0])/float(fraction[1])*100
    
    # if relative humidity is less than 1
    if float(RH) < 1:
        RH = float(RH) * 100
    
    # Check if above 40% (error handle)
    try:
        if int(RH) < 40:
            raise InvalidRH
        print 'Relative Humidity is Valid \n'
    except InvalidRH:
        print 'Relative Humidity is Invalid, must be over 40%!'
        break
    except:
        tb = sys.exc_info()[2]
        tbinfo = traceback.format_tb(tb)[0]
        pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nErrorInfo:\n" + str(sys.exc_info()[1])
        print pymsg + "\n"
    
    # Temperature–humidity index
    THI = None
    
    
    # Function to calculate THI = Tdb–[0.55–(0.55*(RH/100))]*(Tdb–58)
    def getTHI(tdb, rh):
        rh = float(rh)/100
        global THI
        THI = tdb - (0.55 - (0.55 * rh)) * (tdb - 58)
    
    # Execute function
    getTHI(Tdb, RH) 

    # Round THI to integer and print
    print 'Temperature Humidity Index (THI): ' + str(int(round(THI, 0)))
    
    # Ask user if the want to go again
    goAgain = raw_input('Would you like to go again? y/n: ')
    
    # Checks user input to continue or not
    if goAgain.lower() == 'n':
        again = False
    
print 'The End.'