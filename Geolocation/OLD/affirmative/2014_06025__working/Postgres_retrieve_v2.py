#TxDOT - Retrieve data from Geolocation APP
#Adam Breznicky
#2014/04/18

import arcpy, psycopg2, datetime, os

now = datetime.datetime.now()
today = now.strftime("%Y%m%d")
year = now.strftime("%Y")
time = now.strftime("%H%M%S")

#create space to pull data to
if not os.path.exists("C:\\TxDOT\\Shapefiles\\00_FieldCollectedData\\" + today):
    os.makedirs("C:\\TxDOT\\Shapefiles\\00_FieldCollectedData\\" + today)
home = "C:\\TxDOT\\Shapefiles\\00_FieldCollectedData\\" + today


def copyLocal():
    os.chdir("C:\\Program Files (x86)\\Boundless\\OpenGeo\\pgsql\\bin")
    print "We are cd-d."
    os.system(
        """pgsql2shp -f """ + home + """\\GeoLines""" + time + """.shp -h mypostgres.ceiqkhgminol.us-west-2.rds.amazonaws.com -u adam -P test -g TXSMS postgres "SELECT * FROM "geolines";" """)
    print "Lines are now local."
    os.system(
        """pgsql2shp -f """ + home + """\\GeoPoints""" + time + """.shp -h mypostgres.ceiqkhgminol.us-west-2.rds.amazonaws.com -u adam -P test -g TXSMS postgres "SELECT * FROM "geopoints";" """)
    print "Points are now local."


    # Connect to an existing database
    conn = psycopg2.connect(
        "dbname=postgres user=adam password=test host=mypostgres.ceiqkhgminol.us-west-2.rds.amazonaws.com port=5432")
    print "Connected to database for clearing."
    # Open a cursor to perform database operations
    cur = conn.cursor()
    # Query the database and obtain data as Python objects
    #cur.execute("INSERT INTO geolocation VALUES ('LINE', '660AA7874', '', '6664');")
    #conn.commit()
    #print "commited"

    #cur.execute("SELECT * FROM geolocation;")
    #all = cur.fetchall()

    # Make the changes to the database persistent
    cur.execute("DELETE FROM geolines; DELETE FROM geopoints;")
    conn.commit()

    # Close communication with the database
    cur.close()
    conn.close()
    print "Data tables cleared."


def uploadComanche():
    shapefile = home + "\\GeoLines" + time + ".shp"
    #shapefile = home+"\\GeoLines090541.shp"
    roadways = "Database Connections\\Connection to Comanche.sde\\TPP_GIS.APP_TPP_GIS_ADMIN.Roadways\\TPP_GIS.APP_TPP_GIS_ADMIN.Linework_Collected"
    print "LET THE UPLOAD COMMENCE!"

    cursor = arcpy.SearchCursor(shapefile)
    counter = 0
    for i in cursor:
        cur = arcpy.InsertCursor(roadways)
        row = cur.newRow()
        #
        row.setValue("RTE_NM", i.RTE_ID)
        #
        if i.RTE_PRFX == "AA":
            row.setValue("RTE_CLASS", 2)
        elif i.RTE_PRFX == "FC":
            row.setValue("RTE_CLASS", 3)
        elif i.RTE_PRFX == "CS":
            row.setValue("RTE_CLASS", 4)
        elif i.RTE_PRFX == "NA":
            row.setValue("RTE_CLASS", 5)
        else:
            row.setValue("RTE_CLASS", 1)
        #
        if i.HWY_DSGN == 1 or i.HWY_DSGN == 3:
            row.setValue("RTE_DIR", "ONE WAY")
        else:
            row.setValue("RTE_DIR", "TWO WAY")
        #
        row.setValue("RTE_PRFX", i.RTE_PRFX)
        #
        row.setValue("RTE_NBR", i.RTE_NBR)
        #
        row.setValue("CMNT", i.CMNT)
        #
        if i.RDBD_TYPE == "KG":
            row.setValue("RDBD_TYPE", 1)
        elif i.RDBD_TYPE == "LG":
            row.setValue("RDBD_TYPE", 2)
        elif i.RDBD_TYPE == "RG":
            row.setValue("RDBD_TYPE", 3)
        elif i.RDBD_TYPE == "XG":
            row.setValue("RDBD_TYPE", 4)
        elif i.RDBD_TYPE == "AG":
            row.setValue("RDBD_TYPE", 5)
        elif i.RDBD_TYPE == "MG":
            row.setValue("RDBD_TYPE", 12)
        elif i.RDBD_TYPE == "SG":
            row.setValue("RDBD_TYPE", 13)
        elif i.RDBD_TYPE == "PG":
            row.setValue("RDBD_TYPE", 10)
        elif i.RDBD_TYPE == "TG":
            row.setValue("RDBD_TYPE", 11)
        elif i.RDBD_TYPE == "YG":
            row.setValue("RDBD_TYPE", 14)
        elif i.RDBD_TYPE == "BG":
            row.setValue("RDBD_TYPE", 15)
        elif i.RDBD_TYPE == "CONNECTOR":
            row.setValue("RDBD_TYPE", 7)
        elif i.RDBD_TYPE == "RAMP":
            row.setValue("RDBD_TYPE", 6)
        elif i.RDBD_TYPE == "TURNAROUND":
            row.setValue("RDBD_TYPE", 8)
        else:
            row.setValue("RDBD_TYPE", 9)
        #
        row.setValue("RTE_ORDER", 0)
        #
        row.setValue("PROPOSED", 0)
        #
        row.setValue("FULL_ST_NM", i.FULL_ST_NM)
        #
        row.setValue("EDIT_DT", i.COLLN_DT)
        #
        row.setValue("EDIT_NM", "GEOLOCATION APP")
        #
        row.setValue("RTE_ID", i.RTE_ID)
        #
        row.setValue("PREP_TYPE", "N")
        #
        row.setValue("INV_STATUS", "Y")
        #
        row.setValue("INV_NOTES", i.CMNT)
        #
        row.setValue("SURF_TYPE", i.SRFC_TYPE)
        #
        row.setValue("H_DESI", i.HWY_DSGN)
        #
        row.setValue("NUM_LAN", i.NBR_LANES)
        #
        row.setValue("INV_DATE", today)
        #
        row.setValue("INV_CREW", "GEO APP")
        #
        if i.RTE_PRFX == "AA":
            cnty = i.RTE_ID[-3]
            row.setValue("CNUMTXT", cnty)
        #
        row.setValue("INV_EXISTS", "Y")
        #
        row.setValue("INV_YEAR", year)
        #
        row.setValue("SHAPE", i.Shape)
        #
        cur.insertRow(row)
        del cur
        counter += 1
        print "Row: " + str(counter) + " - " + i.RTE_ID
    del cursor
    print str(counter) + " rows added to Linework_Collected."


copyLocal()
#uploadComanche()

print "that's all folks!"