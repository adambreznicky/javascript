__file__ = 'downloadGET_v1'
__date__ = '11/12/2015'
__author__ = 'ABREZNIC'
import arcpy, zipfile, os, shutil, urllib, urllib2, json, glob
# http://blogs.esri.com/esri/arcgis/2013/10/10/quick-tips-consuming-feature-services-with-geoprocessing/

district = arcpy.GetParameterAsText(0)
username = arcpy.GetParameterAsText(1)
password = arcpy.GetParameterAsText(2)
output = arcpy.GetParameterAsText(3).replace("\\", os.sep)

directory = arcpy.env.scratchFolder + os.sep + district + "_GET"
if not os.path.exists(directory):
    os.makedirs(directory)
else:
    shutil.rmtree(directory)
    os.makedirs(directory)
arcpy.AddMessage("directory created.")

baseURL = "http://services.arcgis.com/KTcxiTD9dsQw4r7Z/arcgis/rest/services/GET_Maintenance_AGO/FeatureServer/0/query"
arcpy.AddMessage("url created.")

if district == "Statewide":
    where = "1=1"
else:
    where = ""

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
    arcpy.CreateFileGDB_management(directory, "TxDOT_GuardrailEndTreatments")
    fgdb = directory + os.sep + "TxDOT_GuardrailEndTreatments"
    arcpy.CopyFeatures_management(fs, fgdb + ".gdb" + os.sep + "GET_" + district + "Dist")
    newFC = fgdb + ".gdb" + os.sep + "GET_" + district + "Dist"
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

try:
    arcpy.AddMessage('\nGenerating Token\n')
    server = baseURL.split("//")[1].split("/")[0]
    tokenURL = 'http://' + server + '/arcgis/tokens/?username=' + username + '&password=' + password + '&referer=http%3A%2F%2F' + server + '&f=json'
    req = urllib2.Request(tokenURL)
    response = urllib2.urlopen(req)
    data = json.load(response)
    token = data['token']
except:
    token = ''
    pass

fields ='*'


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