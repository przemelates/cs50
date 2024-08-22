"""
Tic Tac Toe Player
"""

import math
import time
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    def count(board,x):
        sum = 0
        for i in board:
            sum+=i.count(x)
        return sum

    if count(board,X)>count(board,O):
        return O
    elif count(board,X)<=count(board,O):
        return X
    else:
        return None
    
    
    """
    Returns player who has the next turn on a board.
    """
    raise NotImplementedError


def actions(board):
    actions = set()
    if terminal(board) == True:
        return None
    for i in range(len(board)):
        for j in range(len(board[i])):
            if(board[i][j] == EMPTY):
                actions.add((i,j))
    return actions
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    raise NotImplementedError


def result(board, action):
    #if len(board) != 3 or type(board) != list or type(action) != tuple:
    #    print(board)
    #    raise Exception
    #for i in range(len(board)):
    #    for j in board[i]:
    #        if(j not in {X,O,EMPTY}):
    #            raise Exception
            
    board_result = copy.deepcopy(board)
    board_result[action[0]][action[1]] = player(board)
    return board_result

    """
    Returns the board that results from making move (i, j) on the board.
    """
    raise NotImplementedError


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Check rows
    #if (board[0][2] == X and board[1][2] == X and board[2][2] == X):
    #    return X
    if all(i == board[0][0]!= None for i in board[0]):
        return board[0][0]
    elif all(i == board[1][0]!= None for i in board[1]):
        return board[1][0]
    elif all(i == board[2][0]!= None for i in board[2]):
        return board[2][0]
    # Check columns
    elif board[0][0] == board[1][0] and board[1][0] == board[2][0] != None:
        return board[0][0]
    elif board[0][1] == board[1][1] and board[1][1] == board[2][1] != None:
        return board[0][1]
    elif board[0][2] == board[1][2] and board[1][2] == board[2][2] != None:
        return board[0][2]
    # Check diagonals
    elif board[0][0] == board[1][1] and board[1][1] == board[2][2] != None:
        return board[0][0]
    elif board[0][2] == board[1][1] and board[1][1] == board[2][0] != None:
        return board[0][2]
    else:
        return None
    
    """
    Returns the winner of the game, if there is one.
    """
    raise NotImplementedError


def terminal(board):
    if winner(board) is not None:
        return True
    elif winner(board) is None and (EMPTY in board[0] or EMPTY in board[1] or EMPTY in board[2]):
        return False
    else:
        return True
    """
    Returns True if game is over, False otherwise.
    """
    raise NotImplementedError


def utility(board):
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    raise NotImplementedError

def maxvalue(board):
        
        if terminal(board):
            return utility(board), None
        v = -math.inf
        optimum = None
        for action in actions(board):
            x, z = minvalue(result(board,action))
            if x>v:
                v = x
                optimum = action
                if v == 1:
                    return v, optimum
           
            
        
        return v,optimum

def minvalue(board):
      
        if terminal(board):
            return utility(board), None
        v = math.inf
        optimum = None
        for action in actions(board): 
            y, z = maxvalue(result(board,action))
            if y < v:
                v = y   
                optimum = action
                if v == -1:
                    return v, optimum
        
        return v,optimum


def minimax(board):
  
    
    if terminal(board):
        return None
    elif player(board) == X:
        value, move = maxvalue(board)
        print(move)
        return move
              
    elif player(board) == O:
        value, move = minvalue(board)
        print(move)
        return move
       

    """
    Returns the optimal action for the current player on the board.
    """
    raise NotImplementedError
