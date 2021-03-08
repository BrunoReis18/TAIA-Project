  
from itertools import product
import random
import time
import copy
import timeit
import numpy as np

ROWS = 8
COLS = 8
DIRS = [(-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1)]

class Board:

    def __init__(self):
        self.finished = False
        self.skip_count = 0
        self.board_pos = {}
        self.playing = 1
        self.cross_pieces = 2
        self.total_pieces = 4
        self.score = {'Cross':2,'Circle':2}
        self.init_liberty = [
        [ 3, 5, 5, 5, 5, 5, 5, 3 ],
        [ 5, 8, 8, 8, 8, 8, 8, 5 ],
        [ 5, 8, 8, 8, 8, 8, 8, 5 ],
        [ 5, 8, 8, 8, 8, 8, 8, 5 ],
        [ 5, 8, 8, 8, 8, 8, 8, 5 ],
        [ 5, 8, 8, 8, 8, 8, 8, 5 ],
        [ 5, 8, 8, 8, 8, 8, 8, 5 ],
        [ 3, 5, 5, 5, 5, 5, 5, 3 ]]

        self.create_board()
        
        self.liberty = [
        [ 3, 5, 5, 5, 5, 5, 5, 3 ],
        [ 5, 8, 8, 8, 8, 8, 8, 5 ],
        [ 5, 8, 7, 6, 6, 7, 8, 5 ],
        [ 5, 8, 6, 5, 5, 6, 8, 5 ],
        [ 5, 8, 6, 5, 5, 6, 8, 5 ],
        [ 5, 8, 7, 6, 6, 7, 8, 5 ],
        [ 5, 8, 8, 8, 8, 8, 8, 5 ],
        [ 3, 5, 5, 5, 5, 5, 5, 3 ]]

    def create_board(self):
        for row in range(8):
            for column in range(8):
                self.board_pos[(row, column)] = 0 #0 meaning empyt 1 black 2 white maybe
        
        self.board_pos[(3,3)] = 2
        self.board_pos[(3,4)] = 1
        self.board_pos[(4,3)] = 1
        self.board_pos[(4,4)] = 2
        self.board_pos[(3,2)] = 3
        self.board_pos[(2,3)] = 3
        self.board_pos[(4,5)] = 3
        self.board_pos[(5,4)] = 3
    
    def update_liberty(self,pos):

        for d in DIRS:
            new_pos = self.sum_tuples(pos,d)
            if not self.is_outside_board(new_pos):
                self.liberty[new_pos[0]][new_pos[1]] -= 1
            
    def pre_compute_rows_cols(self):
        return

    def get_rep(self,val):
        switcher={
                0:' ',
                1:'X',
                2:'O',
                3:'·'}
        return switcher.get(val,"E")

    # turns board coords like "a3" into cartesian coords like (0,2)
    def convert_board_coords_to_array_coords(self,coord):
        row_b = coord[0]
        col_b = int(coord[1])
        
        if col_b < 1 or col_b > 8 or ord(row_b.upper()) < 65 or ord(row_b.upper()) > 72 :
            col = -1
            row = -1
        else:
            col = col_b-1
            row = ord(row_b.upper())-65

        return row,col
    
    def convert_array_coords_to_board_coords(self,coord):    
        col = coord[1]+1
        row = chr(coord[0]  + 65)
        return row+str(col)

    def check_stability(self):
        #iterate over all pieces and asign stability score (1 stable , -1 not stable (imidiate), 0 semistale (not imidiatly))
        return

    def is_outside_board(self,pos):
        #return False if self.board_pos.get(pos,-1) != -1 else True
        return (pos[0] < 0 or pos[0] >= ROWS or pos[1] < 0 or pos[1] >= COLS)

    @staticmethod
    def sum_tuples(t1,t2):
        return (t1[0]+t2[0],t1[1]+t2[1])
    

    @staticmethod
    def sub_tuples(t1,t2):
        return (t1[0]-t2[0],t1[1]-t2[1])
    
    def turn_piece(self,pos):

        self.board_pos[pos] = self.playing

        if self.playing == 1 :
            self.cross_pieces +=1 
        else: 
            self.cross_pieces -= 1

    #turns pieces in a certain direction if they are flanked
    def turn_pieces_dir(self,cntr,dir):
    
        shft = self.sum_tuples(cntr, dir)
        cnt = 0
        turn = False

        while not self.is_outside_board(shft): #iterate over opponent pieces

            if self.board_pos[shft] == 3-self.playing:
                cnt += 1
            if self.board_pos[shft] == self.playing:
                turn = True
                break
            if self.board_pos[shft] == 0 or self.board_pos[shft] == 3:
                break

            shft = self.sum_tuples(shft,dir)

        if turn:
            for c in range(cnt):
                shft = self.sub_tuples(shft,dir)
                self.turn_piece(shft)

    def check_mobility_dir(self,cntr,dir):
    
        shft = self.sum_tuples(cntr, dir)
        cnt = 0
        turn = False

        while 1: #iterate over opponent pieces note: this config of if statements maximizes 
            
            if self.is_outside_board(shft):
                break

            if self.board_pos[shft] == 0:  
                break
            
            if self.board_pos[shft] == self.playing:
                turn = True
                break

            if self.board_pos[shft] == 3:
                break
            
            if self.board_pos[shft] == 3-self.playing:
                cnt += 1

            
            shft = self.sum_tuples(shft,dir)

        return (cnt > 0 and turn == True)

    #Checks possible moves
    def check_mobility(self):
        for k in self.board_pos.keys():
            if self.board_pos[k] == 3:
                    self.board_pos[k] = 0
        
        for k in self.board_pos.keys():
            if self.board_pos[k] == 0 and self.liberty[k[0]][k[1]] < self.init_liberty[k[0]][k[1]]:

                for dir in DIRS:
                    mob = self.check_mobility_dir(k,dir)
                    if mob:
                        self.board_pos[k] = 3
                        break
    
    def update_board(self,coord,rand=False):
        skip = False

        playable_squares = [k for k,v in self.board_pos.items() if v == 3]


        if len(playable_squares) == 0:
            self.skip_count += 1

            if self.skip_count > 1:
                self.finished = True
                return False # end game

            
            else: # se for só 1 skip muda so o jogador
                if self.playing == 1:
                    self.playing = 2

                else:
                    self.playing = 1

                self.check_mobility()

                return True
        
        self.skip_count = 0

        if rand:
            row,col = random.choice(playable_squares)
        else:
            row,col = self.convert_board_coords_to_array_coords(coord)
        
        if row < 0 or col < 0:
            return -1
        

        self.board_pos[(row,col)] = self.playing
        
        self.update_liberty((row,col))

        for dir in DIRS:
            self.turn_pieces_dir((row,col),dir)
        
        self.total_pieces += 1
        if self.playing == 1:
            self.cross_pieces +=1
            self.playing = 2

        else:
            self.playing = 1

        self.check_mobility()
    
        self.score = {'Cross':self.cross_pieces,'Circle':self.total_pieces-self.cross_pieces}

        if self.total_pieces == 64:
            self.finished = True
            return False
        else:
            return True

    def draw_board(self):
        c = 65

        # First row
        print(f"  ", end='')
        for j in range(8):
            print(f"| {j+1} ", end='')
        print(f"| ", end='')
        print()
        print(f'{(8*4+4)*"-"}')

        # Other rows
        for row in range(8):
            print(f"{chr(c+row)} ", end='')
            for column in range(8):
                print(f"| {self.get_rep(self.board_pos[(row,column)])} ", end='')
            print(f"| ", end='')
            print()
            print(f'{(8*4+4)*"-"}')
        print(f"SCORE - X:{self.score['Cross']} O:{self.score['Circle']}          PLAYING: {self.get_rep(self.playing)}")

def main():

    start = time.process_time()
    othello_board = Board()
    
    for i in range(1000):
        othello_board = Board()
        othello_board.draw_board()
        going = True
        while going:
            going = othello_board.update_board("",True)
            othello_board.draw_board()

    print(time.process_time() - start)



if __name__ == "__main__":
    main()