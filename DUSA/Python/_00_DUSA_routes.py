'''
In this use-case, you will run the script by sending the saved
    FGDB and FeatureClass location as arguments.
Routing will produce a new Featureclass that can be checked against
    the original roads by using the Symmetrical Difference tool.
All the lolipop and baloon alignments (loops) will not make it through the routing process
    because the assets are not in GRID yet due to a grub.  Once we get these in grid they should route correctly.
'''

import os
from arcpy import env
import _01_create_fc_grid_export_v1
import _02_create_fc_updates_v1
import _03_create_routes_v1
import _04_recalc_Lengths_v1


env.workspace = 'in_memory'

_01_create_fc_grid_export_v1.process()
_02_create_fc_updates_v1.process()

fgdb = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Publish.gdb')
local_streets = os.path.join(fgdb,'LocalStreets_Export')
county_roads = os.path.join(fgdb,'CountyRoads_Export')
roads = [local_streets, county_roads]
_03_create_routes_v1.main(fgdb,roads)

_04_recalc_Lengths_v1.process()

print "that's all folks!!"

