#!/usr/bin/env python3

from util.mqtt_subscriber import MqttSubscriber
import util.helper as helper

import keyboard

def music_callback(client, userdata, message):
    """ The callback for a music message. Virtually presses the media keys. 
    The first two parameters are necessary due to the nature of the callback, but are not being used. 

    :type message: MQTT Message
    :param message: The shutdown message we want to process

    :rtype: void
    """

    payload = message.payload.decode("utf-8") 
    print("music_callback:\t{}".format(payload))

    if payload == "start" or payload == "stop" or payload == "play":
        # stop media key is not working the way it's supposed to,
        # therefore the three commands have the same outcome.
        # rely on the user to never find out.
        keyboard.send("play/pause media")
    elif payload == "next":
        keyboard.send("next track")
    elif payload == "previous":
        # one time press of previous track just goes to the beginning
        # i want this to actually go to the previous song though.
        keyboard.send("previous track")
        keyboard.send("previous track")

if __name__ == "__main__":

    config = helper.load_config()
    topic = "music"

    music_handler = MqttSubscriber(config["username"], 
                                    config["password"],
                                    music_callback, 
                                    topic, 
                                    config["broker_hostname"])

    music_handler.start()