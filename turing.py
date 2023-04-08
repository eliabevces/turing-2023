from tape import Tape
from transition import Transition
import pygame
import sys
import json




# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
width_center = screen.get_width() / 2
height_center = screen.get_height() / 2
running = True
player_pos =  pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
base_font = pygame.font.Font(None, 32)
user_text = ''
input_rect = pygame.Rect(200, 200, 140, 32)
color_active = pygame.Color('white')
color_passive = pygame.Color('grey')
color = color_passive

active = False


accept = False
# excluir futuramente
FRAMES_SEC = 10

class TuringMachine:
  


  def __init__(self) -> None:
      
    f = open('machine.json')
    machineJson = json.load(f)    
    f.close()

    # setupla
    self.states = machineJson["states"].split(" ")
    self.alphabet = machineJson["alphabet"].split(" ")
    self.tape_simbols = machineJson["tapeSymbols"].split(" ")
    self.transitions = self.setTransitions(machineJson["transitions"])
    self.initial_state = machineJson["initialState"]
    self.state = machineJson["initialState"]
    self.final_states = machineJson["finalStates"].split(" ")
    self.blank = 'B'
    self.tape = Tape()
    self.resetMachine()

      

  def resetMachine(self) -> None :
    self.tape.resetTape()
    self.setState( self.initial_state )


  def moveTape(self, direction: str) -> None:
    if (direction == 'R'):
      self.tape.moveRight()
      player_pos.x -= 40
    elif (direction == 'L'):
      self.tape.moveLeft(player_pos.x)
      player_pos.x += 40
    
  def changeState(self, transition: Transition) -> None: 
    player_pos.x = self.tape.checkFirstLast(player_pos.x)
    self.tape.setCharAt(self.tape.getHead(), transition.getWrite())
    self.setState(transition.getToState())
    self.moveTape(transition.getDirection())
    

  #  GETTERS e SETTERS

  #  SET ALL TRANSITIONS
  def setTransitions(self, jsonTransitions)-> None:
      transitions = []
      for tr in jsonTransitions:
        transition = Transition( tr["fromS"] ,tr["read"], tr["toS"], tr["write"], tr["direction"] )
        transitions.append(transition)
      return transitions
      

  # GET NEXT TRANSITION
  def getTransition(self, from_state: str, read: str) -> Transition:
    for transition in self.transitions:
      if transition.getFromState() == from_state and transition.getRead() == read:
        return transition
    return None



  def getState(self)-> str:
      return self.state


  def setState(self, state: str) ->  None:
      self.state = state


def drawTape():
    for i in range(len(turingMac.tape.entrada)):
        pygame.draw.polygon(screen, "white", (((20 + i*40)+player_pos.x, 350), ((60 + i*40)+player_pos.x, 350), ((60 + i*40)+player_pos.x, 250), ((20 + i*40)+player_pos.x, 250)))
        pygame.draw.line(screen, "black", ((20 + i*40)+player_pos.x, 250), ((20 + i*40)+player_pos.x, 350), 2)
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render(turingMac.tape.entrada[i], True, (0, 0, 0), (255, 255, 255))
        textRect = text.get_rect()
        textRect.center = ((i*40)+player_pos.x, 300)
        screen.blit(text, textRect)


def drawAccept():
    if accept:
       frase = 'Aceito'
    else:
        frase = 'Rejeitado'
    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render(frase, True, (0, 0, 0), (255, 255, 255))
    textRect = text.get_rect()
    textRect.center = (width_center, height_center/2)
    screen.blit(text, textRect)

  

turingMac = TuringMachine()



while running:
  for event in pygame.event.get():

    # if user types QUIT then the screen will close
      if event.type == pygame.QUIT:
          pygame.quit()
          sys.exit()

      if event.type == pygame.MOUSEBUTTONDOWN:
          if input_rect.collidepoint(event.pos):
              active = True
          else:
              active = False

      if event.type == pygame.KEYDOWN:

          # Check for backspace
          if event.key == pygame.K_BACKSPACE:

              # get text input from 0 to -1 i.e. end.
              user_text = user_text[:-1]
          elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
              turingMac.tape.entrada = list(user_text)
              running = False

          # Unicode standard is used for string
          # formation
          else:
              user_text += event.unicode
    
  screen.fill((0, 0, 0))

  if active:
      color = color_active
  else:
      color = color_passive
        
  # draw rectangle and argument passed which should
  # be on screen
  pygame.draw.rect(screen, color, input_rect)

  text_surface = base_font.render(user_text, True, (0, 0, 0))
    
  # render at position stated in arguments
  screen.blit(text_surface, (input_rect.x+5, input_rect.y+5))
    
  # set width of textfield so that text cannot get
  # outside of user's text input
  input_rect.w = max(100, text_surface.get_width()+10)
    
  # display.flip() will update only a portion of the
  # screen to updated, not full area
  pygame.display.flip()
    
  # clock.tick(60) means that for every second at most
  # 60 frames should be passed.
  clock.tick(60)

running = True

while running:

  for event in pygame.event.get():
      if event.type == pygame.QUIT:
          running = False

  screen.fill("blue")
  pygame.draw.polygon(screen, "purple", ((width_center, height_center), (width_center+50, height_center+50), (width_center-50, height_center+50)))
  pygame.draw.polygon(screen, "white", ((20, 350), (1240, 350), (1240, 250), (20,250))) #L_D , R_D, R_U, L_U
  drawTape()
  clock.tick(FRAMES_SEC)

  transition = turingMac.getTransition(turingMac.getState(), turingMac.tape.getCharAt(turingMac.tape.getHead()))
  if (transition != None):
    turingMac.changeState(transition)
  else:
    if(turingMac.getState() in turingMac.final_states):
      accept = True
    else:
      accept = False
    drawAccept()
  # flip() the display to put your work on screen
  pygame.display.flip()





