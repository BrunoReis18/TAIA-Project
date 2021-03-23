
from abc import ABC, abstractmethod
from collections import defaultdict
import math
import _pickle as cPickle
import random


class MCTS:
    "Monte Carlo tree searcher. First rollout the tree then choose a move."

    def __init__(self, exploration_weight=0.7,alpha=0.6):
        self.Q = defaultdict(int)  # total reward of each node
        self.N = defaultdict(int) # total visit count for each node
        self.H = defaultdict(int) 
        self.children = dict()  # children of each node
        self.exploration_weight = exploration_weight
        self.alpha = alpha

    def choose(self, node):
        "Choose the best successor of node. (Choose a move in the game)"
        if node.is_terminal():
            raise RuntimeError(f"choose called on terminal node")

        if node not in self.children:
            return node.find_random_child()
        
        # print(self.children[node])
        def score(n):
            if self.N[n] == 0:
                return float("-inf")  # avoid unseen moves
            return ((1-self.alpha)*self.Q[n] / self.N[n]) + (self.alpha*self.H[n])  # average reward

        return max(self.children[node], key=score)

    def do_rollout(self, node):
        "Make the tree one layer better. (Train for one iteration.)"
        path = self._select(node)
        leaf = path[-1]
        self._expand(leaf)
        (reward,heuristic) = self._simulate(leaf)
        self._backpropagate(path, reward,heuristic)

    def _select(self, node):
        "Find an unexplored descendent of `node`"
        path = []
        while True:
            path.append(node)
            if node not in self.children or not self.children[node]:
                #node is either unexplored or terminal
                return path
            unexplored = self.children[node] - self.children.keys()
            if unexplored:
                n = unexplored.pop()
                path.append(n)
                return path
            node = self._uct_select(node)  # descend a layer deeper

    def _expand(self, node):
        "Update the `children` dict with the children of `node`"
        if node in self.children:
            return  # already expanded
        

        self.children[node] = node.find_children()

        if len(self.children[node]) == 0:
            return
        def ev(n):
            return n.eval
        # node.update_eval(max(map(lambda x: ev(x), self.children[node])))

    def _simulate(self, node):
        "Returns the reward for a random simulation (to completion) of `node`"
        invert_reward = False
        sign = 1
        while True:
            if node.is_terminal():
                reward = node.reward()
                return (-reward,sign) if invert_reward else (reward,-sign)

            node = node.find_random_child()
            invert_reward = not invert_reward

    def _backpropagate(self, path, reward,sign):
        "Send the reward back up to the ancestors of the leaf"

        def heur(n,s):
            return s*n.board.weighted_score(normalize=True)

        for node in reversed(path):
            self.N[node] += 1
            self.Q[node] += reward
            # print(node.board.score)
            
            
            def ev(n):
                return n.eval
         
            if node.is_terminal():
                self.H[node] = node.eval
            else:
                node.update_eval(max(map(lambda x: ev(x), self.children[node])))
                self.H[node] = node.eval
            # 
            #     self.H[node] = sign*node.board.weighted_score(normalize=True)
            # else:
            #     self.H[node] = max(map(lambda x: heur(x,sign), self.children[node]))
            # self.H[node] = max(heuristic)
            reward = -reward  # 1 for me is 0 for my enemy, and vice versa
            sign = -sign

    def _uct_select(self, node):
        "Select a child of node, balancing exploration & exploitation"

        # All children of node should already be expanded:
        assert all(n in self.children for n in self.children[node])

        log_N_vertex = math.log(self.N[node])

        def uct(n):
            "Upper confidence bound for trees"
            # heur = n.board.weighted_score(normalize=True) *5
            
            return (self.alpha*self.H[n]) +((1-self.alpha)*self.Q[n] / self.N[n]) + self.exploration_weight * math.sqrt(
                log_N_vertex / self.N[n]
            )

        return max(self.children[node], key=uct)



class Node(ABC):
    """
    A representation of a single board state.
    MCTS works by constructing a tree of these Nodes.
    """

    @abstractmethod
    def find_children(self):
        "All possible successors of this board state"
        return set()

    @abstractmethod
    def find_random_child(self):
        "Random successor of this board state (for more efficient simulation)"
        return None

    @abstractmethod
    def is_terminal(self):
        "Returns True if the node has no children"
        return True

    @abstractmethod
    def reward(self):
        "Assumes `self` is terminal node. 1=win, 0=loss, .5=tie, etc"
        return 0

    @abstractmethod
    def __hash__(self):
        "Nodes must be hashable"
        return 123456789

    @abstractmethod
    def __eq__(node1, node2):
        "Nodes must be comparable"
        return True

class othello_tree(Node):

    def __init__(self, board):
      self.board = board
      self.eval = board.weighted_score(normalize=True)

    def update_eval(self,new_eval):
        self.eval = new_eval
    
    def find_children(self):

        if self.board.is_over():
            return set()
        
        return {self.make_move(m) for m in self.board.moves}
    
    def find_random_child(self):

        if self.board.is_over():
            return None
        
        return self.make_move("",True)

    def reward(self):
        # self.board.draw_board()
        if not self.board.is_over():
            raise RuntimeError(f"reward called on nonterminal board")

        circle_pieces = self.board.total_pieces - self.board.cross_pieces

        if self.board.cross_pieces < circle_pieces:
            # It's your turn and you've already won. Should be impossible.
            return 1
        if self.board.cross_pieces > circle_pieces:
            return -1  # Your opponent has just won. Bad.
        if self.board.cross_pieces == circle_pieces:
            return 0  # Board is a tie
        # The winner is neither True, False, nor None
        raise RuntimeError(f"board has unknown winner type")

    def make_move(self,move,rand=False):

        board_state_ = cPickle.loads(cPickle.dumps(self.board, -1))

        if not rand:
            board_state_.play_move(move)
        else:
            board_state_.play_move("",True)
        return othello_tree(board_state_)

    def is_terminal(self):
        return self.board.is_over()

    def __eq__(self,other):
        if isinstance(other,othello_tree):
            return self.board == other.board
        
        return False
    
    def __hash__(self):
        return self.board.__hash__()
    def __str__(self):
        return str(self.board.score)