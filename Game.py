import random as rd
import numpy as np
from copy import deepcopy
from Score import Score
from Magician import Magician

MOVE_ACTIONS = ["move_up", "move_down", "move_left", "move_right"]
MOVE_COORDS = [(1, 0), (-1, 0), (0, -1), (0, 1)]

class Action:
    def __init__(self, player, act, row, col):
        self.player = player
        self.act = act
        self.row = row
        self.col = col

    def __eq__(self, other):
        return self.player == other.player and self.act == other.act and self.row == other.row and self.col == other.col
    
    def __hash__(self):
        return hash((self.player, self.act, self.row, self.col))

    def __str__(self):
        return self.act + " " + str((self.row, self.col))

class Board:
    def __init__(self, board=None):
        self.current_player = 1
        self.rows = 6
        self.columns = 6                        
        self.player_turn = 1 
        self.states = np.ndarray((self.rows, self.columns), dtype=Magician)
        self.num_magicians = rd.randint(7, 11)
        self.num_witches = rd.randint(5, 6)
        for r in range(self.rows):
            for c in range(self.columns):
                self.states[r][c] = None            
        self.populate()        

    def isValidCoordinate(self, row, col):
        return (
            row < self.rows
            and row >= 0
            and col < self.columns
            and col >= 0 )

    def isAdjacentTo(self, row, col, is_witch):
        for i in range(4):            
            if (
                self.isValidCoordinate(row+MOVE_COORDS[i][0], col+MOVE_COORDS[i][1])
                and self.states[row+MOVE_COORDS[i][0]][col+MOVE_COORDS[i][1]] is not None
                and not self.states[row+MOVE_COORDS[i][0]][col+MOVE_COORDS[i][1]].isStunned
                and self.states[row+MOVE_COORDS[i][0]][col+MOVE_COORDS[i][1]].iswitch == is_witch
            ):
                return True                                            
        return False

    def getCurrentPlayer(self):
        return self.current_player

    def getPossibleActions(self):
        ret = []

        is_witch = self.current_player != 1

        if not is_witch:
            for row in range(self.rows):
                for col in range(self.columns):
                    if self.states[row][col] is not None and self.states[row][col].iswitch:
                        if self.isAdjacentTo(row, col, False):                        
                            ret.append(Action(self.current_player, "kill", row, col))

            for row in range(self.rows):
                for col in range(self.columns):
                    if self.states[row][col] is not None and not self.states[row][col].isVaccinated:
                        if self.states[row][col].iswitch:
                            if self.isAdjacentTo(row, col, False):                      
                                ret.append(Action(self.current_player, "heal", row, col))
                        else:
                            ret.append(Action(self.current_player, "heal", row, col))
                            
        else:
            for row in range(self.rows):
                for col in range(self.columns):
                    if self.states[row][col] is not None and not self.states[row][col].iswitch:
                        if not self.states[row][col].isVaccinated and self.isAdjacentTo(row, col, True):
                            ret.append(Action(self.current_player, "infect", row, col))

        for i in range(4):
            for index, val in np.ndenumerate(self.states):
                if val is not None and val.iswitch == is_witch and not val.isStunned:
                    nrow, ncol = index[0]+MOVE_COORDS[i][0], index[1]+MOVE_COORDS[i][1]                    
                    if self.isValidCoordinate(nrow, ncol) and self.states[nrow][ncol] is None:
                        ret.append(Action(self.current_player, MOVE_ACTIONS[i], index[0], index[1]))

        if len(ret) == 0:
            return [Action(self.current_player, "skip", -1, -1)]

        return ret

    def takeAction(self, action):
        new_board = deepcopy(self)        
        
        new_board.current_player *= -1

        if action.act == "move_up":
            new_board.moveUp(action.row, action.col)
        elif action.act == "move_down":
            new_board.moveDown(action.row, action.col)
        elif action.act == "move_left":
            new_board.moveLeft(action.row, action.col)
        elif action.act == "move_right":
            new_board.moveRight(action.row, action.col)
        elif action.act == "kill":
            new_board.auto_kill(action.row, action.col)
        elif action.act == "heal":
            new_board.auto_heal(action.row, action.col)
        elif action.act == "infect":
            new_board.auto_infect(action.row, action.col)        

        return new_board

    def isTerminal(self):
        return self.num_magicians == 0 or self.num_witches == 0

    def getReward(self):
        return self.num_magicians - self.num_witches

    def __str__(self):
        ret = ""
        for row in self.states:
            for p in row:
                if p is None: ret += "."
                elif p.iswitch:
                    if p.halfCured: ret += "h"
                    else: ret += "z"
                else:
                    if p.isVaccinated: ret += "v"
                    else: ret += "p"
            ret += "\n"
        return ret    

    def move(self, row, col, nrow, ncol):                
        if not self.isValidCoordinate(nrow, ncol):
            return False                
        if self.states[nrow][ncol] is None:
            self.states[nrow][ncol] = deepcopy(self.states[row][col])
            self.states[row][col] = None
            return True
        return False        

    def moveUp(self, row, col):        
        return self.move(row, col, row+1, col)    
    def moveDown(self, row, col):        
        return self.move(row, col, row-1, col)
    def moveLeft(self, row, col):        
        return self.move(row, col, row, col-1)    
    def moveRight(self, row, col):        
        return self.move(row, col, row, col+1)

    def infect(self, row, col):                
        if self.states[row][col] is None:
            return False

        chance = 100
        if self.states[row][col].isVaccinated:
            chance = 0
        elif self.states[row][col].wasVaccinated != self.states[row][col].wasCured:
            chance = 75
        elif self.states[row][col].wasVaccinated and self.states[row][col].wasCured:
            chance = 50
        r = rd.randint(0, 99)
        if r < chance:            
            self.states[row][col] = Magician(True)
            self.num_magicians -= 1
            self.num_witches += 1
            Score.magicians_infected += 1
        return True

    def heal(self, row, col):                
        if self.states[row][col] is None:            
            return (False, None)
        
        if self.states[row][col].iswitch:
            if not self.isAdjacentTo(row, col, False):                                
                return (False, None)

            self.states[row][col] = Magician(False)                
            self.states[row][col].wasCured = True
            self.num_witches -= 1
            self.num_magicians += 1                
            Score.witches_cured += 1
            return (True, "full")                           
        else:
            if self.states[row][col].isVaccinated:
                return (False, None)            
            self.states[row][col].isVaccinated = True
            Score.magicians_vaccinated += 1
            return (True, "vaccine")

    def kill(self, row, col):                  
        if self.states[row][col] is None or not self.states[row][col].iswitch:            
            return False
        if not self.isAdjacentTo(row, col, False):            
            return False
        
        self.states[row][col] = None
        self.num_witches -= 1
        Score.witches_killed += 1
        return True

    def get_possible_human_targets(self):
        coords = []
        for r in range(self.rows):
            for c in range(self.columns):
                if (
                    self.states[r][c] is not None 
                    and not self.states[r][c].iswitch
                    and not self.isAdjacentTo(r, c, True)
                ):                    
                    coords.append((r, c))            
        return coords

    def get_possible_witches_to_move(self):
        coords = []        
        for r in range(self.rows):
            for c in range(self.columns):                            
                if (
                    self.states[r][c] is not None 
                    and self.states[r][c].iswitch 
                    and not self.states[r][c].isStunned 
                    and not self.isAdjacentTo(r, c, False)
                ):
                    coords.append((r, c))    
        return coords        

    def clean_board(self):
        self.states = [[None for _ in range(self.columns)] for _ in range(self.rows)]

    def populate(self):        
        for _ in range(self.num_magicians):
            r = rd.randint(0, self.rows-1)
            c = rd.randint(0, self.columns-1)
            while self.states[r][c] is not None:
                r = rd.randint(0, self.rows-1)
                c = rd.randint(0, self.columns-1)
            self.states[r][c] = Magician(False)
        
        for _ in range(self.num_witches):
            r = rd.randint(0, self.rows-1)
            c = rd.randint(0, self.columns-1)
            while self.states[r][c] is not None:
                r = rd.randint(0, self.rows-1)
                c = rd.randint(0, self.columns-1)
            self.states[r][c] = Magician(True)                

    def witch_move(self):
        possible_infect = []        
        vaccine_infect = []
        for r in range(self.rows):
            for c in range(self.columns):
                p = self.states[r][c]            
                if (
                    p is not None 
                    and not p.iswitch
                    and self.isAdjacentTo(r, c, True)
                ):
                    if not p.isVaccinated: possible_infect.append((r, c))
                    else: vaccine_infect.append((r, c))
        
        if len(possible_infect) > 0:
            coord = rd.choice(possible_infect)
            self.infect(coord[0], coord[1])
            self.current_player *= -1
            return True
        else:            
            human_coords = self.get_possible_human_targets()
            witch_coords = self.get_possible_witches_to_move()
            min_dist = 9999999
            selected_human, selected_witch = (-1, -1), (-1, -1)

            for human in human_coords:
                for witch in witch_coords:
                    dist = abs(human[0] - witch[0]) + abs(human[1] - witch[1])
                    if dist < min_dist and dist > 1:
                        min_dist = dist
                        selected_human, selected_witch = human, witch
            
            if selected_witch == (-1, -1): 
                bored_witches = [] 
                for r in range(self.rows):
                    for c in range(self.columns):                                
                        state = self.states[r][c]
                        if state is not None and state.iswitch and not state.isStunned:                            
                            if not self.isAdjacentTo(r, c, False):
                                bored_witches.append((r, c))

                if len(bored_witches) > 0:                    
                    has_moved = False
                    count = 10
                    while len(bored_witches) > 0 and not has_moved and count > 0:                    
                        witch = rd.choice(bored_witches)
                        action = rd.choice(MOVE_ACTIONS)
                        if action == "moveUp":
                            has_moved = self.moveUp(witch[0], witch[1])
                        elif action == "moveDown":
                            has_moved = self.moveDown(witch[0], witch[1])
                        elif action == "moveLeft":
                            has_moved = self.moveLeft(witch[0], witch[1])
                        elif action == "moveRight":
                            has_moved = self.moveRight(witch[0], witch[1])
                        count -= 1                 

            else: 
                diff_y = selected_human[0] - selected_witch[0]
                diff_x = selected_human[1] - selected_witch[1]

                # Top Left corner is (0, 0)
                if abs(diff_y) > abs(diff_x):
                    if diff_y > 0: self.moveUp(selected_witch[0], selected_witch[1])
                    else: self.moveDown(selected_witch[0], selected_witch[1])
                else:
                    if diff_x > 0: self.moveRight(selected_witch[0], selected_witch[1])
                    else: self.moveLeft(selected_witch[0], selected_witch[1])
        
        self.current_player *= -1
        return False    

    def update_effects(self):        
        for r in range(self.rows):
            for c in range(self.columns):
                if self.states[r][c] is not None:
                    if self.states[r][c].isStunned: self.states[r][c].isStunned = False                
                    if self.states[r][c].isVaccinated:
                        self.states[r][c].turnsVaccinated += 1
                        if self.states[r][c].turnsVaccinated >= 5:
                            self.states[r][c].turnsVaccinated = 0
                            self.states[r][c].isVaccinated = False
                            self.states[r][c].wasVaccinated = True        
        
        Score.turns_taken += 1
