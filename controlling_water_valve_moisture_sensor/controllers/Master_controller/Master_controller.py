"""Master_controller controller
Author: Raj Kumar Gupta
"""

from controller import Supervisor
from datetime import datetime
import math
from datetime import date
from datetime import timedelta
import pandas as pd
import yaml  


class supervisor:   
    """This class initialise the Supervisor which control the environmental variables of the world""" 
    def __init__(self):
        self.master = Supervisor()
        
    def set_soil(self, arg_PH_value , arg_condition, arg_temp , arg_Humidity):
        """Function to set the propeties in the soil"""
        #PH_data
        self.PH_data_1 = '1P:'+ str(arg_PH_value[0])+',2P:'+ str(arg_PH_value[1])+',3P:' + str(arg_PH_value[2])
        self.PH_data_2 = '4P:'+ str(arg_PH_value[3])+',5P:'+ str(arg_PH_value[4])+',6P:' + str(arg_PH_value[5])
        self.PH_data = self.PH_data_1 + ',' + self.PH_data_2
        #soilmoisture data
        self.Moisture_data_1 = '1M:'+ str(arg_condition[0])+',2M:'+ str(arg_condition[1])+',3M:' + str(arg_condition[2])
        self.Moisture_data_2 = '4M:'+ str(arg_condition[3])+',5M:'+ str(arg_condition[4])+',6M:' + str(arg_condition[5])
        self.Moisture_data = self.Moisture_data_1 + ',' + self.Moisture_data_2     
        
        self.soil_data = self.PH_data+','+self.Moisture_data+','+'T:'+str(arg_temp)+',H:'+str(arg_Humidity)
        self.master.setCustomData(self.soil_data)

class Water_Node:
    """Class for Sub Vavles"""    
    def __init__(self, arg_pump,arg_num_valves=6):
        #Valve list
        self.valve_list = [] 
        #Dictionary to stor valves and water fields
        self.water_translation = {}
        self.water_size = {}
        self.water_transparency = {}
        self.valve_pipe_translation = {}
        self.valve_pipe_length = {}
        #Variable for total no of valves present in farm
        self.num_of_valves = arg_num_valves
        #pump
        self.pump = arg_pump
               
    
    def get_valves(self):
        """Function to get sub valves"""
        for i in range(1 , self.num_of_valves+1):
            self.valve_list.append('valve'+ str(i))
        return self.valve_list
    
    def get_fields(self):
        """Function to get the water fields"""
        for valve in self.valve_list:
            Water = self.pump.getFromDef(valve+'_Water')
            water_geometry = self.pump.getFromDef(valve+'_water_geometry')
            water_appearance = self.pump.getFromDef(valve+'_water_appearance')
            valve_pipe = self.pump.getFromDef(valve+'_pipe')
            self.water_translation[valve] = Water.getField('translation')
            self.water_size[valve] = water_geometry.getField('size') 
            self.water_transparency[valve] = water_appearance.getField('transparency')
            self.valve_pipe_translation[valve] = valve_pipe.getField('translation')
            self.valve_pipe_length[valve] = valve_pipe.getField('height')  
        
    def set_valve(self):
        """Function to set the valves"""
        for valves in self.valve_list:
            self.pipe_translate = self.valve_pipe_translation[valves].getSFVec3f()
            self.pipe_length = self.valve_pipe_length[valves].getSFFloat()       
            self.length_water = 0.1
            self.water_height = self.pipe_length-1.0
            self.water_size[valves].setSFVec2f([self.water_height,self.length_water])
            self.water_translation[valves].setSFVec3f([self.pipe_translate[0],self.pipe_translate[1], (self.pipe_translate[2]/abs(self.pipe_translate[2]))*(abs(self.pipe_translate[2]) + 0.5)]) 
            self.water_transparency[valves].setSFFloat(0)
          
    def start(self):
        """Function to initialise the valves"""
        self.get_valves()
        self.get_fields()
        self.set_valve()
              
    def start_water(self,arg_valve_name , arg_y_trans=-0.2):
        """Function to open the valve and water start flowing"""
        self.length_moved = self.water_size[arg_valve_name].getSFVec2f()[1] + 0.1
        self.x_trans = self.water_translation[arg_valve_name].getSFVec3f()[0] + 0.05
        self.y_trans = arg_y_trans
        self.water_translation[arg_valve_name].setSFVec3f([self.x_trans , self.y_trans , self.water_translation[arg_valve_name].getSFVec3f()[2] ])
        self.water_size[arg_valve_name].setSFVec2f([self.valve_pipe_length[arg_valve_name].getSFFloat()-1.0 ,self.length_moved])

    def set_water_transparency(self, arg_valve, arg_transparency):
        """Function to set the transparency of the water node""" 
        self.water_transparency[arg_valve].setSFFloat(arg_transparency)
                         
        
def Reset_Irrigation_Status():
    """Function to reset the Irrigation status""" 
    reset_status = {  'valve1' : 
                                {'IrrigationOccuring':False,
                                  'IrrigationDone':False},
                      'valve2' : 
                                {'IrrigationOccuring':False,
                                 'IrrigationDone':False},  
                      'valve3' : 
                                {'IrrigationOccuring':False,
                                 'IrrigationDone':False},
                       'valve4' : 
                                {'IrrigationOccuring':False,
                                'IrrigationDone':False},
                       'valve5' : 
                                {'IrrigationOccuring':False,
                                'IrrigationDone':False},  
                       'valve6' : 
                                {'IrrigationOccuring':False,
                                'IrrigationDone':False}
                                 } 
    with open('IrrigationStatus.yaml', 'w') as file: 
        dumped = yaml.dump(reset_status,file)

def Update_Irrigation_Status(arg_data):  
    with open('IrrigationStatus.yaml', 'w') as file: 
        dumped_status = yaml.dump(arg_data,file)
            
def Open_Irrigation_Status():
    """Function to readthe Irrigation status""" 
    with open('IrrigationStatus.yaml') as file: 
        Irrigation_Status = yaml.load(file, Loader=yaml.FullLoader)
        return Irrigation_Status
    
           
class RHumidity:
    """Class to get the  variation of Relative environmental Humidity vs Temperature"""
    def __init__(self):
        self.data_df = pd.read_csv('dataFrame/TempHumidity.csv')
        self.temperature_series = []
        self.humidity_temperature = []
        self.humidity_dic = {}
        
    def fetch_Humidity(self):
        """This function fetch the data from dataframe"""
        self.temperature = self.data_df['Temperature']
        self.Humidity   =  self.data_df['RelativeHumidity']
        self.index = self.data_df.index
        for temperature in self.temperature:
            if self.temperature_series.count(round(temperature)) == 0:
                self.temperature_series.append(round(temperature))
        for i in self.index:
            self.humidity_temperature.append((round(self.temperature[i]),self.Humidity[i]))
        
                          
    def get_Humidity(self):
        """This function return a Humidity-Temperature dictionary, average Humidity is calculated from the fetched data
        and a Temperature-KEY and Humidity -VALUE pair is created"""
        for temperature in self.temperature_series:
            self.temp_humidity_list = []
            for pair in self.humidity_temperature:
                if pair[0] == temperature:
                    self.temp_humidity_list.append(pair[1])
            self.avg_humidity = sum(self.temp_humidity_list)/len(self.temp_humidity_list)
            self.humidity_dic[temperature] = self.avg_humidity
            
        return self.humidity_dic
        
       
def main():
    """Main Function"""
    
    #Reset irrigation status
    Reset_Irrigation_Status()
    
    #Initialise Supervisor
    supervisor_master  = supervisor()
    
    #set timestep
    timestep = int(supervisor_master.master.getBasicTimeStep())
    
    #Get the sun
    sun = supervisor_master.master.getFromDef('Sun')
    sun_field = sun.getField('direction')
    sun_intensity = sun.getField('intensity') 
    
    #Humidity Data
    Past_data = RHumidity()
    Past_data.fetch_Humidity()
    Humid_dic_data = Past_data.get_Humidity()
        
    #Light Sensor
    #The light sensor is only used to record the change in the sensor reading w.r.t to change in the position of the Sun 
    #which is saved in a .csv for later use
    #light_sensor = supervisor_master.master.getLightSensor("light sensor")
    #light_sensor.enable(timestep)
    
    
    #Time varaibles 
    day_time = datetime.now()
    #start_time = datetime.now()
    
    #World Intensity
    intensity = 0
    #Set the world
    sun_intensity.setSFFloat(intensity)
    sun_field.setSFVec3f([-1,0,0])  
    #Sun evlevation step , Here Scaling the 12 hours of day  equivalent to 1hour in the simulation 
    #So , we get insight on the working farm in a constarined time interval
    theta_step = math.pi/3600
    #Intensity Step
    intensity_step = 0.0167
    #Step counter
    step_count = 1
    #Day Flag Counter
    quater_day_start = False
    half_day_complete = False
    day_complete = False
    #General Morning Temperature
    Temp_morning = 23
    
    #For sand type soil the soil moisture between 5 to 11 %  is optimum and below it causes stress 
    #to the plant as we already done one irrigation cycle and the irrigation scheduled after every
    #10 day for Tomato and 11 day for Groundnut ,So near 10th day  moisture content reached near the threshold 5 % so assuming it 6.3%
    
    #Field_1 for Tomato
    soil_moisture_remain_Field_one_1 = 6.2
    soil_moisture_remain_Field_one_2 = 6.2
    soil_moisture_remain_Field_one_3 = 6.2
    soil_moisture_Field_one_1 = 6.2
    soil_moisture_Field_one_2 = 6.2
    soil_moisture_Field_one_3 = 6.2
    #PH value 
    PH_value_Field_one_1 = 7.2
    PH_value_Field_one_2 = 7.2
    PH_value_Field_one_3 = 7.2
    

    
    #Field_2 for Groundnut
    soil_moisture_remain_Field_two_4 = 5.4
    soil_moisture_remain_Field_two_5 = 5.4
    soil_moisture_remain_Field_two_6 = 5.4
    soil_moisture_Field_two_4 = 5.4
    soil_moisture_Field_two_5 = 5.4
    soil_moisture_Field_two_6 = 5.4
    #PH value 
    PH_value_Field_two_4 = 6.89
    PH_value_Field_two_5 = 6.89
    PH_value_Field_two_6 = 6.89
    
    
    #Flags
    infiltration_valve1 = False
    infiltration_valve2 = False
    infiltration_valve3 = False
    infiltration_valve4 = False
    infiltration_valve5 = False
    infiltration_valve6 = False
    
    #water 
    water = Water_Node(supervisor_master.master)
    water.start()
    
    #Main Loop
    while supervisor_master.master.step(timestep) != -1: 
        
        irrigation_status = Open_Irrigation_Status()
        
        #Wait for a second and check whether a new day is started or not if not then start the day and set the 
        #environmental variables accordingly 
        if (datetime.now()-day_time).total_seconds() >=1 and not day_complete and irrigation_status is not None: 
            #Sun's w.r.t to the ground 
            angle_sun = theta_step*step_count
            x_sun = -math.cos(theta_step*step_count)
            y_sun = -math.sin(theta_step*step_count)       
                    
            #Check whether the sun is completed over the horizon in that time slowing increase its intensity          
            if step_count <= 300:
                intensity = intensity + intensity_step
                sun_intensity.setSFFloat(intensity)
            sun_field.setSFVec3f([x_sun,y_sun,0])  
            day_time = datetime.now()  
            
            #If the Quater day is not started yet then incraeses the temperature linearly with time with a gradient
            #of "0.002003" calculate from analysing Data availabe in reasearch papers.
            if step_count <= 1500 and not quater_day_start:
                Temp =  Temp_morning + 0.002003 * step_count
                if step_count == 1500:
                    quater_day_start = True 
          
            #If the quater day started and half day is not completed then temperature vary as a lograthmic function 
            #of time give the temperature in Kelvin
            if step_count <=2350 and quater_day_start and not half_day_complete:  
                sun_angle = angle_sun
                Temp_calc = math.log((1000*math.sin(sun_angle))*10**26/3)/0.2403
                Temp_calc_C = Temp_calc - 273.15
                Temp = Temp + (Temp_calc_C*0.00008*step_count)
                if step_count == 2350:
                    half_day_complete = True
                    
            #If half day is completed then the Temperature decraeses slowly with assuming it linear as cooling 
            #takes place
            if half_day_complete: 
                Temp = Temp - 0.00345
                
            #----------------------------------valve1--------------------------------- 
            if irrigation_status['valve1']['IrrigationOccuring']: 
                #Decrease the PH_Value slightly due to effect of water  
                PH_value_Field_one_1 = PH_value_Field_one_1 - 0.00003*step_count 
                water.start_water('valve1')
                
            if irrigation_status['valve1']['IrrigationDone'] and not infiltration_valve1 : 
                infiltration_valve1 = True
                irrigation_status['valve1']['IrrigationDone'] = False
                infiltration_time_valve1 = datetime.now()
                
            if infiltration_valve1: 
                water_infiltrate_1 = 0.000089*(datetime.now()-infiltration_time_valve1).total_seconds()
                PH_value_Field_one_1 = PH_value_Field_one_1 - 0.000000267*step_count
                water_transparency_1 = 0.00188*(datetime.now()-infiltration_time_valve1).total_seconds()
                 
                soil_moisture_Field_one_1 = soil_moisture_remain_Field_one_1 + (water_infiltrate_1)*100
                 
                water.set_water_transparency('valve1', water_transparency_1)
                 
                 #Check whether the infiltration completed or not , if the time pass is greater or equal to 500 seconds /8 minutes approx
                 #then the water is completed infiltrated in the soil , depending on the height of water and soil infiltration the value is obatined.
                if (datetime.now()-infiltration_time_valve1).total_seconds()>=500: 
                    water.set_water_transparency('valve1' , 1) 
                    infiltration_valve1 = False
                    
            #-------------------valve2----------------------
            if irrigation_status['valve2']['IrrigationOccuring']:
               #Decrease the PH_Value slightly due to effect of water  
               PH_value_Field_one_2 = PH_value_Field_one_2 - 0.00003*step_count 
               water.start_water('valve2')               
                
            if irrigation_status['valve2']['IrrigationDone'] and not infiltration_valve2 :
                infiltration_valve2 = True
                irrigation_status['valve2']['IrrigationDone'] = False
                infiltration_time_valve2 = datetime.now()
                
            if infiltration_valve2:
                water_infiltrate_2 = 0.000089*(datetime.now()-infiltration_time_valve2).total_seconds()
                PH_value_Field_one_2 = PH_value_Field_one_2 - 0.000000267*step_count
                water_transparency_2 =  0.00188*(datetime.now()-infiltration_time_valve2).total_seconds()
                 
                soil_moisture_Field_one_2 = soil_moisture_remain_Field_one_2 + (water_infiltrate_2)*100
                 
                water.set_water_transparency('valve2', water_transparency_2)
                 
                 #Check whether the infiltration completed or not , if the time pass is greater or equal to 500 seconds /8 minutes approx
                 #then the water is completed infiltrated in the soil , depending on the height of water and soil infiltration the value is obatined.
                if (datetime.now()-infiltration_time_valve2).total_seconds()>=500: 
                    water.set_water_transparency('valve2', 1) 
                    infiltration_valve2 = False
                
            #-------------------valve3----------------------
            if irrigation_status['valve3']['IrrigationOccuring']:
               #Decrease the PH_Value slightly due to effect of water  
               PH_value_Field_one_3 = PH_value_Field_one_3 - 0.00003*step_count 
               water.start_water('valve3')
                
            if irrigation_status['valve3']['IrrigationDone'] and not infiltration_valve3 :
                infiltration_valve3 = True
                irrigation_status['valve3']['IrrigationDone'] = False
                infiltration_time_valve3 = datetime.now()
                
            if infiltration_valve3:
                water_infiltrate_3 = 0.000089*(datetime.now()-infiltration_time_valve3).total_seconds()
                PH_value_Field_one_3 = PH_value_Field_one_3 - 0.000000267*step_count
                water_transparency_3 =  0.00188*(datetime.now()-infiltration_time_valve3).total_seconds()
                 
                soil_moisture_Field_one_3 = soil_moisture_remain_Field_one_3 + (water_infiltrate_3)*100
                 
                water.set_water_transparency('valve3' , water_transparency_3)
                 
                 #Check whether the infiltration completed or not , if the time pass is greater or equal to 500 seconds /8 minutes approx
                 #then the water is completed infiltrated in the soil , depending on the height of water and soil infiltration the value is obatined.
                if (datetime.now()-infiltration_time_valve3).total_seconds()>=500: 
                    water.set_water_transparency('valve3', 1) 
                    infiltration_valve3 = False 
                
            #-------------------valve4----------------------
            if irrigation_status['valve4']['IrrigationOccuring']:
               #Decrease the PH_Value slightly due to effect of water  
               PH_value_Field_two_4 = PH_value_Field_two_4 - 0.00003*step_count 
               water.start_water('valve4')               
                
            if irrigation_status['valve4']['IrrigationDone'] and not infiltration_valve4 :
                infiltration_valve4 = True
                irrigation_status['valve4']['IrrigationDone'] = False
                infiltration_time_valve4 = datetime.now()
                
            if infiltration_valve4:
                water_infiltrate_4 = 0.000089*(datetime.now()-infiltration_time_valve4).total_seconds()
                PH_value_Field_two_4 = PH_value_Field_two_4 - 0.000000267*step_count
                water_transparency_4 =  0.00188*(datetime.now()-infiltration_time_valve4).total_seconds()
                 
                soil_moisture_Field_two_4 = soil_moisture_remain_Field_two_4 + (water_infiltrate_4)*100
                 
                water.set_water_transparency('valve4' , water_transparency_4)
                 
                 #Check whether the infiltration completed or not , if the time pass is greater or equal to 500 seconds /8 minutes approx
                 #then the water is completed infiltrated in the soil , depending on the height of water and soil infiltration the value is obatined.
                if (datetime.now()-infiltration_time_valve4).total_seconds()>=500: 
                    water.set_water_transparency('valve4', 1) 
                    infiltration_valve4 = False  
    
 
           #-------------------valve5----------------------
            if irrigation_status['valve5']['IrrigationOccuring']:
               #Decrease the PH_Value slightly due to effect of water  
               PH_value_Field_two_5 = PH_value_Field_two_5 - 0.00003*step_count
               water.start_water('valve5')
                
            if irrigation_status['valve5']['IrrigationDone'] and not infiltration_valve5 :
                infiltration_valve5 = True
                irrigation_status['valve5']['IrrigationDone'] = False
                infiltration_time_valve5 = datetime.now()
                
            if infiltration_valve5:
                water_infiltrate_5 = 0.000089*(datetime.now()-infiltration_time_valve5).total_seconds()
                PH_value_Field_two_5 = PH_value_Field_two_5 - 0.000000267*step_count
                water_transparency_5 =  0.00188*(datetime.now()-infiltration_time_valve5).total_seconds()
                 
                soil_moisture_Field_two_5 = soil_moisture_remain_Field_two_5 + (water_infiltrate_5)*100
                 
                water.set_water_transparency('valve5', water_transparency_5)
                 
                 #Check whether the infiltration completed or not , if the time pass is greater or equal to 500 seconds /8 minutes approx
                 #then the water is completed infiltrated in the soil , depending on the height of water and soil infiltration the value is obatined.
                if (datetime.now()-infiltration_time_valve5).total_seconds()>=500: 
                    water.set_water_transparency('valve5', 1) 
                    infiltration_valve5 = False 

 
            #-------------------valve6----------------------
            if irrigation_status['valve6']['IrrigationOccuring']:
               #Decrease the PH_Value slightly due to effect of water  
               PH_value_Field_two_6 = PH_value_Field_two_6 - 0.00003*step_count
               water.start_water('valve6')                
                
            if irrigation_status['valve6']['IrrigationDone'] and not infiltration_valve6 :
                infiltration_valve6 = True
                irrigation_status['valve6']['IrrigationDone'] = False
                infiltration_time_valve6 = datetime.now()
                
            if infiltration_valve6:
                water_infiltrate_6 = 0.000089*(datetime.now()-infiltration_time_valve6).total_seconds()
                PH_value_Field_two_6 = PH_value_Field_two_4 - 0.000000267*step_count
                water_transparency_6 =  0.00188*(datetime.now()-infiltration_time_valve6).total_seconds()
                 
                soil_moisture_Field_two_6 = soil_moisture_remain_Field_two_6 + (water_infiltrate_6)*100
                 
                water.set_water_transparency('valve6' , water_transparency_6)
                 
                 #Check whether the infiltration completed or not , if the time pass is greater or equal to 500 seconds /8 minutes approx
                 #then the water is completed infiltrated in the soil , depending on the height of water and soil infiltration the value is obatined.
                if (datetime.now()-infiltration_time_valve6).total_seconds()>=500: 
                    water.set_water_transparency('valve6', 1) 
                    infiltration_valve6 = False 
                    
            #Vary the Humidity according to the change in the temperature of the environment 
            Humidity_gradient = Humid_dic_data[int(Temp)+1] - Humid_dic_data[int(Temp)] 
            Humidity = Humid_dic_data[int(Temp)] + Humidity_gradient*(Temp-int(Temp))
            
            #Soil PH list 
            PH_value = [ PH_value_Field_one_1 , PH_value_Field_one_2 , PH_value_Field_one_3 , 
                        PH_value_Field_two_4, PH_value_Field_two_5 ,PH_value_Field_two_6]
            
            #Soil Moisture List
            soil_moisture = [soil_moisture_Field_one_1 , soil_moisture_Field_one_2, soil_moisture_Field_one_3 ,
                             soil_moisture_Field_two_4 , soil_moisture_Field_two_5 , soil_moisture_Field_two_6]
            
            #Set properties to the soil                                         
            supervisor_master.set_soil(PH_value, soil_moisture ,Temp ,Humidity)                       
            
            Update_Irrigation_Status(irrigation_status)
            
            #Check whether the day is overed or not
            if step_count == 3600: 
                sun_intensity.setSFFloat(0)
                sun_field.setSFVec3f([1,0,0])
                day_complete = True
                
            #Update the step_count for each cycle + 1  
            step_count = step_count + 1
            
if __name__ == '__main__':
    main()

                                                                                    