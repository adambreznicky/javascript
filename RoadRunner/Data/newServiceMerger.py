__file__ = 'newServiceMerger'
__date__ = '2/17/2016'
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
import arcpy
fc = "C:\\TxDOT\\Scripts\\javascript\\RoadRunner\\Data\\MaintenanceDeficiencies.gdb\\Deficiency"
tbl = "C:\\TxDOT\\Scripts\\javascript\\RoadRunner\\Data\\domains\\DeficienciesDomain.dbf"

dict = {}
print "building dictionary"
cursor = arcpy.da.SearchCursor(tbl, ["DESC", "ORIG"])
for row in cursor:
    orig = row[1]
    if orig != "" and orig is not None:
        if "," in orig:
            array = orig.split(",")
            for i in array:
                dict[i] = row[0]
        else:
            dict[orig] = row[0]
del cursor
print "populating new deficiency types"
cursor = arcpy.da.UpdateCursor(fc, ["Deficiency"])
for row in cursor:
    d = row[0]
    try:
        row[0] = dict[d]
        cursor.updateRow(row)
    except:
        print "Bad: " + d
del cursor
print "running near tool"
rds = "C:\\TxDOT\\Scripts\\javascript\\RoadRunner\\Data\\MaintenanceRoadways.gdb\\Roadways"
arcpy.Near_analysis(fc, rds)
print "building dictionary (2)"
dict2 = {}
cursor = arcpy.da.SearchCursor(rds, ["OBJECTID", "RTE_NM"])
for row in cursor:
    oid = row[0]
    nm = row[1]
    dict2[oid] = nm
del cursor
print "applying route name"
cursor = arcpy.da.UpdateCursor(fc, ["NEAR_FID", "Route"])
for row in cursor:
    fid = row[0]
    row[1] = dict2[fid]
    cursor.updateRow(row)
del cursor
print "fixing fields"
arcpy.DeleteField_management(fc, ["NEAR_FID", "NEAR_DIST"])
arcpy.AddField_management(fc, "AssignedCrew", "TEXT", "", "", 100)
# print "gonna try and delete the global id"
# arcpy.DeleteField_management(fc, ["GlobalID"])
print "that's all folks!!"