# get dependencies
from __future__ import print_function
from uszipcode import ZipcodeSearchEngine
from flask import Flask, jsonify, render_template, request 
import MySQLdb

#Flask setup 
app = Flask(__name__)

# data setup
db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                     user="root",         # your username
                     passwd="AshPon",     # your password
                     db="where_are_your_stores")        # name of the data base 

cur = db.cursor()

sqlStr = ("SELECT njstores.LOCATION_NAME,\
	              njstores.CITY_NAME  \
	         FROM where_are_your_stores.njstores")

# define search object for uszips
search = ZipcodeSearchEngine()
zipcode = search.by_state('New Jersey', returns=0)
# print(zipcode)

# for aRec in zipcode:
# 	print (aRec)


# start the engine
@app.route("/")
def homepage():
	return render_template("index.html")
# define a route called by index and base js
# this route will return all the stores information from the file in a list
# the file I loaded I will convert it into a list and return it 
# you need to assume that you have the list and continue workking
# that cities list in the class code, just replace with a few sample data and go on....

@app.route("/app/yourloc")
def yourLoc():

	# define lists 
	names= []
	# Grab the file and return all store locations
	cur.execute(sqlStr)
	# print all the first cell of all the rows
	for row in cur.fetchall():
		namesDict = {}
		# namesDict["Name"] = "Sample ID"
		# namesDict["Value"] = row[LOCATION_NAME]
		# names.append(namesDict)
		names.append(row)

	#close dbConnection
	db.close()
	return jsonify(names)

@app.route("/app/allZips")
def getZips(baseLat, baseLong, rad):
	# by default it returns only 5 zipcodes
	# res = search.by_coordinate(baseLat, baseLong, radius=rad)
	res = search.by_coordinate(baseLat, baseLong, radius=rad, returns=0)

	allZips = []
	# allPop = []
	# allIncome = []

	for aRec in res:
		# print(aRec.to_json())
		allZips.append(aRec.Zipcode)
		# allPop.append(aRec.Population)
		# allIncome.append(aRec.Total)
	return (allZips)


zipList = getZips(39.122229, -77.133578, 10)

# for zip in zipList:
# 	zipInfo = search.by_zipcode(zip)
# 	print(zipInfo)

#Default app settings
if __name__ == '__main__':
	app.run(debug=True)