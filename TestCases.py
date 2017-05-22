from classes import Node
import pyautogui
import os, time
import subprocess
import math
import thread


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
        ### AUT ###
        # Launch Phase
        # 
        # try:
        #     thread.start_new_thread(launch("vlc"))
        # except:
        #     print "Error"
        launch("vlc")
        # Execute Phase    
        timeAUT = executeAUT(self.nodes)
        # Shut Down Phase    
        quitFunc("vlc")
        print "Finished execution for AUT"
        ### Oracle ###
        # Launch Phase       
        launch("Oracle")
        # Execute Phase    
        timeOr = executeOracle(self.nodes)
        # Shut Down Phase    
        quitFunc("Oracle")
        print "Finished execution for AUT"
        timediff = math.fabs(timeAUT - timeOr)
        print "Time difference"
        print timediff
        return timediff

        """ Old Code """
        # starttime = time.time()
        # children =[]
        # for eachelem in self.nodes:
        #     """ Get Root """
        #     if eachelem.parent.name == "Root":
        #         rootElem = eachelem
        #         children.append(rootElem)
        #         break
        
        
        # while(len(children) > 0):
        #     elename = children.pop()
        #     nodeChildren = elename.children
        #     for eachele in nodeChildren:
        #         if eachele not in children:
        #             children.append(eachele)
        #     """ Execute test case """
        #     name = os.path.join("./Elements/",elename.name+".png")
        #     print "Elemnae:"+name            
        #     testpos = pyautogui.locateOnScreen(str(name))
        #     print testpos
        #     if(testpos != None):
        #         posX, posY = pyautogui.center(testpos)
        #         pyautogui.moveTo(posX , posY)
        #         pyautogui.click()
        
        # endtime = time.time()
        # difftime = (starttime - endtime)
        # return difftime
        """ Old Code """
            
 

class Gene(object):
    testcases =[]

    def __init__(self):
        pass
    
    def addGene(self, testcase):
        self.testcases.append(testcase)

    def empty(self):
        self.testcases = []



""" Generic Functions """
def launch(app):
    if(app == "Oracle"):
        """ Launch.sh for Oracle """
        # subprocess.call(["./scripts/launchoracle.sh"]) 
        proc = subprocess.Popen(["./scripts/launchoracle.sh"], shell=True,
             stdin=None, stdout=None, stderr=None, close_fds=True)    
        
    else:
        """ Launch.sh for AUT"""
        # subprocess.call(["./scripts/launchaut.sh"])
        proc = subprocess.Popen(["./scripts/launchaut.sh"], shell=True,
             stdin=None, stdout=None, stderr=None, close_fds=True) 
    time.sleep(5)

def quitFunc(app):
    time.sleep(5)
    if(app == "Oracle"):
        """ quit.sh for Oracle """
        subprocess.call(["./scripts/quitoracle.sh"])
    else:
        """ quit.sh for AUT"""
        subprocess.call(["./scripts/quitaut.sh"])
    time.sleep(5)

def executeOracle(nodes):
    starttime = time.time()
    children =[]
    for eachelem in nodes:
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
            name = os.path.join("./OracleElements/",elename.name+".png")
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
    

def executeAUT(nodes):
        starttime = time.time()
        children =[]
        for eachelem in nodes:
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