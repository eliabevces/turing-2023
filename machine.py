import json

class Machine:

  def __init__(self) -> None:

    f = open('machine.json')
    machineJson = json.load(f)    
    f.close()

    self.states = machineJson["states"].split(" ")
    self.alphabet = machineJson["alphabet"].split(" ")
    self.tape_simbols = machineJson["tapeSymbols"].split(" ")
    self.transitions = (machineJson["transitions"])
    self.initial_state = machineJson["initialState"]
    self.final_states = machineJson["finalStates"].split(" ")
