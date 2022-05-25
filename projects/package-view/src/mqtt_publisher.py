import time
import paho.mqtt.client as mqtt

# define the server parameters
OPENSTACK_BROKER = "127.0.0.1"
OPENSTACK_PORT = 1883
OPENSTACK_TOPIC = "/openstack/cloudifin/servers/"


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        print("Failed to connect, return code %d\n", rc)


def publish_command(user_id, vm_id, command):
    client = mqtt.Client(str(user_id))
    client.on_connect = on_connect

    # start the connection in order to publish messages on the proper topic
    client.connect(OPENSTACK_BROKER, OPENSTACK_PORT)
    client.loop_start()
    client.publish(f'{OPENSTACK_TOPIC}{vm_id}', command)
    client.loop_stop()
