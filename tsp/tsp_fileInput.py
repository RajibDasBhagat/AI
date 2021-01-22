
# coding: utf-8

# In[26]:


import sys
import math
import random
import numpy as np
import copy
import fileinput


start=[]
startNew=[]
tempStart=[]


# In[27]:


def initial_tour(nodes):
    #initial tour from [0, 1, 2, ... , n-1]
    init=[]
    for i in range(nodes):
        init.append(i)
    return init

def cost(start,distMatrix):
    #print(start)
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


# In[28]:


def simulatedAnneling(nodes,distMatrix):

    epsilon = nodes * (10**6)
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
    print("\n __________________________________________________________________")
        
    for i in range(10):
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
                print("\n __________________________________________________________________")    

        elif (probability_acceptance(oldCost, newCost, temperature)):
            start = startNew[:]

        temperature = newTemperature(temperature,constant)

    return minTour,minCost


# In[29]:


def insertXY(nodes,points,p,x,y):
    i=0
    while i < (nodes):
        points.append(map(float,p[i].strip().split(' ')))
        i += 1
            
    for i in range(nodes):
            x.append(points[i][0])
            y.append(points[i][1])        
    return x, y  

def insertDistance(nodes,d,distMatrix):
    j = 0
    while j < nodes:
            distMatrix.append(map(float,d[j].strip().split(' ')))
            j = j + 1
    return distMatrix    
    


# In[30]:


def distance_noneuc(nodes,distMatrix,x,y):
    n=nodes
    tempCost=[]
    #print(x,y)
    for i in range(n):
        for j in range(n):
            c=math.sqrt(((x[i]-x[j])**2) + ((y[i]-y[j])**2))
            tempCost.append(c)
    #print(tempCost)
    distMatrix = [ tempCost[i*n:(i+1)*n] for i in range(n) ]
    return distMatrix


# In[31]:


if __name__ == "__main__":
    points=[]
    x=[]
    y=[]
    distMatrix=[]
    
    line=[]
    for i in fileinput.input():
        line.append(i) 	
        
    eucType=line[0].strip('\n')
    
    if eucType=="euclidean":
        nodes=int(line[1])
        p=line[2:2+nodes]
        d=line[2+nodes:]
        
        insertXY(nodes,points,p,x,y)
        insertDistance(nodes,d,distMatrix)
        simulatedAnneling(nodes,distMatrix)
	