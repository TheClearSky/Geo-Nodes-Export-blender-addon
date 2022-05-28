import inspect
import bpy

def spacing(nooflines,noofcharacters=100):
    for i in range(nooflines):
        print("-"*noofcharacters);
        
def printattr(obj): #prints names of attributes of an object
    for i in dir(obj):
        print(i)

def printattr2(obj): #prints name-value pairs of attributes of an object
    for i in inspect.getmembers(obj):
        print(i)

def fixgeometrynodes(geometrymodifier):
    nodes = geometrymodifier.node_group
    spacing(2)
    printattr2(nodes)
    spacing(2)
    printattr2(nodes.nodes[0])
        
def main():
    ctx = bpy.context
    active_obj = ctx.active_object #get active object
    modifiers = active_obj.modifiers #get modifiers list of active object

    printattr2(modifiers[0])
    #currently assuming only one geometry nodes modifier(no stack)
    #loop through all modifiers of active object
    for modifier in modifiers:
        
        #if it is a geometry node
        if modifier.type == "NODES":
            print("got it")
            fixgeometrynodes(modifier)
            break
        else:
            print("didn't get")

  