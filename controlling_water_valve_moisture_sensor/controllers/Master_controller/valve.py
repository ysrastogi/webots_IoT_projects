"""
Valve API

@author: Raj Kumar Gupta
"""

import yaml
import os

class Valves:
    """Class for Sub Vavles""" 
    
    #class variable
    irrigation_status = {   'valve1' : 
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
        #valve status
        self.valve_closed = {}
        #valves distribution in the field
        self.valve_distribution ={'TOMATO': ['valve1','valve2','valve3'] ,
                                  'GROUNDNUT':['valve3','valve5','valve6']}
    
    
        #Running path
        self.directory = os.getcwd()
        self.splited_directory = self.directory.split("\\")
        del self.splited_directory[len(self.splited_directory)-1]
        self.splited_directory.append('Master_controller')
        self.new_path = ""
        for f in self.splited_directory:
            self.new_path = self.new_path + f + '/'
            
        self.get_valves()
        self.get_fields()
        self.set_valve()
            
    
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
            self.valve_closed[valve] = False
        
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
                       
    def open_valve(self, arg_valve_num):
        """Function to open the valve and water start flowing"""
        if  arg_valve_num in [val_num for val_num in range(1,7)]: 
            #print("inside open valve 1")
            if not Valves.irrigation_status['valve'+str(arg_valve_num)]['IrrigationOccuring']:  
                Valves.irrigation_status['valve'+str(arg_valve_num)]['IrrigationOccuring'] = True  
                self.Update_Irrigation_Status(Valves.irrigation_status)
        else:
            raise Exception("No Valve name:",'valve'+str(arg_valve_num))
        
    def close_valve(self,arg_valve_num):
        """Function to close valve"""     
        if  arg_valve_num in [val_num for val_num in range(1,7)]:  
            print("inside close valve 1")
            if not Valves.irrigation_status['valve'+str(arg_valve_num)]['IrrigationDone'] and Valves.irrigation_status['valve'+str(arg_valve_num)]['IrrigationOccuring']: 
                print("inside close valve 2")
                Valves.irrigation_status['valve'+str(arg_valve_num)]['IrrigationOccuring'] = False 
                Valves.irrigation_status['valve'+str(arg_valve_num)]['IrrigationDone'] = True  
                self.Update_Irrigation_Status(Valves.irrigation_status)        
                print('valve'+str(arg_valve_num),"is closed")
        else:
            raise Exception("No Valve name:",'valve'+str(arg_valve_num))

    def check_irrigation_completed(self , arg_crop_name , arg_stop_len=10):
        """Function to check whether irrigation of a particular crop is completed or not"""
        self.crop_name = arg_crop_name.upper()
        self.valves = self.valve_distribution[self.crop_name] 
        self.field_section_irrigated = 0
        for valve in self.valves:
            if self.water_size[valve].getSFVec2f()[1] >= arg_stop_len:
                self.field_section_irrigated = self.field_section_irrigated + 1
                
        if self.field_section_irrigated == 3:
            flag = True
        else:
            flag = False
        return flag

    def check_section_irrigation_completed(self , arg_section_num , arg_stop_len=10):
        """Function to check whether irrigation of a particular section in the field"""
        if  arg_section_num in [val_num for val_num in range(1,7)]: 
            self.valve_name = 'valve'+str(arg_section_num) 
            if self.water_size[self.valve_name].getSFVec2f()[1] >= arg_stop_len: 
                flag = True 
            else: 
                flag = False 
            return flag
        else:
            raise Exception("No Valve name:",'valve'+str(arg_section_num))
                  
    def Open_Irrigation_Status(self):
        with open(self.new_path+'IrrigationStatus.yaml') as file:
            self.IrrigationStatus = yaml.load(file, Loader=yaml.FullLoader)
            
        return self.IrrigationStatus
            
    def Update_Irrigation_Status(self , arg_data): 
        with open(self.new_path+'IrrigationStatus.yaml', 'w') as file:
            dumped = yaml.dump(arg_data,file)
            
    def Reset_Irrigation_Status(self):
        """Function to reset the irrigation status"""
        with open(self.new_path+'IrrigationStatus.yaml', 'w') as file:
            reset_dumped = yaml.dump(self.irrigation_status,file)
            
