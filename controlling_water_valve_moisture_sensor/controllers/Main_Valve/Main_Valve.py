from controller import Supervisor , Emitter 
from datetime import datetime
import paho.mqtt.client as mqtt
import pandas as pd
import math
from valves import Valves
       
## Class name: Irrigationscheduler
## Use: Class to schedule Irrigation
## Usage: variable_name = Irrigationscheduler('<crop name>')
## Do not edit this class
class Irrigationscheduler:
    def __init__(self , arg_crop):
        #Crop -Tomato
        self.crop = arg_crop
        self.crop_df = pd.read_csv('dataFrame/'+self.crop+'.csv') 
        self.soil_type = "sandy"
        self.net_irrigation_depth = 40
        self.irrigation_eff = 60
        self.gross_irrigation_depth = 5 *round((100 *self.net_irrigation_depth)/300)
        self.current_month = datetime.now().strftime("%B")
        #Irrigation done last time 
        self.last_irrigate = None
        
    def irrigation_water_over_month(self):
        """Function to calculate the Total crop water requirement over the growing period of crop"""
        self.ET_cofficient = self.crop_df['Etvalue']
        self.Kc_cofficient = self.crop_df['KcValue']
        self.growing_month = self.crop_df['Month']
        self.CWR_requirement = []
        i = 0
        for month in self.growing_month:
            CWR = 30 *self.ET_cofficient[i]*self.Kc_cofficient[i]
            self.CWR_requirement.append(CWR)
            i = i + 1
        self.Total_CWR = sum(self.CWR_requirement)
        return self.Total_CWR
    
    def irrigation_scehdule(self):
       """Function the get the interval between two irrigation cycle"""
       self.no_of_irrigation_application =self.Total_CWR/self.net_irrigation_depth
       self.interval_of_irrigation = round((len(self.crop_df)*30)/self.no_of_irrigation_application)
       return self.interval_of_irrigation

## Class name: Publisher
## Use: This is the Publisher class which publish the data on a mqtt topic "/eysip/irrigation/crop_name" to open and close the valves
## Usage: variable_name = Publisher('<crop name>')
## Do not edit this class
class Publisher:
    def __init__(self, arg_crop):
        self.broker_url = "broker.mqttdashboard.com"
        self.broker_port = 1883
        self.pub_client = mqtt.Client()
        self.pub_client.on_publish = self.on_publish
        self.pub_topic = "/eyic/irrigation/" + arg_crop
        self.pub_client.connect(self.broker_url, self.broker_port)
        
    def on_publish(self,client, userdata, mid): 
        """This is a callback it is called whenever something published on the mqtt topic"""
        print("--- Publisher ---") 
        print("[INFO] Topic: {}".format(self.pub_topic)) 

    def publish(self ,arg_message):
        """Function to publish the message"""
        self.pub_client.publish(topic=self.pub_topic, payload=arg_message, qos=0)

def main():
    """Main Function"""  
    
    #Initialise Irrigation Scheduler
    #Tomato
    Irrigation_Tomato = Irrigationscheduler("Tomato")
    Irrigation_Tomato.irrigation_water_over_month()
    Interval_Tomato = Irrigation_Tomato.irrigation_scehdule()
    Irrigation_occuring_Tomato = False
    Irrigation_Tomato.last_irrigate = datetime(2021 ,6 ,12,21,20,00)
        
    #Groundnut
    Irrigation_Groundnut = Irrigationscheduler("Groundnut")
    Irrigation_Groundnut.irrigation_water_over_month()
    Interval_Groundnut = Irrigation_Groundnut.irrigation_scehdule()
    Irrigation_occuring_Groundnut = False
    Irrigation_Groundnut.last_irrigate = datetime(2021 ,6 ,12,21,15,00)
    
    #Create the Robot instance.
    robot = Supervisor()
    
    #Get the time step of the current world.
    timestep = int(robot.getBasicTimeStep())
    
    #Initialise Valve
    #It is used to check whether the required field is irrigated or not and then 
    #advertise the data accordingly 
    valve = Valves(robot)
    
    #Initialise the Publisher
    #Check Usage of Publisher mentioned before the Subscriber class
    #For Tomato
    Pub_Tomato = Publisher('Tomato')
    #For Groundnut
    Pub_Groundnut = Publisher('Groundnut')
    
    #Start Time
    start_time = datetime.now()
        
    #Main Loop
    while robot.step(timestep) != -1:
    
        #--------------------------------Tomato----------------------------------------------------
        #Check whether the Tomato field need irrigation or not as per the schedule, If needed and the irrigation is 
        #not occuring then Publish "On" on the MQTT topic  "/eysip/irrigation/Tomato"              
        if (datetime.now() - Irrigation_Tomato.last_irrigate).days >= Interval_Tomato and not Irrigation_occuring_Tomato:
            Pub_Tomato.publish('On')
            Irrigation_occuring_Tomato = True
            #Update the Last Irrigation Date
            Irrigation_Tomato.last_irrigate = datetime.now()
            print("Message send ON")
            
        #If irrigation is occuring , check whether it is completed or not , If completed then Publish "Off" on the MQTT topic  "/eysip/irrigation/Tomato"  
        if  Irrigation_occuring_Tomato :
            if valve.check_irrigation_completed('Tomato') :
                Pub_Tomato = Publisher('Tomato')
                Pub_Tomato.publish('Off')
                print("Message send OFF")
                Irrigation_occuring_Tomato = False  
 
                                             
        #--------------------------------Groundnut----------------------------------------------------
        #Check whether the Groundnut field need irrigation or not as per the schedule, If needed and the irrigation is 
        #not occuring then Publish "On" on the MQTT topic  "/eysip/irrigation/Groundnut"                
        if (datetime.now() - Irrigation_Groundnut.last_irrigate).days >= Interval_Groundnut and not Irrigation_occuring_Groundnut:
            Pub_Groundnut.publish('On')
            Irrigation_occuring_Groundnut = True
            #Update the Last Irrigation Date
            Irrigation_Groundnut.last_irrigate = datetime.now()
            print("Message send ON")
            
         #If irrigation is occuring , check whether it is completed or not , If completed then then Publish "On" on the MQTT topic  "/eysip/irrigation/Groundnut"  
        if Irrigation_occuring_Groundnut:
            if valve.check_irrigation_completed('Groundnut'):
                Pub_Groundnut = Publisher('Groundnut')
                Pub_Groundnut.publish('Off')
                print("Message send OFF")
                Irrigation_occuring_Groundnut = False  
                                                            
if __name__ == "__main__":
    main()

