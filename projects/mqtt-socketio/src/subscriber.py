import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import paho.mqtt.subscribe as subscribe


def on_message(client, userdata, message):
    print("Received message '" + str(message.payload) + "' on topic '"
          + message.topic + "' with QoS " + str(message.qos))


def on_message_print(client, userdata, message):
    print("%s %s" % (message.topic, message.payload))


mqtt.on_message = on_message


msgs = [{'topic': "paho/test/multiple", 'payload': "multiple 1"},
        ("paho/test/multiple", "multiple 2", 0, False)]
# publish.multiple(msgs, hostname="mqtt.eclipseprojects.io")
# subscribe.simple('clients/topics1', 0)
# subscribe.simple([("clients/topic1", 0), ("clients/topic1", 0)])

subscribe.callback(on_message_print, "clients/#", hostname="127.0.0.1")
