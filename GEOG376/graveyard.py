

# kriging
outKrig = Kriging(selCCVar, "OZONE", KrigingModelOrdinary("CIRCULAR", 2000, 2.6, 542, 0), 2000, RadiusFixed(20000, 1))
outKrig.save("c:/sapyexamples/output/krigout")  
# extract by mask


where = "[FID] = " + str(row[0])
arcpy.SelectLayerByAttribute_management(countries, "NEW_SELECTION", where) 



result = arcpy.GetCount_management(selCCVar)
print result.getOutput(0) 

arcpy.AssignDefaultToField_management(outTable, 'sov_a3', row[1])


# import os
# import sys
# import traceback
# import time
# from collections import Counter
# import urllib
# import re