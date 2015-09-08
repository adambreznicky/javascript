__file__ = 'submitLS_v1'
__date__ = '9/3/2015'
__author__ = 'ABREZNIC'
import arcpy, zipfile, os, shutil
# http://blogs.esri.com/esri/arcgis/2013/10/10/quick-tips-consuming-feature-services-with-geoprocessing/

input = arcpy.GetParameterAsText(0)
output = arcpy.GetParameterAsText(1).replace("\\", os.sep)

directory = arcpy.env.scratchFolder + os.sep + input
if not os.path.exists(directory):
    os.makedirs(directory)
else:
    shutil.rmtree(directory)
arcpy.AddMessage("directory created.")

baseURL = "http://maps.dot.state.tx.us/arcgis/rest/services/TPPuser/gpTester/FeatureServer/0/query"
where = """"RTE_ID" = '""" + input + """'"""
fields ='*'
token = ''
#The above variables construct the query
query = "?where={}&outFields={}&returnGeometry=true&f=json&token={}".format(where, fields, token)
fsURL = baseURL + query
fs = arcpy.FeatureSet()
fs.load(fsURL)
arcpy.CopyFeatures_management(fs, directory + os.sep + input + ".shp")
arcpy.AddMessage("select completed.")

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