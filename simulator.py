import numpy as np
import game
import time
import brain
from mcts import MCTS, Node, othello_tree
import random



# mcts is hardcoded to be white and minimax to be black
def simul_games(num=100,seeded=False,black="Random",white="Random",draw_board=False,verbose=1):

    wins_white = 0
    wins_black = 0
    draws = 0
    black_compound_tpm = 0
    white_compound_tpm = 0

    for i in range(1,num+1):
        start_game_time = time.process_time()
        
        
        othello_board = game.Board()
        while True:

            start_black = time.process_time()
            othello_board = play_black(othello_board,black)
            time_black = time.process_time()-start_black

            black_compound_tpm += time_black

            if draw_board:
                othello_board.draw_board()
            
            if othello_board.finished:
                break
            
            start_white = time.process_time()
            othello_board = play_white(othello_board,white)
            time_white = time.process_time()-start_white

            white_compound_tpm += time_white

            if draw_board:
                othello_board.draw_board()
            
            if othello_board.finished:
                break
        
        if othello_board.veridict == 2:
            wins_white += 1
        if othello_board.veridict == 1:
            wins_black += 1
        if othello_board.veridict == 0:
            draws += 1

        if verbose == 2:
            print(f"Wins White: {wins_white} | White Win Ratio: {wins_white/i:.3f}")
            print(f"Wins Black: {wins_black} | Black Win Ratio: {wins_black/i:.3f}")
            print(f"Draws: {draws} | Draw ratio: {draws/i:.3f}")
            print(f"White TPM:{(white_compound_tpm/64)/i:.4f}")
            print(f"Black TPM:{(black_compound_tpm/64)/i:.4f}")
            print(f"Game Time:{time.process_time()-start_game_time:.4f}")

    if verbose == 1 or verbose == 2:
        print(f"======================================{black} vs {white}=============================================")
        print(f"Wins White({white}): {wins_white} | White Win Ratio: {wins_white/i:.3f}")
        print(f"Wins Black({black}): {wins_black} | Black Win Ratio: {wins_black/i:.3f}")
        print(f"Draws: {draws} | Draw ratio: {draws/i:.3f}")
        print(f"White TPM:{(white_compound_tpm/64)/i:.4f}")
        print(f"Black TPM:{(black_compound_tpm/64)/i:.4f}")
        print("")
        print("")



def play_white(board,player,iterations_mcts=100):
    if player == "Random":
        board.play_move("",True)
        return board
    if player == "Greedy":
        return brain.greedy(board,2)
    if player == "MCTS":
        return mcts_play(board,iterations_mcts)

def play_black(board,player,minimax_depth=4):
    if player == "Random":
        board.play_move("",True)
        return board
    if player == "Greedy":
        return brain.greedy(board,1)
     
    if player == "MiniMax":
        return minmax_play(board,4)

def mcts_play(board_root,iters):
    tree = MCTS()
    othello_board = othello_tree(board_root)
    for _ in range(iters):
        tree.do_rollout(othello_board)
    
    othello_board = tree.choose(othello_board)

    return othello_board.board

def minmax_play(board,depth):
    move_ai = brain.negamax_ab(board,depth)
    board.play_move(move_ai)
    # print(board.board_pos)
    return board

def main():
    s = time.process_time()
    simul_games(num=400,black="MiniMax",white="MCTS")
    print(time.process_time()-s)
    # simul_games(num=400,black="MiniMax",white="Greedy")
    # simul_games(num=400,black="Greedy",white="MCTS")
    # simul_games(num=400,black="MiniMax",white="Random")
    # simul_games(num=400,black="Random",white="MCTS")
    # simul_games(num=400,black="Greedy",white="Random")



if __name__ == "__main__":
    main()