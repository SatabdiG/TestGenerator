#!/usr/bin/env python

import pyautogui
import Tkinter as tk
import sys
import pyscreeze
import pygame
import os
from classes import Node, Graph
import termios
import tty
import pymongo

""" Contains an Application that can be used to create a database for any UI device """


#Global Variables
childOffsetX = 10
screenWidth, screenHeight = pyautogui.size()
client = pymongo.MongoClient()
db = client.input

graphMaster = Graph()
parentRoot = Node(name = "Root")
graphMaster.addNode(parentRoot)
RootElems = []
## Construct the input Tree ###
# get root elem
emptyNode = [] 
seenNodes = []
rootelem = db.inputCollection.find({"name":"Root"})
for eachelem in rootelem:
    #create a Node
    childeelm = eachelem["children"]
    for eachchild in childeelm:
        if(graphMaster.getNode(eachchild) == "Not Found"):
            #create a node
            tmpchild = Node(name = eachchild, parent = parentRoot)
            parentRoot.addChildren(tmpchild)
            graphMaster.addNode(tmpchild) 
            emptyNode.append(eachchild)
            seenNodes.append(eachchild)
            RootElems.append(tmpchild)



while len(emptyNode) > 0 :
    curr = emptyNode.pop()
    currChild = graphMaster.getNode(curr)
    if currChild.name != "Root":
         cursor = db.inputCollection.find({"name":currChild.name})
         if(cursor.count()!=0):
                for each in cursor:
                    childeme = each["children"]
                    for child in childeme:
                        if child not in seenNodes:
                            seenNodes.append(child) 
                            emptyNode.append(child)                      
                            nodechild = Node(name =  child, parent = currChild)
                            currChild.addChildren(nodechild)
                            graphMaster.addNode(nodechild)
                            
   

# for eachnode in graphMaster.nodes:
#     print "--------------------"
#     print"Name"
#     print eachnode.name
#     if eachnode.name != "Root":
#         print "Parent"
#         print eachnode.parent.name
#     for eachele in eachnode.children:
#         print"+++++++++++"
#         print "Child"
#         print eachele.name
#         print"+++++++++++"
#     print "--------------------"



print "Finished constructing the tree"

""" Class for the Main App """
class Application(tk.Frame):
    def __init__(self, master = None):
        tk.Frame.__init__(self,master=None)
        self.grid()       
        self.master.minsize(width=200,height=100)   
        self.master.bind("<Key>", self.show)
        self.filename = "" 
        self.height = 0
        self.width =  0    
        self.listele = ()
        self.createWidjet()
       
              

    def populate(self):
       #create elements and populate array
       """RootElems contains the root level elements """
       templist = list(self.listele)
       for eachelem in RootElems:
           if eachelem.name not in templist:
               templist.append(eachelem.name)
       self.listele = tuple(templist)

       menu = self.parentList["menu"]        
       menu.delete(0, "end")
       for value  in self.listele:
            menu.add_command(label = value , command=lambda v=value:self.varele.set(v))
            
       
    
    def quitFunc(self):
        sys.exit()
    
    """ Called after the root level elems are made """
    """ Creates all the children elems of the root elem in a loop"""
    def done(self):
        #create a collection of children nodes
        childnodes = []
        for nodes in RootElems:
            if nodes.name != "Root":
                for eachChild in nodes.children:
                    childnodes.append(eachChild)
        
        print childnodes
        ###  Get Picture for each child Node ####
        for eachchild in childnodes:
            ## Get Parent
            parentelem  = eachchild.parent.name 
            print "parent Name"+parentelem           
            testpos =  pyautogui.locateOnScreen(str("./OracleElements/"+parentelem+".png"))
            print "position"+str(testpos)
            posx, posy = pyautogui.center(testpos)
            pyautogui.click(posx, posy)
            childNum =  (eachchild.parent.children).index(eachchild)
            print "childNum"+str(childNum)
            if childNum == 0:
                childNum = 1
            numOff = childNum*childOffsetX        
            ### Move mouse by childNum times current position
            newPosX = posx + int((childOffsetX)*childNum)
            ### Take Screen Shot With Name ###
            im=pyautogui.screenshot(region=(posx - 30, posy + numOff, 50, 20))
            im.save("./OracleElements/"+eachchild.name+".png")



    def setValue(self):
        self.filename = self.varele.get()   
        self.stausLabel.config(text="Option chosen as"+ self.filename)



    """ UI for the APP """    
    def createWidjet(self):
        self.populate = tk.Button(self, text = "Populate", command = self.populate)
        self.populate.grid(row = 5 , column = 5)        
        self.varele = tk.StringVar(self)
        self.varele.set("Root")
        tempval = list(self.listele)
        tempval.insert(0,"Root")
        self.listele  = tuple(tempval)
        self.parentList = tk.OptionMenu(self, self.varele , tuple(self.listele))
        self.parentList.grid(row = 5 , column = 7)
        self.quit = tk.Button(self, text = "Quit", command = self.quitFunc)
        self.quit.grid(row = "5", column = "9")

        """ Second Row Buttons """
        self.Done =  tk.Button(self, text="Done", command = self.done)
        self.Done.grid(row = 7 , column = 5)
        """ Second Row Buttons """
        self.SetValue =  tk.Button(self, text="SetValue", command = self.setValue)
        self.SetValue.grid(row = 7 , column = 9)
        self.stausLabel =  tk.Label(self, text="Status")
        self.stausLabel.grid(row = 9 , column = 5)







    def show(self, event):         
        # if(event.keysym == "Return"):
        #     self.master.iconify()              

         if(event.keysym == "space"):              
            #Get mouse position 
            currentMouseX, currentMouseY = pyautogui.position()
            print(currentMouseX)
            print(currentMouseY)
            print "Done!!"
            offsetx=6
            offsety=6            
            #button Click 
            
            im=pyautogui.screenshot(region=(currentMouseX-offsetx, currentMouseY-offsety, 50, 20))

            print self.filename
            if(self.filename != ""):
                 im.save(os.path.join("./OracleElements", self.filename+".png"))
            else:
                self.stausLabel.config(text = "Please enter the component name in the input box" )            
           
            #DONE
            self.stausLabel.config(text="DONE")            
            #pyautogui.click()
            


    
       

app =  Application()
app.master.title('Oracle Database creator')
app.mainloop()

client.close()
