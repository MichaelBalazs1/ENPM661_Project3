#!/usr/bin/env python
# coding: utf-8

# In[ ]:





# In[1]:


#Initialization
import pygame as pyg
from pygame.locals import *
import sys
import numpy as np
import math
import heapq as hpq
import random
import re
import copy
import matplotlib.pyplot as plt


# In[2]:


#Adjust board parameters
boardSize = [400,250] #Will adjust board size and printout size
numObsticles = 50 #40-60 seems to be a good value for testing


# In[3]:


#Draws a circle using the general equation -> (x – h)^2+ (y – k)^2 = r^2
def drawObsticle(boardState, r, centerX, centerY):
    for key in boardState.keys():
        circle = ((key[0]-centerX)**2)+((key[1]-centerY)**2)-(r**2) 
     
        if circle < 0:
            boardState[key] = 0
    return boardState


# In[4]:


#This function creates the board and randomizes the sizes/location of obsticles 
def createBoard(): 
    boardCoordinates = []
    for i in range(0, boardSize[1]):
        for j in range(0, boardSize[0]):
            boardCoordinates.append((j, i))

    boardCoordVals = list(np.ones(boardSize[0] * boardSize[1], dtype=int))
    boardState = dict(zip(boardCoordinates, boardCoordVals))

    for i in range(0,numObsticles):
        randR = random.randint(0,25)
        randX = random.randint(10,400)
        randY = random.randint(10,250)
        
        boardState = drawObsticle(boardState,randR,randX,randY)


    return boardState


# In[5]:


def userInput(boardState):
    placementError = True

    while (placementError):
        usrStrtList = []
        usrGoalList = []
        while ((usrStrtList == []) or (usrGoalList == []) or (len(usrStrtList) > 1) or (len(usrGoalList) > 1)):
            usrStrt = input("Enter the starting coordinates(x,y): ")
            usrGoal = input("Enter the ending coordinates(x,y): ")
            usrStrtList = re.findall(r"[0-2]?[0-9]?[0-9], [0-2]?[0-9]?[0-9]", usrStrt)
            usrGoalList = re.findall(r"[0-2]?[0-9]?[0-9], [0-2]?[0-9]?[0-9]", usrGoal)


        Start = tuple(map(int, usrStrtList[0].split(',')))
        Goal  = tuple(map(int, usrGoalList[0].split(',')))

        if ((0 < Start[0] < boardSize[0]) and (0 < Goal[0] < boardSize[0])):
            if ((0 < Start[1] < boardSize[1]) and (0 < Goal[1] < boardSize[1])):
                if (boardState[Start] == 1):
                    print("Placement Error: may be on obsticle")
                    if (boardState[Goal] == 1):
                        print("Placement Error: may be on obsticle")
                        if (boardState[Goal] == 0):
                            print("Placement Error: may be on obsticle")
                        if (boardState[Start] == 0):
                            print("Placement Error: may be on obsticle")
                        placementError = False
    return Start, Goal


# In[6]:


def randStrtGoal(boardState):
    placementError = True
    randStrt = tuple([random.randint(1,boardSize[0]),random.randint(1,boardSize[1])])
    randGoal = tuple([random.randint(1,boardSize[0]),random.randint(1,boardSize[1])])
    
    while (placementError):
        if ((0 < randStrt[0] < boardSize) and (0 < randGoal[0] < boardSize)):
            if ((0 < randStrt[1] < boardSize) and (0 < randGoal[1] < boardSize)):
                if (boardState[randStrt] == 1):
                    if (boardState[randGoal] == 1):
                        if (boardState[randGoal] == 0):
                            randGoal = tuple([random.randint(1,boardSize),random.randint(1,boardSize)])

                        if (boardState[randStrt] == 0):
                            randStrt = tuple([random.randint(1,boardSize),random.randint(1,boardSize)])
                        placementError = False
                           

    return randStrt, randGoal


# In[7]:


def usrRandOrInput():
    print("Enter 1 for random start/goal and 2 for manual start/goal coordinates")
    print("Note ---> the obsticles are randomly placed/sized each time the code is run")
    
    usrAns = int(input("1 or 2: "))
    return usrAns


# In[8]:


class Node:
    def __init__(self, Node_State_i=[], Node_Cost_i=0, Node_Parent_i=0):
        self.Node_State_i = Node_State_i
        self.Node_Cost_i = Node_Cost_i
        self.Node_Parent_i = Node_Parent_i


def hpqNextNode(Node, nextCost, newNode):
    hpq.heappush(Node.Node_State_i, (nextCost, newNode))

def getNode(currentNode):
    node_removed = hpq.heappop(currentNode.Node_State_i)
    node = node_removed[1]
    cost = node_removed[0]
    return node, cost

def nodeCost(nodeCost, nextCost, currentNode, goal_node):
    possibleMoves = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)]
    moveCost = [1, 1, 1, 1, 1.4, 1.4, 1.4, 1.4]
    index = possibleMoves.index(nextCost)
    nextNodeCost = nodeCost + moveCost[index]
    
    point_x = currentNode[0]
    point_y = currentNode[1]
    goal_x = goal_node[0]
    goal_y = goal_node[1]
    euc_dist = np.sqrt((point_x-goal_x)**2 + (point_y-goal_y)**2)
    point = np.array(currentNode)
    goal = np.array(goal_node)
    euc_dist = np.linalg.norm(point - goal)
    
    nextNodeCost = nextNodeCost+euc_dist
    return nextNodeCost


# In[ ]:





# In[9]:


def astar(start_node, goal_node, boardState):
    count=-1
    possibleMoves = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)]
    moveCost = [1, 1, 1, 1, 1.4, 1.4, 1.4, 1.4]
    
    
    prevNodesPath = {}  
    prevNodesCost = {}  
    
    prevNodesPath[start_node] = 0
    prevNodesCost[start_node] = 0
    
    ndLst = Node()
    hpqNextNode(ndLst, 0, start_node)
    #print("Previous Node Cost ", prevNodesCost)
    #print("List of Nodes ", ndLst.Node_State_i)
    
    while len(ndLst.Node_State_i) > 0:
        count=count+1
        currentNode, currentNodeCost = getNode(ndLst)
        
        #print("Current Node ", currentNode)
        #print("Current Node Cost = ", currentNodeCost)
        
        if currentNode == goal_node:
            break
            
        for newNodeMove in possibleMoves:
            
            newNode = (currentNode[0] + newNodeMove[0],currentNode[1] + newNodeMove[1])
            
            if newNode[0] < 0 or newNode[1] < 0 or newNode[0] == boardSize[0] or newNode[1] == boardSize[1]: 
                
                #print("Node outside of bounds", newNode)
                continue
                
            #print("Move = ", newNode)
            
            newNodeCost = (nodeCost(currentNodeCost, newNodeMove, currentNode, goal_node))
            q = 0
            #print("Cost to go = ", newNodeCost)
            
            if newNode not in prevNodesCost or newNodeCost < prevNodesCost[newNode]:
                #print(boardState)
                
                if boardState[newNode]==0:
                    print("Node outside of bounds")
                    #print(boardState[newNode])
                    
                    
                else:
                    prevNodesCost[newNode] = newNodeCost
                    hpqNextNode(ndLst, newNodeCost, newNode)
                    prevNodesPath[newNode] = currentNode
                    

    q = plt.quiver(currentNode[0],currentNode[1] , newNode[0] , newNode[1],units='xy' ,scale=1,color= 'r',headwidth = 1,headlength=0)  
    plt.grid()
   
    plt.xlim(0,400)
    plt.ylim(0,250)
    plt.show()
            
    print("Current Node Cost = ", currentNodeCost)              
    return prevNodesPath


# In[10]:


def rollBack(Start, Goal, explored_path):
    pathlist = []
    goalpath = Goal
    pathlist.append(Goal)
    while goalpath != Start:
        pathlist.append(explored_path[goalpath])
        goalpath = explored_path[goalpath]
        #print(pathlist)
        

    
    pathlist.reverse()
    

    
    return pathlist


# In[11]:


def Visualize(path, visited, boardState):
    pyg.display.init()
    map_screen = pyg.display.set_mode((boardSize[0], boardSize[1]))
    for event in pyg.event.get():
            
        if (event.type == QUIT):
            pyg.quit()
            sys.exit()

    map_screen.fill((255, 255, 255))
    pyg.display.set_caption("Board")
    for key in boardState.keys():
        if boardState[key] == 0:
            map_screen.set_at(key, (0, 0, 0))
        else:
            map_screen.set_at(key, (255, 255, 255))
    for node in visited:
        #print(visited)
        
        
                    
        map_screen.set_at(node, (0, 0, 255))
        
              
        for event in pyg.event.get():
            if (event.type == QUIT):
                pyg.quit()
                sys.exit()
        pyg.time.delay(1)
        pyg.display.update()
    for node in path:
        map_screen.set_at(node, (0, 255, 0))
        
        pyg.display.update()


# In[ ]:



    


# In[ ]:


def runFunctions():
    boardState = createBoard()
    #usrAns = usrRandOrInput()
    
    
  #  if (usrAns==1):
   #     randStrt, randGoal = randStrtGoal(boardState)
    #    Start = randStart
    #    Goal = randGoal
   # else:
    Start, Goal = userInput(boardState)
    #    Start = Start
    #    Goal = Goal
        

    previous = astar(Start,Goal, boardState)
    
    path = rollBack(Start, Goal, previous)
    
    Visualize(path, previous, boardState)

runFunctions()

# enter y coordinate with space after the comma ---> ex. 100, 100


# 

# In[ ]:




