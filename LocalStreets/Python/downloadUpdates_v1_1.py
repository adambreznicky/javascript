__file__ = 'downloadUpdates_v1'
__date__ = '11/12/2015'
__author__ = 'ABREZNIC'
import arcpy, zipfile, os, shutil
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
arcpy.AddMessage("directory created.")

if updateClass == "CR":
    if chooseData == "SCHEMA":
        baseURL = "http://services.arcgis.com/KTcxiTD9dsQw4r7Z/arcgis/rest/services/InventoryUpdates/FeatureServer/0/query"
        where = "1<>1"
    elif chooseData == "DATA":
        baseURL = "http://services.arcgis.com/KTcxiTD9dsQw4r7Z/arcgis/rest/services/CountyRoads/FeatureServer/0/query"
        # where = """"COUNTY"=""" + str(org)
        where = """"OBJECTID" = """ + str(1510)

elif updateClass == "LS":
    if chooseData == "SCHEMA":
        baseURL = "http://services.arcgis.com/KTcxiTD9dsQw4r7Z/arcgis/rest/services/InventoryUpdates/FeatureServer/0/query"
        where = "1<>1"
    elif chooseData == "DATA":
        baseURL = "http://services.arcgis.com/KTcxiTD9dsQw4r7Z/arcgis/rest/services/CountyRoads/FeatureServer/0/query"
        where = """"COUNTY"=""" + str(org)



fields ='*'
token = ''
#The above variables construct the query
query = "?where={}&outFields={}&returnGeometry=true&f=json&token={}".format(where, fields, token)
fsURL = baseURL + query
arcpy.AddMessage(fsURL)
fs = arcpy.FeatureSet()
fs.load(fsURL)
arcpy.AddMessage("select completed.")

if downloadFormat == "SHP":
    arcpy.CopyFeatures_management(fs, directory + os.sep + "TxDOT_" + updateClass + "_" + str(org) + ".shp")
elif downloadFormat == "FGDB":
    arcpy.CreateFileGDB_management(directory, "TxDOT_" + updateClass + "_" + str(org))
    fgdb = directory + os.sep + "TxDOT_" + updateClass + "_" + str(org)
    arcpy.CopyFeatures_management(fs, fgdb + os.sep + "TxDOT_" + updateClass + "_" + str(org))

zipper = output
if os.path.isfile(zipper):
    os.remove(zipper)
zip = zipfile.ZipFile(zipper, 'w', zipfile.ZIP_DEFLATED)
arcpy.AddMessage("zipfile completed.")
for filename in os.listdir(directory):
    if not filename.endswith('.lock'):
        zip.write(os.path.join(directory, filename), filename)
zip.close()

arcpy.AddMessage("that's all folks!!")