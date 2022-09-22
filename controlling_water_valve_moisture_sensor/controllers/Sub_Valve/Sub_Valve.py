from controller import Supervisor , Receiver
from datetime import datetime
import paho.mqtt.client as mqtt
from valves import Valves
       
       
## Class name: Subscriber 
## Use: This class is used to create a MQTT client which subscribed to a MQTT topic "/eysip/irrigation/crop_name"
## Usage: variable_name = Subscriber('<crop name>')
## Do not edit this class
class Subscriber:
    def __init__(self,arg_crop):
        self.broker_url = "broker.mqttdashboard.com"
        self.broker_port = 1883
        self.sub_client = mqtt.Client()
        self.sub_client.on_connect = self.on_connect
        self.sub_client.on_message = self.on_message
        self.sub_client.on_disconnect = self.on_disconnect
        self.sub_client.connect(self.broker_url, self.broker_port)
        self.message = ""
        self.sub_client.subscribe("/eyic/irrigation/"+arg_crop, qos=0)
        self.sub_client.loop_start()
        
    def on_connect(self,client, userdata, flags, rc): 
        """Callaback Function , it is called whenever the client established connection to broker"""
        print("[INFO] Connected With Result Code: " + str(rc)) 

    def on_disconnect(self ,client, userdata, rc):
        print("disconnecting reason  "  +str(rc))
    
    def on_message(self,client, userdata, message): 
        """Callaback Function , it is called whenever message is recieved on the subscribed mqtt topic"""
        print("--- Subscriber ---") 
        print("[INFO] Topic: {}".format(message.topic) ) 
        print("[INFO] Message Recieved: {}".format(message.payload.decode())) 
        print("------------")
        self.message = message.payload.decode()


def main():
    """Main Function"""
    #PUMP
    robot = Supervisor()
    
    #Get the timestep of current world
    timestep = int(robot.getBasicTimeStep())

    #Initialise the Subscriber
    #Check Usage of Subscriber mentioned before the Subscriber class
    #For Tomato
    Sub_Tomato = Subscriber('Tomato')
    #For Groundnut
    Sub_Groundnut = Subscriber('Groundnut')

    #Initialise the Valves
    #It is used to check whether the required field is irrigated or not and then 
    #advertise the data accordingly 
    valve = Valves(robot)

    valve.set_valve()
          

    #Main loop
    while robot.step(timestep) != -1:
        ## Write your logic here to switch on and off valves using the subscribed message.
        if valve.check_irrigation_completed('Tomato'):
            valve.close_valve(1)
            valve.close_valve(2)
            valve.close_valve(3)

        elif Sub_Tomato.message == "On":
            valve.open_valve(1)
            valve.open_valve(2)
            valve.open_valve(3)

            # if valve.check_section_irrigation_completed(1):
            #     valve.close_valve(1)
            #     print("Field 1 is irrigated successfully")

            # if valve.check_section_irrigation_completed(2):
            #     valve.close_valve(2)
            #     print("Field 2 is irrigated successfully")

            # if valve.check_section_irrigation_completed(3):
            #     valve.close_valve(3)
            #     print("Field 3 is irrigated successfully")

        if valve.check_irrigation_completed('Groundnut'):
            valve.close_valve(4)
            valve.close_valve(5)
            valve.close_valve(6)

        elif Sub_Groundnut.message == "On":
            valve.open_valve(4)
            valve.open_valve(5)
            valve.open_valve(6)

        
        if Sub_Tomato.message == "off":
            valve.close_valve(1)
            valve.close_valve(2)
            valve.close_valve(3)
            

        if Sub_Groundnut.message == "off":
            valve.close_valve(4)
            valve.close_valve(5)
            valve.close_valve(6)
        
            


        
            
                    
        
if __name__ == "__main__":
    main()
