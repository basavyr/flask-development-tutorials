import time
import paho.mqtt.client as paho


# define the server parameters
BROKER = "127.0.0.1"
PORT = 1883
TOPIC = "/test/v1"

# define the client ID
CLIENT_ID = "subscriber"


def on_connect(client, userdata, flags, rc):
    print("Connected to the MQTT broker with result code " + str(rc))


def on_disconnect(client, userdata, rc):
    if rc != 0:
        print("Unexpected disconnection.")
        print(rc)
    else:
        print('Successfully disconnected from the MQTT broker.')


def on_message(client, userdata, message):
    print("Received message '" + str(message.payload) + "' on topic '"
          + message.topic + "' with QoS " + str(message.qos))


client = paho.Client(CLIENT_ID)
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message

client.connect(BROKER, PORT)
client.subscribe(TOPIC)
client.loop_forever()
