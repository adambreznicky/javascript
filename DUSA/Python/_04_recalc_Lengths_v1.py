__file__ = '04_recalc_Lengths_v1'
__date__ = '4/25/2016'
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
publish_db_location = "C:\\TxDOT\\Scripts\\javascript\\DUSA\\Python"
publish_db_name = "Publish.gdb"
update_feature_classes = ["CountyRoads", "LocalStreets"]

# global variables
publish_db = publish_db_location + os.sep + publish_db_name
arcpy.env.workspace = "in_memory"


def recalc_lengths(fc):
    print "updating " + fc
    cursor = arcpy.da.UpdateCursor(fc, ["LENGTH", "SHAPE@LENGTH", "SURFACE", "OBJECTID"])
    for row in cursor:
        meters = row[1]
        miles = meters * 0.000621371192
        row[0] = float(format(float(miles), '.3f'))

        fc_name = os.path.basename(fc)
        if fc_name == "CountyRoads":
            surface = row[2]
            # dirt/natural codes
            if surface in ["", "99", "12"]:
                row[2] = "12"
            # gravel codes
            elif surface in ["13"]:
                row[2] = "13"
            # brick codes
            elif surface in ["11"]:
                row[2] = "11"
            # paved codes
            elif surface in ["8", "9", "10"]:
                row[2] = "10"
            # concrete codes
            elif surface in ["1", "2", "3", "4", "5", "6", "7"]:
                row[2] = "1"
            # print bad code OIDs
            else:
                print row[3]
        elif fc_name == "LocalStreets":
            surface = row[2]
            # dirt/natural codes
            if surface in ["12"]:
                row[2] = "12"
            # gravel codes
            elif surface in ["13"]:
                row[2] = "13"
            # brick codes
            elif surface in ["11"]:
                row[2] = "11"
            # paved codes
            elif surface in ["8", "9", "10", "99", ""]:
                row[2] = "10"
            # concrete codes
            elif surface in ["1", "2", "3", "4", "5", "6", "7"]:
                row[2] = "1"
            # print bad code OIDs
            else:
                print row[3]
        cursor.updateRow(row)
    del cursor
    del row

    arcpy.AssignDomainToField_management(fc, "SURFACE", "RDWY_SURFACE")
    arcpy.AssignDomainToField_management(fc, "DESIGN", "RDWY_DESIGN")


def process():
    for name in update_feature_classes:
        path = os.path.join(publish_db, name)
        recalc_lengths(path)

