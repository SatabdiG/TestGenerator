#!/usr/bin/env python

"""
Description : Test runner Module. Constructs the Tree from inputCollection

"""
import pymongo
from classes import Node, Graph
import os
from TestCases import TestCase, Gene
import Tkinter as tk
import sys, math
import random


#Global Variables
graphmaster = Graph()
population = Gene()
maxRun =  1
matingPool = []

#1 . Reconstruct Tree based on information from input collection
client = pymongo.MongoClient()
db = client.input

rootNodeCursor = db.inputCollection.find({"name":"Root"})
rootNode = Node(name ="Root")
graphmaster.addNode(rootNode)
## Create the root Node
rootEle = rootNodeCursor[0]["children"]
for child in rootEle:
    newchild = Node(name = child, parent = rootNode)
    rootNode.addChildren(newchild)
    graphmaster.addNode(newchild)

""" Contains only the first level nodes """
nodes = graphmaster.nodes
"""Construct the rest of the tree """
for node in nodes:
    nodeName = node.name
    if(nodeName != "Root"):       
        restNodes = db.inputCollection.find({"name":nodeName})
        #get the children
        if(restNodes.count() != 0):            
            children = restNodes[0]["children"]
            for child in children:
               isPresent = node.isPresent(child)               
               if(isPresent == False):                
                newchild = Node(name = child, parent = node)
                node.addChildren(newchild)
                graphmaster.addNode(newchild)



""" View The Tree """
# for eachn in nodes:
#     print "NodeName" +eachn.name    
#     if eachn.parent == None:
#         print "Parent is Root"
#     else:
#         print "Parent is "+eachn.parent.name

print "Tree Construction is finished"

"""Construct each test case """
# for files in os.listdir("./TestCases"):
#     """ Create a new Test case obj """
#     tc1 = TestCase(files.strip(".txt"))
#     population.addGene(tc1)
#     tmpfile = open(os.path.join("./TestCases",files))
#     for eachline in tmpfile.readlines():       
#         eachNode = graphmaster.getNode(eachline.strip())       
#         tc1.addNode(eachNode)


    # nodeeles.execute()




""" The Main Test Runner APP """
class Application(tk.Frame):
    def __init__(self, master = None):
        tk.Frame.__init__(self,master=None)
        self.grid()       
        self.master.minsize(width=200,height=100)        
        self.filename = "" 
        self.height = 0
        self.width =  0    
        self.listele = ()
        self.createWidjet()
    
    def QUIT(self):
        sys.exit()

    def RunButton(self):
        """ Execute each testcase in current population 
        assign a fitness value for each """
        for i in range(0, maxRun):
            population.empty()
            matingPool = []
            currDir = str("./TestCases/Run"+str(i))
            for files in os.listdir(currDir):
                """ Create a new Test case obj """
                tc1 = TestCase(files.strip(".txt"))
                population.addGene(tc1)
                tmpfile = open(os.path.join(currDir,files), "r+")
                for eachline in tmpfile.readlines():       
                    eachNode = graphmaster.getNode(eachline.strip())       
                    tc1.addNode(eachNode)
                tmpfile.close()
            """ Execute each tc in population 
            get the fitness for each tc """

            for nodeeles in population.testcases:            
                retval = nodeeles.execute()        
                fitVal = math.fabs(retval)    
                nodeeles.fitness(fitVal)
                for j in range(0, int(fitVal*100)):
                    matingPool.append(nodeeles)
            
           
            """ Create new population based on fitness value """
            for j in range(0, len(population.testcases)):
                randNUMA = random.randint(0, len(matingPool)-1)
                randNUMB =  random.randint(0, len(matingPool)-1)
                parentA = matingPool[randNUMA]
                parentB = matingPool[randNUMB]
                newChild = parentA.crossover(parentB)
                """ Create new population """
                newDir =  str("./TestCases/Run"+str(i+1))
                # check if newDir exists 
                if not os.path.exists(newDir):
                    os.makedirs(newDir)
                tempFile = open(os.path.join(newDir, "tc"+str(j)+".txt") , "w+" )
                newChild.WriteFile(tempFile)
                tempFile.close
                  
    def createWidjet(self):
        self.labelX=tk.Label(self, text="Welcome to Test Runner")
        self.labelX.grid(row = 2,column = 5  )
        self.RunButton=tk.Button(self, text='RUN', command = self.RunButton)
        self.RunButton.grid(row = 4, column = 4 )   
        self.QuitButton=tk.Button(self, text='QUIT', command = self.QUIT)
        self.QuitButton.grid(row = 4, column = 6 )  
        



app =  Application()
app.master.title('Main test Executor')
app.mainloop()
















client.close()