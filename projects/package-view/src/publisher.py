import paho.mqtt.client as mqtt
import time
# The callback for when the client receives a CONNACK response from the server.


def on_connect(client, userdata, flags, rc):
    print("Connected to the MQTT broker with result code " + str(rc))


def on_disconnect(client, userdata, rc):
    if rc != 0:
        print("Unexpected disconnection.")
    else:
        print('Successfully disconnected from the MQTT broker.')


client = mqtt.Client(client_id="publisher")

client.on_connect = on_connect
client.on_disconnect = on_disconnect

client.connect("broker.hivemq.com", 1883, 60)
client.loop_start()
for i in range(0, 100):
    client.publish("vm/numbers", i)
    time.sleep(1)
client.loop_stop()
client.disconnect()
