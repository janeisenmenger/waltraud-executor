from util.mqtt_subscriber import MqttSubscriber
import util.helper as helper
import winsound

def beep_callback(client, userdata, message):
    """ A function that triggers a high pitched sound upon call.
    It has some parameters due to the nature of the callbacks.   
    """
    winsound.Beep(1500, 250)

if __name__ == "__main__":

    config = helper.load_config()
    topic = "beep"

    trigger_beep = MqttSubscriber(config["username"], 
                                    config["password"],
                                    beep_callback, 
                                    topic, 
                                    config["broker_hostname"])

    trigger_beep.start()