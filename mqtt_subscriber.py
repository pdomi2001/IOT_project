#
#pip install paho-mqtt
#
#pip install mysql-connector-python
#

import paho.mqtt.client as mqttclient
import time
import datetime

import mysql.connector

def GetDataArray(line):
	array_singolo_elemento = []
	elements = line.split(";")
	#print(len(elements))
	if len (elements) >= 8:
		array_singolo_elemento = []
		for elemento in elements:
			dati = elemento.split("=")
			array_singolo_elemento.append(dati[-1])
	return array_singolo_elemento

def writeOnDatabase(timestamp, line):
	mydb = mysql.connector.connect(
	  host="localhost",
	  user="paride",
	  password="12345",
	  database="iot"
	)
	dati = GetDataArray(line)
	mycursor = mydb.cursor()

	sql = "INSERT INTO sensori (time, sender_ip, clientID, h_stanza, t_stanza, t_termosifone, count, count_wifi_c, count_mqtt_c) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
	val = (str(timestamp)[:19].replace("-","").replace(".","").replace(":","").replace(" ",""), dati[0], dati[1], dati[2], dati[3], dati[4], dati[5], dati[6], dati[7])

	mycursor.execute(sql, val)

	mydb.commit()
	

def on_connect(client, usedata, flags, rc):
	if (rc == 0):
		print("client is connected")
		global connected
		connected = True
	else:
		print("connection failed")

def on_message(client, userdata, message):
	#	global Messagereceived
	Messagereceived = True
	#print ("Message received %s" % (str(message.payload.decode("utf-8"))))
	#print ("Message topic=%s" %  (message.topic))
	print ("%s;%s" % (datetime.datetime.now(), str(message.payload.decode("utf-8"))))
	f = open("registrazioni.txt", "a")
	f.write("%s;%s\n" % (datetime.datetime.now(), str(message.payload.decode("utf-8"))))
	f.close()
	
	# scrivo anche nel DB
	writeOnDatabase(datetime.datetime.now(), str(message.payload.decode("utf-8")))

connected=False
Messagereceived= False
broker_address="192.168.0.10"
port=1883
user="mqtt_user"
password="123456"

client = mqttclient.Client("MQTT")
#client.username_pw_set(user, password=password)
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker_address, port=port)
client.loop_start()
#client.subscribe("mqtt/firstcode")
client.subscribe("iot/message")
while connected != True:
	time.sleep(0.2)
while Messagereceived != True:
	time.sleep(0.2)
client.loop_stop()



