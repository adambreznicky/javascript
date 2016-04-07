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

if updateClass == "CR":
    if chooseData == "SCHEMA":
        baseURL = "https://maps.dot.state.tx.us/arcgis/rest/services/TPPuser/CountyRoads_Updates/FeatureServer/0/query"
    elif chooseData == "DATA":
        baseURL = "https://maps.dot.state.tx.us/arcgis/rest/services/TPPuser/CountyRoads/FeatureServer/0/query"
        where = """"COUNTY"=""" + str(org)

elif updateClass == "LS":
    if chooseData == "SCHEMA":
        baseURL = "https://maps.dot.state.tx.us/arcgis/rest/services/TPPuser/LocalStreets_Updates/FeatureServer/0/query"
    elif chooseData == "DATA":
        baseURL = "http://services.arcgis.com/KTcxiTD9dsQw4r7Z/arcgis/rest/services/CountyRoads/FeatureServer/0/query"
        where = """"COUNTY"=""" + str(org)
arcpy.AddMessage("url created.")

def getObjectIDs():
    params = {'where': """"COUNTY"=""" + str(org), 'returnIdsOnly': 'true', 'token': token, 'f': 'json'}
    req = urllib2.Request(baseURL, urllib.urlencode(params))
    response = urllib2.urlopen(req)
    data = json.load(response)
    array = data["objectIds"]
    array.sort()
    arcpy.AddMessage("Object IDs Found")
    return array

def createFC(fs):
    if downloadFormat == "SHP":
        arcpy.CopyFeatures_management(fs, directory + os.sep + "TxDOT_" + updateClass + "_" + str(org) + ".shp")
        newFC = directory + os.sep + "TxDOT_" + updateClass + "_" + str(org) + ".shp"
    elif downloadFormat == "FGDB":
        arcpy.CreateFileGDB_management(directory, "TxDOT_" + updateClass + "_" + str(org))
        fgdb = directory + os.sep + "TxDOT_" + updateClass + "_" + str(org)
        arcpy.CopyFeatures_management(fs, fgdb + ".gdb" + os.sep + "TxDOT_" + updateClass + "_" + str(org))
        newFC = fgdb + ".gdb" + os.sep + "TxDOT_" + updateClass + "_" + str(org)
    arcpy.AddMessage("feature class created.")
    return newFC

def updatedQuery(low, high):
    if low != high:
        addition = """ AND "OBJECTID" >= """ + str(low) + " AND " + """"OBJECTID" < """ + str(high)
    else:
        addition = """ AND "OBJECTID" = """ + str(low)
    newQuery = where + addition
    return newQuery

fields ='*'
token = ''
objectIDs = getObjectIDs()

if chooseData == "SCHEMA":
    where = """"OBJECTID" = """ + objectIDs[0]
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
        except:
            max = objectIDs[totalFixed - 1]
        OIDquery = updatedQuery(min, max)
        query = "?where={}&outFields={}&returnGeometry=true&f=json&token={}".format(OIDquery, fields, token)
        fsURL = baseURL + query
        arcpy.AddMessage(fsURL)
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
arcpy.AddMessage(directory)
zipper = output
# if os.path.isfile(zipper):
#     os.remove(zipper)
# zip = zipfile.ZipFile(zipper, 'w', zipfile.ZIP_DEFLATED)
arcpy.AddMessage("zipfile completed.")

filename = "TxDOT_" + updateClass + "_" + str(org) + ".gdb"
# for filename in glob.glob(filename+"/*")::
#     zip.write(infile, os.path.basename(inFileGeodatabase)+"/"+os.path.basename(infile), zipfile.ZIP_DEFLATED)
# zip.close()

shutil.make_archive(zipper, "zip", directory)
# infile = filename
# outfile = zipper
# arcpy.AddMessage(filename)
# arcpy.AddMessage(zipper)
# def zipFileGeodatabase(inFileGeodatabase, newZipFN):
#    if not (os.path.exists(inFileGeodatabase)):
#       return False
#
#    if (os.path.exists(newZipFN)):
#       os.remove(newZipFN)
#
#    zipobj = zipfile.ZipFile(newZipFN,'w')
#
#    for infile in glob.glob(inFileGeodatabase+"/*"):
#       zipobj.write(infile, os.path.basename(inFileGeodatabase)+"/"+os.path.basename(infile), zipfile.ZIP_DEFLATED)
#       print ("Zipping: "+infile)
#
#    zipobj.close()
#
#    return True
#
# zipFileGeodatabase(infile,outfile)

arcpy.AddMessage("that's all folks!!")