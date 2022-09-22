"""e-puck-supervisor controller."""

from controller import Supervisor, Robot
import sys
import json
import functools
from functools import reduce
from colorama import Fore
from colorama import Style

supervisor = Supervisor()



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

