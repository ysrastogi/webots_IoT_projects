"""sensor_controller controller."""
#Import the Supervisor
from controller import Supervisor
import time
from datetime import datetime
import paho.mqtt.client as mqtt
#Import Device class from Sensor class
from Sensors import Device
#To use this class the Supervisor field of the robot must be true
#Import Valves class
from valves import Valves

class Sensor_publisher:
    """Class to publish the sensors data collected from the environment on their respective
    mqtt topic"""    
    def __init__(self):
        self.broker_url = "broker.mqttdashboard.com"
        self.broker_port = 1883
        self.pub_client = mqtt.Client()
        #self.pub_client.on_publish = self.on_publish
        #mqtt topics for publishing sensor data
        self.pub_topic_1 = "/sensor/PH"
        self.pub_topic_2 = "/sensor/Temperature"
        self.pub_topic_3 = "/sensor/Humidity"
        self.pub_topic_4 = "/sensor/SoilMoisture"
        #Connect to broker
        self.pub_client.connect(self.broker_url, self.broker_port)
        
    def on_publish(self,client, userdata, mid):
        """Callback Function , it is called everytime when a message  is published on the topc""" 
        print("--- Published-------")
        
    def PH_publish(self ,arg_message,arg_field):
        """Function to publish PH value data"""
        self.pub_client.publish(topic=self.pub_topic_1+arg_field, payload=arg_message, qos=0, retain=False)
        
    def Temperature_publish(self ,arg_message):
        """Function to publish Temperature data"""
        self.pub_client.publish(topic=self.pub_topic_2, payload=arg_message, qos=0, retain=False)     
        
    def Humidity_publish(self ,arg_message):
        """Function to publish Humidity data"""
        self.pub_client.publish(topic=self.pub_topic_3, payload=arg_message, qos=0, retain=False)        

    def SoilMoisture_publish(self ,arg_message,arg_field):
        """Function to publish Soil Moisture"""
        self.pub_client.publish(topic=self.pub_topic_4+arg_field, payload=arg_message, qos=0, retain=False)        
                
#Main Function        
def main():
    #Initialise the robot
    robot = Supervisor()
    # get the time step of the current world.
    timestep = int(robot.getBasicTimeStep())
    
    #Initialise the Device class
    device = Device(robot)

    ########################
    #Initialise the Valves
    valve = Valves(robot)
    ####################
  
    #Initialise the senors
    #PH sensor
    PHsensor1 = device.get_Device('PH sensor1') #Field_1
    PHsensor2 = device.get_Device('PH sensor2')  #Field_2
    #Enable
    PHsensor1.enable(timestep)
    PHsensor2.enable(timestep)
        
    #Moisture sensor
    MoistureSensor1 = device.get_Device('Moisture sensor1') #Field_1
    MoistureSensor2 = device.get_Device('Moisture sensor2') #Field_2
    #Enable
    MoistureSensor1.enable(timestep)
    MoistureSensor2.enable(timestep)
    
    #Temperature sensor
    TempSensor = device.get_Device('Temperature')
    #Enable
    TempSensor.enable(timestep)
       
    #Humidity
    HumidSensor = device.get_Device('Humidity')
    #Enable
    HumidSensor.enable(timestep)
    
    #Main loop
    #Get current time
    start_time = datetime.now()

    valve.open_valve(1)

    while robot.step(timestep) != -1:
        #Wait for few seconds to initialisation of world
        
        publish = Sensor_publisher()

        # print("before off")
        # if valve.check_section_irrigation_completed(1):
        #     print("inside off if")
        #     valve.close_valve(1)
        
        if (datetime.now() - start_time).total_seconds() > 5:
        
            #Get sensors data
            val1 = TempSensor.getValue()
            val2 = HumidSensor.getValue()
            val3 = PHsensor1.getValue()
            val4 = PHsensor2.getValue()
            val5 = MoistureSensor1.getValue()
            val6 = MoistureSensor2.getValue()


            
            #Constantly publish sensors data on their respective mqtt topic
            # publish.Temperature_publish(val1)
            # publish.Humidity_publish(val2)
            # publish.PH_publish(val3,'field1') 
            # publish.PH_publish(val4,'field2') 
                    
            # publish.SoilMoisture_publish(val5,'field1')
            # publish.SoilMoisture_publish(val6,'field2')
            #print("Temperature:",val1 , "humidity:",val2 , "PH_value_Field1:", val3 ,"PH_value_Field2:",val4, "Moisture_Field1:" , val5 , "Moisture_Field2:" , val6)
            
            start_time = datetime.now()
       
if __name__ == "__main__":
    main()