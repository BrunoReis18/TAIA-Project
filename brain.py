import _pickle as cPickle
import game
import random

from abc import ABC, abstractmethod
from collections import defaultdict
import math
SIGN=(1,-1)
COUNT = 0

def negamax(board,depth):
      
    best = -float("Inf")
    poses_scores = {}

    for m in board.moves:
        board_ = cPickle.loads(cPickle.dumps(board, -1)) #about 10 times faster
        board_.play_move(m)
        score = -negamax_(board_,depth-1)
        best = max(score,best) 
        poses_scores[m] = score

    print(f"Best:{best}")
    print(f"Scores:{poses_scores}")
    print(f"End-Nodes:{COUNT}")
    return

def negamax_(board,depth):
    if(depth == 0):
        global COUNT
        COUNT+=1
        return board.weighted_score()
      
    best = -float("Inf")

    for m in board.moves:
        board_ = cPickle.loads(cPickle.dumps(board, -1)) #about 10 times faster
        board_.play_move(m)
        
        score = -negamax_(board_,depth-1)
        # print(''.join("|||" for x in range(depth))+str(score))
        best = max(score,best) 
       
    return best

####################################################################################

 
def negamax_ab(board,depth,alpha=-float("Inf"),beta=float("Inf")):
    COUNT = 0
    best = -float("Inf")
    poses_scores = {}
    best_pos = ()
    # print(board.moves)

    
    for m in board.moves:
        board_ = cPickle.loads(cPickle.dumps(board, -1)) #about 10 times faster
        board_.play_move(m)
        score = -negamax_ab_(board_,depth-1,alpha,beta)
        
        if score > best:
            best = score
            best_pos = m
        
        # if score == best and random.randint(0, 1): # if scores for positions are equal randomize
        #     best = score

        poses_scores[m] = score
    # print(f"pod_scores:{poses_scores}")
    return best_pos

def negamax_ab_(board,depth,alpha,beta):

    best = -float("Inf")
    
    if (board.is_over()):
        return board.parity_score()

    # if (board.skip_count == 1):
    moves = board.moves

    if depth == 0 or len(moves - {"skip"})==0 :
        global COUNT
        COUNT += 1
        return board.weighted_score()
        
      
    for m in moves:
        board_ = cPickle.loads(cPickle.dumps(board, -1)) #about 10 times faster
        board_.play_move(m)
        
        score = -negamax_ab_(board_,depth-1,-beta,-alpha)
        # print(f"DEPTH:{depth}|MOVE:{m}|SCORE:{best}")
        best = max(best, score)
        alpha = max(alpha,score)

        if alpha >= beta:
            break

    return best

####################################################
# Monte-Carlos Tree Search (UTC)

# def MCTS(board_state,sims_num):

#max_player == 1 optimzie cross/black max player == 2 optimize circle/white
def greedy(board_state,max_player):
    
    if board_state.playing != max_player:
        raise RuntimeError(f"Greedy player different from current player")
    
    def score(move):
        board_ = cPickle.loads(cPickle.dumps(board_state, -1)) 
        board_.play_move(move)
        if max_player == 1:
            return board_.weighted_score()
        else:
            return -board_.weighted_score()

    best_move = max(board_state.moves,key=score)

    board_state.play_move(best_move)
    return board_state
        


