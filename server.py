from flask import Flask, jsonify
import paho.mqtt.client as mqtt
import json

app = Flask(__name__)

# Store the latest data
latest_data = {}

# MQTT Configuration
MQTT_BROKER = "a33kmmzjqzsgb9-ats.iot.us-east-1.amazonaws.com"
MQTT_PORT = 8883
MQTT_TOPIC = "gym/sensor/data"

# Callback function when message is received
def on_message(client, userdata, message):
    global latest_data
    payload = message.payload.decode('utf-8')
    latest_data = json.loads(payload)
    print(f"Received data: {latest_data}")

# MQTT Client Setup
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

client.on_message = on_message
client.tls_set("AmazonRootCA1.pem", "de963c1dcb7222f786c096fcf50915124c2fec94c441a6c5d888abc5685ad787-certificate.pem.crt", "de963c1dcb7222f786c096fcf50915124c2fec94c441a6c5d888abc5685ad787-private.pem.key") 
client.connect(MQTT_BROKER, MQTT_PORT)
client.subscribe(MQTT_TOPIC)
client.loop_start()

# Flask API Endpoint to Serve Data
import os

@app.route('/data', methods=['GET'])
def get_data():
    try:
        file_path = os.path.join(os.path.dirname(__file__), 'data.json')
        with open(file_path, 'r') as file:
            data = json.load(file)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    
if __name__ == '__main__':
    app.run(debug=True)

