#Import the Supervisor
from controller import Supervisor
from Sensors import Device
import requests


                
#Main Function        
def main():
    ######### Do not change these lines ###########
    #Initialise the robot
    robot = Supervisor()
    # get the time step of the current world.
    timestep = int(robot.getBasicTimeStep())
    ###############################################

    # initialise the sensors
    device = Device(robot)

    print("getting sensors.................................")
    ts = device.get_Device('Temperature')
    hs = device.get_Device('Humidity')
    ph1 = device.get_Device('PH sensor1')
    ph2 = device.get_Device('PH sensor2')
    ms1 = device.get_Device('Moisture sensor1')
    ms2 = device.get_Device('Moisture sensor2')
    print("Sensors are ready to use............")

    ts.enable(timestep)
    hs.enable(timestep)
    ph1.enable(timestep)
    ph2.enable(timestep)
    ms1.enable(timestep)
    ms2.enable(timestep)

    value = [0,0,0,0,0,0]
    
    
    
    
    #Main loop
    while robot.step(timestep) != -1:
        value[0] = ts.getValue()
        value[1] = hs.getValue()
        value[2] = ph1.getValue()
        value[3] = ph2.getValue()
        value[4] = ms1.getValue()
        value[5] = ms2.getValue()

        print("Sensors values are: {} {} {} {} {} {}".format( value[0], value[1], value[2], value[3], value[4], value[5]) )
        parameters = {"id": "Sheet1", "Team_ID": 'eyic_iot_714', "Temperature" : value[0], "Humidity" : value[1], "PH_value_Field1": value[2], "PH_value_Field2" : value[3], "Moisture_Field1" : value[4], "Moisture_Field2" : value[5]}
        URL = "https://script.google.com/macros/s/AKfycbxV1CiDBadbLcviN61uCDJIzQY_FYeW5vGkuvD06ZZhez-ZiqRrHU2sQMXEFMj4h-ikdA/exec"
        response = requests.get(URL, params = parameters)
        print(response.content)
        
            
            
       
if __name__ == "__main__":
    main()