__file__ = 'Time_format_v1'
__date__ = '6/22/2015'
__author__ = 'ABREZNIC'
import arcpy

input = "C:\\TxDOT\\Scripts\\javascript\\Guardrail\\Snake\\BACKUP\\GETdisplay.gdb\\GETdisplay"

cursor = arcpy.da.UpdateCursor(input, ["Date", "TIME"], "Date IS NOT NULL")
for row in cursor:
    year = row[0].split("-")[0]
    month = row[0].split("-")[1]
    day = row[0].split("-")[2]
    hour = row[0].split("-")[3]
    min = row[0].split("-")[4]
    sec = row[0].split("-")[5]

    if len(month) == 1:
        month = "0" + month
    if len(day) == 1:
        day = "0" + day
    if len(hour) == 1:
        hour = "0" + hour
    if len(min) == 1:
        min = "0" + min
    if len(sec) == 1:
        sec = "0" + sec
    row[1] = year + month + day + hour + min + sec
    cursor.updateRow(row)
del cursor

print "that's all folks!"