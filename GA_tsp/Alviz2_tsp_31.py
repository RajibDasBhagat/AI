#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys
from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QApplication,QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QApplication,QLabel, QPlainTextEdit
from PyQt5.QtGui import QPainter,QPen
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QSize    
import sys, random
import pickle
import random
import numpy as np
import scipy.spatial
from PyQt5.QtCore import QPoint
import collections
import time
#from sA_Class import ISA
import sys
import math
import tkinter as tk
import heapq


# In[2]:


def population(n_node):
    #initial tour from [0, 1, 2, ... , n-1]
    init=[]
    for i in range(n_node):
        init.append(i+1)
    random.shuffle(init)    
    init.append(init[0])
    return init

def fitness_calculate(start,d):
    #print(d)
    #print((start))
    length = len(start)-1;
    #print(len(d), length)
    distCost = 0.0;
    for i in range(length):
            distCost += d[start[i]-1][start[i+1]-1]
            #print(distCost)
    distCost += d[start[length]-1][start[0]-1]
    #print(distCost)
    return 1/distCost

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
def split_list(a_list):
    half = len(a_list)//2
    return a_list[:half], a_list[half:]

distMatrix=[]
def distance_euc(n_nodes,distMatrix,x,y):
    #print(distMatrix)
    n=n_nodes
    tempCost=[]
    for i in range(n):
        for j in range(n):
            c=math.sqrt(((x[i]-x[j])**2) + ((y[i]-y[j])**2))
            tempCost.append(c)
    #print(tempCost)
    distMatrix = [ tempCost[i*n:(i+1)*n] for i in range(n) ]
    #print(distMatrix)
    return distMatrix

def find_max2(fit):
    a, b = heapq.nlargest(2, range(len(fit)), key=fit.__getitem__)        
    return a,b

def find_max3(fit):
    a, b, c = heapq.nlargest(3, range(len(fit)), key=fit.__getitem__)        
    return a,b,c

def roulette_wheel(parent1,max_x,d):
    #print(len(parent1),len(d))
    probability=[]
    avg=1/max_x
    length=len(parent1)-1
    for i in range(length):
        p=d[parent1[i]-1][parent1[i+1]-1]
        #print(p)
        probability.append(p/avg)    
    probability.append((d[parent1[length]-1][parent1[0]-1])/avg)
    return probability

def mutation(child):
    #print("in mutation:",child)
    temp=[]
    temp1, temp2=split_list(child)
    #print(temp1)
    #print(temp2)
    temp1.reverse()
    temp2.reverse()
    temp=temp2+temp1
    #print("temp",temp)
    return temp


# In[3]:


root = tk.Tk()
screen_width = root.winfo_screenwidth()
# screen_width = 1750
screen_height = root.winfo_screenheight()
# screen_height = 950
closed_set=set()
open_set = set()
n_node = 1000
t_coord_in={}
t_in_coord={}
# adjacency_list =[]

# node_colour = [0 for i in range(n_node)] # 0  - not visited, 1 - open list, 2 - closed set, 3- Start node, 4 - Goal node


# In[4]:



# def generate_points(xl,yl,number=100):
def generate_points(xl,yl,number=50):
    x_coordinates = np.random.randint(xl, size=number)
    y_coordinates = np.random.randint(yl, size=number)
    t=[]
    for i,j in zip(list(x_coordinates),list(y_coordinates)):
          t.append([i,j+70])

    with open('node_list.pkl', 'wb') as f:
          pickle.dump(t, f)      
      
    return t

def make_edge_list_tsp(node,n_nodes):
    edg = []
    for i in range(n_nodes):
            for j in range(n_nodes):
                  if (i<j):
                        edg.append([(node[i][0],node[i][1]),(node[j][0],node[j][1])])

    with open('edge_list.pkl', 'wb') as f:
            pickle.dump(edg, f)      

    return edg                   


def find_neighbors(pindex, triang):
      return triang.vertex_neighbor_vertices[1][triang.vertex_neighbor_vertices[0][pindex]:triang.vertex_neighbor_vertices[0][pindex+1]]

# return list of list of tuples Ex.[[(x1,y1),(x2,y2)]]
def make_edge_list(node,n_node,tri,bf):
    temp=[]
    for k in range(n_node):
            pindex = k
            neighbor_indices = find_neighbors(pindex,tri)
            for i in range(len(neighbor_indices)):
                  # if i%2!=0:
                if i%bf!=0:
                        temp.append([(node[pindex][0],node[pindex][1]),(node[neighbor_indices[i]][0],node[neighbor_indices[i]][1])])      
    with open('edge_list.pkl', 'wb') as f:
            pickle.dump(temp, f)
    return temp

# Make adjacency list 
def make_adj_list(a,d,n):
    t=[[]for i in range(n+1)]
    tt=[]
    for i in a:
            t[d[i[0]]].append(d[i[1]])
            t[d[i[1]]].append(d[i[0]])
    for i in t:
            tt.append(list(set(i)))
    return tt


def make_dict_index_coord(points):
      # t = {}
    t_in_coord={}
      # print("points in in - co")
      # print(points)
    cnt=1
    for i in points:
            t_in_coord[cnt] = (i[0],i[1])
            cnt+=1
    return t_in_coord


# Mapping co-ordinates to node index.
def make_dict_coord_index(points):
      # t={}
    t_coord_in={}
      # print("points in co - in")
      # print(points)
    cnt=1
    for i in points:
            t_coord_in[(i[0],i[1])] = cnt
            cnt+=1
    return t_coord_in
                        
# Make dictionary for indexing nodes.
def make_dict_node(points):
    dict_node = {}
    cnt=1
    for i in points:
            dict_node[1] = i
            cnt+=1
    return make_dict_node

def ret_edg():
    with open('edge_list.pkl', 'rb') as f:
                  edg = pickle.load(f)
    return edg

# def make_dict_index_coord(points):
#       t = {}
#       cnt=1
#       for i in points:
#             t[cnt] = (i[0],i[1])
#             cnt+=1
#       return t

def movegen(adj,n_ind):
      return adj[n_ind]

def backtrace(parent, start, end):
    path = [end]
    while path[-1] != start:
            path.append(parent[path[-1]])
    path.reverse()
    return path

def distance(city1, city2):
    cord1 = dict_index_coord[city1]
    cord2 = dict_index_coord[city2]
    return math.sqrt((cord1[0] - cord2[0]) ** 2 + (cord2[1] - cord2[1]) ** 2)

def eval(node,goal_node):
    cord1 = dict_index_coord[node]
    cord2 = dict_index_coord[goal_node]
    return abs(cord1[0] - cord2[0]) + abs(cord2[1] - cord2[1])


# In[5]:



x=[]
y=[]

def Algorithm(adjacency_list, dict_index_coord, n_node):#you have to add the assigned algorith here
    path=[]# this is the path or tour to be returned
    
    for i in dict_index_coord:
        x.append(dict_index_coord[i][0])
        y.append(dict_index_coord[i][1])
    #print("x:",x)
    #print("y:",y)
    
    d=distance_euc(n_node,distMatrix,x,y)        
    #print("d",d)
    init_start=population(n_node)
    #print("start",init_start)
    path.append(init_start)
    init_fitness=fitness_calculate(init_start,d)
    #print("fit",init_fitness)
    l=len(path)
    no_generation=30
    population_size=5
    count=0
    chromosomes=[]
    while(no_generation>0):
        #print(init_start)
        count += 1
        print("generation:", count)
        fitness=[]
        no_generation = no_generation-1
        #generate chromosomes 
        for i in range(population_size):
            ch=population(n_node)
            #ch=init_start[:]
            #print("ch",ch)
            if ch not in chromosomes:
                chromosomes.append(ch)
        #print("chromosomes:",chromosomes)
        #calculate fitness         
        for i in range(len(chromosomes)):
            fitness.append(fitness_calculate(chromosomes[i],d))
        #print(fitness)
    
        #choose best two chromosomes as parents    
        max_a,max_b = find_max2(fitness)
        #print(max_a,max_b)
        #print("fit",fitness[max_a], fitness[max_b] )
        
        if(fitness[max_a] >= fitness[max_b]):
            new_fitness=fitness[max_a]
        else:
            new_fitness=fitness[max_b]
            
        if(new_fitness >= init_fitness):    
                #print(chromosomes[max_a], chromosomes[max_b] )
                parent1 = chromosomes[max_a]
                parent2 = chromosomes[max_b]
                #parent1.append(parent1[0])
                #parent2.append(parent2[0])
                #print("p1",parent1)
                #print("p2",parent2)
                new_start=parent1[:]
                if new_start not in path:
                    path.append(new_start)
                    #print("path:",path[l-1])
                #return path[l-1]   
                
        #print("path",path)        
        
        #selection for crossover by probability
        prob1=roulette_wheel(parent1,fitness[max_a],d)
        p1_max_a,p1_max_b,p1_max_c = find_max3(prob1)        
        prob2=roulette_wheel(parent2,fitness[max_b],d)
        p2_max_a,p2_max_b,p2_max_c = find_max3(prob2)
        
        #print("p1",parent1,"p2",parent2)
        
        #crossover
        length=len(parent1)-1
        child1=parent1[:length]
        child2=parent2[:length]
        #print("c1",child1,"c2",child2)
        
        child2.remove(parent1[p1_max_a])
        child2.remove(parent1[p1_max_b])
        child2.remove(parent1[p1_max_c])
        #print("c2",child2)
        child2.append(parent1[p1_max_a])
        child2.append(parent1[p1_max_b])
        child2.append(parent1[p1_max_c])
        #print("c2",child2)
        child1.remove(parent2[p2_max_a])
        child1.remove(parent2[p2_max_b])
        child1.remove(parent2[p2_max_c])
        child1.append(parent2[p2_max_a])
        child1.append(parent2[p2_max_b])
        child1.append(parent2[p2_max_c])
        #print("c1",child1)
     
        #selection for mutation and mutate (split the array and swap the two parts)
        mutation1 = mutation(child1)
        mutation2 = mutation(child2)
        #print("m1",mutation1)
        #print("m2",mutation2)
        #check fitness again
        fit1=fitness_calculate(mutation1,d)
        fit2=fitness_calculate(mutation2,d)
        #print(fit1,fit2)
        
        if (fit1>fit2):
            init_start=mutation1[:]
        else:
            init_start=mutation2[:]    
    
    #l=len(path)
    #print(path)
    #print(path[l-1])
    return path[l-1]
  


# In[6]:


def my_main(n_node = 100, bf = 2,gg=0):
    x_dim = screen_width-100
    y_dim = screen_height-150
    edge_list=[]
    
    global dict_index_coord
    global dict_coord_index
    global adjacency_list 

    if (gg==0):
            node = generate_points(x_dim,y_dim,n_node)
            # with open('node_list.pkl', 'rb') as f:
            #       node = pickle.load(f)
            # global dict_index_coord
            dict_index_coord = make_dict_index_coord(node) # indexing to pixels pair. Ex. 1->(10,10)
            # global dict_coord_index
            dict_coord_index = make_dict_coord_index(node) # mapping pixels to index pair. Ex. (10,10) -> 1
            # print("MAP")
            # print(dict_coord_index)
            # print(dict_index_coord)
            tri = scipy.spatial.Delaunay(np.array(node))

            # with open('edge_list.pkl', 'rb') as f:
            #       edge_list = pickle.load(f)                  
            
            edge_list = make_edge_list(node,n_node,tri,bf)                  
            # print(edge_list)
            # global adjacency_list 
            adjacency_list= make_adj_list(edge_list,dict_coord_index,n_node) #adjcency list                   
            
            return edge_list
    elif (gg==2):
            node = generate_points(x_dim,y_dim,n_node)
            # with open('node_list.pkl', 'rb') as f:
            #       node = pickle.load(f)
            # global dict_index_coord
            dict_index_coord = make_dict_index_coord(node) # indexing to pixels pair. Ex. 1->(10,10)
            # global dict_coord_index
            dict_coord_index = make_dict_coord_index(node) # mapping pixels to index pair. Ex. (10,10) -> 1
            # print("MAP")
            # print(dict_coord_index)
            # print(dict_index_coord)
            edge_list = make_edge_list_tsp(node,n_node)
            # with open('edge_list.pkl', 'rb') as f:
            #       edge_list = pickle.load(f)      
            # global adjacency_list 
            adjacency_list= make_adj_list(edge_list,dict_coord_index,n_node)
            return edge_list

    elif (gg==1):
            # tree code  TODO
            return edge_list





class Example(QMainWindow):
      
    def __init__(self):
            super().__init__()
            self.nodes = 100
            self.bf = 2
            self.dict_index_coord = {}
            self.open_list = []
            self.closed_list = []      
            self.init_phase = -1
            self.start_x=0
            self.start_y=0
            self.goal_x=0
            self.goal_y=0
            self.initUI()
            self.setMinimumSize(QSize(screen_width,screen_height))    
            self.setWindowTitle("Alviz v0.2") 
            
            
    def initUI(self):                       
            self.exitAct = QAction( '&Exit', self)        
            self.exitAct.setShortcut('Ctrl+Q')
            self.exitAct.setStatusTip('Exit application')
            self.exitAct.triggered.connect(qApp.quit)
            self.genAct = QAction( '&Generate Graph', self)
            self.genAct.triggered.connect(self.clickMethod)
            self.genTreeAct = QAction( '&Generate Tree', self)
            self.genTreeAct.triggered.connect(self.clickMethod1)
            self.genTSPAct = QAction( '&Generate TSP', self)
            self.genTSPAct.triggered.connect(self.clickMethod2)
            self.startAct = QAction( '&Start Node', self)
            self.goalAct = QAction( '&Goal Node', self)
            self.genRevertAct = QAction( '&Revert', self)
            self.genRevertAct.triggered.connect(self.clickMethodRevert)
            self.nodeLabel = QLabel('Number of nodes:')
            self.nodeText = QPlainTextEdit('100')
            self.nodeText.setFixedSize(80,28)
            self.bfLabel = QLabel('Branching Factor:')
            self.bfText = QPlainTextEdit('2')
            self.bfText.setFixedSize(80,28)
            self.resetAct =  QAction( '&Reset Screen', self)
            self.resetAct.triggered.connect(self.reset_screen)
            self.menubar = self.menuBar()
            self.fileMenu = self.menubar.addMenu('File')
            self.fileMenu.addAction(self.exitAct)
            self.toolbar = self.addToolBar('')
            self.toolbar.addWidget(self.nodeLabel)
            self.toolbar.addWidget(self.nodeText)
            self.toolbar.addWidget(self.bfLabel)
            self.toolbar.addWidget(self.bfText)
            self.toolbar.addAction(self.genAct)
            self.toolbar.addAction(self.genTreeAct)
            self.toolbar.addAction(self.genTSPAct)
            self.toolbar.addAction(self.startAct)
            self.toolbar.addAction(self.goalAct)
            self.toolbar.addAction(self.genRevertAct)
            self.toolbar.addAction(self.resetAct)
            self.setMouseTracking(True)
            self.startAct.setEnabled(False)
            self.goalAct.setEnabled(False)
            self.path_t=[]

            # my_main()

    def reset_screen(self):
            self.init_phase = -1
            self.startAct.setEnabled(False)
            self.goalAct.setEnabled(False)
            self.update()
            

    def clickMethod(self):
            self.init_phase = 0
            # print('Clicked Pyqt button.')
            self.nodes = int(self.nodeText.toPlainText())
            self.bf = int(self.bfText.toPlainText())
            global node_colour
            node_colour = [0 for i in range(self.nodes+1)] 
            my_main(self.nodes,self.bf,0)
            self.update()

    def clickMethod1(self):
            self.init_phase = 0
            # print('Clicked Pyqt button. 1')
            self.nodes = int(self.nodeText.toPlainText())
            self.bf = int(self.bfText.toPlainText())
            global node_colour
            node_colour = [0 for i in range(self.nodes+1)] 
            my_main(self.nodes,self.bf,1)
            self.update()
            
    def clickMethod2(self):
            self.init_phase = 6
            # print('Clicked Pyqt button. 2')
            self.nodes = int(self.nodeText.toPlainText())
            self.bf = int(self.bfText.toPlainText())
            global node_colour
            node_colour = [0 for i in range(self.nodes+1)] 
            my_main(self.nodes,self.bf,2)
            self.update()
    def clickMethodRevert(self):
            self.init_phase = 0
            print('Clicked Pyqt button. Revert')
            self.nodes = int(self.nodeText.toPlainText())
            self.bf = int(self.bfText.toPlainText())
            global node_colour
            node_colour = [0 for i in range(self.nodes+1)] 
            # my_main(self.nodes,self.bf,2)
            self.update()                  
      # def mouseClickEvent(self,e):
    def mousePressEvent(self, e):
            x=e.x()
            y=e.y()
            text = "x: {0},  y: {1}".format(x, y)
            min_x=99999
            max_x=-99999
            min_y=99999
            max_y=-99999
            self.findClosestCoordinate(min_x,min_y,x,y)
            # self.label.setText(text)
            # print(text)
      
    def findClosestCoordinate(self,min_x,min_y,x,y):
            edg=ret_edg()
            myset = set()
            min_dist=999999999
            for e in edg: 
                  # myset.add(e[0])
                  # myset.add(e[1])
                dist=(x-e[0][0])**2+(y-e[0][1])**2
                if(dist<min_dist) :
                        min_dist=dist
                        min_x=e[0][0]
                        min_y=e[0][1]
            print("minimum x :"+str(min_x))
            print("minimum y :"+str(min_y))
            if(self.init_phase==0):#initial phase for planar graph generation
                self.start_x=min_x
                self.start_y=min_y
                self.init_phase=1
                  # self.update()
            elif(self.init_phase==1):#After selecting the start node      
                self.goal_x=min_x
                self.goal_y=min_y
                self.init_phase=5
                  # self.update()
            elif(self.init_phase==5):#After selecting the goal node
                 # print("start_x , start_y"+str(self.start_x)+","+str(self.start_y))
                start_node = dict_coord_index[(self.start_x,self.start_y)]#1
                print(start_node)
                l=dict_index_coord[start_node]
                print(l)

                  # print("coord - to - int ")
                  # print(dict_coord_index)
                  # print("int - to - coord ")
                  # print(dict_index_coord)
                  # print("###################################")
                goal_node =  dict_coord_index[(self.goal_x,self.goal_y)]
                self.path_t = Algorithm(adjacency_list,dict_coord_index,self.nodes) ##########################HERE
                print("color",node_colour)
                  # print("###################################")
                  # print (len(node_colour))
                self.init_phase=3
            elif(self.init_phase==3):#show the bfs
                self.init_phase=4                  #init_phase=4 is the default end phase of all types of graph
            elif(self.init_phase==6):#initial phase for tsp
                print ('Algo called')
                #print(adjacency_list)  
                self.path_t = Algorithm(adjacency_list,dict_index_coord,self.nodes) #########################HERE
                self.init_phase=7      #change
            elif(self.init_phase==7):#final phase for tsp
                self.init_phase=4                                    

    def paintEvent(self, e):

            qp = QPainter()
            qp.begin(self)
            # self.print_s(qp)
            if (self.init_phase!=-1):
                self.drawPoints(qp)
                if(self.init_phase!=6):
                       self.drawLines(qp)
                qp.end()


    def drawPoints(self, qp):

            qp.setPen(Qt.red)
            size = self.size()
            edg=ret_edg()
            myset = set()
            for e in edg: 
                myset.add(e[0])
                myset.add(e[1])

            xx = list(myset)      
            self.dict_index_coord = make_dict_index_coord(xx)

            # print(self.init_phase)
            # print(self.start_x)
            # print(self.start_y)



            if (self.init_phase == 0):#draw points to create planar graph

                  for e in edg :
                        center = QPoint(e[0][0],e[0][1])
                        qp.setBrush(Qt.yellow)
                        qp.drawEllipse(center,5,5)
                     #qp.drawPoint(e[0][0],e[0][1])
                  
                  self.startAct.setEnabled(True)
                  
                  self.update()
            # else:
            elif (self.init_phase == 1):#draw start node
                for e in edg :
                        center = QPoint(e[0][0],e[0][1])
                        qp.setBrush(Qt.yellow)
                        qp.drawEllipse(center,5,5)

                center = QPoint(self.start_x,self.start_y)
                qp.setBrush(Qt.green)
                qp.drawEllipse(center,10,10)      
                  
                self.startAct.setEnabled(False)
                self.goalAct.setEnabled(True)
                self.update()
            elif (self.init_phase == 5):#draw goal node
                for e in edg :
                        center = QPoint(e[0][0],e[0][1])
                        qp.setBrush(Qt.yellow)
                        qp.drawEllipse(center,5,5)

                center = QPoint(self.start_x,self.start_y)
                qp.setBrush(Qt.green)
                qp.drawEllipse(center,10,10)
                        
                center = QPoint(self.goal_x,self.goal_y)
                qp.setBrush(Qt.red)
                qp.drawEllipse(center,10,10)      

                self.startAct.setEnabled(False)
                self.goalAct.setEnabled(False)
                self.update()
                  # self.init_phase = 5
            elif (self.init_phase == 3):#draw the path and color different nodes as per the color coding mentioned
                  i=1
                  # print("node col size "+str(len(node_colour)))
                  for i in range(1,len(node_colour)):
                        point=dict_index_coord[i]
                        e = node_colour[i]
                        center = QPoint(point[0],point[1])
                        if(e==0) :
                              # qp.setBrush(Qt.gray)
                            qp.setBrush(Qt.yellow)
                            qp.drawEllipse(center,8,8)
                        if(e==1) :
                            qp.setBrush(Qt.magenta)
                            qp.drawEllipse(center,8,8)
                        if(e==2) :
                            qp.setBrush(Qt.blue)
                            qp.drawEllipse(center,8,8)
                        if(e==3) :
                            qp.setBrush(Qt.cyan)
                            qp.drawEllipse(center,15,15)
                        if(e==4) :
                            qp.setBrush(Qt.red)
                            qp.drawEllipse(center,15,15)
                        # i=i+1                              
                        # qp.drawEllipse(center,5,5)                        
                        self.update()
      
            elif(self.init_phase == 4):      #default final state of all graph
                  self.update()
            elif(self.init_phase == 6): #initial phase of tsp
                for e in edg :
                        center = QPoint(e[0][0],e[0][1])
                        qp.setBrush(Qt.yellow)
                        qp.drawEllipse(center,5,5)
                     #qp.drawPoint(e[0][0],e[0][1])
                  
                self.startAct.setEnabled(True)                 
                self.update()
            elif(self.init_phase == 7):      #finall tour plot
                print ('hello')
                  # for e in edg :#you have to use the tour returned by TSP in place of edg
                  #       center = QPoint(e[0][0],e[0][1])
                  #       qp.setBrush(Qt.red)
                  #       qp.drawEllipse(center,5,5)
                  #    #qp.drawPoint(e[0][0],e[0][1])

                for e in edg :
                        center = QPoint(e[0][0],e[0][1])
                        qp.setBrush(Qt.yellow)
                        qp.drawEllipse(center,5,5)

                pen = QPen(Qt.black, 5, Qt.DashDotLine)
                  # qp.setPen(Qt.red)
                  # qp.setWidth(10)
                pen.setBrush(Qt.red)
                pen.setWidth(5)
                qp.setPen(pen)
                for i in range(len(self.path_t)-1):
                        a=self.path_t[i]
                        # print("---- point a --- ")
                        # print(a)
                        a_pos=dict_index_coord[a]
                        b=self.path_t[i+1]
                        # print("---- point b --- ")
                        # print(b)
                        b_pos=dict_index_coord[b]      
                        qp.drawLine(a_pos[0],a_pos[1],b_pos[0],b_pos[1])  
                self.startAct.setEnabled(True)
                self.update()


    def drawLines(self, qp):
            pen = QPen(Qt.black, 2, Qt.SolidLine)
            qp.setPen(Qt.gray)

            with open('edge_list.pkl', 'rb') as f:
                  edg = pickle.load(f)
            
               #main()
            if (self.init_phase!=6 and self.init_phase!=7) :
                for e in edg :
                    qp.drawLine(e[0][0],e[0][1],e[1][0],e[1][1])      

            if(self.init_phase == 3):
                pen = QPen(Qt.black, 5, Qt.DashDotLine)
                  # qp.setPen(Qt.red)
                  # qp.setWidth(10)
                pen.setBrush(Qt.red)
                pen.setWidth(5)
                qp.setPen(pen)
                for i in range(len(self.path_t)-1):
                        a=self.path_t[i]
                        # print("---- point a --- ")
                        # print(a)
                        a_pos=dict_index_coord[a]
                        b=self.path_t[i+1]
                        # print("---- point b --- ")
                        # print(b)
                        b_pos=dict_index_coord[b]      
                        qp.drawLine(a_pos[0],a_pos[1],b_pos[0],b_pos[1])
            
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())



# In[ ]:





# In[ ]:




