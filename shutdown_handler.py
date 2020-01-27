#!/usr/bin/env python3

from util.mqtt_subscriber import MqttSubscriber
import util.helper as helper

import os
import winsound

def shutdown_callback(client, userdata, message):
    """ The callback for a shutdown message. Sets the timer accordingly. 
    The first two parameters are necessary due to the nature of the callback, but are not being used. 

    :type message: MQTT Message
    :param message: The shutdown message we want to process

    :rtype: void
    """
    payload = message.payload.decode("utf-8") 
    print("shutdown_callback:\t{}".format(payload))

    if payload == "abort":
        os.system("shutdown /a")
        helper.play_audio_string("shutdown aborted")

    elif payload == "now":
        # shutdown any previous shutdown timer.
        os.system("shutdown /a")
        os.system("shutdown /s /t 30")
        helper.play_audio_string("shutdown imminent in 30 seconds")
    else:
        try:
            timer = int(payload)
            # we don't want to have an immediate shutdown in case waltraud detected the command wrongly. 
            # just set it to one minute.
            timer = timer if timer != 0 else 1
                
            helper.play_audio_string("shutdown in {} minutes".format(timer))
            # shutdown any previous shutdown timer.
            os.system("shutdown /a")
            # timer as per command is in minutes, shutdown takes seconds though
            os.system("shutdown /s /t " + str(timer * 60))
        except Exception as e:
            # ignore and keep on going
            print(e) 

if __name__ == "__main__":
        
    config = helper.load_config()
    topic = "shutdown"

    shutdown_handler = MqttSubscriber(config["username"], 
                                    config["password"],
                                    shutdown_callback, 
                                    topic, 
                                    config["broker_hostname"])

    shutdown_handler.start()