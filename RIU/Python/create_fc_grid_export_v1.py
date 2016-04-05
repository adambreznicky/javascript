__file__ = 'create_fc_grid_export_v1'
__date__ = '4/5/2016'
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

grid_export = "Database Connections\\Connection to Comanche.sde\\TPP_GIS.APP_TPP_GIS_ADMIN.GRID_Export\\TPP_GIS.APP_TPP_GIS_ADMIN.Roadways_GRID_Export"
local_streets_poly = "Database Connections\\Cherokee_Prod_Admin.sde\\CHEROKEE.APP_TPP_GIS_ADMIN.Roadways\\CHEROKEE.APP_TPP_GIS_ADMIN.LocalStreets_Poly"
publish_db = "C:\\TxDOT\\Scripts\\javascript\\RIU\\Python\\Publish.gdb"
arcpy.env.workspace = "in_memory"


def delete_current(name):
    feature_class = publish_db + os.sep + name
    if arcpy.Exists(feature_class):
        arcpy.Delete_management(feature_class)


def filter_roads(prefix_code, name):
    print "deleting current " + name
    delete_current(name)
    print "making layer for " + name
    arcpy.Select_analysis(grid_export, "layer", "RTE_PRFX = " + prefix_code + " AND RDBD_STAT = 2")
    sr = arcpy.SpatialReference("WGS 1984 Web Mercator (auxiliary sphere)")
    print "projecting " + name
    arcpy.Project_management("layer", publish_db + os.sep + name, sr)
    return publish_db + os.sep + name


def local_streets_schema(ls):
    print "formatting schema LocalStreets"
    # rename_fields = ["SEG_LEN", "RTE_RB_NM", "MAP_LBL"]
    print "adding fields"
    arcpy.AddField_management(ls, "LENGTH", "DOUBLE")
    arcpy.AddField_management(ls, "ROUTE_ID", "TEXT", "", "", 17)
    arcpy.AddField_management(ls, "STREET_NM", "TEXT", "", "", 100)
    arcpy.AddField_management(ls, "PRIME_ADMN", "TEXT", "", "", 100)
    arcpy.AddField_management(ls, "ADMN_TYPE", "TEXT", "", "", 50)
    arcpy.AddField_management(ls, "ADMN_ACRNM", "TEXT", "", "", 20)
    arcpy.AddField_management(ls, "COG_NM", "TEXT", "", "", 100)
    arcpy.AddField_management(ls, "COG_ACRNM", "TEXT", "", "", 20)
    arcpy.AddField_management(ls, "TxDOT_DIST", "TEXT", "", "", 100)
    arcpy.AddField_management(ls, "DIST_ACRNM", "TEXT", "", "", 20)

    print "re-populating new fields"
    cursor = arcpy.da.UpdateCursor(ls, ["SEG_LEN", "RTE_RB_NM", "MAP_LBL", "LENGTH", "ROUTE_ID", "STREET_NM"])
    for row in cursor:
        row[3] = row[0]
        row[4] = row[1]
        row[5] = row[2]
        cursor.updateRow(row)
    del cursor
    del row
    print "deleting fields"
    delete_fields = ["SEG_LEN", "RTE_RB_NM", "MAP_LBL", "BEGIN_DFO", "END_DFO", "RTE_NBR", "RTE_GRID", "RTE_PRFX", "RTE_SFX", "RDBD_TYPE", "DES_DRCT", "RDBD_STAT", "COUNTY", "CREATE_DT", "CREATE_NM", "EDIT_DT", "EDIT_NM", "OGEOMS", "EDIT_TYPE", "ETL_JOB_ID", "ETL_STAT", "GSC", "ZOOM"]
    for field in delete_fields:
        print field
        arcpy.DeleteField_management(ls, field)


def populate_ls_admin(ls, poly):
    print "making feature layers"
    arcpy.MakeFeatureLayer_management(ls, 'ls_lyr')
    arcpy.MakeFeatureLayer_management(poly, 'poly_lyr')
    poly_layer = arcpy.mapping.Layer('poly_lyr')

    print "starting cog cursor"
    cursor = arcpy.da.SearchCursor(poly, ["SOURCE", "NAME", "ACRNM"], "SOURCE = 'COG'")
    for row in cursor:
        print row[1]
        poly_layer.definitionQuery = "NAME = '" + row[1] + "'"
        arcpy.SelectLayerByLocation_management('ls_lyr', 'INTERSECT', poly_layer)
        updator = arcpy.da.UpdateCursor('ls_lyr', ["ADMN_TYPE", "PRIME_ADMN", "ADMN_ACRNM", "COG_NM", "COG_ACRNM"])
        for record in updator:
            record[0] = row[0]
            record[1] = row[1]
            record[2] = row[2]
            record[3] = row[1]
            record[4] = row[2]
            updator.updateRow(record)
    del updator
    del cursor

    print "starting admin cursor"
    cursor = arcpy.da.SearchCursor(poly, ["SOURCE", "NAME", "ACRNM"], "SOURCE <> 'DISTRICT' AND SOURCE <> 'STATE' AND SOURCE <> 'COG' AND NAME <> 'Medina 911'")
    for row in cursor:
        print row[1]
        poly_layer.definitionQuery = "NAME = '" + row[1] + "'"
        arcpy.SelectLayerByLocation_management('ls_lyr', 'INTERSECT', poly_layer)
        updator = arcpy.da.UpdateCursor('ls_lyr', ["ADMN_TYPE", "PRIME_ADMN", "ADMN_ACRNM"])
        for record in updator:
            record[0] = row[0]
            record[1] = row[1]
            record[2] = row[2]
            updator.updateRow(record)
    del updator
    del cursor

    print "starting district cursor"
    cursor = arcpy.da.SearchCursor(poly, ["SOURCE", "NAME", "ACRNM"], "SOURCE = 'DISTRICT'")
    for row in cursor:
        print row[1]
        poly_layer.definitionQuery = "NAME = '" + row[1] + "'"
        arcpy.SelectLayerByLocation_management('ls_lyr', 'INTERSECT', poly_layer)
        updator = arcpy.da.UpdateCursor('ls_lyr', ["TxDOT_DIST", "DIST_ACRNM"])
        for record in updator:
            record[0] = row[1]
            record[1] = row[2]
            updator.updateRow(record)
    del updator
    del cursor

    print "duplicating medina for medina 911"
    arcpy.Select_analysis(ls, "medina_layer", "PRIME_ADMN = 'Medina'")
    cursor = arcpy.da.UpdateCursor("medina_layer", ["PRIME_ADMN", "ADMN_ACRNM", "ADMN_TYPE"])
    for row in cursor:
        row[0] = "Medina 911"
        row[1] = "MDA911"
        row[2] = "E911_COUNTY"
        cursor.updateRow(row)
    del cursor
    arcpy.Append_management(["medina_layer"], ls, "NO_TEST")


# local streets filter
local_streets = filter_roads("7", "LocalStreets")
local_streets_schema(local_streets)
populate_ls_admin(local_streets, local_streets_poly)

print "that's all folks!!"
