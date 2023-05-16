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
player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
base_font = pygame.font.Font(None, 32)
label_font = pygame.font.Font(None, 40)
user_text = ""
input_rect = pygame.Rect(200, height_center - 16, 140, 32)
color_active = pygame.Color("white")
color_passive = pygame.Color("grey")
color = color_passive
active = False

running = True
accept = False
FRAMES_SEC = 1


class TuringMachine:
    def __init__(self) -> None:
        f = open("machine.json")
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
        self.blank = "B"
        self.tape = Tape()
        self.resetMachine()

    def resetMachine(self) -> None:
        self.tape.resetTape()
        self.setState(self.initial_state)

    def moveTape(self, direction: str) -> None:
        if direction == "R":
            self.tape.moveRight()
            player_pos.x -= 40
        elif direction == "L":
            self.tape.moveLeft(player_pos.x)
            player_pos.x += 40

    def changeState(self, transition: Transition) -> None:
        self.tape.setCharAt(self.tape.getHead(), transition.getWrite())
        self.setState(transition.getToState())
        self.moveTape(transition.getDirection())

    #  GETTERS e SETTERS

    #  SET ALL TRANSITIONS
    def setTransitions(self, jsonTransitions) -> None:
        transitions = []
        for tr in jsonTransitions:
            transition = Transition(
                tr["fromS"], tr["read"], tr["toS"], tr["write"], tr["direction"]
            )
            transitions.append(transition)
        return transitions

    # GET NEXT TRANSITION

    def getTransitions(self, from_state: str, read: str) -> list[Transition]:
        transition_list = []
        for transition in self.transitions:
            if (transition.getFromState() == from_state and (transition.getRead() == read or transition.getRead() == "E") ) :
                transition_list.append(transition)
        return transition_list

    def getState(self) -> str:
        return self.state

    def setState(self, state: str) -> None:
        self.state = state


def drawTape():
    player_pos.x = turingMac.tape.checkFirstLast(player_pos.x)
    for i in range(len(turingMac.tape.entrada)):
        pygame.draw.polygon(
            screen,
            "white",
            (
                ((20 + i * 40) + player_pos.x, 349),
                ((60 + i * 40) + player_pos.x, 348),
                ((60 + i * 40) + player_pos.x, 251),
                ((20 + i * 40) + player_pos.x, 251),
            ),
        )
        pygame.draw.line(
            screen,
            "black",
            ((20 + i * 40) + player_pos.x, 249),
            ((20 + i * 40) + player_pos.x, 350),
            2,
        )
        font = pygame.font.Font("freesansbold.ttf", 32)
        text = font.render(turingMac.tape.entrada[i], True, (0, 0, 0), (255, 255, 255))
        textRect = text.get_rect()
        textRect.center = ((i * 40) + player_pos.x, 300)
        screen.blit(text, textRect)


def drawAccept():
    if accept:
        color = (2, 153, 42) # Verde
        frase = "Aceito!"
    else:
        color = (156, 3, 3) # Vermelho
        frase = "Rejeitado!"
    font = pygame.font.Font("freesansbold.ttf", 32)
    text = font.render(frase, True, color)
    textRect = text.get_rect()
    textRect.center = (width_center, height_center / 2)
    screen.blit(text, textRect)

def drawRollback():
    color = (0, 0, 250) # Verde
    frase = "Rollback!"
    font = pygame.font.Font("freesansbold.ttf", 32)
    text = font.render(frase, True, color)
    textRect = text.get_rect()
    textRect.center = (width_center, height_center / 2)
    screen.blit(text, textRect)
    pygame.display.flip()
    refreshscreen()


def drawCurrentState():
    font = pygame.font.Font("freesansbold.ttf", 32)
    text = font.render(turingMac.getState(), True, (0, 0, 0))
    textRect = text.get_rect()
    textRect.center = (width_center, height_center + height_center / 4)
    screen.blit(text, textRect)
    
def drawInputScreen():
    screen.fill((0, 0, 0))

    if active:
        color = color_active
    else:
        color = color_passive

    # desenha retangulo e argumento passado que deveriam estar na tela
    pygame.draw.rect(screen, color, input_rect)

    label_field = label_font.render("Digite uma entrada:", True, (255, 255, 255))
    text_surface = base_font.render(user_text, True, (0, 0, 0))

    # renderiza nas posicoes indicadas nos argumentos
    screen.blit(label_field, (input_rect.x, input_rect.y - 40))
    screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))

    # seta largura do campo de texto para que o texto não saia do input do usuário
    input_rect.w = max(100, text_surface.get_width() + 10)

    # atualiza tela
    pygame.display.flip()

    # para cada segundo, no máximo 60 frames serão passados
    clock.tick(60)
    
def drawTapeScreen():
    screen.fill("grey")
    pygame.draw.polygon(
        screen,
        "purple",
        (
            (width_center, height_center),
            (width_center + 50, height_center + 50),
            (width_center - 50, height_center + 50),
        ),
    )
    pygame.draw.polygon(
        screen, "white", ((5, 350), (1275, 350), (1275, 250), (5, 250))
    )  # L_D , R_D, R_U, L_U
    pygame.draw.polygon(
        screen, "black", ((5, 350), (1275, 350), (1275, 250), (5, 250)), 1
    )  # L_D , R_D, R_U, L_U

def refreshscreen():
    drawTapeScreen()
    drawTape()
    
    drawCurrentState()

    clock.tick(FRAMES_SEC)
    pygame.display.flip()


# RECURSÃO DE EXECUÇÃO     
def mtn(turingMac, transition_list):
    refreshscreen()
    
    global accept
    if accept:
        return
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    for transition in transition_list:
        turingMac.changeState(transition)

        mtn(turingMac, turingMac.getTransitions(
            turingMac.getState(), turingMac.tape.getCharAt(turingMac.tape.getHead())
        ))

        if turingMac.getState() in turingMac.final_states:
            accept = True
            return
        else:
            if transition.getDirection() == "R":
                direction = "L"
                turingMac.tape.setCharAt(turingMac.tape.getHead()-1, transition.read)
            elif transition.getDirection() == "L":
                direction = "R"
                turingMac.tape.setCharAt(turingMac.tape.getHead()+1, transition.read)

            turingMac.setState(transition.fromState)
            turingMac.moveTape(direction)

            drawRollback()
            refreshscreen()


# INICIO DA EXECUCAO

turingMac = TuringMachine()

##############################
# Primeira tela - Ler input do usuário
##############################
while running:
    drawInputScreen()
    
    for event in pygame.event.get():
        # Detecta acao de fechar a tela pelo usuario e da QUIT no programa
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if input_rect.collidepoint(event.pos):
                active = True
            else:
                active = False

        if event.type == pygame.KEYDOWN:
            # Verifica tecla de backspace ("apagar")
            if event.key == pygame.K_BACKSPACE:
                # para cada vez pressionado tira um elemento do input
                user_text = user_text[:-1]
            elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                turingMac.tape.entrada = list(user_text)
                running = False

            # É utilizado padrão Unicode para strings
            else:
                user_text += event.unicode

running = True

##############################
# Segunda tela - Processar input do usuário
##############################
mtn(
    turingMac,
    turingMac.getTransitions(
            turingMac.getState(), turingMac.tape.getCharAt(turingMac.tape.getHead())
        )
)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    drawAccept()

    pygame.display.flip()
