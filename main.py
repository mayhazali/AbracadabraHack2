import pygame
import random as rd 
import UI as UI
from Score import Score
from Game import Board

running = True
take_action = []
playerMoved = False

pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.mixer.init()
click = pygame.mixer.Sound("Assets/click.wav")

StartButton = pygame.Rect(455, 600, 300, 100)
procstart = False
starthover = ""
while procstart == False:
    for event in pygame.event.get():
        UI.display_start_screen(starthover)
        starthover = ""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if StartButton.collidepoint(pygame.mouse.get_pos()):
                click.play()
                procstart = True
        elif event.type == pygame.MOUSEMOTION:
            if StartButton.collidepoint(pygame.mouse.get_pos()):
                starthover = "start"
        elif event.type == pygame.QUIT:
            pygame.quit()

global GameBoard
GameBoard = Board()
proceed = True
clock = pygame.time.Clock()
frame = 0

hat_img = pygame.image.load("Assets/hat.png").convert_alpha()
hat_img = pygame.transform.scale(hat_img, (100,100))
KillButton = hat_img.get_rect(topleft=(880, 180))

wand_img = pygame.image.load("Assets/wand.png").convert_alpha()
HealButton = wand_img.get_rect(topleft=(880, 400))

def play_game():
    global GameBoard

    if action.act == "move_up":
        GameBoard.moveUp(action.row, action.col)        
    elif action.act == "move_down":
        GameBoard.moveDown(action.row, action.col)
    elif action.act == "move_left":
        GameBoard.moveLeft(action.row, action.col)
    elif action.act == "move_right":
        GameBoard.moveRight(action.row, action.col)
    elif action.act == "kill":
        GameBoard.auto_kill(action.row, action.col, simulation=False)
    elif action.act == "heal":
        GameBoard.auto_heal(action.row, action.col, simulation=False)
    elif action.act == "infect":
        raise "Player is not allowed to infect"    

    GameBoard.current_player *= -1    

score = 0
move = 0
game_number = 1
button_press = pygame.mixer.Sound("Assets/button_press.wav")
button_up = pygame.mixer.Sound("Assets/button_up.wav")
throw = pygame.mixer.Sound("Assets/throw.wav")
potion_break = pygame.mixer.Sound("Assets/hat.wav")
unfect = pygame.mixer.Sound("Assets/unfect.wav")
vaccine = pygame.mixer.Sound("Assets/wand.wav")
witch_infect = pygame.mixer.Sound("Assets/witches-spell.wav")
hat = pygame.mixer.Sound("Assets/hat.wav")
Score.reset_data()

while running:        
    UI.run(GameBoard)                
    for event in pygame.event.get():
        if HealButton.collidepoint(pygame.mouse.get_pos()):
            if event.type == pygame.MOUSEBUTTONUP:                          
                button_up.play()
                take_action.append("heal")
            elif event.type == pygame.MOUSEBUTTONDOWN:                     
                button_press.play()                     
        if KillButton.collidepoint(pygame.mouse.get_pos()):
            if event.type == pygame.MOUSEBUTTONUP:                          
                button_up.play()
                take_action.append("kill")
            elif event.type == pygame.MOUSEBUTTONDOWN:                      
                button_press.play()
        if event.type == pygame.MOUSEBUTTONUP:
            if len(take_action) < 2:                                        
                x, y = pygame.mouse.get_pos()                               
                action = UI.get_action(GameBoard, x, y)                                       
                if action != None:                                                
                    if take_action == []:                                   
                        if ((GameBoard.states[action[0]][action[1]] is not None) and (GameBoard.states[action[0]][action[1]].iswitch == False)):
                            click.play()
                            take_action.append(action)
                    else:                                                  
                        click.play()                          
                        take_action.append(action)
        if event.type == pygame.QUIT:
            running = False

    if len(take_action) == 2:
        if take_action[0] == take_action[1]:
            take_action = []
        elif isinstance(take_action[1], str):
            take_action.pop(0)

    if len(take_action) == 1:
        if not isinstance(take_action[0], str):
            UI.select(take_action[0])

    if len(take_action) == 2:
        if not isinstance(take_action[0], str):
            result = None
            directionToMove = UI.direction(take_action[0], take_action[1])
            if directionToMove == "moveUp":
                result = GameBoard.moveUp(take_action[0][0], take_action[0][1])
            elif directionToMove == "moveDown":
                result = GameBoard.moveDown(take_action[0][0], take_action[0][1])              
            elif directionToMove == "moveLeft":
                result = GameBoard.moveLeft(take_action[0][0], take_action[0][1])
            elif directionToMove == "moveRight":
                result = GameBoard.moveRight(take_action[0][0], take_action[0][1])
            if result != False:
                playerMoved = True
            take_action = []
        elif take_action[0] == "heal":
            result = GameBoard.heal(take_action[1][0], take_action[1][1])
            if result[0] != False:
                playerMoved = True
                if result[1] == "half": 
                    while frame < 27:
                        if frame == 0:
                            throw.play()
                        if frame == 5:
                            potion_break.play()
                        UI.half_heal_animation(frame)
                        pygame.display.update()                            
                        clock.tick(12)
                        frame += 1
                    frame = 0
                    score += 25
                elif result[1] == "full":
                    while frame < 27:
                        if frame == 0:
                            throw.play()
                        if frame == 3:
                            unfect.play()
                        UI.full_heal_animation(frame)
                        pygame.display.update()                            
                        clock.tick(8)
                        frame += 1
                    frame = 0
                    score += 25
                elif result[1] == "vaccine": 
                    while frame < 27:
                        if frame == 0:
                            throw.play()
                        if frame == 3:
                            vaccine.play()
                        UI.vaccine_animation(frame)
                        pygame.display.update()                            
                        clock.tick(8)
                        frame += 1
                    frame = 0
                    score += 10
            take_action = []
        elif take_action[0] == "kill":
            result = GameBoard.kill(take_action[1][0], take_action[1][1])
            if result != False:
                playerMoved = True                         
                while frame < 24:
                    if frame == 5:
                        hat.play()
                    UI.kill_animation(frame)
                    pygame.display.update()                        
                    clock.tick(8)
                    frame += 1
                frame = 0
                score += 50
            take_action = []
        move += 1
    if GameBoard.num_magicians == 0:
        UI.display_lose_screen(GameBoard.num_witches)
        if event.type == pygame.QUIT:
            running = False
    if GameBoard.num_witches == 0:
        times = 1000 - (move*50)
        bonus = GameBoard.num_magicians*100
        Score.magicians_remaining = GameBoard.num_magicians
        UI.display_win_screen(GameBoard.num_magicians, score, times, bonus)
        if event.type == pygame.QUIT:
            running = False
            break            

    # Computer turn
    if playerMoved:
        UI.run(GameBoard)
        pygame.display.update()
        playerMoved = False
        take_action = []
        tempcalc = GameBoard.num_magicians           
        actions = GameBoard.witch_move()
        if GameBoard.num_magicians == tempcalc-1:
            while frame < 19:
                if frame == 4:
                    witch_infect.play()
                UI.witch_infect(frame)
                pygame.display.update()                            
                clock.tick(8)
                frame += 1
            frame = 0     
            score += -50        
        GameBoard.update_effects()
    pygame.display.update()
