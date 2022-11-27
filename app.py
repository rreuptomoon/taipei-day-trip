from flask import *
from flask import Flask, render_template, request, redirect,session,jsonify,make_response
import mysql.connector 
from mysql.connector import pooling
import numpy as np     
import json
from flask_cors import CORS

app=Flask(__name__)
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True


dbconfig={
    "user" : "root",
    "password" : "",
    "host" : "localhost",
    "database" : "taipei",
}

connection_pool = mysql.connector.pooling.MySQLConnectionPool(
    pool_name = "data_pool",
    pool_size = 5,
    pool_reset_session = True,
    **dbconfig
)
# Pages


@app.errorhandler(400)
def error_entry(e):
	return jsonify({"error":True,
					"message":"景點編號不正確"})

@app.errorhandler(404)
def Not_Found(e):
	return jsonify({"error":True,
					"message":"Not_Found"})
					
@app.errorhandler(500)
def server_error(e):
	return jsonify({"error":True,
					"message":"wrong entry"})

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/api/attractions",methods=["GET"])
def attraction():
	page=request.args.get("page")
	keyword=request.args.get("keyword")
	page=int(page)
	startpage=1
	nextpage=page+startpage
	perpage_count=12
	offset_count=page*perpage_count

	if  keyword == "":	#http://127.0.0.1:3000/api/attractions?page=1&keyword=

		return Not_Found(404)

	if keyword :
				try:
					key='%'+keyword+'%'
					connection = connection_pool.get_connection()
					mycursor =  connection.cursor()
					mycursor.execute('SELECT `taipei-attractions`.`id`,`taipei-attractions`.`name`,`taipei-attractions`.`category`,`taipei-attractions`.`description`,`taipei-attractions`.`address`,`taipei-attractions`.`transport`, `taipei-attractions`.`MRT`,`taipei-attractions`.`latitude`,`taipei-attractions`.`longitude`,group_concat(`img`.`images` ) FROM  `taipei-attractions` INNER JOIN `img` ON `taipei-attractions`.id = `img`.`taipei-att_id` WHERE  `category` = %s OR `name` LIKE %s group by `taipei-attractions`.`id` LIMIT %s OFFSET %s' ,(keyword,key,perpage_count,offset_count))
					datas=mycursor.fetchall()
					data_count=len(datas)
					alldata=[]
					for data in range(len(datas)):
						images=datas[data][9].replace(","," , ")
						alldata.append({
							"id":datas[data][0],
							"name":datas[data][1],
							"category":datas[data][2],
							"description":datas[data][3],
							"address":datas[data][4],
							"transport":datas[data][5],
							"mrt":datas[data][6],
							"lat":datas[data][7],
							"lng":datas[data][8],
							"images":(images.split(","))
						})
					
					if data_count == perpage_count:
							return  jsonify({"nextpage":nextpage,
												"data":alldata})
					else:		
						return jsonify({"nextpage":None,
										"data":alldata})
							
				finally:
						mycursor.close()
						connection.close()

	if page >= 0 : #include 0	#http://127.0.0.1:3000/api/attractions?page=1
			try: #
					connection = connection_pool.get_connection()
					mycursor =  connection.cursor()
					mycursor.execute('SELECT `taipei-attractions`.`id`,`taipei-attractions`.`name`,`taipei-attractions`.`category`,`taipei-attractions`.`description`,`taipei-attractions`.`address`,`taipei-attractions`.`transport`, `taipei-attractions`.`MRT`,`taipei-attractions`.`latitude`,`taipei-attractions`.`longitude`,group_concat(`img`.`images` ) FROM  `taipei-attractions` INNER JOIN `img` ON `taipei-attractions`.id = `img`.`taipei-att_id` group by `taipei-att_id` LIMIT %s OFFSET %s ',(perpage_count,offset_count))
					datas=mycursor.fetchall()
					data_count=len(datas)
					alldata=[]
					for data in range(len(datas)):
						images=datas[data][9].replace(","," , ")
						alldata.append({
							"id":datas[data][0],
							"name":datas[data][1],
							"category":datas[data][2],
							"description":datas[data][3],
							"address":datas[data][4],
							"transport":datas[data][5],
							"mrt":datas[data][6],
							"lat":datas[data][7],
							"lng":datas[data][8],
							"images":(images.split(","))
						})
					
					if data_count == perpage_count:
							return  jsonify({"nextpage":nextpage,
												"data":alldata})
					else:		
						return jsonify({"nextpage":None,
										"data":alldata})
			finally:
						mycursor.close()
						connection.close()
	
	return render_template("attraction.html")


@app.route("/api/attractions/<id>",methods=["GET"])
def attraction_id(id): #http://127.0.0.1:3000/api/attractions/10
	if id != None:
		try:
			connection_object = connection_pool.get_connection()
			mycursor =  connection_object.cursor()
			mycursor.execute('SELECT `taipei-attractions`.`id`,`taipei-attractions`.`name`,`taipei-attractions`.`category`,`taipei-attractions`.`description`,`taipei-attractions`.`address`,`taipei-attractions`.`transport`, `taipei-attractions`.`MRT`,`taipei-attractions`.`latitude`,`taipei-attractions`.`longitude`,group_concat(`img`.`images` ) FROM  `taipei-attractions` INNER JOIN `img` ON `taipei-attractions`.id = `img`.`taipei-att_id` WHERE `taipei-attractions`.`id` = %s group by `taipei-att_id`',(id,))
			datas=mycursor.fetchone()
			datas=list(datas)
			images=datas[9].replace(","," , ")
			data={
					"id":datas[0],
					"name":datas[1],
					"category":datas[2],
					"description":datas[3],
					"address":datas[4],
					"transport":datas[5],
					"mrt":datas[6],
					"lat":datas[7],
					"lng":datas[8],
					"images":(images.split(","))
							}
			if datas:
					return jsonify({"data":data})
			else:
				return jsonify({"error":True,
								"message":"景點編號不正確"})
		except:
		  		return server_error(500)
			
		finally:
			mycursor.close()
			connection_object.close()
			
	return render_template("attraction.html")
				


@app.route("/api/categories")
def categories(): #http://127.0.0.1:3000/api/categories
		try:
			connection_object = connection_pool.get_connection()
			mycursor =  connection_object.cursor()
			mycursor.execute('SELECT `category` FROM `taipei-attractions` group by `category`')
			datas=mycursor.fetchall()
			for data in range(len(datas)):
				print(data)
			if data:
				return  jsonify({"data":datas})
			return server_error(500)
		finally:
				mycursor.close()
				connection_object.close()
		return render_template("attraction.html")

# @app.route("/booking")
# def booking():
# 	return render_template("booking.html")
# @app.route("/thankyou")
# def thankyou():
# 	return render_template("thankyou.html")

app.run(host='0.0.0.0',port=3000)

