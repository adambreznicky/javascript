__file__ = 'mySQL_retrieve_v1'
__date__ = '4/8/14'
__author__ = 'ABREZNIC'

import MySQLdb


db = MySQLdb.connect(host="sql306.byethost7.com", user="b7_13340779", passwd="Hendrix9", db="b7_13340779_geolocation")
					 
print "connected"
# you must create a Cursor object. It will let
#  you execute all the queries you need
cur = db.cursor()

# Use all the SQL you like
cur.execute("SELECT * FROM geolocation_data")

# print all the first cell of all the rows
for row in cur.fetchall() :
    print row

print "that's all folks!"
