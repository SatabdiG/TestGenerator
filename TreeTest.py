#!/usr/bin/env python

from classes import Node, Graph


graphobj = Graph()

n1 = Node(name="test")
graphobj.addNode(n1)
n2 = Node(name="Child1", parent = n1)
graphobj.addNode(n2)
n3 = Node(name="Child2", parent = n1)
graphobj.addNode(n3)
n1.addChildren(n2)
n1.addChildren(n3)

nodes = graphobj.nodes

print "^^^^^^^^^^^^^^^^"
selectnode = graphobj.getNode("Child2")
print selectnode.name
print "^^^^^^^^^^^^^^^^"


for eachnode in nodes:
    print eachnode.name
    children = eachnode.getChildren()
    if len(children) > 0 :
        for i in children:
            print "name"
            print i.name
            print "Parent"
            print i.parent.name
            print "(((((((("

    print "___________________"