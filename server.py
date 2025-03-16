from flask import Flask, jsonify
import paho.mqtt.client as mqtt
import json
import os

app = Flask(__name__)

# Global variable to store the latest data from AWS IoT
latest_data = {}

# MQTT Configuration
MQTT_BROKER = "a33kmmzjqzsgb9-ats.iot.us-east-1.amazonaws.com"
MQTT_PORT = 8883
MQTT_TOPIC = "gym/sensor/data"

# Callback function when a new MQTT message is received
def on_message(client, userdata, message):
    global latest_data
    try:
        payload = message.payload.decode('utf-8')
        latest_data = json.loads(payload)
        print(f"Received data: {latest_data}")
    except Exception as e:
        print(f"Error processing message: {e}")

# Setup the MQTT client with TLS security
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_message = on_message
client.tls_set("AmazonRootCA1.pem",
               "de963c1dcb7222f786c096fcf50915124c2fec94c441a6c5d888abc5685ad787-certificate.pem.crt",
               "de963c1dcb7222f786c096fcf50915124c2fec94c441a6c5d888abc5685ad787-private.pem.key")
client.connect(MQTT_BROKER, MQTT_PORT)
client.subscribe(MQTT_TOPIC)
client.loop_start()  # Start the MQTT client loop in a separate thread

# Flask API endpoint to return the latest live data
@app.route('/data', methods=['GET'])
def get_data():
    return jsonify(latest_data)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
