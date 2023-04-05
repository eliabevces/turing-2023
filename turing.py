from asyncio import sleep
from tape import Tape
from transition import Transition
from machine import Machine

# excluir futuramente
SLEEP_TIME = 300

class TuringMachine:
  


  def __init__(self, machine) -> None:


      # setupla
      self.states = machine.states
      self.alphabet = machine.alphabet
      self.tape_simbols = machine.tape_simbols
      self.transitions = []
      self.state = machine.initial_state
      self.blank = 'B'
      self.final_states = machine.final_states
      self.tape = Tape()
      self.transitions = self.setTransitions(machine.transitions)
      self.resetMachine()

  def resetMachine(self) -> None :
    self.tape.resetTape()
    # self.setState( machine.initial_state ) TODO

  
  def runMachine (self, entrada: list) -> bool :
    self.tape.setEntrada(entrada)
    while (True):
      transition = self.getTransition(self.getState(), self.tape.getCharAt(self.tape.getHead()))
      if (transition != None):
        # sleep(SLEEP_TIME)
        print(transition.fromState, transition.read, transition.toState, transition.write, transition.direction)
        self.changeState(transition)
      else:
        if(self.getState() in self.final_states):
          return True
        else:
          return False

  def moveTape(self, direction: str) -> None:
    if (direction == 'R'):
      self.tape.moveRight()
    elif (direction == 'L'):
      self.tape.moveLeft()
    
  def changeState(self, transition: Transition) -> None: 
    self.tape.setCharAt(self.tape.getHead(), transition.getWrite())
    self.setState(transition.getToState())
    self.moveTape(transition.getDirection())
    

  #  GETTERS e SETTERS

  #  SET ALL TRANSITIONS
  def setTransitions(self, jsonTransitions)-> None:
      transitions = []
      for tr in jsonTransitions:
        transition = Transition( tr["fromS"] ,tr["read"], tr["toS"], tr["write"], tr["direction"] )
        print( tr["fromS"] ,tr["read"], tr["toS"], tr["write"], tr["direction"] )
        transitions.append(transition)
      return transitions
      

  # GET NEXT TRANSITION
  def getTransition(self, from_state: str, read: str) -> Transition:
    for transition in self.transitions:
      if transition.getFromState() == from_state and transition.getRead() == read:
        print(transition)
        return transition
    return None



  def getState(self)-> str:
      return self.state


  def setState(self, state: str) ->  None:
      self.state = state

        
  
mac = Machine()
TuringMachine(mac)