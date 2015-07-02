#####################################################################################
# Author: Tyler Austin
# Name: Lab03.py
# Date Written: 2/20/15
# Date Modified: 2/20/15
# Variables Used: filePath, sourcePath, tansform_method, perimeters, taiga, tundra, 
# fires, firesInTundra, firesInTaiga, numFiresInTundra, numFiresInTaiga, numFiresAK,
# numScarsAK, scarsInTaiga, numScarsTaiga, firesPerScarTaiga, scarsInTundra, 
# numScarsTundra, firesPerScarTundra
# Purpose: Bring datasets into a common projection so that analysis can answer
# questions pertaining to the relationship of fires and burn scars in Alaska
# specifically in areas comprised completely of tundra or taiga.
#####################################################################################

# Importing the ArcPy library
import arcpy

# Variable where data is stored
filePath = 'S:/376/Spring15/tea/lab03_data/'
# Variable where data is copied from
sourcePath = 'R:/376/Spring15/Lab03/lab03_data/'
# Variable for tansformation method used in Project_management
transform_method = 'WGS_1984_(ITRF00)_To_NAD_1983'

# Variables for paths to data
perimeters = filePath + '2004perimeters'
taiga = filePath + 'AK_taiga'
tundra = filePath + 'AK_tundra'
fires = filePath + '2004_af.shp'

# Copies data from source to student folder
arcpy.CopyFeatures_management(sourcePath + '2004_af.shp', filePath + '2004_af.shp')
arcpy.CopyFeatures_management(sourcePath + '2004perimeters.shp', filePath + '2004perimeters.shp')
arcpy.CopyFeatures_management(sourcePath + 'AK_taiga.shp', filePath + 'AK_taiga.shp')
arcpy.CopyFeatures_management(sourcePath + 'AK_tundra.shp', filePath + 'AK_tundra.shp')

# if dataset is missing a projection file then the projection is defined using the spatial
# reference object of the properly projected fires data. Else convert current GCS (Lat/Long)
# projection 
if arcpy.Describe(perimeters + '.shp').spatialReference.name == 'Unknown':
    arcpy.DefineProjection_management(perimeters + '.shp', fires)
else:
    arcpy.Project_management(perimeters + '.shp', perimeters + '_projected.shp', fires, transform_method)

if arcpy.Describe(taiga + '.shp').spatialReference.name == 'Unknown':
    arcpy.DefineProjection_management(taiga + '.shp', fires)
else:
    arcpy.Project_management(taiga + '.shp', taiga + '_projected.shp', fires, transform_method)
    
if arcpy.Describe(tundra + '.shp').spatialReference.name == 'Unknown':
    arcpy.DefineProjection_management(tundra + '.shp', fires)
else:
    arcpy.Project_management(tundra + '.shp', tundra + '_projected.shp', fires, transform_method)

# How many active fires were detected in tundra?
# Clip fires in tundra
firesInTundra = filePath + 'firesInTundra.shp'
arcpy.Clip_analysis(fires, tundra + '_projected.shp', firesInTundra)
# Get Count
numFiresTundra = arcpy.GetCount_management(firesInTundra).getOutput(0)
print str(numFiresTundra) + ' active fires were detected in tundra during the summer of 2004.'

# How many active fires were detected in taiga?
# Clip fires in taiga
firesInTaiga = filePath + 'firesInTaiga.shp'
arcpy.Clip_analysis(fires, taiga + '_projected.shp', firesInTaiga)
# Get Count
numFiresTaiga = arcpy.GetCount_management(firesInTaiga).getOutput(0)
print str(numFiresTaiga) + ' active fires were detected in taiga during the summer of 2004.'

# How many active fires per burn scar were detected on average in Interior Alaska?
# All fires in Alaska Get Count
numFiresAK = arcpy.GetCount_management(fires).getOutput(0)
# All burn scars in Alaska Get Count
numScarsAk = arcpy.GetCount_management(perimeters + '.shp').getOutput(0)
# Divide by all burn scar perimeters
firesPerScarAK = float(numFiresAK)/float(numScarsAk)
print str(firesPerScarAK) + ' active fires per burn scar were detected in Interior Alaska during the summer of 2004.'

# How many active fires per burn scar were detected on average in tundra?
# Clip burn scars in tundra
scarsInTundra = filePath + 'scarsInTundra.shp'
arcpy.Clip_analysis(tundra + '_projected.shp', perimeters + '.shp', scarsInTundra)
# Get count of burn scars in tundra
numScarsTundra = arcpy.GetCount_management(scarsInTundra).getOutput(0)
# Divide fires by scars in tundra
firesPerScarTundra = float(numFiresTundra)/float(numScarsTundra)
print str(firesPerScarTundra) + ' active fires per burn scar were detected in tundra during the summer of 2004.'

# How many active fires per burn scar were detected on average in taiga?
# Clip burn scars in taiga
scarsInTaiga = filePath + 'scarsInTaiga.shp'
arcpy.Clip_analysis(taiga + '_projected.shp', perimeters + '.shp', scarsInTaiga)
# Get count of burn scars in taiga
numScarsTaiga = arcpy.GetCount_management(scarsInTaiga).getOutput(0)
# Divide fires by scars in taiga
firesPerScarTaiga = float(numFiresTaiga)/float(numScarsTaiga)
print str(firesPerScarTaiga) + ' active fires per burn scar were detected in taiga during the summer of 2004.'

