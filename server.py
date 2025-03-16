from flask import Flask, jsonify
import paho.mqtt.client as mqtt
import json
import os

app = Flask(__name__)

# Global variable to store the latest data
latest_data = {}

# MQTT Configuration
MQTT_BROKER = "a33kmmzjqzsgb9-ats.iot.us-east-1.amazonaws.com"
MQTT_PORT = 8883
MQTT_TOPIC = "gym/sensor/data"

# Fixed on_connect callback (4 parameters for VERSION1)
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe(MQTT_TOPIC)
    print(f"Subscribed to topic: {MQTT_TOPIC}")

def on_message(client, userdata, msg):
    global latest_data
    try:
        payload = msg.payload.decode("utf-8")
        latest_data = json.loads(payload)
        print(f"Received data: {latest_data}")
    except Exception as e:
        print(f"Error processing message: {e}")

# Configure MQTT client with VERSION1 explicitly
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)  # Critical fix
client.on_connect = on_connect
client.on_message = on_message

# TLS configuration (verify certificate paths)
client.tls_set(
    ca_certs="AmazonRootCA1.pem",
    certfile="de963c1dcb7222f786c096fcf50915124c2fec94c441a6c5d888abc5685ad787-certificate.pem.crt",
    keyfile="de963c1dcb7222f786c096fcf50915124c2fec94c441a6c5d888abc5685ad787-private.pem.key"
)

client.connect(MQTT_BROKER, MQTT_PORT)
client.loop_start()

@app.route("/data", methods=["GET"])
def get_data():
    return jsonify(latest_data)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
