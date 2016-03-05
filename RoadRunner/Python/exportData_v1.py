__file__ = 'exportData_v1'
__date__ = '2/18/2016'
__author__ = 'ABREZNIC'
"""
The MIT License (MIT)

Copyright (c) 2016 Texas Department of Transportation
Author: Adam Breznicky

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""
import arcpy, zipfile, os, shutil, urllib, urllib2, json, glob, base64, datetime, csv
# http://blogs.esri.com/esri/arcgis/2013/10/10/quick-tips-consuming-feature-services-with-geoprocessing/
now = datetime.datetime.now()
curMonth = now.strftime("%m")
curDay = now.strftime("%d")
curYear = now.strftime("%Y")
today = str(curYear) + str(curMonth) + str(curDay)

theQuery = arcpy.GetParameterAsText(0)
downloadFormat = arcpy.GetParameterAsText(1)
output = arcpy.GetParameterAsText(2).replace("\\", os.sep)

boundary = theQuery.split("'")[1]

directory = arcpy.env.scratchFolder + os.sep + boundary + "_" + downloadFormat
if not os.path.exists(directory):
    os.makedirs(directory)
else:
    arcpy.AddMessage(directory)
    shutil.rmtree(directory)
    os.makedirs(directory)
arcpy.AddMessage("directory created.")

baseURL = "http://services.arcgis.com/KTcxiTD9dsQw4r7Z/arcgis/rest/services/MaintenanceDeficiencies/FeatureServer/0/query"
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
    arcpy.CreateFileGDB_management(directory, boundary + "_" + downloadFormat + "_" + "DB")
    fgdb = directory + os.sep + boundary + "_" + downloadFormat + "_" + "DB"
    arcpy.CopyFeatures_management(fs, fgdb + ".gdb" + os.sep + boundary + "_" + downloadFormat + "_" + "FC")
    newFC = fgdb + ".gdb" + os.sep + boundary + "_" + downloadFormat + "_" + "FC"
    arcpy.AddMessage("feature class created.")
    return newFC

def generateToken():
    arcpy.AddMessage('\nGenerating Token\n')
    username = "Adam.Breznicky_TXDOT"
    password = base64.b64decode("VHVlc2RheTEyMw==")
    tokenURL = 'https://www.arcgis.com/sharing/rest/generateToken'
    params = {'f': 'pjson', 'username': username, 'password': password, 'referer': 'http://www.arcgis.com'}
    req = urllib2.Request(tokenURL, urllib.urlencode(params))
    response = urllib2.urlopen(req)
    data = json.load(response)
    tkn = data['token']
    return tkn

fields ='*'
token = generateToken()
arcpy.AddMessage("token acquired")
objectIDs = getObjectIDs(theQuery)
total = len(objectIDs)
arcpy.AddMessage("Total: " + str(total))
totalFixed = total - 1
last = objectIDs[-1]
low = 0
high = 300
theFC = ""

while low <= total:
    arcpy.AddMessage(low)
    currentOIDs = objectIDs[low:high]
    theOIDs = ""
    for id in currentOIDs:
        thisOID = str(id) + ","
        theOIDs += thisOID
    theOIDs = theOIDs[:-1]
    arcpy.AddMessage(theOIDs)
    arcpy.AddMessage(len(currentOIDs))
    query = "?objectIds={}&outFields={}&returnGeometry=true&f=json&token={}".format(theOIDs, fields, token)
    fsURL = baseURL + query
    fs = arcpy.FeatureSet()
    fs.load(fsURL)
    arcpy.AddMessage("select completed.")
    if low == 0:
        theFC = createFC(fs)
    else:
        arcpy.Append_management(fs, theFC, "NO_TEST")
    low += 300
    high += 300

arcpy.AddMessage("converting to " + downloadFormat)
if downloadFormat == "CSV":
    data = []
    field_names = [f.name for f in arcpy.ListFields(theFC)]
    data.append(field_names)
    cursor = arcpy.da.SearchCursor(theFC, field_names)
    for row in cursor:
        data.append(row)
    theFile = open(directory + os.sep + boundary + "_" + downloadFormat + "_" + today + ".csv", 'wb')
    writer = csv.writer(theFile)
    writer.writerows(data)
    theFile.close()
    outbound = directory + os.sep + boundary + "_" + downloadFormat + "_" + today + ".csv"
elif downloadFormat == "KML":
    arcpy.MakeFeatureLayer_management(theFC, "temp")
    arcpy.LayerToKML_conversion("temp", directory + os.sep + boundary + "_" + downloadFormat + "_" + today + ".kmz")
    outbound = directory + os.sep + boundary + "_" + downloadFormat + "_" + today + ".kmz"

arcpy.AddMessage("packing up...")
zipper = output
arcpy.AddMessage(zipper)
if os.path.isfile(zipper):
    os.remove(zipper)
arcpy.AddMessage("zipfile started.")
zip = zipfile.ZipFile(zipper, 'w', zipfile.ZIP_DEFLATED)
zip.write(outbound, os.path.basename(outbound))
zip.close()
arcpy.AddMessage("zipfile completed.")

arcpy.AddMessage("that's all folks!!")