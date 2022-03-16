import paho.mqtt.client as mqtt
import time


TOPIC = 'clients/'
HOST = '127.0.0.1'
PORT = 1883
KEEP_ALIVE = 60


def on_connect(client, userdata, flags, rc):
    print("Connected to the MQTT broker with result code " + str(rc))


def publish_message(topic, msg, c_id):
    client = mqtt.Client(client_id=c_id)
    client.on_connect = on_connect
    client.connect(HOST, PORT, KEEP_ALIVE)
    client.publish(topic, msg)
    client.disconnect()


def process_client(topic, msg, client_id):
    publish_message(topic, msg, client_id)


def main():
    for idx in range(10):
        publish_message(topic='clients/',
                        msg=f'message #{idx}', c_id=f'client{idx}')


if __name__ == '__main__':
    main()
