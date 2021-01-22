
# coding: utf-8

# In[1]:


import sys
import math
import random
import numpy as np
import copy

distMatrix=[]
start=[]
startNew=[]
tempStart=[]


# In[2]:


def randomNumber(a,b):
    #generates random number between start and end inclusively
    r=random.randint(a,b)
    return r


# In[38]:


def coordinates(points):
    x=[]
    y=[]
    for i in range(len(points)):
        if(i%2 == 0):
            x.append(points[i])
        else:
            y.append(points[i])
    #Sprint(x,y)
    return x,y

#points=[-73.3518340151, 88.1847984526, 75.5877459981, -2.53004018712, 77.3500734546, -69.1675063635, 97.6948545817, -48.4341182624, -49.0228125157, -40.0398982543]
#x,y=coordinates(points)


# In[39]:


def distance_euc(nodes,distMatrix,distanceCost):
    n = nodes
    distMatrix = [ distanceCost[i*n:(i+1)*n] for i in range(n) ]
    return distMatrix

#distanceCost=[0, 4, 5, 6, 4, 0, 1, 2, 5, 1, 0, 1, 6, 2, 1, 0]
#d=distance_euc(4,distMatrix,distanceCost)
#print(d)


# In[41]:


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
#d=distance_noneuc(4,distMatrix,x,y)
#print(d)


# In[42]:


def initial_tour(nodes):
    #initial tour from [0, 1, 2, ... , n-1]
    init=[]
    for i in range(nodes):
        init.append(i)
    return init

#i=initial_tour(4)
#print(i)


# In[43]:


def cost(start,distMatrix):
    length = len(start)-1;
    distCost = 0.0;
    for i in range(length):
            distCost += distMatrix[start[i]][start[i+1]]
    distCost += distMatrix[start[length]][start[0]]
    #print(distCost)
    return distCost
#start=i[:]
#distMatrix=d[:]
#print(len(distMatrix))
#c=cost(i,distMatrix)


# In[44]:


def initialTemperature():
    return 1

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


# In[45]:


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


# In[ ]:


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

        elif (probability_acceptance(oldCost, newCost, temperature)):
            start = startNew[:]

        temperature = newTemperature(temperature,constant)
        print(minTour)

    return minTour,minCost


#simulatedAnneling(4,d)


# In[11]:


if __name__ == "__main__":

    program_name = sys.argv[0]
    euc = sys.argv[1]


    if(euc == "euclidean"):
        nodes = int(sys.argv[2])
        points = map(float,sys.argv[3: (nodes*2)+3])
        distanceCost = map(float,sys.argv[(nodes*2)+3:])

        x, y = coordinates(points)
        d = distance_euc(nodes,distMatrix,distanceCost)
        simulatedAnneling(nodes,d)

    elif(euc=="noneuclidean"):
        nodes = int(sys.argv[2])
        points = map(float,sys.argv[3: (nodes*2)+3])

        x, y = coordinates(points)
        d = distance_noneuc(nodes,distMatrix,x,y)
        simulatedAnneling(nodes,d)
    else:
        print("ERROR!")
        print("input format: python filename.py euclidean no_nodes [node_point_x1 node_point_y1 node_point_x2 node_point_y2] [distance_cost c1 c2 c3 ...]") 
