from classes import Node
import pyautogui
import os, time


class TestCase(object):
    nodes = []
    def __init__(self, name):
        self.name = name
    
    def addNode(self, node):
        self.nodes.append(node)
    
    def fitness(self , fitval):
        self.fitness = fitval

    def crossover(self, parentb):
        """ Code for crossover """
        return parentb
    
    def WriteFile(self , filehandle):
        print "In WriteFile"
        for n1 in self.nodes:
            print n1
            filehandle.write(n1.name)
            filehandle.write("\n")

    def execute(self):
        starttime = time.time()
        children =[]
        for eachelem in self.nodes:
            """ Get Root """
            if eachelem.parent.name == "Root":
                rootElem = eachelem
                children.append(rootElem)
                break
        
        
        while(len(children) > 0):
            elename = children.pop()
            nodeChildren = elename.children
            for eachele in nodeChildren:
                if eachele not in children:
                    children.append(eachele)
            """ Execute test case """
            name = os.path.join("./Elements/",elename.name+".png")
            print "Elemnae:"+name            
            testpos = pyautogui.locateOnScreen(str(name))
            print testpos
            if(testpos != None):
                posX, posY = pyautogui.center(testpos)
                pyautogui.moveTo(posX , posY)
                pyautogui.click()
        
        endtime = time.time()
        difftime = (starttime - endtime)
        return difftime
            
 

class Gene(object):
    testcases =[]

    def __init__(self):
        pass
    
    def addGene(self, testcase):
        self.testcases.append(testcase)

    def empty(self):
        self.testcases = []