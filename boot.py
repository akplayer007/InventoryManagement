# Complete project details at https://RandomNerdTutorials.com

import time
from umqttsimple import MQTTClient
import ubinascii
import machine
import micropython
import network
import esp
import gc

import machine, neopixel
import network
import time
from umqttsimple import MQTTClient
import ubinascii
import machine
import micropython
import esp


esp.osdebug(None)
gc.collect()

ssid = 'voorraadbeheer'
password = 'welkom01'
mqtt_server = '10.3.141.1'
#EXAMPLE IP ADDRESS
#mqtt_server = '192.168.1.144'
client_id = ubinascii.hexlify(machine.unique_id())


last_message = 0
message_interval = 5
counter = 0

station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
  pass

print('Connection successful')
print(station.ifconfig())


# #########################

sta_if = network.WLAN(network.STA_IF)
ap_if = network.WLAN(network.AP_IF)
mqtt_server = '10.3.141.1'
topic_sub = b'Kabels/5.2 mm kabel'
topic_pub = b'hello'
client_id = ubinascii.hexlify(machine.unique_id())
np = neopixel.NeoPixel(machine.Pin(15), 4)

topiclist = [b"Kabels/1 mm kabel", b"Kabels/2.5 mm kabel", b"Kabels/4.5 mm kabel", b"Kabels/5.2 mm kabel"]
buttonlist = [b'0', b'1', b'2', b'3', b'4', b'5', b'6', b'7', b'8', b'9' ]


light_dict = {
  b'0': (255, 0, 0),
  b'1': (0, 255, 0),
  b'2': (0, 0, 255),
  b'3': (85, 85, 85),
  
}

dark_dict = {
  b'0': (0, 0, 0),
  b'1': (0, 0, 0),
  b'2': (0, 0, 0),
  b'3': (0, 0, 0),
  
}

def subscribe_to_topics(client):

  topic_list = [b"Kabels/1 mm kabel", b"Kabels/2.5 mm kabel", b"Kabels/4.5 mm kabel", b"Kabels/5.2 mm kabel"]
  
  for topic in topic_list:
    client.subscribe(topic)
  
  return client

def sub_cb(topic, msg):
    light = light_dict[msg]
    dark = dark_dict[msg]
    np[int(msg)] = light
    np.write()
    time.sleep(3)
    np[int(msg)] = dark
    np.write()
    print('sub_cb')
    
def connect_and_subscribe():
  global client_id, mqtt_server, topic_sub
  client = MQTTClient(client_id, mqtt_server)
  client.set_callback(sub_cb)
  client.connect()
  client = subscribe_to_topics(client)
  client.set_callback(sub_cb)
  print('Connected to MQTT broker')
  return client

def restart_and_reconnect():
  print('Failed to connect to MQTT broker. Reconnecting...')
  time.sleep(10)
  machine.reset()
  
def run():


  while True:
    try:
      client = connect_and_subscribe()
    except OSError as e:
      restart_and_reconnect()

# #########################
run()
print('Done')

