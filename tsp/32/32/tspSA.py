
# coding: utf-8

# In[1]:


import sys
import math
import random
import numpy as np
import copy

start=[]
startNew=[]
tempStart=[]

# In[2]:


def initial_tour(nodes):
    #initial tour from [0, 1, 2, ... , n-1]
    init=[]
    for i in range(nodes):
        init.append(i)
    return init

def cost(start,distMatrix):
    length = len(start)-1;
    distCost = 0.0;
    for i in range(length):
            distCost += distMatrix[start[i]][start[i+1]]
    distCost += distMatrix[start[length]][start[0]]
    #print(distCost)
    return distCost

def initialTemperature():
    return 100

def newTemperature(temperature,constant):
    temperature = temperature * constant
    return temperature
def probability_acceptance(oldCost, newCost, temperature):
    #choose random
    prob = np.exp ( -(newCost - oldCost) / temperature)
    randomProb = random.uniform(0, 1)
    if (randomProb < prob):
        return 1
    else:
        return 0
def randomNextState(tempStart):

    length=len(tempStart)-1
    next1=randomNumber(0,length)%length
    next2=randomNumber(0,length)%length
    if(next1 != next2):
        temp=tempStart[next1]
        tempStart[next1]=tempStart[next2]
        tempStart[next2]=temp
    else:
        randomNextState(tempStart)

    return tempStart

def randomNumber(a,b):
    #generates random number between start and end inclusively
    r=random.randint(a,b)
    return r


# In[27]:


def simulatedAnneling(nodes,distMatrix):

    epsilon = nodes * (10**8)
    constant = 0.99

    #initial tour
    init = initial_tour(nodes)
    start=init[:]
    minCost = cost(start,distMatrix)
    minTour = start[:]

    #initial temperature
    temperature = initialTemperature()
    #print(minTour)
    for i in range(nodes):
        print(minTour[i]),
    #print("\n_________________________________________________________________________________________________")	
    for i in range(epsilon):
        #random neighbores
        tempStart=start[:]
        startNew = randomNextState(tempStart)

        #if best
        oldCost = cost(start,distMatrix)
        newCost = cost(startNew,distMatrix)
        if (newCost < oldCost):
            start = startNew[:]

            if (newCost < minCost):
                minCost = newCost
                minTour = startNew[:]
                #print(minTour)
                for i in range(nodes):
                    print(minTour[i]),
                #print("\n_________________________________________________________________________________________________")

        elif (probability_acceptance(oldCost, newCost, temperature)):
            start = startNew[:]

        temperature = newTemperature(temperature,constant)

    return minTour,minCost


# In[28]:


def insertPoints(nodes,points,x,y):
    i = 0
    while i< nodes:
        points.append(map(float,raw_input().strip().split(' ')))
        i += 1
    for i in range(nodes):
        x.append(points[i][0])
        y.append(points[i][1])
            
    return x, y  

def insertDistance(nodes):
    i=0
    while(i<nodes):
        distMatrix.append(map(float,raw_input().strip().split(' ')))
        i = i+1
    return distMatrix    
    


# In[29]:


def calculateDistance(nodes,distMatrix,x,y):
    n=nodes
    temp=[]
    #print(x,y)
    for i in range(n):
        for j in range(n):
            val=math.sqrt(((x[i]-x[j])**2) + ((y[i]-y[j])**2))
            temp.append(val)
    #print(temp)
    distMatrix = [ temp[i*n:(i+1)*n] for i in range(n) ]
    return distMatrix


# In[ ]:


if __name__ == "__main__":
    points=[]
    x=[]
    y=[]
    distMatrix=[]
        
    eucType=raw_input()
    if eucType=="euclidean":
        nodes=int(raw_input())
        insertPoints(nodes,points,x,y)
        insertDistance(nodes)
        simulatedAnneling(nodes,distMatrix)
    elif eucType=="noneuclidean" or eucType=="non euclidean":
        nodes=int(raw_input())
        insertPoints(nodes,points,x,y)
		insertDistance(nodes)
        calculateDistance(nodes)
        simulatedAnneling(nodes,distMatrix) 

