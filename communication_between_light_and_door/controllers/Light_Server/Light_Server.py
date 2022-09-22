#Import required
from controller import Robot
from controller import Device
import socket
import struct
from controller import LED

########## Do not touch these values #############
COMMUNICATION_CHANNEL = 1
message_printed = 0
robot_type = 1
##################################################
FORMAT ='utf-8'


class Server:
    #Server Class    
    def __init__(self, robot_type):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = '192.168.101.4'
        self.port = 8888
        self.server.bind(('', self.port))
           
        
        
    def server_listen(self):
        self.server.listen(1024)
        
              
    def accept_connection(self, robot_type):
        self.connection , self.address = self.server.accept()
        print("Server: Connection has been established from ", self.address)
        
        ########## Do not touch these lines ###########
        if robot_type == 0:
            s = struct.Struct(b'c 19s')
            packed_data = s.pack('S'.encode('utf-8'), str(self.connection.getsockname()).encode('utf-8'))
            emitter.send(packed_data)
        ##################################################
        
        
    def get_message(self):
        self.message = self.connection.recv(1024).decode(FORMAT)
        self.message_1 = self.connection.recv(1024).decode(FORMAT)
        print("Server: Message recieved",self.message, self.message_1)
        
        
        ########## Do not touch these lines ###########
        s = struct.Struct(b'3s')
        packed_data = s.pack(str(self.message).encode('utf-8'))
        emitter.send(packed_data)
        ##################################################
              
    def close_socket(self):
        self.connection.close()
        
        


def accept(arg_server , light_on, process_finished):
        #This function accept the request made by the client and process the request
        # conn , addr = 
        pass
        


########## Do not touch these lines ###########           
robot = Robot()
if str(robot.getName())=="light1":
    robot_type = 0
    emitter = robot.getDevice("emitter")
    #emitter.enable(timestep)
    channel = emitter.getChannel()
    if channel != COMMUNICATION_CHANNEL:
        communication.setChannel(COMMUNICATION_CHANNEL)
##############################################


#Main Function 
def main():
         
    
    timestep = int(robot.getBasicTimeStep())
    server = Server(robot_type)
    
    
    light = LED('led')
    
    
    
    # Main loop 
    while robot.step(timestep) != -1:
        server.server_listen()
        server.accept_connection(robot_type)
        server.get_message()
        
    
        """
        Start a thread to accept the client connection request and wait for the process to finished
        and then close the socket from client side and continue loop to wait for other request from new client
        Use server.accept() in thread because it is blocking in nature
        """
        
        

        if server.message == "On":
            light.set(1)
            val_light = light.get()
            print("Value from LED: ",val_light)

            print("------------------Light is on------------------")
        

        elif server.message == "Off":
            light.set(0)
            val_light_1 = light.get()
            print("Value from LED: ",val_light_1)
            print("-----------Light is off---------------")
        server.close_socket
            


if __name__ == "__main__":
    main()

