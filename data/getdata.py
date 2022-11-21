from flask import *
import mysql.connector 
from mysql.connector import pooling     
import json
import re

app=Flask(__name__)

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

json_data=open("taipei-attractions.json",encoding="utf-8").read()
json_obj=json.loads(json_data)
datas=json_obj["result"]["results"]




try:
    connection=connection_pool.get_connection()
    mycursor=connection.cursor()
    for data in datas:
        id=data.get("_id")
        name=data.get("name")
        Category=data.get("CAT")
        description=data.get("description")
        address=data.get("address")
        transport=data.get("direction")
        MRT=data.get("MRT")
        longitude=data.get("longitude")
        latitude=data.get("latitude") 
        print(latitude)
        sql="INSERT INTO `taipei-attractions`(`id`,`name`,`Category`,`description`,`address`,`transport`,`MRT`,`longitude`,`latitude`)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        val=(id,name,Category,description,address,transport,MRT,longitude,latitude)               
        mycursor.execute(sql,val)
        connection.commit()
    
finally:
        mycursor.close()
        connection.close()

try:
    connection=connection_pool.get_connection()
    mycursor=connection.cursor(dictionary=True)
    for data in datas:
        taipei_att_id=data.get("_id")
        file=data.get("file")
        file=data["file"].lower() #class :str
        img=file.replace("jpg","jpg\n")
        img=re.split('\n',img)# images="\n".join(images)
        images=[]
        for match in img:
            if "jpg" in match:
                        images.append(match)
        for image in images:
        # images="\n".join(images)
        # images=images.replace("https","'https").replace("jpg","jpg',\n")
        # print(images)
            sql="INSERT INTO `IMG`(`taipei-att_id`,`images`)VALUES(%s,%s)"
            val=(taipei_att_id,image)               
            mycursor.execute(sql,val)
            connection.commit()
finally:
        mycursor.close()
        connection.close()


# for image in zip(range(len(images)), images):
# print(image{i})   