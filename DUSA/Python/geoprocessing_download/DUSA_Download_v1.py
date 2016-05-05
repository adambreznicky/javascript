__file__ = 'downloadUpdates_v1'
__date__ = '4/1/2015'
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
import arcpy, zipfile, os, shutil, urllib, urllib2, json, glob
# http://blogs.esri.com/esri/arcgis/2013/10/10/quick-tips-consuming-feature-services-with-geoprocessing/

updateClass = arcpy.GetParameterAsText(0)
org = arcpy.GetParameterAsText(1)
downloadFormat = arcpy.GetParameterAsText(2)
chooseData = arcpy.GetParameterAsText(3)
label = ""
the_filename = ""

directory = arcpy.env.scratchFolder + os.sep + updateClass + str(org)
if not os.path.exists(directory):
    os.makedirs(directory)
else:
    shutil.rmtree(directory)
    os.makedirs(directory)
arcpy.AddMessage("directory created.")


if updateClass == "CR":
    if chooseData == "SCHEMA":
        baseURL = "http://services.arcgis.com/KTcxiTD9dsQw4r7Z/arcgis/rest/services/CountyRoads_Updates/FeatureServer/0/query"
    elif chooseData == "DATA":
        baseURL = "http://services.arcgis.com/KTcxiTD9dsQw4r7Z/arcgis/rest/services/CountyRoads_DUSA/FeatureServer/0/query"
        where = "CNTY_NBR = '" + str(org) + "'"

elif updateClass == "LS":
    if chooseData == "SCHEMA":
        baseURL = "http://services.arcgis.com/KTcxiTD9dsQw4r7Z/arcgis/rest/services/LocalStreets_Updates/FeatureServer/0/query"
    elif chooseData == "DATA":
        baseURL = "http://services.arcgis.com/KTcxiTD9dsQw4r7Z/arcgis/rest/services/LocalStreets_DUSA/FeatureServer/0/query"
        if org != "CSEC":
            where = "(ADMN_ACRNM='" + str(org) + "' OR DIST_ACRNM='" + str(org) + "' OR COG_ACRNM='" + str(org) + "')"
        else:
            where = "ADMN_ACRNM <> 'MDA911'"
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
        arcpy.CopyFeatures_management(fs, directory + os.sep + the_filename + ".shp")
        newFC = directory + os.sep + the_filename + ".shp"
    elif downloadFormat == "FGDB":
        arcpy.CreateFileGDB_management(directory, "TxDOT_" + updateClass + "_" + str(org))
        fgdb = directory + os.sep + "TxDOT_" + updateClass + "_" + str(org)
        arcpy.CopyFeatures_management(fs, fgdb + ".gdb" + os.sep + the_filename)
        newFC = fgdb + ".gdb" + os.sep + the_filename
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


def download_file(download_url):
    urllib.urlretrieve(download_url, directory + os.sep + "DataDictionary.pdf")
    # response = urllib2.urlopen(download_url)
    # file = open(directory + os.sep + "DataDictionary.pdf", 'wb+')
    # file.write(response.read())
    # file.close()
    arcpy.AddMessage("Data Dictionary Completed")

fields ='*'
token = ''


if chooseData == "SCHEMA":
    label = "Updates"
    the_filename = "TxDOT_" + label + "_" + updateClass + "_" + str(org)
    everything = "1=1"
    objectIDs = getObjectIDs(everything)
    arcpy.AddMessage(objectIDs)
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
    the_filename = "TxDOT_" + label + "_" + updateClass + "_" + str(org)
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

download_file("http://elcamino.atwebpages.com/DataDictionary.pdf")
# download_file("http://www.txdot.gov/apps/statewide_mapping/dusa/DataDictionary.pdf")

arcpy.AddMessage("packing up...")
outputPath = os.path.join(arcpy.env.scratchFolder, the_filename + ".zip")
arcpy.SetParameterAsText(4, outputPath)
zipper = outputPath
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