#TxDOT - Clear Uploaded within Linework_Collected data from Geolocation APP
#Adam Breznicky
#2014/04/18

import arcpy


def clearTestData():
    roadways = "Database Connections\\Connection to Comanche.sde\\TPP_GIS.APP_TPP_GIS_ADMIN.Roadways\\TPP_GIS.APP_TPP_GIS_ADMIN.Linework_Collected"
    print "LET THE CLEARING COMMENCE!"

    cursor = arcpy.UpdateCursor(roadways)
    counter = 0
    for i in cursor:
        if i.INV_CREW == "GEO APP":
            cursor.deleteRow(i)
            counter += 1
        #cursor.updateRow(i)
    del cursor
    print str(counter) + " rows deleted from Linework_Collected."


clearTestData()

print "that's all folks!"