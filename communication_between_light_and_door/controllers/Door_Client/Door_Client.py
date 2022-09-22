#Import required
import socket
from controller import Robot
import struct

########## Do not touch these values #############
COMMUNICATION_CHANNEL = 1
message_printed = 0
robot_type = 1
##################################################
FORMAT = 'utf-8'

class Client:
    #Client Class    
    def __init__(self,robot_type):
        #Create Client socket
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #localhost
        self.host = socket.gethostname()
        #Reserved port
        self.port = 8888
        #Connect to the reserved port
        self.client.connect((self.host, self.port))
        
        ########## Do not touch these lines ###########
        if robot_type == 0:
           
            s = struct.Struct(b'c 19s')
            data = s.pack('C'.encode('utf-8'), str(self.client.getpeername()).encode('utf-8'))
            emitter.send(data)
        ##############################################
        
    def client_send(self, arg_message):
        #Function to send message
        mssg = bytes(arg_message.encode('utf-8'))
        self.client.send(mssg)
        # emitter.send(mssg)
        print("Client: Message sent successfully")

              
    def close_socket(self):
        #Function to close the client socket
        self.client.close()
        
        
########## Do not touch these lines ###########
robot = Robot()
if str(robot.getName())=="smartdoor":
    robot_type = 0
    emitter = robot.getDevice("emitter")
    channel = emitter.getChannel()
    if channel != COMMUNICATION_CHANNEL:
        communication.setChannel(COMMUNICATION_CHANNEL)
##############################################


#Main Function                  
def main():
    
        
    #Time Step
    timestep = int(robot.getBasicTimeStep())

    #getting devices
    ds1 = robot.getDevice('ds1')
    ds2 = robot.getDevice('ds2')
    ps = robot.getDevice('ps')
    motor = robot.getDevice('door motor')

    ds1.enable(timestep)
    ds2.enable(timestep)
    ps.enable(timestep)

    ds1_max_value = ds1.getMaxValue()
    ds2_max_value = ds2.getMaxValue()
    print("The maximum value of ds 1 is", ds1_max_value)

    motor.setPosition(float('inf'))
    motor.setVelocity(0.0)
    motor_speed1 = -1
    motor_speed2 = 1.5

    value = [0,0,0]
    
    print("-----------------------")
    
  
    #Main loop
    while robot.step(timestep) != -1:
        client = Client(robot_type)
        
        value[0] = ds1.getValue()
        value[1] = ds2.getValue()
        value[2] = ps.getValue()
        print("values : {} {} {}".format(value[0], value[1], value[2]))

        if(value[0] < ds1_max_value):
            ds1.enable(timestep)
            ds2.disable()
            print("Entering")
            message_1 = "On"
            client.client_send(message_1)
            motor.setVelocity(motor_speed1)

        if(value[2] <= -1.57):
            ds2.enable(timestep)
            motor.setVelocity(0.0)

        if(value[1] < ds2_max_value):
            ds1.disable()
            print("Exiting")
            message_2 = "Off"
            client.client_send(message_2)
            motor.setVelocity(motor_speed2)
    
        client.close_socket()
        
        

    

                                           
if __name__ == "__main__":
    main()
