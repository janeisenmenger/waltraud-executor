#!/usr/bin/env python3

from util.mqtt_subscriber import MqttSubscriber
import util.helper as helper

from ctypes import POINTER, cast
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import keyboard

# hard coded volume dictionary since the scale is logarithmic
# and i couldn't be bothered to do the math
VOLUME_DICT = {
        0:   -62.53,
        10:  -33.24,
        20:  -23.65,
        30:  -17.82,
        40:  -13.62,
        50:  -10.33,
        60:  -7.63,
        70:  -5.33,
        80:  -3.34,
        90:  -1.58,
        100: 0
        }

# setup the devices and interfaces for volume setting
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

def get_current_system_volume_level():
    """ A function that returns the current system volume level (0-100) based on VOLUME_DICT

    :rtype: int
    """
    global volume, VOLUME_DICT
    current_master_volume_db = volume.GetMasterVolumeLevel()

    # calculate closest volume level as in the dictionary
    current_best_distance = 120
    current_system_volume_level = 0
    for system_volume_level, volume_level_db in VOLUME_DICT.items(): 
        if abs(current_master_volume_db - volume_level_db) < current_best_distance:
            current_system_volume_level = system_volume_level
            current_best_distance = abs(current_master_volume_db - volume_level_db)
    
    return current_system_volume_level

def volume_callback(client, userdata, message):
    """ The callback for a volume message.  
    The first two parameters are necessary due to the nature of the callback, but are not being used. 

    :type message: MQTT Message
    :param message: The message we want to process.

    :rtype: void
    """
    global volume, VOLUME_DICT
    payload = message.payload.decode("utf-8") 
    
    print("volume_callback:\t{}".format(payload))

    current_system_volume_level = get_current_system_volume_level()

    if payload == "up":
        # don't exceed the limit
        current_system_volume_level = current_system_volume_level + 20
        if (current_system_volume_level) > 100:
            current_system_volume_level = 100
        # take the dB value from the dict
        volume.SetMasterVolumeLevel(VOLUME_DICT[current_system_volume_level], None)
    elif payload == "down":       
        # don't exceed the limit 
        current_system_volume_level = current_system_volume_level - 20
        if (current_system_volume_level) < 0:
            current_system_volume_level = 0
            # take the dB value from the dict
        volume.SetMasterVolumeLevel(VOLUME_DICT[current_system_volume_level], None)
    elif payload == "mute":
        volume.SetMute(1, None)
    elif payload == "unmute":
        volume.SetMute(0, None)
    else:
        # set volume to a specific value
        # as per the command detection side the value can only be multiples of 10
        # which conincides with our dictionary above, so we're good.
        try:
            level = int(payload)
            volume.SetMasterVolumeLevel(VOLUME_DICT[level], None)
        except Exception as e: 
            print(e)


    # doesn't actually do anything, just to show the media overlay, so the user knows
    # that something did happen. 
    keyboard.send("stop media")

if __name__ == "__main__":
    config = helper.load_config()
    topic = "volume"

    volume_setter = MqttSubscriber(config["username"], 
                                    config["password"],
                                    volume_callback, 
                                    topic, 
                                    config["broker_hostname"])

    volume_setter.start()