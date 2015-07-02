__file__ = 'GETindividual_Maps'
__date__ = '7/1/2015'
__author__ = 'ABREZNIC'
import arcpy
output = "C:\\TxDOT\\Scripts\\javascript\\Guardrail\\Snake\\QC\\Analysis\\GETmaps\\"
mxd = "C:\\TxDOT\\Scripts\\javascript\\Guardrail\\Snake\\QC\\Analysis\\GET_individual.mxd"
print "and away we go..."
#make directory

types = ["ETPLUS", "ET2000", "OTHER", "SKT350", "SOFTSTOP", "TURNDOWN", "XLITE"]
map = arcpy.mapping.MapDocument(mxd)
dataFrame = arcpy.mapping.ListDataFrames(map)[0]
for type in types:
    pretty = ""
    if type == "ETPLUS":
        pretty = "ET Plus"
    elif type == "ET2000":
        pretty = "ET 2000"
    elif type == "OTHER":
        pretty = "Other"
    elif type == "SKT350":
        pretty = "SKT 350"
    elif type == "SOFTSTOP":
        pretty = "SoftStop"
    elif type == "TURNDOWN":
        pretty = "Turndown"
    elif type == "XLITE":
        pretty = "X-Lite"

    for textElement in arcpy.mapping.ListLayoutElements(map, "TEXT_ELEMENT"):
        if textElement.name == "title":
            textElement.text = "Guardrail End Treatments: " + pretty
    arcpy.RefreshActiveView()


    for lyr in arcpy.mapping.ListLayers(map, "", dataFrame):
       if lyr.name == "GETdisplay":
           lyr.definitionQuery = "TreatmentType = '" + type + "'"
    arcpy.RefreshActiveView()
    arcpy.mapping.ExportToPDF(map, output + "StatewideGET_" + type + ".pdf")
    print pretty + " done."
del map
del dataFrame
print "that's all folks!!"