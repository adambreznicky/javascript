'''
Will Need cx_Oracle installed
'''
import os.path
import arcpy
from arcpy import env
import cx_Oracle
import datetime

#set Environment Variables
env.workspace = 'in_memory'
env.qualifiedFieldNames = False
env.overwriteOutput = True


#Declare Table Schemas
def create_schema():
    srfcTable = "SRFC_TABLE"
    srfcSchema = [
                ['GID', 'LONG'],
                ['BEGIN_DFO', 'DOUBLE'],
                ['END_DFO', 'DOUBLE'],
                ['SURFACE', 'TEXT'],
            ]
    srfcSQL = '''SELECT 
                      GRIDOP.ASSET.RDBD_GMTRY_LN_ID         AS GID,
                      GRIDOP.ASSET_LN.ASSET_LN_BEGIN_DFO_MS AS BEGIN_DFO,
                      GRIDOP.ASSET_LN.ASSET_LN_END_DFO_MS   AS END_DFO,
                      GRIDOP.SRFC_TYPE.SRFC_TYPE_CD         AS SURFACE
                    FROM GRIDOP.SRFC_TYPE
                    INNER JOIN GRIDOP.RDBD_SRFC
                    ON GRIDOP.SRFC_TYPE.SRFC_TYPE_ID = GRIDOP.RDBD_SRFC.SRFC_TYPE_ID
                    INNER JOIN GRIDOP.ASSET_LN
                    ON GRIDOP.ASSET_LN.ASSET_ID = GRIDOP.RDBD_SRFC.ASSET_ID
                    INNER JOIN GRIDOP.ASSET
                    ON GRIDOP.ASSET.ASSET_ID = GRIDOP.ASSET_LN.ASSET_ID
                    '''

    dsgnTable = 'DSGN_TABLE'
    dsgnSchema = [
                ['GID', 'LONG'],
                ['BEGIN_DFO', 'DOUBLE'],
                ['END_DFO', 'DOUBLE'],
                ['DESIGN', 'TEXT'],
            ]
    dsgnSQL = '''SELECT 
                      GRIDOP.ASSET.RDBD_GMTRY_LN_ID             AS GID,
                      GRIDOP.ASSET_LN.ASSET_LN_BEGIN_DFO_MS     AS BEGIN_DFO,
                      GRIDOP.ASSET_LN.ASSET_LN_END_DFO_MS       AS END_DFO,
                      GRIDOP.RDWAY_DSGN_TYPE.RDWAY_DSGN_TYPE_CD AS DESIGN
                    FROM GRIDOP.RDWAY_DSGN
                    INNER JOIN GRIDOP.RDWAY_DSGN_TYPE
                    ON GRIDOP.RDWAY_DSGN_TYPE.RDWAY_DSGN_TYPE_ID = GRIDOP.RDWAY_DSGN.RDWAY_DSGN_TYPE_ID
                    INNER JOIN GRIDOP.ASSET_LN
                    ON GRIDOP.ASSET_LN.ASSET_ID = GRIDOP.RDWAY_DSGN.ASSET_ID
                    INNER JOIN GRIDOP.ASSET
                    ON GRIDOP.ASSET.ASSET_ID = GRIDOP.ASSET_LN.ASSET_ID
                    '''

    laneTable = 'NBR_LANE_TABLE'
    laneSchema = [
                ['GID', 'LONG'],
                ['BEGIN_DFO', 'DOUBLE'],
                ['END_DFO', 'DOUBLE'],
                ['NUM_LANES', 'LONG'],
            ]
    laneSQL = '''SELECT 
                      GRIDOP.ASSET.RDBD_GMTRY_LN_ID          AS GID,
                      GRIDOP.ASSET_LN.ASSET_LN_BEGIN_DFO_MS  AS BEGIN_DFO,
                      GRIDOP.ASSET_LN.ASSET_LN_END_DFO_MS    AS END_DFO,
                      GRIDOP.NBR_THRU_LANE.NBR_THRU_LANE_CNT AS NUM_LANES
                    FROM GRIDOP.NBR_THRU_LANE
                    INNER JOIN GRIDOP.ASSET_LN
                    ON GRIDOP.ASSET_LN.ASSET_ID = GRIDOP.NBR_THRU_LANE.ASSET_ID
                    INNER JOIN GRIDOP.ASSET
                    ON GRIDOP.ASSET.ASSET_ID = GRIDOP.ASSET_LN.ASSET_ID
                    '''
    
    schemaList = [[srfcTable,srfcSchema,srfcSQL], [dsgnTable,dsgnSchema,dsgnSQL], [laneTable,laneSchema,laneSQL]]
    return schemaList

#Method to build and populate tables
def buildTable(con, tableName, tableSchema, tableSQL):
    print "Building Table: " + tableName
    arcpy.CreateTable_management(env.workspace, tableName)
    schemaFields = []
    for field in tableSchema:
        schemaFields.append(field[0])
        arcpy.AddField_management(tableName,
                                  field_name=field[0],
                                  field_type=field[1])

    cursed = con.cursor()
    rows = cursed.execute(tableSQL)
    #cursed.execute(tableSQL)
    #rows = cursed.fetchmany(500)
    print "Inserting rows..."
    with arcpy.da.InsertCursor(tableName,schemaFields) as icursed:
        for row in rows:
            icursed.insertRow(row)
    cursed.close()

#Route Events, Join Fiellds, Save Final FeatureClass
def route_events(fgdb,roads,eventTables):
    whole_layerName = os.path.basename(roads)
    layerName = whole_layerName.split("_")[0]
    routeProps = 'GID LINE BEGIN_DFO END_DFO'
    savedFc = os.path.join(fgdb,layerName)
    print "Routing events for: " + layerName

    arcpy.OverlayRouteEvents_lr(eventTables[0], routeProps, eventTables[1], routeProps, 'UNION', 'TEMP_ROUTE',routeProps)
    arcpy.OverlayRouteEvents_lr('TEMP_ROUTE', routeProps, eventTables[2], routeProps, 'UNION', 'FIN_ROUTE',routeProps)
    arcpy.MakeRouteEventLayer_lr(roads, "GID", "FIN_ROUTE",routeProps, "Routed_Temp",'','ERROR_FIELD')
    arcpy.Select_analysis('Routed_Temp', savedFc, "LOC_ERROR = 'NO ERROR'")
    arcpy.DeleteField_management(savedFc,['LOC_ERROR','BEGIN_DFO', 'END_DFO'])
    view_name = layerName + "_View"
    arcpy.MakeTableView_management(roads, out_view=view_name)
    if layerName == 'LocalStreets':
        arcpy.JoinField_management(savedFc, "GID", view_name, "GID", "ROUTE_ID;STREET_NM;PRIME_ADMN;ADMN_TYPE;ADMN_ACRNM;COG_NM;COG_ACRNM;TxDOT_DIST;DIST_ACRNM;LENGTH")
    elif layerName == 'CountyRoads':
        print('Create Join for County Roads')
        arcpy.JoinField_management(savedFc, "GID", view_name, "GID", "ROUTE_ID;STREET_NM;CNTY_NM;CNTY_NBR;TxDOT_DIST;LENGTH")
#Main Process to kick off creation of Routed FeatureClass
def main(fgdb, roads):
    schemaList = create_schema()
    eventTables = []
    
    print('Creating Event Tables')
    try:
        con = cx_Oracle.connect('app_texas_grid_rpt/semperfi@//oracle-amazon-gridprod:1521/GRIDDB')
        for schema in schemaList:
            buildTable(con,schema[0], schema[1], schema[2])
            eventTables.append(schema[0])
    finally:
        con.close()
    
    print('Routing Events to FeatureClass')
    now = datetime.datetime.now()
    print now
    for road_class in roads:
        route_events(fgdb,road_class,eventTables)
    now = datetime.datetime.now()
    print now
    
if __name__ == "__main__":
    print('\n')
    fgdb = raw_input("Please enter complete path to File Geodatabase: ")
    print('\n')
    roads = os.path.join(fgdb, raw_input("Please enter name of roads FeatureClass: "))
    main(fgdb,roads)