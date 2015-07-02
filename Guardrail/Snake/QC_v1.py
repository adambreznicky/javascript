__file__ = 'QC_v1'
__date__ = '6/16/2015'
__author__ = 'ABREZNIC'
import arcpy, datetime, os

output = "C:\\TxDOT\\Scripts\\javascript\\Guardrail\\Snake\\QC"
GET = "C:\\TxDOT\\Scripts\\javascript\\Guardrail\\Snake\\QC\\Analysis\\GET_20150629_QC.gdb\\GuardrailEndTreatments"
roadways = "Database Connections\\Connection to Comanche.sde\\TPP_GIS.APP_TPP_GIS_ADMIN.Roadways\\TPP_GIS.APP_TPP_GIS_ADMIN.TXDOT_Roadways"
offices = "Database Connections\\Connection to Comanche.sde\\TPP_GIS.APP_TPP_GIS_ADMIN.Facility\\TPP_GIS.APP_TPP_GIS_ADMIN.Office"

now = datetime.datetime.now()
curMonth = now.strftime("%m")
curDay = now.strftime("%d")
curYear = now.strftime("%Y")
arcpy.CreateFileGDB_management(output, "QC_GET" + curYear + curMonth + curDay)
werkspace = output + os.sep + "QC_GET" + curYear + curMonth + curDay + ".gdb"
print "Workspace created."

###############bad speed and accuracy##########
query = "(Speed = '0' OR Speed IS NULL) AND AccuracyFeet > 250"

badGET = werkspace + os.sep + "GET_BadSpdAcc"
arcpy.Select_analysis(GET, badGET, query)
print "Bad accuracy and speed records found."

#########cursor checks############

##### same lat, long check
list = []
latlongFreq = werkspace + os.sep + "LatLongFreq"
arcpy.Frequency_analysis(GET, latlongFreq, ["Latitude", "Longitude"])
cursor = arcpy.da.UpdateCursor(latlongFreq, ["FREQUENCY", "Latitude", "Longitude"])
for row in cursor:
    if row[0] == 1:
        cursor.deleteRow()
    else:
        identifier = str(row[1]) + str(row[2])
        list.append(identifier)
del cursor
print "Lat/Long Duplicates identified."

dupes = werkspace + os.sep + "DupeLatLong"
arcpy.Copy_management(GET, dupes)
cursor = arcpy.da.UpdateCursor(dupes, ["Latitude", "Longitude"])
for row in cursor:
    identifier = str(row[0]) + str(row[1])
    if identifier not in list:
        cursor.deleteRow()
del cursor
print "DupeLatLong feature class complete."

############txdot offices buffer############
officeBuff = werkspace + os.sep + "TxdotOfficeBuffer"
arcpy.Buffer_analysis(offices, officeBuff, ".1 Miles")
print "Office buffer created."

officeGET = werkspace + os.sep + "GET_officeTests"
arcpy.Clip_analysis(GET, officeBuff, officeGET)
print "Office GETs found."

############onsystem buffer############
query2 = "RTE_CLASS = '1'"

onsystem = werkspace + os.sep + "OnSystemRoadways"
arcpy.Select_analysis(roadways, onsystem, query2)
print "OnSystem roads isolated."

onsysBuff = werkspace + os.sep + "OnSystemBuffer"
arcpy.Buffer_analysis(onsystem, onsysBuff, "125 Feet")
print "Roads buffer created."

onsysGET = werkspace + os.sep + "GET_offRoadways"
arcpy.Erase_analysis(badGET, onsysBuff, onsysGET)
print "Road GETs found."


print "that's all folks!!"