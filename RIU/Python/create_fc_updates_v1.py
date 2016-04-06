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

publish_db = "C:\\TxDOT\\Scripts\\javascript\\RIU\\Python\\Publish.gdb"
arcpy.env.workspace = "in_memory"

def create_feature_class(name):
    sr = arcpy.SpatialReference("WGS 1984 Web Mercator (auxiliary sphere)")
    arcpy.CreateFeatureclass_management(publish_db, name, "POLYLINE", "", "DISABLED", "DISABLED", sr)

create_feature_class("LocalStreets_Updates")

print "that's all folks!!"
