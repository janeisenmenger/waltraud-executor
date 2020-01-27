import paho.mqtt.client as mqtt

class MqttSubscriber():
    """ A class that handles incoming mqtt messages with the given parameters forever	"""
    
    def __init__(self, username, password, callback_function, topic, hostname, port=1883):
        """ 
        A function that initiates the subscriber with the given parameters.
   
        :type username: string
        :param username: The username we want to use when connecting to the broker.
    
        :type password: string
        :param password: The password to the given username.
    
        :type callback_function: function(client, userdata, message)
        :param callback_function: The function that will be called when receiving a message.
    
        :type topic: string
        :param topic: The topic we subscribe to
    
        :type hostname: string
        :param hostname: The MQTT broker's hostname we want to connect to.

        :type port: int
        :param port: The port we want to connect to at the broker. 1883 by default. 
    
        :rtype: void
        """    
        
        self.mqtt_client = mqtt.Client()

        self.mqtt_client.username_pw_set(username, password=password)
        self.mqtt_client.connect(hostname, port=port)

        self.mqtt_client.subscribe(topic, qos=0)
        
        self.mqtt_client.on_message = callback_function

    def start(self):
        """ A function that starts the handler in a blocking fashion.  
        :rtype: void
        """    
        self.mqtt_client.loop_forever()