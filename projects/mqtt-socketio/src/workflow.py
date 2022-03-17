from sys import stderr
import paho.mqtt.client as mqtt
import time
import subprocess
from subprocess import PIPE


TOPIC = 'clients/'
HOST = '127.0.0.1'
PORT = 1883
KEEP_ALIVE = 60


def on_connect(client, userdata, flags, rc):
    print("Connected to the MQTT broker with result code " + str(rc))


def on_disconnect(client, userdata, rc):
    if rc != 0:
        print("Unexpected disconnection.")
    else:
        print('Successfully disconnected from the MQTT broker.')


def docker_command(cmd):
    process = subprocess.Popen(cmd, stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    print(stdout)
    print(stderr)


def publish_message(topic, msg, client_id):
    client = mqtt.Client(client_id=client_id)

    client.on_connect = on_connect
    client.on_disconnect = on_disconnect

    client.connect(HOST, PORT, KEEP_ALIVE)
    client.loop_start()
    time.sleep(1)
    client.publish(topic, msg)
    time.sleep(1)
    client.loop_stop()
    client.disconnect()


def process_client(topic, msg, client_id):
    proper_topic = TOPIC + topic
    publish_message(proper_topic, msg, client_id)


def main():
    # publish_message(topic='clients/topic1',
    #                 msg=f'message #{1}', c_id=f'client{1}')
    cmd = ['docker', 'exec', 'ubuntu', 'uname', '-a']
    docker_command(cmd)


if __name__ == '__main__':
    main()
