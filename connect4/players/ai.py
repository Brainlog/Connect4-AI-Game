import random as rd
from shutil import which
from webbrowser import get
import numpy as np
from typing import List, Tuple, Dict
from connect4.utils import get_pts, get_valid_actions, Integer





class AIPlayer:
    def __init__(self, player_number: int, time: int):
        """
        :param player_number: Current player number
        :param time: Time per move (seconds)
        """
        self.player_number = player_number
        self.type = 'ai'
        self.player_string = 'Player {}:ai'.format(player_number)
        self.time = time
        # Do the rest of your implementation here
    
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
    
    def heuristicfn(self, playernumber, state, value, features):
        board = state[0]
        dict = [(0,"score"),(1,"diff"),(2,"relative"),(3,"featues")]
        points = 0 
        if value == 0:
            points = get_pts(playernumber, board)
        if value ==1:
            points = get_pts(playernumber, board)-get_pts(3-playernumber, board)
        if value == 2:
            points = get_pts(playernumber, board)-get_pts(3-playernumber, board)
            if get_pts(3-playernumber,board) != 0:
                points = points/get_pts(3-playernumber,board)
        if value == 3:
            features_name = [(0,"pop_outs_left"),(1,"pop_outs_left_opposite"),(2,"points_opposite"),(3,"points"),(4,"4-cons"),(5,"3-cons"),(6,"2-cons"),(7,"whichplayer"),(8,"potential")]
            # print("I AM HERE")
            pop_outs_left = state[1][playernumber].get_int()
            points += (features[0]*pop_outs_left)
            pop_outs_left_opp = state[1][3-playernumber].get_int()
            points += (features[1]*pop_outs_left_opp)            
            points_opp = get_pts(3-playernumber,board)
            points += (features[2]*points_opp)            
            points_mine = get_pts(playernumber, board)
            points += (features[3]*points_mine)            
            cons4 = 0
            points += (features[4]*cons4)            
            cons3 = 0
            points += (features[5]*cons3)            
            cons2 = 0
            points += (features[6]*cons2)            
            # if features[7] == 1:
            #     potential_diff = 1000
            #     moves = get_valid_actions(3-playernumber,state)
            #     for move in moves:
            #         updated_state = self.state_update(state, move, 3-playernumber)
            #         potential_diff = min(potential_diff, get_pts(3-playernumber,updated_state[0]))
            #     points += (features[8]*potential_diff)    
            # else:
            #     potential_diff = 0
            #     moves = get_valid_actions(playernumber,state)
            #     for move in moves:
            #         updated_state = self.state_update(state, move, playernumber)
            #         potential_diff = max(potential_diff, get_pts(playernumber,updated_state[0]))
            #     points += (features[8]*potential_diff) 
        return points
        
    def tree_create(self, state, depth, random, debug, heuiristic, features):
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
                        next_state = self.state_update(curr_state, next_move, self.player_number)
                        num_actions_next = len(get_valid_actions(3-self.player_number, next_state))
                        if(i==depth-1):
                            points = self.heuristicfn(self.player_number, next_state, heuiristic, features)   
                            # points = get_pts(self.player_number, next_state[0])                                
                            tup = [next_state, points, j, num_actions_next]
                            level.append(tup)
                        else:
                            if(random):
                                tup = [next_state, 0, j, num_actions_next]
                            else:
                                tup = [next_state, 10000, j, num_actions_next]
                            level.append(tup)
                    else:
                        next_move = get_valid_actions(3-self.player_number, curr_state)[k]
                        next_state = self.state_update(curr_state, next_move, 3-self.player_number)
                        
                        num_actions_next = len(get_valid_actions(self.player_number, next_state))
                        if(i==depth-1):  
                            points = self.heuristicfn(self.player_number, next_state, heuiristic, features)  
                            # points = get_pts(self.player_number, next_state[0])                                                       
                            tup = [next_state, points, j, num_actions_next]
                            level.append(tup)
                        else:
                            if(random):
                                tup = [next_state, 0, j, num_actions_next]
                            else:
                                tup = [next_state, -10000, j, num_actions_next]
                            # tup = [next_state, 0, j, num_actions_next]
                            level.append(tup)

            tree.append(level) 

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
        for i in range(0,2):
            print(f'Level {i}:\n{tree[i]}\n\n')
        pathselect = get_valid_actions(self.player_number, tree[0][0][0])[0]
        noofactions = len(get_valid_actions(self.player_number, tree[0][0][0]))
        p = rd.randint(0,19)
        if p == 5:
            indexi = rd.randint(0,noofactions-1)
            pathselect = get_valid_actions(self.player_number, tree[0][0][0])[indexi]
        else:           
            for i in range(noofactions):
                # tree[0][0][1] = -100000
                if(tree[0][0][1]==tree[1][i][1]):
                    print("I AM HERE 16OCT")
                    pathselect = get_valid_actions(self.player_number, tree[0][0][0])[i]
                    tree[0][0][1] = tree[1][i][1]
                    break
        return pathselect    
        # print(tree)         
    


    def get_intelligent_move(self, state: Tuple[np.array, Dict[int, Integer]]) -> Tuple[int, bool]:
        # if self.player_number == 1:
        #     choice = self.tree_create(state, 3, False, True, 0)
        # if self.player_number == 2:
        #     choice = self.tree_create(state, 3, False, True, 0) 
        if self.player_number == 1:
         choice = self.tree_create(state, 3, False, True, 3,[1,0,0,1,0,0,0,1,-1]) 
        else:
         choice = self.tree_create(state, 3, False, True, 3, [1,-1,-1,1,0,0,0,1,-1])       
        print(f'Action selected by tree: {choice}')
        return choice 
        # Do the rest of your implementation here
        raise NotImplementedError('Whoops I don\'t know what to do')

    def get_expectimax_move(self, state: Tuple[np.array, Dict[int, Integer]]) -> Tuple[int, bool]:
        choice = self.tree_create(state, 3, True, True, 3,[1,-1,-1,1,0,0,0,1,-1])
        print(f'Action selected by tree: {choice}')
        return choice  
        # Do the rest of your implementation here
        raise NotImplementedError('Whoops I don\'t know what to do')
