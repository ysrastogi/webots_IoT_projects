"""
valves script
This python script is used to import Valves class present in the valve module which is 
located in master_controller directory
@author: 
"""
#Import required modules
import os
import sys

#get current working directory of script
current_directory = os.getcwd()
#split the directory path
splited_directory = current_directory.split("\\")
del splited_directory[len(splited_directory)-1]
#new path variable
new_path = ""

#append Master_controller directory in path list
splited_directory.append('Master_controller')

#create the path
for f in splited_directory:
         new_path = new_path + f + '/'

#append the new path to system
sys.path.append(new_path)

#import Valves class
from valve import Valves