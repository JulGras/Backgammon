# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 19:28:42 2020

@author: ntb
"""
# %% imports
import random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# %% comments
### the starting position we use is as in the following picture:
### https://en.wikipedia.org/wiki/Backgammon#/media/File:BackgammonBoard.svg
### 
### Further, we use a labeling of the 24 points (triangles) as follows: 
### The most upper right point is point 1, the most lower right point is point 24.
### The points in between are counted up counter clock-wise
### 
### The colours of the two sets of 15 checkers are blue ('b') and red ('r').  
 
# %% initialize backgammon board
### initial backgammon board; each of the 24 point numbers is mapped to a 
### list [colour of checker, number of checkers] 
### colours can be 'b' (blue), 'r' (red) or 'n' (neutral; if point is empty) 
init_board = {}
for i in range(1,25):
    init_board[i]=['n',0]   # empty board
init_board[1]=['b',2]       # blue checkers
init_board[12]=['b',5]
init_board[17]=['b',3]
init_board[19]=['b',5]
init_board[6]=['r',5]       # red checkers
init_board[8]=['r',3]
init_board[13]=['r',5]
init_board[24]=['r',2]

# print(init_board)

# %% visualize board
def ShowBoard(board):
    '''input: board i.e. init_board see above'''
    for i in range(1,13):
        tup = board[i]
        plt.plot([i-0.5,i], [0,7.5], 'k', linewidth=1)
        plt.plot([i,i+0.5], [7.5,0],'k', linewidth=1)
        for j in range(tup[1]):
            plt.plot(13-i, 20-j, tup[0]+'o', markersize=12)
    for i in range(13,25):
        tup = board[i]
        plt.plot([i-12.5,i-12], [20,12.5], 'k', linewidth=1)
        plt.plot([i-12,i-11.5], [12.5,20],'k', linewidth=1)
        for j in range(tup[1]):
            plt.plot(i-12, j, tup[0]+'o', markersize=12)
    plt.plot([6.5,6.5], [-0.5,20.5], 'k', linewidth=5)
    ax = plt.gca()
    ax.axes.xaxis.set_visible(False)
    ax.axes.yaxis.set_visible(False)
    plt.show()

## check if it works
ShowBoard(init_board)

# %% roll dice
# function roll the two dice
def ThrowTwoDice():
    dye_1=random.randint(1,6)
    dye_2=random.randint(1,6)
    return dye_1,dye_2

# check
for i in range(6):
    print(ThrowTwoDice())

# %% class: table of a backgammon game
class TableofaGame(object):
    def __init__(self):
        self.board = init_board
        self.middlebar = []       # list where hit (thrown out) checkers are stored as 'b' or 'r'
        self.blue_bearedoff=0
        self.red_bearedoff=0
    
    def ShowTable(self):
        ShowBoard(self.board)
        
    def GetScore(self):
        '''
        counts the total number of steps, each colour has to take to clear;
        returns tuple (blue total steps, red total steps)
        '''
        blue=0
        red=0
        for i in range(1,25):
            tup=self.board[i]
            if tup[0]=='b':
                blue+=(25-i)*tup[1]
            if tup[0]=='r':
                red+=tup[1]*i
        return blue, red
    
    def CountBlueHome(self):
        '''counts how many blue checkers are in the blue home (on one of the points 1 to 6)'''
        blue_home=0
        for i in range(19,25):
           if self.board[i][0]=='b':
               blue_home+=self.board[i][1]
        return blue_home
           
    def CountRedHome(self):
        '''counts how many red checkers are in the red home (on one of the points 19 to 24)'''
        red_home=0
        for i in range(1,7):
           if self.board[i][0]=='r':
               red_home+=self.board[i][1]  
        return red_home
                
    def PossibleMoves(self, colour, nr_of_steps):
        '''
        returns a list of integers representing the starting points of all possible moves
        str: colour - of checker which shall be moved (either 'b' or 'r')
        int: nr_of_steps - number of steps for the movement, between 1 and 6
        '''
        col_list=['b', 'r']
        col_list.remove(colour)
        other_colour=col_list[0]
        # getting list of points which have at least one checker of the colour
        points_colour=[]
        for i in range(1,25):
            if self.board[i][0]==colour:
                points_colour.append(i)
        # checking if target point (i.e. starting + nr_of_steps) is blocked by other coulour
        points_possible=points_colour.copy()
        for i in points_colour:
            if colour=='b':
                if self.board[i+nr_of_steps][0]=='r' and self.board[i+nr_of_steps][1]>1:
                    points_possible.remove(i)
            else:
                if self.board[i-nr_of_steps][0]=='b' and self.board[i+nr_of_steps][1]>1:
                    points_possible.remove(i)
        # return list
        return points_possible
            
        
    
    def UpdateBoard(self, colour, starting_point, nr_of_steps):
        '''input: 
            str: colour - of checker which shall be moved (either 'b' or 'r')
            int: starting_point - point where movement shall start, between 1 and 24
                 nr_of_steps - number of steps for the movement, between 1 and 6
        '''
        col_list=['b', 'r']
        col_list.remove(colour)
        other_colour=col_list[0]
        if self.board[starting_point][0]!=colour:
            print('Move impossible!')
        elif self.board[starting_point+nr_of_steps][0]==other_colour:
            if self.board[starting_point+nr_of_steps][1]>1:
                print('Move impossible!')
            else:
                self.board[starting_point][1]-=1
                self.board[starting_point+nr_of_steps][0]=colour
                self.middlebar.append(other_colour)
        else:
            self.board[starting_point][1]-=1
            self.board[starting_point+nr_of_steps][0]=colour
            self.board[starting_point+nr_of_steps][1]+=1
        
    def CountCheckers(self, colour='both', area='complete'):
        '''input: 
            str: colour - of checker which shall be counted (default 'both', alternatively 'b' or 'r')
                 area - where to count (default 'complete', alternatively 'home_red' or 'home_blue')
                 nr_of_steps - number of steps for the movement, between 1 and 6
            returns: int - count
        '''    
        # set counts to 0
        count=0
        count_b=0
        count_r=0
       
        # define range object
        if area=='complete':
            range_obj = range(1,25)
        elif area=='home_red':
            range_obj = range(1,7)   # red home is upper right corner, i.e. points 1 to 6
        else:
            range_obj = range(19,25)    # blue home is lower right corner, i.e. points 19 to 24
      
        # count   
        for i in range_obj:
            if self.board[i][0]=='r':
                count_r += self.board[i][1]
            elif self.board[i][0]=='b':
                count_b += self.board[i][1]
        
        # get the right count
        if colour=='both':
            count = count_r + count_b
        elif colour=='r':
            count = count_r
        else:
            count = count_b 
        
        return count
        
        
        
        
# %% trying out methods of class              
game=TableofaGame()
#game.ShowTable()
print(game.GetScore())
print(game.CountBlueHome())
print(game.CountRedHome())
game.UpdateBoard('b',1,6)
game.ShowTable()
print(game.PossibleMoves('b',2))
print(game.PossibleMoves('b',1))
print(game.PossibleMoves('r',1))
print(game.CountCheckers())
print(game.CountCheckers(colour='r',area='complete'))
print(game.CountCheckers(colour='r'))
print(game.CountCheckers(area='home_red'))