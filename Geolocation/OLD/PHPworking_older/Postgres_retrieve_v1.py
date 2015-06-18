import arcpy, psycopg2, datetime, os
now = datetime.datetime.now()
today = now.strftime("%m"+"/"+"%d"+"/"+"%Y")
year = now.strftime("%Y")


roadways = "Database Connections\\Connection to Comanche.sde\\TPP_GIS.APP_TPP_GIS_ADMIN.Roadways\\TPP_GIS.APP_TPP_GIS_ADMIN.Linework_Collected"
# Connect to an existing database
conn = psycopg2.connect("dbname=postgres user=adam password=test host=mypostgres.ceiqkhgminol.us-west-2.rds.amazonaws.com port=5432")
print "connected"
# Open a cursor to perform database operations
cur = conn.cursor()

# Query the database and obtain data as Python objects
#cur.execute("INSERT INTO geolocation VALUES ('LINE', '660AA7874', '', '6664');")
#conn.commit()
#print "commited"

cur.execute("SELECT * FROM geolocation;")
#all = cur.fetchall()
C:\Program Files (x86)\Boundless\OpenGeo\pgsql\bin
pgsql2shp -f C:\TxDOT\Scripts\Geolocation\tester2.shp -h mypostgres.ceiqkhgminol.us-west-2.rds.amazonaws.com -u adam -P test -g WGS84 postgres "SELECT * FROM geolocation;"
#cursor = arcpy.InsertCursor(roadways)
# counter = 0
# for i in cur:
	# feat_type = i[0]
	# rte_id = i[1]
	# rte_prfx = i[2]
	# rte_nbr = i[3]
	# rdbd_type = i[4]
	# colln_dt = i[5]
	# colln_accry = i[6]
	# alt = i[7]
	# spd = i[8]
	# hdg = i[9]
	# alt_accry = i[10]
	# avg_accry = i[11]
	# worst_accry = i[12]
	# best_accry = i[13]
	# avg_spd = i[14]
	# slow_spd = i[15]
	# fast_spd = i[16]
	# avg_alt_accry = i[17]
	# worst_alt_accry = i[18]
	# best_alt_accry = i[19]
	# avg_hdg = i[20]
	# hwy_dsgn = i[21]
	# srfc_type = i[22]
	# nbr_lanes = i[23]
	# full_st_nm = i[24]
	# rdway_feat_cd = i[25]
	# intsect_feat_type = i[26]
	# rdsd_feat_type = i[27]
	# cmnt = i[28]
	# shape = i[29]
	
	# counter += 1
	# print "Row: " + counter + " - " + rte_id
	
	
	
	# row = cursor.newRow()
	# if feat_type == "LINE":
		# row.setValue("RTE_NM", rte_id)

		# if rte_prfx == "AA":
			# row.setValue("RTE_CLASS", 2)
		# elif rte_prfx == "FC":
			# row.setValue("RTE_CLASS", 3)
		# elif rte_prfx == "CS":
			# row.setValue("RTE_CLASS", 4)
		# elif rte_prfx == "NA":
			# row.setValue("RTE_CLASS", 5)
		# else:
			# row.setValue("RTE_CLASS", 1)
		
		
		# if hwy_dsgn == 1 or hwy_dsgn == 3:
			# row.setValue("RTE_DIR", "ONE WAY")
		# else hwy_dsgn == 2:
			# row.setValue("RTE_DIR", "TWO WAY")
		
		# row.setValue("RTE_PRFX", rte_prfx)
		# row.setValue("RTE_NBR", rte_nbr)
		# row.setValue("CMNT", cmnt)
		
		# if rdbd_type == "KG":
			# row.setValue("RDBD_TYPE", 1)
		# elif rdbd_type == "LG":
			# row.setValue("RDBD_TYPE", 2)
		# elif rdbd_type == "RG":
			# row.setValue("RDBD_TYPE", 3)
		# elif rdbd_type == "XG":
			# row.setValue("RDBD_TYPE", 4)
		# elif rdbd_type == "AG":
			# row.setValue("RDBD_TYPE", 5)
		# elif rdbd_type == "MG":
			# row.setValue("RDBD_TYPE", 12)
		# elif rdbd_type == "SG":
			# row.setValue("RDBD_TYPE", 13)
		# elif rdbd_type == "PG":
			# row.setValue("RDBD_TYPE", 10)
		# elif rdbd_type == "TG":
			# row.setValue("RDBD_TYPE", 11)
		# elif rdbd_type == "YG":
			# row.setValue("RDBD_TYPE", 14)
		# elif rdbd_type == "BG":
			# row.setValue("RDBD_TYPE", 15)
		# elif rdbd_type == "CONNECTOR":
			# row.setValue("RDBD_TYPE", 7)
		# elif rdbd_type == "RAMP":
			# row.setValue("RDBD_TYPE", 6)
		# elif rdbd_type == "TURNAROUND":
			# row.setValue("RDBD_TYPE", 8)
		# else:
			# row.setValue("RDBD_TYPE", 9)
		
		# row.setValue("RTE_ORDER", 0)
		# row.setValue("PROPOSED", 0)
		# row.setValue("FULL_ST_NM", full_st_nm)
		# row.setValue("EDIT_DT", colln_dt + " " + today)
		# row.setValue("EDIT_NM", "GEOLOCATION APP")
		# row.setValue("RTE_ID", rte_id)
		# row.setValue("PREP_TYPE", "N")
		# row.setValue("INV_STATUS", "Y")
		# row.setValue("INV_NOTES", cmnt)
		# row.setValue("SURF_TYPE", srfc_type)
		# row.setValue("H_DESI", hwy_dsgn)
		# row.setValue("NUM_LAN", nbr_lanes)
		# row.setValue("INV_DATE", today)
		# row.setValue("INV_CREW", "GEOLOCATION APP")
		
		# if rte_prfx == "AA":
			# cnty = rte_id[-3]
			# row.setValue("CNUMTXT", cnty)
		
		# row.setValue("INV_EXISTS", "Y")
		# row.setValue("INV_YEAR", year)
		
		
		
	
	# cursor.insertRow(row)
	
	# print rte_id

# Make the changes to the database persistent
#cur.execute("DELETE FROM geolocation;")
#conn.commit()




# Close communication with the database
cur.close()
conn.close()

print "that's all folks!"