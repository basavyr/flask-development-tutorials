import time
import paho.mqtt.client as paho

# define the server parameters
BROKER = "127.0.0.1"
PORT = 1883
TOPIC = "/test/v1"

# define the client ID
CLIENT_ID = "publisher"


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        print("Failed to connect, return code %d\n", rc)


client = paho.Client(CLIENT_ID)

client.on_connect = on_connect

client.connect(BROKER, PORT)

client.loop_start()

# the procedure for sending messages to the subscriber on a particular topic
for idx in range(0, 100):
    publish_procedure = client.publish(TOPIC, 'xxx')
    status = publish_procedure[0]
    print(status)
    time.sleep(2)

client.loop_stop()
