__file__ = 'uploadUpdates_v1'
__date__ = '11/18/2015'
__author__ = 'ABREZNIC'
import arcpy


updateClass = arcpy.GetParameterAsText(0)
input = arcpy.GetParameterAsText(1)

fs = arcpy.FeatureSet()
fs.load(input)

