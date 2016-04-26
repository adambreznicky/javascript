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

# set input variables
grid_export = "Database Connections\\Connection to Comanche.sde\\TPP_GIS.APP_TPP_GIS_ADMIN.GRID_Export\\TPP_GIS.APP_TPP_GIS_ADMIN.Roadways_GRID_Export"
local_streets_poly = "Database Connections\\Cherokee_Prod_Admin.sde\\CHEROKEE.APP_TPP_GIS_ADMIN.Roadways\\CHEROKEE.APP_TPP_GIS_ADMIN.LocalStreets_Poly"
publish_db_location = "C:\\TxDOT\\Scripts\\javascript\\DUSA\\Python"
publish_db_name = "Publish.gdb"
comanche_counties = "Database Connections\\Connection to Comanche.sde\\TPP_GIS.APP_TPP_GIS_ADMIN.County\\TPP_GIS.APP_TPP_GIS_ADMIN.County"

# global variables
publish_db = publish_db_location + os.sep + publish_db_name
arcpy.env.workspace = "in_memory"


def create_dbase_domains():
    dbase_exist = os.path.exists(publish_db)
    if dbase_exist is False:
        print "creating dbase"
        arcpy.CreateFileGDB_management(publish_db_location, publish_db_name)

    domains = arcpy.da.ListDomains(publish_db)
    domain_names = []
    for domain in domains:
        domain_names.append(domain.name)

    if "RDWY_UPDATE" not in domain_names:
        print "creating domain " + "RDWY_UPDATE"
        arcpy.CreateDomain_management(publish_db, "RDWY_UPDATE", "Inventory Update Type", "TEXT", "CODED")
        arcpy.AddCodedValueToDomain_management(publish_db, "RDWY_UPDATE", "Add", "Add Road")
        arcpy.AddCodedValueToDomain_management(publish_db, "RDWY_UPDATE", "Remove", "Remove Road")
        arcpy.AddCodedValueToDomain_management(publish_db, "RDWY_UPDATE", "Update", "Update Attributes/Alignment")

    if "RDWY_DESIGN" not in domain_names:
        print "creating domain " + "RDWY_DESIGN"
        arcpy.CreateDomain_management(publish_db, "RDWY_DESIGN", "Road Design", "TEXT", "CODED")
        arcpy.AddCodedValueToDomain_management(publish_db, "RDWY_DESIGN", '1', "One Way")
        arcpy.AddCodedValueToDomain_management(publish_db, "RDWY_DESIGN", '2', "Two Way")
        arcpy.AddCodedValueToDomain_management(publish_db, "RDWY_DESIGN", '3', "Boulevard")

    if "RDWY_SURFACE" not in domain_names:
        print "creating domain " + "RDWY_SURFACE"
        arcpy.CreateDomain_management(publish_db, "RDWY_SURFACE", "Road Surface Type", "TEXT", "CODED")
        arcpy.AddCodedValueToDomain_management(publish_db, "RDWY_SURFACE", '12', "Dirt/Natural")
        arcpy.AddCodedValueToDomain_management(publish_db, "RDWY_SURFACE", '13', "Gravel")
        arcpy.AddCodedValueToDomain_management(publish_db, "RDWY_SURFACE", '11', "Brick")
        arcpy.AddCodedValueToDomain_management(publish_db, "RDWY_SURFACE", '10', "Paved")
        arcpy.AddCodedValueToDomain_management(publish_db, "RDWY_SURFACE", '1', "Concrete")


def delete_current(name):
    feature_class = publish_db + os.sep + name
    if arcpy.Exists(feature_class):
        arcpy.Delete_management(feature_class)


def filter_roads(prefix_code, name):
    print "deleting current " + name
    delete_current(name)
    print "making layer for " + name
    arcpy.Select_analysis(grid_export, name, "RTE_PRFX = " + prefix_code + " AND RDBD_STAT = 2")
    sr = arcpy.SpatialReference("WGS 1984 Web Mercator (auxiliary sphere)")
    print "projecting " + name
    arcpy.Project_management(name, publish_db + os.sep + name, sr)
    return publish_db + os.sep + name


def local_streets_schema(ls):
    print "formatting schema LocalStreets"
    # rename_fields = ["SEG_LEN", "RTE_RB_NM", "MAP_LBL"]
    print "adding fields"
    arcpy.AddField_management(ls, "PRIME_ADMN", "TEXT", "", "", 100)
    arcpy.AddField_management(ls, "ADMN_TYPE", "TEXT", "", "", 50)
    arcpy.AddField_management(ls, "ADMN_ACRNM", "TEXT", "", "", 20)
    arcpy.AddField_management(ls, "COG_NM", "TEXT", "", "", 100)
    arcpy.AddField_management(ls, "COG_ACRNM", "TEXT", "", "", 20)
    arcpy.AddField_management(ls, "TxDOT_DIST", "TEXT", "", "", 100)
    arcpy.AddField_management(ls, "DIST_ACRNM", "TEXT", "", "", 20)
    arcpy.AddField_management(ls, "LENGTH", "DOUBLE", "", 3)
    arcpy.AddField_management(ls, "ROUTE_ID", "TEXT", "", "", 17)
    arcpy.AddField_management(ls, "STREET_NM", "TEXT", "", "", 100)


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


def county_roads_schema(cr):
    print "formatting schema LocalStreets"
    rename_fields = ["SEG_LEN", "RTE_RB_NM", "MAP_LBL"]
    print "adding fields"
    arcpy.AddField_management(cr, "CNTY_NM", "TEXT", "", "", 50)
    arcpy.AddField_management(cr, "CNTY_NBR", "TEXT", "", "", 3)
    arcpy.AddField_management(cr, "TxDOT_DIST", "TEXT", "", "", 100)
    arcpy.AddField_management(cr, "LENGTH", "DOUBLE", "", 3)
    arcpy.AddField_management(cr, "ROUTE_ID", "TEXT", "", "", 17)
    arcpy.AddField_management(cr, "STREET_NM", "TEXT", "", "", 100)

    print "county number & name domain"
    county_dictionary = {}
    cursor = arcpy.da.SearchCursor(comanche_counties, ["CNTY_NBR", "CNTY_NM", "DIST_NM"])
    for row in cursor:
        nbr_string = str(row[0])
        county_dictionary[nbr_string] = [row[1], row[2]]

    print "re-populating new fields"
    cursor = arcpy.da.UpdateCursor(cr, ["SEG_LEN", "RTE_RB_NM", "MAP_LBL", "COUNTY", "LENGTH", "ROUTE_ID", "STREET_NM", "CNTY_NBR", "CNTY_NM", "TxDOT_DIST"])
    for row in cursor:
        row[4] = row[0]
        row[5] = row[1]
        row[6] = row[2]
        row[7] = str(row[3])
        values = county_dictionary[str(row[3])]
        row[8] = values[0]
        row[9] = values[1]
        cursor.updateRow(row)
    del cursor
    del row
    print "deleting fields"
    delete_fields = ["SEG_LEN", "RTE_RB_NM", "MAP_LBL", "BEGIN_DFO", "END_DFO", "RTE_NBR", "RTE_GRID", "RTE_PRFX", "RTE_SFX", "RDBD_TYPE", "DES_DRCT", "RDBD_STAT", "COUNTY", "CREATE_DT", "CREATE_NM", "EDIT_DT", "EDIT_NM", "OGEOMS", "EDIT_TYPE", "ETL_JOB_ID", "ETL_STAT", "GSC", "ZOOM"]
    for field in delete_fields:
        print field
        arcpy.DeleteField_management(cr, field)


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


def process():
    # dbase creator
    create_dbase_domains()
    # local streets filter
    local_streets = filter_roads("7", "LocalStreets_Export")
    local_streets_schema(local_streets)
    populate_ls_admin(local_streets, local_streets_poly)
    # county roads filter
    county_roads = filter_roads("1", "CountyRoads_Export")
    county_roads_schema(county_roads)

