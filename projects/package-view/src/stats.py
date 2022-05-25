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


def publish_command(user_id, vm_id):
    client = mqtt.Client(str(user_id))
    client.on_connect = on_connect

    # establish the connection with the broker in order to publish the command
    client.connect(OPENSTACK_BROKER, OPENSTACK_PORT)
    client.loop_start()
    vm_topic = f'{OPENSTACK_TOPIC}{vm_id}'
    stats_command = 'python graphs.py'
    print(f'Will publish on the topic: {vm_topic}')
    client.publish(vm_topic, stats_command)
    client.loop_stop()
