__file__ = 'create_update_feature_classes_v1'
__date__ = '4/6/2016'
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
import arcpy, os

# set input variables
publish_db = "C:\\TxDOT\\Scripts\\javascript\\DUSA\\Python\\Publish.gdb"
updates_feature_classes = ["LocalStreets_Updates", "CountyRoads_Updates"]

# global variables
arcpy.env.workspace = "in_memory"


def create_feature_class(name):
    print "creating feature class " + name
    sr = arcpy.SpatialReference("WGS 1984 Web Mercator (auxiliary sphere)")
    arcpy.CreateFeatureclass_management(publish_db, name, "POLYLINE", "", "DISABLED", "DISABLED", sr)


def create_fields(name):
    print "creating fields for " + name
    fc = publish_db + os.sep + name
    arcpy.AddField_management(fc, "SOURCE", "TEXT", "", "", 75)
    arcpy.AddField_management(fc, "UPDATE_DT", "DATE")
    arcpy.AddField_management(fc, "LENGTH", "DOUBLE")
    arcpy.AddField_management(fc, "CHANGE", "TEXT", "", "", 10, "", "", "", "RDWY_UPDATE")
    arcpy.AddField_management(fc, "STREET_NM", "TEXT", "", "", 100)
    arcpy.AddField_management(fc, "DESIGN", "TEXT", "", "", 1, "", "", "", "RDWY_DESIGN")
    arcpy.AddField_management(fc, "SURFACE", "TEXT", "", "", 2, "", "", "", "RDWY_SURFACE")
    arcpy.AddField_management(fc, "NUM_LANES", "LONG", 2)
    arcpy.AddField_management(fc, "COMMENT", "TEXT", "", "", 150)


def build(fc_list):
    for fc in fc_list:
        create_feature_class(fc)
        create_fields(fc)


def process():
    build(updates_feature_classes)

