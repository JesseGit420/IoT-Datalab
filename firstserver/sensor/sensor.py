# Nep-sensor: een stekker met een laptop aan, en af en toe de waterkoker
import json, os, random, time
import paho.mqtt.client as mqtt

def na_verbinden(client, userdata, flags, reden, properties):
    print("Verbinden met de broker:", reden)
    client.publish("stekker/status", "online")
kwh = 0
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.will_set("stekker/status", "offline" , qos=1, retain=True)
client.username_pw_set("sensor", os.environ["SENSOR_WACHTWOORD"])
client.on_connect = na_verbinden
client.connect("mosquitto", 1883)   # de broker, op zijn servicenaam
client.loop_start()                 # paho houdt de verbinding open

while True:
    time.sleep(5)
    meting = {
        "spanning": round(random.uniform(228, 234), 1),
        "vermogen": round(random.uniform(60, 80)),
    }
    if random.random() < 0.1:       # één kans op tien: de waterkoker
        meting["vermogen"] += 2000
    meting["stroom"] = round(meting["vermogen"]/meting["spanning"], 2)
    kwh += round((meting["vermogen"])*0.001388, 2) /1000
    meting["energie"]  = kwh
    bericht = json.dumps(meting)
    client.publish("stekker/meting", bericht)
    print(bericht)
