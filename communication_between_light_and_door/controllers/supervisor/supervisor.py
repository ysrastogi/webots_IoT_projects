"""e-puck-supervisor controller."""

from controller import Supervisor, Robot
import sys
import json
import functools
from functools import reduce
from colorama import Fore
from colorama import Style

supervisor = Supervisor()

door = supervisor.getFromDef("smartdoor") 
human = supervisor.getFromDef("pedestrian")
ps = supervisor.getFromDef("HingeJoint") 
light = supervisor.getFromDef("PointLight") 
   

if door is None:
    sys.stderr.write("No DEF smartdoor node found in the current world file\n")
    sys.exit(1)
if human is None:
    sys.stderr.write("No DEF pedestrian node found in the current world file\n")
    sys.exit(1)
if light is None:
    sys.stderr.write("No DEF Smartlight1 node found in the current world file\n")
    sys.exit(1)

# get the time step of the current world.
TIME_STEP=16
light_flag = 0
MAX_TIME = 180 #Max time in seconds to complete the simulation after which the simulation would stop automatically
COMMUNICATION_CHANNEL = 1
message_printed = 0
# get the time step of the current world.
timestep = int(supervisor.getBasicTimeStep())

trans_field_door = door.getField("translation")
trans_field_human = human.getField("translation")
#print("trans_field_human",trans_field_human)
trans_field_position = ps.getField("position")
door_values = trans_field_door.getSFVec3f()
start_human_value = trans_field_human.getSFVec3f()
light_status = light.getField("on")
light_value = light_status.getSFBool()
#print("door_values",door_values)
check_start_human_value=[4.0, 1.3188727272727272, 5.0512000000000015]

robot_position_time = [] #This list stores lists containing simulation time and position of the robot

team_info = {} #This would store team info, primarily the team ID after reading it from the JSON file
try:
	with open('../../teaminfo.json') as team_file:
	    team_info = json.load(team_file) #Read team information from the file and store it
except:
	supervisor.simulationSetMode(supervisor.SIMULATION_MODE_PAUSE)
	raise Exception("File not found, please make sure teaminfo.json exists in the parent folder")
	
team_id = team_info['team_id'] #Extract the team ID
if team_id == "eYIC#<Team_id>":
	supervisor.simulationSetMode(supervisor.SIMULATION_MODE_PAUSE)
	raise Exception("Please first edit the teaminfo.json file and enter your team ID in place of eYIC#<Team_id>")

output = {"Team_ID":str(team_id),"door_translation":str(door_values), "start_pedestrian":str(start_human_value), "light_status":str(light_status), "light_value":str(light_value)}

# using map() & reduce() to check if both the lists are exactly equal
result = reduce(lambda a, b: a and b, map(lambda x, y: x == y, start_human_value, check_start_human_value))
if not result:
    supervisor.simulationSetMode(supervisor.SIMULATION_MODE_PAUSE)
    raise Exception("You have changed the position of Pedestrian model")



if str(supervisor.getName())=="robot":
    robot_type=1
    receiver = supervisor.getDevice("receiver")
    receiver.enable(timestep)
    receiver.setChannel(COMMUNICATION_CHANNEL)
else:
    print("Unrecognized robot name", robot.getName())


run_completed=False
message_sent = False 
remaining_time=MAX_TIME
while supervisor.step(TIME_STEP) != -1:

    
    if not run_completed: 
        if receiver.getQueueLength() > 0:
            #time.sleep(5)
            #print("data coming")
            buffer = receiver.getData()
            #print("buffer",buffer)
            if message_printed != 1:
                #print("Communicating: received ", buffer)
                message_printed = 1
            #dataList=struct.unpack("5c",buffer)
            #print("Communicating: received",buffer)
            buffer1 = {"buffer":buffer}
            output.update(buffer1)
            if buffer.startswith(b"S"):
                server_ip = buffer
                server_ip1 = {"server_ip":server_ip}
                output.update(server_ip1)
                #print("server_ip =",server_ip)
            elif buffer.startswith(b"C"):
                client_ip = buffer
                client_ip1 = {"client_ip":client_ip}
                output.update(client_ip1)
                #print("client_ip =",client_ip)
            receiver.nextPacket()
        else:
            if message_printed != 2 :
                #print("Communication broken!")
                message_printed = 2   
        
        light_value = light_status.getSFBool()
        #print("###########")
        #print("light status = ", light_value)  
        #print("###########")             
        human_values = trans_field_human.getSFVec3f()
        #print("human_values",human_values)
        
        ps_values = trans_field_position.getSFFloat()
        #print("ps_values",ps_values)
        
        default_human_values1= [4.0, 1.298, 4.144]
        default_door_values1= [3.95, 0.0, 3.89]
        default_ps_values1= -0.009
        
        default_human_values2= [4.0, 1.340981818181818, 3.0496000000000003]
        default_door_values2= [3.95, 0.0, 3.89]
        default_ps_values2= -1.57
        
        default_human_values3= [4.0, 1.2468000000000006, 3.9663999999999993]
        default_door_values3= [3.95, 0.0, 3.89]
        default_ps_values3= -1.57
        
        default_human_values4= [4.0, 1.25, 5.08]
        default_door_values4= [3.95, 0.0, 3.89]
        default_ps_values4= 0.009
        
        
        
        if functools.reduce(lambda x, y : x and y, map(lambda p, q: p == q,default_human_values1,human_values), True): 
            #actual=round(ps_values,3)
            #print("actual",actual)
             if 0.005 < ps_values < 0.008:
                human_values1=str(human_values)
                ps_values1=ps_values
                message1="Door opening"
                #print("Door opening")
                condition1 = {"human_values1":str(human_values1),"ps_values1":str(ps_values1), "message1":str(message1)}
                output.update(condition1)
                supervisor.simulationSetMode(supervisor.SIMULATION_MODE_PAUSE) #Pause the simulation
             else:
                human_values1=str(human_values)
                ps_values1=ps_values
                message1="Door is not opening"
                print(Fore.RED +"Error : Door is not opening"+ Style.RESET_ALL)
                supervisor.simulationSetMode(supervisor.SIMULATION_MODE_PAUSE) #Pause the simulation
                condition1 = {"human_values1":str(human_values1),"ps_values1":str(ps_values1), "message1":str(message1)}
                output.update(condition1)
            # Send a message back to the robot window
            #supervisor.wwiSendText(message1)
            
        if functools.reduce(lambda x, y : x and y, map(lambda p, q: p == q,default_human_values2,human_values), True): 
            #actual=round(ps_values,3)
            #print("actual",actual)
            if -1.57 < ps_values < -1.40:
                human_values2=str(human_values)
                ps_values2=ps_values
                message2="Door completely opened"
                #print("Door completely opened")
                if light_value == True:
                    #print("Light On")
                    light_flag = 1
                condition2 = {"human_values2":str(human_values2),"ps_values2":str(ps_values2), "message2":str(message2), "light_flag":light_flag}
                output.update(condition2)
                supervisor.simulationSetMode(supervisor.SIMULATION_MODE_PAUSE) #Pause the simulation
            else:
                human_values2=str(human_values)
                ps_values2=ps_values
                message2="Door is not opened"
                print(Fore.RED +"Error : Door is not opened"+ Style.RESET_ALL)
                condition2 = {"human_values2":str(human_values2),"ps_values2":str(ps_values2), "message2":str(message2)}
                output.update(condition2)
                supervisor.simulationSetMode(supervisor.SIMULATION_MODE_PAUSE) #Pause the simulation
            # Send a message back to the robot window
            supervisor.wwiSendText(message2)
                
        if functools.reduce(lambda x, y : x and y, map(lambda p, q: p == q,default_human_values3,human_values), True): 
            #actual=round(ps_values,2)
            #print("actual",actual)
            if -1.57 < ps_values < -1.40 :
                human_values3=str(human_values)
                ps_values3=ps_values
                message3="Door closing"
                #print("Door closing")
                condition3 = {"human_values3":str(human_values3),"ps_values3":str(ps_values3), "message3":str(message3)}
                output.update(condition3)
                supervisor.simulationSetMode(supervisor.SIMULATION_MODE_PAUSE) #Pause the simulation
            else:
                human_values3=str(human_values)
                ps_values3=ps_values
                message3="Door is not closing"
                print(Fore.RED +"Error : Door is not closing"+ Style.RESET_ALL)
                condition3 = {"human_values3":str(human_values3),"ps_values3":str(ps_values3), "message3":str(message3)}
                output.update(condition3)
                supervisor.simulationSetMode(supervisor.SIMULATION_MODE_PAUSE) #Pause the simulation
                
            # Send a message back to the robot window
            supervisor.wwiSendText(message3)
            
        if functools.reduce(lambda x, y : x and y, map(lambda p, q: p == q,default_human_values4,human_values), True): 
            actual=round(ps_values,3)
            #print("actual",actual)
            if 0.009 < ps_values < 0.004:
                human_values4=str(human_values)
                ps_values4=ps_values
                message4="Door completely closed"
                #print("Door completely closed")
                supervisor.simulationSetMode(supervisor.SIMULATION_MODE_PAUSE) #Pause the simulation
                
                if light_value == False:
                    #print("Light Off")
                    light_flag = 0
                condition4 = {"human_values4":str(human_values4),"ps_values4":str(ps_values4), "message4":str(message4), "light_flag":light_flag}
                output.update(condition4)
                supervisor.simulationSetMode(supervisor.SIMULATION_MODE_PAUSE)
                
            else:
                human_values4=str(human_values)
                ps_values4=ps_values
                message4="Door is not closed"
                print(Fore.RED +"Error : Door is not closed"+ Style.RESET_ALL)
                condition4 = {"human_values4":str(human_values4),"ps_values4":str(ps_values4), "message4":str(message4), "light_flag":light_flag}
                output.update(condition4)
                supervisor.simulationSetMode(supervisor.SIMULATION_MODE_PAUSE) #Pause the simulation
            # Send a message back to the robot window
            supervisor.wwiSendText(message4)
            
    f = open('result.bin', 'wb')
    #print("output",output)
    for key in output: # dictionary bypass
        # get the value
        value = output[key]
                
        # Write sequentially key, then value
        svalue = str(value) + '\n' # convert value to string
        skey = key + '\n' # add '\n' to key string
                
        # Convert key:svalue from string to bytes
        b_key = skey.encode()
        b_svalue = svalue.encode()
                
        # write b_key, b_svalue to the file
        f.write(b_key)
        f.write(b_svalue)
    f.close()    
           
        
