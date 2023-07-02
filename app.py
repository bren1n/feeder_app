import json
from flask import Flask, render_template
from flask_mqtt import Mqtt
from flask_socketio import SocketIO
from ssl import PROTOCOL_TLS


app = Flask(__name__)

app.config['TEMPLATES_AUTO_RELOAD'] = True

app.config['MQTT_BROKER_URL'] = 'a6f482a56f444686828e98b0d3302672.s1.eu.hivemq.cloud'
app.config['MQTT_BROKER_PORT'] = 8883
app.config['MQTT_USERNAME'] = 'testuser'
app.config['MQTT_PASSWORD'] = 'testpassword'
app.config['MQTT_KEEPALIVE'] = 5
app.config['MQTT_TLS_ENABLED'] = True
app.config['MQTT_TLS_VERSION'] = PROTOCOL_TLS
topic = '/plat/food'

mqtt = Mqtt(app)
socketio = SocketIO(app)

@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
   if rc == 0:
       print('Connected successfully')
       mqtt.subscribe(topic) # subscribe topic
   else:
       print('Bad connection. Code:', rc)

@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
   data = dict(
       topic=message.topic,
       payload=message.payload.decode()
  )
   print('Received message on topic: {topic} with payload: {payload}'.format(**data))
   socketio.emit('food', data=data)

@app.route("/")
def hello_world():
    return render_template("index.html")

@socketio.on('schedule')
def handle_publish(json_str):
    data = json.loads(json_str)
    mqtt.publish(data['topic'], data['payload'])

@socketio.event
def connect():
    print('Client connected')

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0')