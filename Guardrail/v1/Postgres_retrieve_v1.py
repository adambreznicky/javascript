#TxDOT - Retrieve data from Geolocation APP
#Adam Breznicky
#2014/04/18

import arcpy, psycopg2, datetime, os

now = datetime.datetime.now()
today = now.strftime("%Y%m%d")
year = now.strftime("%Y")
time = now.strftime("%H%M%S")

#create space to pull data to
if not os.path.exists("C:\\TxDOT\\Scripts\\Guardrail\\Data\\" + today):
    os.makedirs("C:\\TxDOT\\Scripts\\Guardrail\\Data\\" + today)
home = "C:\\TxDOT\\Scripts\\Guardrail\\Data\\" + today


def copyLocal():
    # os.chdir("C:\\Program Files (x86)\\Boundless\\OpenGeo\\pgsql\\bin")
    # print "We are cd-d."
    # os.system(
    #     """pgsql2shp -f """ + home + """\\GuardrailPoints""" + time + """.shp -h stevie.heliohost.org -u smudge_adam -P 05M-w}J$.;F[ -g TXSMS postgres "SELECT * FROM "Guardrails"; """)
    # print "Points are now local."


    # Connect to an existing database
    conn = psycopg2.connect(
        "dbname=smudge_assets user=smudge_adam password=05M-w}J$.;F[ host=stevie.heliohost.org port=5432")
    print "Connected to database."
    # Open a cursor to perform database operations
    cur = conn.cursor()
    # Query the database and obtain data as Python objects
    #cur.execute("INSERT INTO geolocation VALUES ('LINE', '660AA7874', '', '6664');")
    #conn.commit()
    #print "commited"

    cur.execute(""" SELECT * FROM "Guardrails"; """)
    rows = cur.fetchall()
    print "Data retrieved."

    template = "C:\\TxDOT\\Scripts\\Guardrail\\Data\\TemplateTable.dbf"
    arcpy.CreateTable_management(home, "CollectedData.dbf", template)
    dataTable = "C:\\TxDOT\\Scripts\\Guardrail\\Data\\" + today + os.sep + "CollectedData.dbf"

    allRows = []
    counter = 0
    for row in rows:
        thisRow = []
        for i in row:
            if i is not None:
                thisRow.append(i)
            else:
                thisRow.append(9999)
        allRows.append(thisRow)
    for n in allRows:
        print n
        cursor = arcpy.da.InsertCursor(dataTable, ["TYPE", "SIDE", "TIME", "ACCRY", "ALT", "SPEED", "HDG", "ALTACCRCY", "USER", "DEVICE", "LAT", "LONG"])
        cursor.insertRow(n)
        counter += 1
    print str(counter) + " records found."

    # Make the changes to the database persistent
    cur.execute(""" DELETE FROM "Guardrails"; """)
    conn.commit()

    # Close communication with the database
    cur.close()
    conn.close()
    print "Data tables cleared."



copyLocal()

print "that's all folks!"