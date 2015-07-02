__file__ = 'Time_format_v1'
__date__ = '6/22/2015'
__author__ = 'ABREZNIC'

import arcpy, csv

input = "C:\\TxDOT\\Scripts\\javascript\\Guardrail\\Snake\\QC\\Analysis\\GET_20150629_QC.gdb\\GET_Analysis150630"


counter = 0

device = {}
time = {}
speed = 0
acc = float(0)
cursor = arcpy.da.SearchCursor(input, ["Device", "TIME", "Speed", "AccuracyFeet"])
for row in cursor:
    counter += 1
    print counter
    d = row[0]
    t = row[1]
    s = row[2]
    a = row[3]
    if d not in device.keys():
        device[d] = 1
    else:
        dT = device[d]
        ndt = dT + 1
        device[d] = ndt
    day = t[:8]
    if day not in time.keys():
        time[day] = 1
    else:
        dyt = time[day]
        ndyt = dyt + 1
        time[day] = ndyt
    if s is not None:
        speed = speed + int(s)
    if a is not None:
        acc = acc + a




del cursor

avgSpd = speed/counter
avgAcc = acc/counter

data = [["average speed", avgSpd], ["average accuracy (feet)", avgAcc], ["", ""]]

for i in device.keys():
    this = [i, device[i]]
    data.append(this)
for n in time.keys():
    that = [n, time[n]]
    data.append(that)


final = open("C:\\TxDOT\\Scripts\\javascript\\Guardrail\\Snake\\QC\\Analysis\\GeneralStats.csv", 'wb')
writer = csv.writer(final)
writer.writerows(data)
final.close()

print "that's all folks!"