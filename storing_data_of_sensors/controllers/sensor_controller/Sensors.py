# -*- coding: utf-8 -*-
"""
Created on Wed Jul 21 10:36:25 2021

@author: Raj Kumar Gupta
"""

class Device:
    """Class to initialise the Device"""    
    def __init__(self , arg_robot):
        self.robot = arg_robot
        
    def get_Device(self,arg_name):
        self.sensor = self.robot.getDevice(arg_name)
        #Sensor Object
        self.sensor_object = Sensor(self.sensor,self.robot)
        #return Sensor Object
        return self.sensor_object
    
class Sensor:
    """Class to initialise the sensor"""
    def __init__(self , arg_sensor, arg_robot):
        self.robot = arg_robot
        self.sensor = arg_sensor
        self.enabled = False
        #Field section Flags
        self.section_1 = False
        self.section_2 = False
        self.section_3 = False
        self.section_4 = False
        self.section_5 = False
        self.section_6 = False
        #Field Flag
        self.inside_field = False
        
    def enable(self , arg_timestep):
        """Function to enable the sensor"""
        self.sensor.enable(arg_timestep)
        self.enabled = True
        
    def disable(self):
        """Function to disable the sensor"""
        self.sensor.disable()
        self.enabled = False
        
    def getValue(self):
        #If sensor , then process to get the respective value
        if self.enabled: 
            self.sensor_node = self.robot.getFromDevice(self.sensor)
            self.translation_field = self.sensor_node.getField('translation')
            self.model_field = self.sensor_node.getField('model')
            self.value = SensorValue(self.robot)
            self.translation = self.translation_field.getSFVec3f()
            self.model = self.model_field.getSFString()
            self.x_coord = self.translation[0]
            self.y_coord = self.translation[1]
            self.z_coord = self.translation[2]

            #---------------PH-----------------------
            if self.model == 'PH' and self.value.get_PH_Value() is not None:
                
                if self.y_coord > -0.05 and self.y_coord <0.05:
                    
                    #----------------------section1------------
                    if (self.x_coord<=34 and self.x_coord >=20) and (self.z_coord>=-1 and self.z_coord<=20):
                        self.section_1 = True
                        
                    else:
                        self.section_1 = False
                        
                    #--------------------section2-------------   
                    if (self.x_coord<=20 and self.x_coord >=8) and (self.z_coord>=-1 and self.z_coord<=20):
                        self.section_2 = True
                        
                    else:
                        self.section_2 = False
                    
                    #--------------------section3--------------    
                    if (self.x_coord<=8 and self.x_coord >=-4) and (self.z_coord>=-1 and self.z_coord<=20):
                        self.section_3 = True
                        
                    else:
                        self.section_3 = False 
                        
                   #--------------------Section4----------------
                    if (self.x_coord<=8 and self.x_coord >=-4) and (self.z_coord<=-1 and self.z_coord>=-25):
                        self.section_4 = True
                        
                    else:
                        self.section_4 = False
                        
                   #--------------------Section5----------------
                    if (self.x_coord<=20 and self.x_coord >=8) and (self.z_coord<=-1 and self.z_coord>=-25):
                        self.section_5 = True
                        
                    else:
                        self.section_5 = False                           
                        
                  #--------------------Section5----------------
                    if (self.x_coord<=34 and self.x_coord >=20) and (self.z_coord<=-1 and self.z_coord>=-25):
                        self.section_6 = True
                        
                    else:
                        self.section_6 = False
                        
                    
                    #------------Iniside field--------------
                    if (self.x_coord<=40 and self.x_coord>=-40) and (self.z_coord<=40 and self.z_coord):
                        self.inside_field = True
                    else:
                        self.inside_field = False
                        
                    if self.section_1:
                        self.PH = self.value.get_PH_Value()['1P']
                        
                    elif self.section_2:
                        self.PH = self.value.get_PH_Value()['2P']
 
                    elif self.section_3:
                        self.PH = self.value.get_PH_Value()['3P']                        
                    
                    elif self.section_4:
                        self.PH = self.value.get_PH_Value()['4P']                    
                        
                    elif self.section_5:
                        self.PH = self.value.get_PH_Value()['5P']

                    elif self.section_6:
                        self.PH = self.value.get_PH_Value()['6P'] 
                        
                    elif self.inside_field:
                        self.PH = 7.0
                        
                    else:
                        self.PH = None
                    
                    return self.PH
                
                else:
                    return None
                               
            #-----------------------Moisture---------------  
            if self.model == 'Moisture' and self.value.get_Moisture_Value() is not None:
                
                if self.y_coord > -0.05 and self.y_coord <0.05:
                    
                    #----------------------section1------------
                    if (self.x_coord<=34 and self.x_coord >=20) and (self.z_coord>=-1 and self.z_coord<=20):
                        self.section_1 = True
                        
                    else:
                        self.section_1 = False
                        
                    #--------------------section2-------------   
                    if (self.x_coord<=20 and self.x_coord >=8) and (self.z_coord>=-1 and self.z_coord<=20):
                        self.section_2 = True
                        
                    else:
                        self.section_2 = False
                    
                    #--------------------section3--------------    
                    if (self.x_coord<=8 and self.x_coord >=-4) and (self.z_coord>=-1 and self.z_coord<=20):
                        self.section_3 = True
                        
                    else:
                        self.section_3 = False 
                        
                   #--------------------Section4----------------
                    if (self.x_coord<=8 and self.x_coord >=-4) and (self.z_coord<=-1 and self.z_coord>=-25):
                        self.section_4 = True
                        
                    else:
                        self.section_4 = False
                        
                   #--------------------Section5----------------
                    if (self.x_coord<=20 and self.x_coord >=8) and (self.z_coord<=-1 and self.z_coord>=-25):
                        self.section_5 = True
                        
                    else:
                        self.section_5 = False                           
                        
                  #--------------------Section5----------------
                    if (self.x_coord<=34 and self.x_coord >=20) and (self.z_coord<=-1 and self.z_coord>=-25):
                        self.section_6 = True
                        
                    else:
                        self.section_6 = False
                        
                    
                    #------------Iniside field--------------
                    if (self.x_coord<=40 and self.x_coord>=-40) and (self.z_coord<=40 and self.z_coord):
                        self.inside_field = True
                    else:
                        self.inside_field = False
                        
                    if self.section_1:
                        self.Moisture = self.value.get_Moisture_Value()['1M']
                        
                    elif self.section_2:
                        self.Moisture = self.value.get_Moisture_Value()['2M']
 
                    elif self.section_3:
                        self.Moisture = self.value.get_Moisture_Value()['3M']                        
                    
                    elif self.section_4:
                        self.Moisture = self.value.get_Moisture_Value()['4M']                    
                        
                    elif self.section_5:
                        self.Moisture = self.value.get_Moisture_Value()['5M']

                    elif self.section_6:
                        self.Moisture = self.value.get_Moisture_Value()['6M'] 
                        
                    elif self.inside_field:
                        self.Moisture = 9
                        
                    else:
                        self.Moisture = None
                    
                    return self.Moisture
                else:
                    return None

            #-----------------------Temperature---------------------  
            if self.model == 'Temperature'and self.value.get_Temperature_Value() is not None:
                
                if (self.x_coord<=40 and self.x_coord>=-40) and (self.z_coord<=40 and self.z_coord>=-40):
                    self.inside_field = True
                else:
                    self.inside_field = False
                                                              
                if self.inside_field:
                    self.Temperature = self.value.get_Temperature_Value()
                    return self.Temperature
                else:
                    return None

            #-----------------------Humidity---------------  
            if self.model == 'Humidity' and self.value.get_Humidity_Value() is not None :
                
                if (self.x_coord<=40 and self.x_coord>=-40) and (self.z_coord<=40 and self.z_coord>=-40):
                    self.inside_field = True
                else:
                    self.inside_field = False
                
               
                if self.inside_field:
                    self.Humidity = self.value.get_Humidity_Value()
                    return self.Humidity
                else:
                    return None
                
                
        else:
            raise Exception('Sensor is not enable')

                       
class SensorValue:
    """Class to get the Sensor values"""
    def __init__(self , arg_robot):    
        #get the soil node
        self.soil = arg_robot.getFromDef('Soil')
        #get custom data field
        self.CustomData = self.soil.getField('customData')
        #dictionay to store sensor value pair
        self.values = {}

    def get_PH_Value(self):
        """Function to get the PH value of field"""
        self.custom_data = self.CustomData.getSFString()
        if self.custom_data:
            self.custom_data_list = self.custom_data.split(",")
            for data in self.custom_data_list:
                if data[1]=="P":
                    PH_value = data.split(":")
                    self.values[PH_value[0]] = float(PH_value[1])
            return self.values
        else:
            return None        
        
    def get_Moisture_Value(self):
        """This function return the value of soil moisture depending upon the condition of the soil"""    
        self.custom_data = self.CustomData.getSFString()
        if self.custom_data:
            self.custom_data_list = self.custom_data.split(",")
            for data in self.custom_data_list:
                if data[1]=="M":
                    soil_moisture = data.split(":")
                    self.values[soil_moisture[0]] = float(soil_moisture[1])
            return self.values
        else:
            return None

    def get_Temperature_Value(self):
        """Function to get the temperature in the farm"""
        self.custom_data = self.CustomData.getSFString()
        if self.custom_data:
            self.custom_data_list = self.custom_data.split(",")
            for data in self.custom_data_list:
                if data[0]=="T":
                    Temperature = float(data.split(":")[1])
                    return Temperature
        else:
            return None
        
    def get_Humidity_Value(self):
        """Function to get the humidity in the farm"""
        self.custom_data = self.CustomData.getSFString()
        if self.custom_data:
            self.custom_data_list = self.custom_data.split(",")
            for data in self.custom_data_list:
                if data[0]=="H":
                    Humidity = float(data.split(":")[1]) 
                    return Humidity 
        else:
            None