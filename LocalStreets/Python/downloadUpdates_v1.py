__file__ = 'downloadUpdates_v1'
__date__ = '11/12/2015'
__author__ = 'ABREZNIC'
import arcpy, zipfile, os, shutil, urllib, urllib2, json, glob
# http://blogs.esri.com/esri/arcgis/2013/10/10/quick-tips-consuming-feature-services-with-geoprocessing/

updateClass = arcpy.GetParameterAsText(0)
org = arcpy.GetParameterAsText(1)
downloadFormat = arcpy.GetParameterAsText(2)
chooseData = arcpy.GetParameterAsText(3)
output = arcpy.GetParameterAsText(4).replace("\\", os.sep)

directory = arcpy.env.scratchFolder + os.sep + updateClass + str(org)
if not os.path.exists(directory):
    os.makedirs(directory)
else:
    shutil.rmtree(directory)
    os.makedirs(directory)
arcpy.AddMessage("directory created.")
label = ""

if updateClass == "CR":
    if chooseData == "SCHEMA":
        baseURL = "https://maps.dot.state.tx.us/arcgis/rest/services/TPPuser/CountyRoads_Updates/FeatureServer/0/query"
    elif chooseData == "DATA":
        baseURL = "https://maps.dot.state.tx.us/arcgis/rest/services/TPPuser/CountyRoads/MapServer/0/query"
        where = """"COUNTY"=""" + str(org)

elif updateClass == "LS":
    if chooseData == "SCHEMA":
        baseURL = "https://maps.dot.state.tx.us/arcgis/rest/services/TPPuser/LocalStreets_Updates/FeatureServer/0/query"
    elif chooseData == "DATA":
        baseURL = "https://maps.dot.state.tx.us/arcgis/rest/services/TPPuser/LocalStreets/MapServer/0/query"
        where = "(ACRNM1='" + str(org) + "' OR ACRNM2='" + str(org) + "')"
arcpy.AddMessage("url created.")

def getObjectIDs(query):
    params = {'where': query, 'returnIdsOnly': 'true', 'token': token, 'f': 'json'}
    req = urllib2.Request(baseURL, urllib.urlencode(params))
    response = urllib2.urlopen(req)
    data = json.load(response)
    array = data["objectIds"]
    array.sort()
    arcpy.AddMessage("Object IDs Found")
    return array

def createFC(fs):
    if downloadFormat == "SHP":
        arcpy.CopyFeatures_management(fs, directory + os.sep + "TxDOT_" + label + "_" + updateClass + "_" + str(org) + ".shp")
        newFC = directory + os.sep + "TxDOT_" + label + "_" + updateClass + "_" + str(org) + ".shp"
    elif downloadFormat == "FGDB":
        arcpy.CreateFileGDB_management(directory, "TxDOT_" + updateClass + "_" + str(org))
        fgdb = directory + os.sep + "TxDOT_" + updateClass + "_" + str(org)
        arcpy.CopyFeatures_management(fs, fgdb + ".gdb" + os.sep + "TxDOT_" + label + "_" + updateClass + "_" + str(org))
        newFC = fgdb + ".gdb" + os.sep + "TxDOT_" + label + "_" + updateClass + "_" + str(org)
    arcpy.AddMessage("feature class created.")
    return newFC

def updatedQuery(low, high, trigger):
    if low != high:
        addition = """ AND "OBJECTID" >= """ + str(low) + " AND " + """"OBJECTID" < """ + str(high)
        if trigger == 1:
            addition = """ AND "OBJECTID" >= """ + str(low)
    else:
        addition = """ AND "OBJECTID" = """ + str(low)
    newQuery = where + addition
    return newQuery

fields ='*'
token = ''


if chooseData == "SCHEMA":
    label = "Updates"
    everything = "1=1"
    objectIDs = getObjectIDs(everything)
    where = """"OBJECTID" = """ + str(objectIDs[0])
    query = "?where={}&outFields={}&returnGeometry=true&f=json&token={}".format(where, fields, token)
    fsURL = baseURL + query
    fs = arcpy.FeatureSet()
    fs.load(fsURL)
    arcpy.AddMessage("select completed.")
    theFC = createFC(fs)
    cursor = arcpy.da.UpdateCursor(theFC, ["*"])
    for row in cursor:
        cursor.deleteRow()
    arcpy.AddMessage("template cleaned out.")

elif chooseData == "DATA":
    label = "Inventory"
    objectIDs = getObjectIDs(where)
    total = len(objectIDs)
    arcpy.AddMessage("Total: " + str(total))
    totalFixed = total - 1
    last = objectIDs[-1]
    low = 0
    high = 1000
    theFC = ""

    while low <= total:
        arcpy.AddMessage(low)
        min = objectIDs[low]
        try:
            max = objectIDs[high]
            trigger = 0
        except:
            max = objectIDs[totalFixed]
            trigger = 1
        OIDquery = updatedQuery(min, max, trigger)
        query = "?where={}&outFields={}&returnGeometry=true&f=json&token={}".format(OIDquery, fields, token)
        fsURL = baseURL + query
        fs = arcpy.FeatureSet()
        fs.load(fsURL)
        arcpy.AddMessage("select completed.")
        if low == 0:
            theFC = createFC(fs)
        else:
            arcpy.Append_management(fs, theFC, "NO_TEST")
        low += 1000
        high += 1000

arcpy.AddMessage("packing up...")
zipper = output
if os.path.isfile(zipper):
    os.remove(zipper)
arcpy.AddMessage("zipfile started.")
if downloadFormat == "FGDB":
    newZipper = zipper[:-4]
    shutil.make_archive(newZipper, "zip", directory)
elif downloadFormat == "SHP":
    zip = zipfile.ZipFile(zipper, 'w', zipfile.ZIP_DEFLATED)
    for filename in os.listdir(directory):
        if not filename.endswith('.lock'):
            zip.write(os.path.join(directory, filename), filename)
    zip.close()
arcpy.AddMessage("zipfile completed.")

arcpy.AddMessage("that's all folks!!")