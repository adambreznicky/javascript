__file__ = 'Time_format_v1'
__date__ = '6/22/2015'
__author__ = 'ABREZNIC'

import arcpy, csv

input = "C:\\TxDOT\\Scripts\\javascript\\Guardrail\\Snake\\QC\\Analysis\\GET_20150629_QC.gdb\\GET_Analysis150630"
dist = "Database Connections\\Connection to Comanche.sde\\TPP_GIS.APP_TPP_GIS_ADMIN.District\\TPP_GIS.APP_TPP_GIS_ADMIN.District"

districts = []
cursor = arcpy.da.SearchCursor(dist, ["DIST_NM"])
for row in cursor:
    if row[0] not in districts:
        districts.append(row[0])
del cursor

counter = 0

dictionary = {}
dictionary["Statewide"] = [0, 0, 0, 0, 0, 0, 0]
cursor = arcpy.da.SearchCursor(input, ["DIST_NM", "TreatmentType"])
for row in cursor:
    counter += 1
    print counter
    d = row[0]
    t = row[1]
    if d not in dictionary.keys():
        dictionary[d] = [0, 0, 0, 0, 0, 0, 0]
    if t == "ETPLUS":
        dTotals = dictionary[d]
        oldTotal = dTotals[0]
        newTotal = oldTotal + 1
        dictionary[d] = [newTotal, dTotals[1], dTotals[2], dTotals[3], dTotals[4], dTotals[5], dTotals[6]]

        sTotals = dictionary["Statewide"]
        sOld = sTotals[0]
        sNew = sOld + 1
        dictionary["Statewide"] = [sNew, sTotals[1], sTotals[2], sTotals[3], sTotals[4], sTotals[5], sTotals[6]]
    if t == "ET2000":
        dTotals = dictionary[d]
        oldTotal = dTotals[1]
        newTotal = oldTotal + 1
        dictionary[d] = [dTotals[0], newTotal, dTotals[2], dTotals[3], dTotals[4], dTotals[5], dTotals[6]]

        sTotals = dictionary["Statewide"]
        sOld = sTotals[1]
        sNew = sOld + 1
        dictionary["Statewide"] = [sTotals[0], sNew, sTotals[2], sTotals[3], sTotals[4], sTotals[5], sTotals[6]]
    if t == "OTHER":
        dTotals = dictionary[d]
        oldTotal = dTotals[2]
        newTotal = oldTotal + 1
        dictionary[d] = [dTotals[0], dTotals[1], newTotal, dTotals[3], dTotals[4], dTotals[5], dTotals[6]]

        sTotals = dictionary["Statewide"]
        sOld = sTotals[2]
        sNew = sOld + 1
        dictionary["Statewide"] = [sTotals[0], sTotals[1], sNew, sTotals[3], sTotals[4], sTotals[5], sTotals[6]]
    if t == "SKT350":
        dTotals = dictionary[d]
        oldTotal = dTotals[3]
        newTotal = oldTotal + 1
        dictionary[d] = [dTotals[0], dTotals[1], dTotals[2], newTotal, dTotals[4], dTotals[5], dTotals[6]]

        sTotals = dictionary["Statewide"]
        sOld = sTotals[3]
        sNew = sOld + 1
        dictionary["Statewide"] = [sTotals[0], sTotals[1], sTotals[2], sNew, sTotals[4], sTotals[5], sTotals[6]]
    if t == "SOFTSTOP":
        dTotals = dictionary[d]
        oldTotal = dTotals[4]
        newTotal = oldTotal + 1
        dictionary[d] = [dTotals[0], dTotals[1], dTotals[2], dTotals[3], newTotal, dTotals[5], dTotals[6]]

        sTotals = dictionary["Statewide"]
        sOld = sTotals[4]
        sNew = sOld + 1
        dictionary["Statewide"] = [sTotals[0], sTotals[1], sTotals[2], sTotals[3], sNew, sTotals[5], sTotals[6]]
    if t == "TURNDOWN":
        dTotals = dictionary[d]
        oldTotal = dTotals[5]
        newTotal = oldTotal + 1
        dictionary[d] = [dTotals[0], dTotals[1], dTotals[2], dTotals[3], dTotals[4], newTotal, dTotals[6]]

        sTotals = dictionary["Statewide"]
        sOld = sTotals[5]
        sNew = sOld + 1
        dictionary["Statewide"] = [sTotals[0], sTotals[1], sTotals[2], sTotals[3], sTotals[4], sNew, sTotals[6]]
    if t == "XLITE":
        dTotals = dictionary[d]
        oldTotal = dTotals[6]
        newTotal = oldTotal + 1
        dictionary[d] = [dTotals[0], dTotals[1], dTotals[2], dTotals[3], dTotals[4], dTotals[5], newTotal]

        sTotals = dictionary["Statewide"]
        sOld = sTotals[6]
        sNew = sOld + 1
        dictionary["Statewide"] = [sTotals[0], sTotals[1], sTotals[2], sTotals[3], sTotals[4], sTotals[5], sNew]


del cursor


data = []
header = ["District", "ETPLUS", "ET2000", "OTHER", "SKT350", "SOFTSTOP", "TURNDOWN", "XLITE"]
data.append(header)

distList = dictionary.keys()
print distList
distList.sort()
for i in distList:
    numbers = dictionary[i]
    numbers.insert(0, i)
    data.append(numbers)


final = open("C:\\TxDOT\\Scripts\\javascript\\Guardrail\\Snake\\QC\\Analysis\\TypeTable.csv", 'wb')
writer = csv.writer(final)
writer.writerows(data)
final.close()

print "that's all folks!"