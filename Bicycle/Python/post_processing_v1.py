__file__ = 'post_processing_v1'
__date__ = '8/14/2015'
__author__ = 'ABREZNIC'
import arcpy, datetime, os

now = datetime.datetime.now()
curMonth = now.strftime("%m")
curDay = now.strftime("%d")
curYear = now.strftime("%Y")
today = curYear + "_" + curMonth + "_" + curDay

output = "C:\\TxDOT\\Scripts\\javascript\\Bicycle\\Python"
bikeroutes = "Database Connections\\Connection to ch-osd-db1_User.sde\\CHEROKEE.APP_TPP_GIS_ADMIN.BICYCLE\\CHEROKEE.APP_TPP_GIS_ADMIN.OnSystem_Bicycle_Routes"
counties = "Database Connections\\Connection to Comanche.sde\\TPP_GIS.APP_TPP_GIS_ADMIN.County\\TPP_GIS.APP_TPP_GIS_ADMIN.County"
areaoffices = "Database Connections\\Connection to Comanche.sde\\TPP_GIS.APP_TPP_GIS_ADMIN.District\\TPP_GIS.APP_TPP_GIS_ADMIN.Area_Office"
roads = "Database Connections\\Connection to Comanche.sde\\TPP_GIS.APP_TPP_GIS_ADMIN.HPMS_Spatial\\TPP_GIS.APP_TPP_GIS_ADMIN.HPMS_ROUTES_TABLE_2014_REPORTED"

arcpy.CreateFileGDB_management(output, "PostProcessing_" + today + ".gdb")
dbase = output + os.sep + "PostProcessing_" + today + ".gdb"
sr = arcpy.SpatialReference("NAD 1983 Texas Statewide Mapping System (Meters)")
arcpy.Project_management(bikeroutes, dbase + os.sep + "BikeRoutes_Projected", sr)
projected = dbase + os.sep + "BikeRoutes_Projected"
arcpy.AddMessage("Projected.")

dict = {}
arcpy.AddField_management(projected, "UNIQUE_ID", "SHORT")
cursor = arcpy.da.UpdateCursor(projected, ["OBJECTID", "UNIQUE_ID", "RTE_ID"])
for row in cursor:
    row[1] = row[0]
    cursor.updateRow(row)
    dict[row[1]] = row[2]
del cursor
arcpy.Identity_analysis(projected, counties, dbase + os.sep + "BikeRoutes_Counties")
arcpy.Identity_analysis(dbase + os.sep + "BikeRoutes_Counties", areaoffices, dbase + os.sep + "BikeRoutes_Identity")
identityroutes = dbase + os.sep + "BikeRoutes_Identity"
arcpy.AddMessage("Identitied.")

arcpy.FeatureVerticesToPoints_management(identityroutes, dbase + os.sep + "EndPoints", "BOTH_ENDS")
endpoints = dbase + os.sep + "EndPoints"
arcpy.AddMessage("Point'd.")

mxd = arcpy.mapping.MapDocument("CURRENT")
df = arcpy.mapping.ListDataFrames(mxd, "*")[0]
pointslayer = arcpy.mapping.Layer(endpoints)
arcpy.mapping.AddLayer(df, pointslayer)
roadslayer = arcpy.mapping.Layer(roads)
arcpy.mapping.AddLayer(df, roadslayer)
for lyr in arcpy.mapping.ListLayers(mxd):
    if lyr.name == "EndPoints":
        pointslayer = lyr
    if lyr.name == "TPP_GIS.APP_TPP_GIS_ADMIN.HPMS_ROUTES_TABLE_2014_REPORTED":
        roadslayer = lyr
arcpy.AddMessage("Layers acquired.")

counter = 1
for UID in dict.keys():
    if dict[UID] is not None:
        roadslayer.definitionQuery = " ROUTE_ID = '" + dict[UID] + "' "
    else:
        arcpy.AddMessage("BAD RTE ID: " + str(UID))
    pointslayer.definitionQuery = " UNIQUE_ID = " + str(UID)
    arcpy.RefreshActiveView()
    arcpy.AddMessage(str(counter) + "/" + str(len(dict.keys())) + " " + str(UID))
    arcpy.LocateFeaturesAlongRoutes_lr(pointslayer, roadslayer, "ROUTE_ID", "5 Miles", dbase + os.sep + "UID" + str(UID), "ROUTE_ID POINT DFO")
    counter += 1
arcpy.AddMessage("Tables created.")

bundle = {}
arcpy.env.workspace = dbase
tables = arcpy.ListTables()
for table in tables:
    arcpy.AddMessage(table)
    measures = []
    cnty = ""
    office = ""
    UID = ""
    cursor = arcpy.da.SearchCursor(table, ["UNIQUE_ID", "CNTY_NM", "OFFICE_NM", "DFO", "SEGMENT_LENGTH"], sql_clause=(None,'ORDER BY SEGMENT_LENGTH ASC'))
    for row in cursor:
        UID = row[0]
        cnty = row[1]
        office = row[2]
        measures.append(row[3])
    del cursor
    bundle[UID] = [cnty, office, measures]
arcpy.AddMessage("Values bundled.")

cursor = arcpy.da.UpdateCursor(projected, ["UNIQUE_ID", "COUNTY", "AREA_OFFICE", "FROM_DFO", "TO_DFO"])
for row in cursor:
    UID = row[0]
    arcpy.AddMessage(UID)
    values = bundle[UID]
    row[1] = values[0]
    row[2] = values[1]
    measures = values[2]
    row[3] = measures[0]
    row[4] = measures[1]
    cursor.updateRow(row)
del cursor
arcpy.AddMessage("Populated.")

print "that's all folks!!"
arcpy.AddMessage("that's all folks!!")