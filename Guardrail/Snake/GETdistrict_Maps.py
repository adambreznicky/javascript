__file__ = 'GETindividual_Maps'
__date__ = '7/1/2015'
__author__ = 'ABREZNIC'
import arcpy
output = "C:\\TxDOT\\Scripts\\javascript\\Guardrail\\Snake\\QC\\Analysis\\GETmaps\\"
mxd = "C:\\TxDOT\\Scripts\\javascript\\Guardrail\\Snake\\QC\\Analysis\\GET_district.mxd"
districts = "Database Connections\\Connection to Comanche.sde\\TPP_GIS.APP_TPP_GIS_ADMIN.District\\TPP_GIS.APP_TPP_GIS_ADMIN.District"
print "and away we go..."
#make directory

map = arcpy.mapping.MapDocument(mxd)
dataFrame = arcpy.mapping.ListDataFrames(map)[0]
cursor = arcpy.da.SearchCursor(districts, ["DIST_NM", "SHAPE@"])
for row in cursor:
    dist = row[0]
    shape = row[1]
    extent = shape.extent
    dataFrame.extent = extent
    dataFrame.scale *= 1.05
    arcpy.RefreshActiveView()

    for textElement in arcpy.mapping.ListLayoutElements(map, "TEXT_ELEMENT"):
        if textElement.name == "title":
            textElement.text = "Guardrail End Treatments: " + dist + " District"
    arcpy.RefreshActiveView()



    arcpy.mapping.ExportToPDF(map, output + "GET_" + dist + ".pdf")
    print dist + " done."
del map
del dataFrame
print "that's all folks!!"