

import json
import threading
import time
import paho.mqtt.client as mqtt
import alphabot.servo as servo
import alphabot.controller as controller


FACE_DISTANCE_THRESHOLD = 150
CAMERA_CENTER_ANGLE = 95


class State:
    camera_angle = CAMERA_CENTER_ANGLE
    search_direction = 1
    search_range = [20, 170]

    face = 0
    face_position = 0
    face_size = 0
    no_face_time = 0


def search_face():
    State.camera_angle += State.search_direction
    if State.camera_angle <= State.search_range[0]:
        State.search_direction = 1
    elif State.camera_angle >= State.search_range[1]:
        State.search_direction = -1
    
    servo.write(1, State.camera_angle)

def track_face():
    if State.camera_angle > CAMERA_CENTER_ANGLE:
        State.camera_angle -= 1
    elif State.camera_angle < CAMERA_CENTER_ANGLE:
        State.camera_angle += 1

    servo.write(1, State.camera_angle)

    if controller.is_edge():
        controller.t_down(20, 0.2)
    else:
        if State.face_position < -FACE_DISTANCE_THRESHOLD:
            controller.t_right(40, 0.02)
        elif State.face_position > FACE_DISTANCE_THRESHOLD:
            controller.t_left(40, 0.02)
        else:
            controller.t_up(20, 0.2)

    controller.t_stop(0.5)


def task():
    while True:
        if not State.face:
            search_face()
        elif State.no_face_time == 0:
            print((State.face_position, State.camera_angle, controller.is_edge()))
            track_face()

        time.sleep(0.05)



thread = threading.Thread(target=task)
thread.daemon = True
thread.start()


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    client.subscribe("bus")

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    if msg.topic == 'bus':
        try:
            data = json.loads(msg.payload)
            if data[0] == 0:
                if State.no_face_time > 20:
                    State.face = 0
                else:
                    State.no_face_time += 1
            else:
                State.no_face_time = 0
                State.face = data[0]
                State.face_position = (data[1] + data[3] - 640)
                State.face_size = data[3] = data[1]
        except Exception as e:
            print(e)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)
client.loop_forever()