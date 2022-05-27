#
#pip install paho-mqtt
#

import paho.mqtt.client as mqttclient
import time

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
	print ("Message received %s" % (str(message.payload.decode("utf-8"))))
	print ("Message topic=%s" %  (message.topic))

connected=False
Messagereceived= False
broker_address="192.168.1.19"
port=1883
user="mqtt_user_ext"
password="123456"

client = mqttclient.Client("MQTT")
client.on_message = on_message
# client.username_pw_set(user, password=password)
client.on_connect = on_connect
client.connect(broker_address, port=port)
client.loop_start()
client.subscribe("iot/message")
while connected != True:
	time.sleep(0.2)
while Messagereceived != True:
	time.sleep(0.2)

client.loop_stop()



