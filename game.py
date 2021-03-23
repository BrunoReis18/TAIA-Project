  
from itertools import product
import random
import time
import copy
import timeit
import numpy as np

from immutables import Map



BEST_ORDER = [(7, 7), (7, 0), (0, 7), (0, 0), (7, 3), (5, 0), (0, 2), (0, 3), (0, 4), (0, 5), (7, 5), (2, 0), (2, 7), (3, 0), (7, 2), (4, 0), (4, 7), (3, 7), (7, 4), (5, 7), (5, 5), (3, 4), (5, 2), (2, 2), (2, 5), (4, 4), (4, 3), (3, 3), (2, 3), (2, 4), (5, 4), (3, 2), (3, 5), (5, 3), (4, 2), (4, 5), (3, 6), (5, 1), (6, 5), (1, 2), (1, 3), (1, 4), (1, 5), (6, 4), (2, 1), (2, 6), (5, 6), (6, 3), (6, 2), (3, 1), (4, 1), (4, 6), (0, 6), (0, 1), (7, 1), (7, 6), (6, 7), (1, 0), (6, 0), (1, 7), (6, 6), (1, 1), (1, 6), (6, 1)]

class Board:

    rows = 8
    cols = 8

    dirs = [(-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1)]
    conerns = {(0,0),(0,7),(7,0),(7,7),(1,0),(0,1),(0,6),(6,0),(1,7),(7,1),(6,7),(7,6)}


    corner_sqr_1 = [(0,0),(1,0),(0,1),(2,0),(1,1),(0,2),(3,0),(2,1),(1,2),(0,3),(3,1),(2,2),(1,3),(3,2),(2,3),(3,3)]
    corner_sqr_2 = [(0,7),(0,6),(1,7),(0,5),(1,6),(2,7),(0,4),(1,5),(2,6),(3,7),(1,4),(2,5),(3,6),(2,4),(3,5),(3,4)]
    corner_sqr_3 = [(7,0),(6,0),(7,1),(5,0),(6,1),(7,2),(4,0),(5,1),(6,2),(7,3),(4,1),(5,2),(6,3),(4,2),(5,3),(4,3)]
    corner_sqr_4 = [(7,7),(6,7),(7,6),(5,7),(6,6),(7,5),(4,7),(5,6),(6,5),(7,4),(4,6),(5,5),(6,4),(4,5),(5,4),(4,4)]

    outside_board = {(-1,-1),(-1,0),(-1,1),(-1,2),(-1,3),(-1,4),(-1,5),(-1,6),(-1,7),(-1,8),(8,-1),(8,0),(8,1),(8,2),(8,3),(8,4),(8,5),(8,6),(8,7),(8,8),(0,-1),(1,-1),(2,-1),(3,-1),(4,-1),(5,-1),(6,-1),(7,-1),(0,8),(1,8),(2,8),(3,8),(4,8),(5,8),(6,8),(7,8)}
    

    init_liberty = [
        [ 3, 5, 5, 5, 5, 5, 5, 3 ],
        [ 5, 8, 8, 8, 8, 8, 8, 5 ],
        [ 5, 8, 8, 8, 8, 8, 8, 5 ],
        [ 5, 8, 8, 8, 8, 8, 8, 5 ],
        [ 5, 8, 8, 8, 8, 8, 8, 5 ],
        [ 5, 8, 8, 8, 8, 8, 8, 5 ],
        [ 5, 8, 8, 8, 8, 8, 8, 5 ],
        [ 3, 5, 5, 5, 5, 5, 5, 3 ]]
    
    pos_values = [
        [ 4,-3, 2, 2, 2, 2,-3, 4],
        [-3,-4,-1,-1,-1,-1,-4,-3],
        [ 2,-1, 1, 0, 0, 1,-1, 2],
        [ 2,-1, 0, 1, 1, 0,-1, 2],
        [ 2,-1, 0, 1, 1, 0,-1, 2],
        [ 2,-1, 1, 0, 0, 1,-1, 2],
        [-3,-4,-1,-1,-1,-1,-4,-3],
        [ 4,-3, 2, 2, 2, 2,-3, 4]]

    stable_configurations = set([15,30,60,120,135,195,225,240])

    def __init__(self):
        self.finished = False
        self.skip_count = 0
        self.board_pos = {}
        self.playing = 1
        self.veridict = -1
        self.moves = set()
        self.moves_x = set()
        self.moves_o =set()
        self.stable = set()
        self.stable_cross = 0
        self.stable_circle = 0
        self.cross_corners = 0
        self.corners_played = 0
        self.cross_values = 2
        self.circle_values = 2
        self.potential_mob_cross = 10
        self.potential_mob_circle = 10
        self.cross_pieces = 2
        self.total_pieces = 4
        self.score = {'Cross':2,'Circle':2}

        # vai de 
        self.backward_diagonal_pieces = {0:1,1:2,2:3,3:4,4:5,5:6,6:6,7:6,8:6,9:6,10:5,11:4,12:3,13:2,14:1}
        self.forward_diagonal_pieces = {0:1,1:2,2:3,3:4,4:5,5:6,6:6,7:6,8:6,9:6,10:5,11:4,12:3,13:2,14:1}
        self.column_pieces = {0:8,1:8,2:8,3:6,4:6,5:8,6:8,7:8}
        self.row_pieces = {0:8,1:8,2:8,3:6,4:6,5:8,6:8,7:8}
        


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

        self.stability_liberty = [
        [ 3, 5, 5, 5, 5, 5, 5, 3 ],
        [ 5, 8, 8, 8, 8, 8, 8, 5 ],
        [ 5, 8, 8, 8, 8, 8, 8, 5 ],
        [ 5, 8, 8, 8, 8, 8, 8, 5 ],
        [ 5, 8, 8, 8, 8, 8, 8, 5 ],
        [ 5, 8, 8, 8, 8, 8, 8, 5 ],
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

        self.moves_x.add((3,2))
        self.moves_x.add((2,3))
        self.moves_x.add((5,4))
        self.moves_x.add((4,5))

        self.moves_o.add((4,2))
        self.moves_o.add((5,3))
        self.moves_o.add((2,4))
        self.moves_o.add((3,5))

        self.moves = self.moves_x
  
    def update_liberty(self,pos):

        for d in self.dirs:
            new_pos = self.sum_tuples(pos,d)
            if not self.is_outside_board(new_pos):
                self.liberty[new_pos[0]][new_pos[1]] -= 1
    
    def update_stability_liberty(self,pos):

        for d in self.dirs:
            new_pos = self.sum_tuples(pos,d)
            if not self.is_outside_board(new_pos):
                self.stability_liberty[new_pos[0]][new_pos[1]] -= 1
            
    def pre_compute_rows_cols(self):
        return
    def get_diag_num(self,pos,type="forward"):
        if type is "forward":
            return pos[0] + pos[1]
        if type is "backward":
            return pos[0] - pos[1] + 7  # diagonal em que 0 é o canto direito/cima e 7 é o canto  esquerda/baixa

    def update_quantity(self,pos):
        self.backward_diagonal_pieces[pos[0] - pos[1] + 7] -= 1
        self.forward_diagonal_pieces[pos[0] + pos[1]] -= 1
        self.column_pieces[pos[1]] -= 1
        self.row_pieces[pos[0]] -= 1

    def is_full_every_dir(self,pos):
        
        if (self.backward_diagonal_pieces[pos[0] - pos[1] + 7] == 0 and
            self.forward_diagonal_pieces[pos[0] + pos[1]] == 0 and 
            self.column_pieces[pos[1]] == 0 and
            self.row_pieces[pos[0]] == 0):
            return True
        
        return False

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
    #not used
    def check_potential_mobility(self):
        self.potential_mob_cross = 0
        self.potential_mob_circle = 0

        for k in self.board_pos.keys():
            
            lib = self.liberty[k[0]][k[1]]
            if lib > 0:
                if self.board_pos[k] == 1:
                    self.potential_mob_circle += lib
                
                if self.board_pos[k] == 2:
                    self.potential_mob_cross += lib
    #not used
    def check_potential_mobility_exact(self):
        self.potential_mob_cross_e = 0
        self.potential_mob_circle_e = 0

        for k in self.board_pos.keys():
            if self.board_pos[k] == 0:
                c_x = 0
                c_o = 0
                for d in self.dirs:
                    new_pos = self.sum_tuples(k,d)
                    if not self.is_outside_board(new_pos):
                        if self.board_pos[new_pos] == 1:
                            c_x +=1
                        if self.board_pos[new_pos] == 2:
                            c_o += 1
                
                if c_x > 0:
                    self.potential_mob_circle_e += 1
                if c_o > 0:
                    self.potential_mob_cross_e += 1


    def add_if_not_stable_already(self,pos):
        

        if self.stability_liberty[pos[0]][pos[1]] < self.init_liberty[pos[0]][pos[1]] and self.board_pos[pos] != 0 and pos not in self.stable:

            if self.is_stable_full(pos):
                self.stable.add(pos)
                if self.board_pos[pos] == 1:
                    self.stable_cross += 1
                else:
                    self.stable_circle += 1
                self.update_stability_liberty(pos)
                return

            if self.is_stable_near_stable(pos):
                self.stable.add(pos)
                if self.board_pos[pos] == 1:
                    self.stable_cross += 1
                else:
                    self.stable_circle += 1
                self.update_stability_liberty(pos)
                return

    def check_stability(self):
        col = 0
        row = 0

        
        for sq1,sq2,sq3,sq4 in zip(self.corner_sqr_1,self.corner_sqr_2,self.corner_sqr_3,self.corner_sqr_4):

            self.add_if_not_stable_already(sq1)
            self.add_if_not_stable_already(sq2)
            self.add_if_not_stable_already(sq3)
            self.add_if_not_stable_already(sq4)



    def is_stable_full(self,pos):
        if self.is_full_every_dir(pos):
            return True
        return False
    
    def is_stable_near_stable(self,pos):
        sum = 0
        for i,d in enumerate(self.dirs):
            new_pos = self.sum_tuples(pos,d)
            if (new_pos in self.stable and self.board_pos[new_pos] == self.board_pos[pos]) or self.is_outside_board(new_pos):
                sum = sum + 2**i 

        for m in self.stable_configurations:
            if (m & sum) in self.stable_configurations: 
                return True

        return False


    def is_outside_board(self,pos):
        #return False if self.board_pos.get(pos,-1) != -1 else True
        # return (pos[0] < 0 or pos[0] >= self.rows or pos[1] < 0 or pos[1] >= self.cols)
        return pos in self.outside_board

    @staticmethod
    def sum_tuples(t1,t2):
        return (t1[0]+t2[0],t1[1]+t2[1])
    
    def check_corner_move(self,pos):
        if pos in self.conerns:
            self.corners_played += 1
            if self.playing == 1:
                self.cross_corners +=1

    @staticmethod
    def sub_tuples(t1,t2):
        return (t1[0]-t2[0],t1[1]-t2[1])
    
    def turn_piece(self,pos):

        self.board_pos[pos] = self.playing

        lib = self.liberty[pos[0]][pos[1]]
        val = self.pos_values[pos[0]][pos[1]]

        if self.playing == 1:
            if lib > 0:
                self.potential_mob_circle += lib
            
            self.cross_values += val
            self.circle_values -= val
            self.cross_pieces +=1 
        else:
            if lib >0:
                self.potential_mob_cross += lib

            self.cross_values -= val
            self.circle_values += val

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
            if self.board_pos[shft] == 0:
                break

            shft = self.sum_tuples(shft,dir)

        if turn:
            for c in range(cnt):
                shft = self.sub_tuples(shft,dir)
                self.turn_piece(shft)


    def check_mobility_dir(self,cntr,dir,playing):
    
        shft = self.sum_tuples(cntr, dir)
        cnt = 0
        turn = False
        
        while not self.is_outside_board(shft): #iterate over opponent pieces note: this config of if statements maximizes perf    
            
            pos = self.board_pos[shft]

            if pos == 0:  
                break
            
            if pos == playing:
                turn = True
                break
            
            if shft in self.stable: 
                break      
            
            if pos == 3-playing:
                cnt += 1
            
            shft = self.sum_tuples(shft,dir)

        return (cnt > 0 and turn == True)
    
    def parity_score(self):
        if self.total_pieces == 0:
            return 0
        return int(1000 * ((2*self.cross_pieces - self.total_pieces)/(self.total_pieces)))

    def position_score(self):
        return int(1000*((self.cross_values-self.circle_values)/(abs(self.cross_values)+abs(self.circle_values)+2)))
    
    def corner_score(self):
        if self.corners_played == 0:
            return 0

        return int(1000*((2*self.cross_corners - self.corners_played)/(self.corners_played)))
    
    def stability_score(self):

        if (self.stable_cross+self.stable_circle) == 0:
            return 0
        return int(1000*(self.stable_cross - self.stable_circle)/(self.stable_cross+self.stable_circle))

    def mobility_score(self):
        if (len(self.moves_x)+len(self.moves_o)) == 0:
            return 0
        return int(1000*(len(self.moves_x) - len(self.moves_o))/(len(self.moves_x)+len(self.moves_o)))

    def weighted_score(self,normalize=False):

    

        w_mob = 16
        w_par = 4
        w_cor = 10
        w_stab = 10        
        # print(f"Mob {mobility}")
        # print(f"Parity{parity}")
     
        # print(mobility)
        potential_mobility =  int(1000*(self.potential_mob_cross - self.potential_mob_circle)/(self.potential_mob_cross+self.potential_mob_circle + 2))

        if normalize:
            # norm_mob = (self.mobility_score() + 1)/2
            # norm_par = (self.parity_score() + 1)/2
            # norm_cor = (self.corner_score() + 1) /2
            # norm_stab = (self.stability_score() + 1)/2

            max_w = w_mob + w_par + w_stab + w_cor

            weighted = w_mob*(self.mobility_score()/1000) + w_par*(self.parity_score()/1000) + w_stab*(self.stability_score()/1000) + w_cor*(self.corner_score()/1000)
            
            if self.playing == 1:
                return - weighted/max_w
            else:
                return weighted/max_w
             

        # print(f"Before:{mobility}")
        return 18*self.mobility_score() + 4*self.parity_score() + 10*self.corner_score() + 10*self.stability_score()

    #Checks possible moves
    def generate_moves(self):
    
        self.moves_o=set()
        self.moves_x=set()

        # for k in self.board_pos.keys():
        for k in BEST_ORDER:
            if self.board_pos[k] == 0 and self.liberty[k[0]][k[1]] < self.init_liberty[k[0]][k[1]]:

                for dir in self.dirs:
                    mob = self.check_mobility_dir(k,dir,1)
                    mob_2 = self.check_mobility_dir(k,dir,2)
                    if mob:
                        self.moves_x.add(k)
                    if mob_2:
                        self.moves_o.add(k)
                    if mob and mob_2:
                        break
        
        
        if self.playing == 1:
            self.moves = self.moves_x
        else:
            self.moves = self.moves_o

        if len(self.moves) == 0:
            self.moves.add("skip")

    def player_pass(self):
 
      # se for só 1 skip muda so o jogador
        if self.playing == 1:
            self.playing = 2

        else:
            self.playing = 1

        self.generate_moves()
    
    def is_over(self):

        if self.skip_count == 2 or self.total_pieces == 64 :
            self.finished = True
            if self.cross_pieces > self.total_pieces - self.cross_pieces:
                self.veridict = 1
            elif self.cross_pieces < self.total_pieces - self.cross_pieces:
                self.veridict = 2
            else:
                self.veridict = 0
            return True
        else:
            return False

        return
    
    def __eq__(self, other):
        if isinstance(other, Board):
            if other.skip_count == self.skip_count and \
               other.board_pos == self.board_pos and \
               other.playing == self.playing and \
               other.moves == self.moves:

               return True
        return False

    

    def __hash__(self):
        return hash((self.skip_count,self.playing,self.playing,Map(self.board_pos)))

    def play_move(self,coord,rand=False):
        
        #playable_squares = [k for k,v in self.board_pos.items() if v == 3
        
        if rand:
            # print("----------------")
            # print(self.playing)
            # print(self.score)
            # print(self.moves)
            # print("-------------")
            coord = random.choice(list(self.moves))

        if coord == 'skip':
            self.skip_count += 1

            if self.is_over():

                return False
            else:
                self.player_pass()
                return True

        # check if there are any moves available
        # if len(self.moves) == 0:
        #     self.skip_count += 1

        #     if self.is_over():

        #         return False
        #     else:
        #         self.player_pass()
        #         return True

        
        self.skip_count = 0
        

    
        if type(coord) is tuple:
            row = coord[0]
            col = coord[1]
        else:
            row,col = self.convert_board_coords_to_array_coords(coord)
        
        if row < 0 or col < 0:
            return -1
        

        self.board_pos[(row,col)] = self.playing
        
        self.check_corner_move((row,col))
        self.update_quantity((row,col))
        

  
        lib = self.liberty[row][col]
        val = self.pos_values[row][col]

        if self.board_pos[(row,col)] == 1:

            self.cross_values += val

            if lib > 0:
                self.potential_mob_circle+= lib
        else:
            self.circle_values += val

            if lib > 0:
                self.potential_mob_cross += lib

        self.update_liberty((row,col))

        for dir in self.dirs:
            self.turn_pieces_dir((row,col),dir)

        # self.check_potential_mobility()
        # self.check_potential_mobility_exact()
        
        if self.is_stable_near_stable((row,col)):
            self.stable.add((row,col))
            if self.board_pos[(row,col)] == 1:
                self.stable_cross += 1
            else:
                self.stable_circle += 1
            self.update_stability_liberty((row,col))

        if self.corners_played > 0:
            self.check_stability()

        self.total_pieces += 1
        if self.playing == 1:
            self.cross_pieces +=1
            self.playing = 2

        else:
            self.playing = 1

        self.generate_moves()

        self.score = {'Cross':self.cross_pieces,'Circle':self.total_pieces-self.cross_pieces}

        return not self.is_over()

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
                if (row,column) in self.moves:
                    print(f"| {self.get_rep(3)} ", end='')
                else:
                    print(f"| {self.get_rep(self.board_pos[(row,column)])} ", end='')
            print(f"| ", end='')
            print()
            print(f'{(8*4+4)*"-"}')
        print(f"SCORE - X:{self.score['Cross']} O:{self.score['Circle']}          PLAYING: {self.get_rep(self.playing)}")
        # print('\n'.join(' '.join(str(x) for x in row) for row in self.liberty))
        # print(f"STABLE NUM:{len(self.stable)}")
        # print(self.stable)
        # print(self.weighted_score())

