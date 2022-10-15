import random
from typing import Tuple, Dict
import numpy as np
from connect4.utils import get_valid_actions, Integer, get_pts



class RandomPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'random'
        self.player_string = 'Player {}:random'.format(player_number)
     
    def state_update(self, state, action, playernumber):
        board = state[0].copy()
        player1keys = state[1][1].get_int()
        player2keys = state[1][2].get_int()
        player1K = Integer(player1keys)
        player2K = Integer(player2keys)
        keys = {1:player1K,2:player2K}
        col = action[0]
        if action[1] == False:
            locking = True
            for j in range(len(board)):
                if board[j][col] != 0:
                        board[j-1][col] = playernumber
                        # print(board)
                        return (board, keys)
            if locking == True:
                board[len(board)-1][col] = playernumber
                # print(board)
                return (board, keys)        
        else:
            print(board, " Before")
            n = keys[playernumber].get_int()
            # print(n, " these are keys, ", playernumber, " player number before")
            lis_col = []
            for j in range(len(board)):
                lis_col.append(board[j][col])
            lis_col.pop()
            lis_col.insert(0,0)
            for j in range(len(board)):
                board[j][col] = lis_col[j]
            # new_state[0] = board
            keys[playernumber].decrement()
            n = keys[playernumber].get_int()
            # print(n, " these are keys, ", playernumber, " player number")
            # print(board)
            return (board,keys)
        
    def tree_create(self, state, depth, random, debug, heuiristic):
        # fil = open("tree.txt", "a")
        tree = []
        num_actions = len(get_valid_actions(self.player_number, state))
        level = [[state,0,0,num_actions]] #(state, utilityvalue, parentindex, numofvalidnextmoves)
        tree.append(level)
        # print(tree)
        for i in range(depth): 
            # print(f'i = {i}, depth = {depth}')
            level = [] #level of tree
            for j in range(len(tree[i])): #expanding nodes of the level
                # num_actions = tree[i][j][3]
                if(i%2==0):
                    num_actions = len(get_valid_actions(self.player_number, tree[i][j][0]))
                else:
                    num_actions = len(get_valid_actions(3-self.player_number, tree[i][j][0]))
                curr_state = tree[i][j][0]
                # valid_list_even = get_valid_actions(self.player_number, curr_state)
                # valid_list_odd = get_valid_actions(3-self.player_number, curr_state)
                # print(f'curr_state: {curr_state}, {len(valid_list_even)} and {num_actions}',num_actions==len(valid_list_even) and i%2 == 0)
                # print(f'curr_state: {curr_state}, {len(valid_list_odd)} and {num_actions}', num_actions==len(valid_list_odd) and i%2 == 1)
                
                for k in range(num_actions):
                    tup=[]
                    if(i%2 == 0):
                        next_move = get_valid_actions(self.player_number, curr_state)[k]
                        # print(f'Tree here is [1] {tree}')
                        # print(f'current state before : {curr_state}')
                        next_state = self.state_update(curr_state, next_move, self.player_number)
                        # print(f'current state after: {curr_state}')
                        
                        # if(debug):
                            # print(f"next move of player {self.player_number}: {next_move} in expanding node {j} of level {i}")
                            # print(f'State: {next_state}')
                        num_actions_next = len(get_valid_actions(3-self.player_number, next_state))
                        if(i==depth-1):
                            points = get_pts(self.player_number, next_state[0])
                            # print(f'POINTS={points}')
                            tup = [next_state, points, j, num_actions_next]
                            level.append(tup)
                        else:
                            tup = [next_state, 0, j, num_actions_next]
                            level.append(tup)
                    else:
                        next_move = get_valid_actions(3-self.player_number, curr_state)[k]
                        next_state = self.state_update(curr_state, next_move, 3-self.player_number)
                        # if(debug):
                            # print(f"next move of player {3-self.player_number}: {next_move} in expanding node {j} of level {i}")
                            # print(f'State: {next_state}')
                        
                        num_actions_next = len(get_valid_actions(self.player_number, next_state))
                        if(i==depth-1):
                            points = get_pts(3-self.player_number, next_state[0])
                            # print(f'POINTS={points}')
                            tup = [next_state, points, j, num_actions_next]
                            level.append(tup)
                        else:
                            tup = [next_state, 0, j, num_actions_next]
                            level.append(tup)
                # print(f'Tree here is [2] {tree}')
                    
            # print(f'level: {level}')
            # print(f'Tree before appending level = {tree}')
            tree.append(level) 
            
            # print(f'Tree after appending level =')
            # for i in range(0,len(tree)):
                # print(f'Level {i}:\n{tree[i]}\n\n')
            # fil.close()
        # print(f'Tree before updating expectimax values:')
        # for i in range(0,len(tree)):
            # print(f'Level {i}:\n{tree[i]}\n\n')
        height = len(tree)
        
        for i in range(height-1,0,-1):
            curr_level = i
            parent_level = i-1
            num_nodes = len(tree[curr_level])
            for j in range(num_nodes-1,-1,-1):
                
                parent_index = tree[curr_level][j][2]
                if(i%2==0):
                    numchild = len(get_valid_actions(3-self.player_number,tree[parent_level][parent_index][0]))
                else:
                    numchild = len(get_valid_actions(self.player_number,tree[parent_level][parent_index][0]))
                if(i%2 == 1): #parent will take max values of children
                    tree[parent_level][parent_index][1] = max(tree[parent_level][parent_index][1], tree[curr_level][j][1])     
                else: #parents will take values acc to type of game
                    if(random): #expected value
                        tree[parent_level][parent_index][1] = tree[parent_level][parent_index][1] + tree[curr_level][j][1]/numchild
                    else: #minimum value
                        tree[parent_level][parent_index][1] = min(tree[parent_level][parent_index][1], tree[curr_level][j][1])
        print(f'Tree after updating expectimax values:')
        for i in range(0,len(tree)):
            print(f'Level {i}:\n{tree[i]}\n\n')
        for i in range(len(tree[1])):
            if(tree[0][0][1]==tree[1][i][1]):
                pathselect = get_valid_actions(self.player_number, tree[0][0][0])[i]
        return pathselect    
        # print(tree)     

    def get_move(self, state: Tuple[np.array, Dict[int, Integer]]) -> Tuple[int, bool]:
        """
        Given the current state returns the next action
        :param state: Contains:
                        1. board
                            - a numpy array containing the state of the board using the following encoding:
                            - the board maintains its same two dimensions
                                - row 0 is the top of the board and so is the last row filled
                            - spaces that are unoccupied are marked as 0
                            - spaces that are occupied by player 1 have a 1 in them
                            - spaces that are occupied by player 2 have a 2 in them
                        2. Dictionary of int to Integer. It will tell the remaining popout moves given a player
        :return: action (0 based index of the column and if it is a popout move)
        """
        valid_actions = get_valid_actions(self.player_number, state)
        # treemove = self.tree_create(state, 2, True, True, 0)
        # print(f'Action selected by tree: {treemove}')
        # for i in range(0,len(tree)):
        #     print(f'Level {i}:\n{tree[i]}\n\n')
        #     print(self.player_number, " player number")
        action, is_popout = random.choice(valid_actions) 
        # print("next move")
        return action,is_popout         
    
