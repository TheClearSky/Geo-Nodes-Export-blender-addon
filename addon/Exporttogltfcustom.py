import inspect
import bpy
import os

#for debugging, disable in build
nodetree = bpy.data.texts["nodetree.py"].as_module() 

#for build, disable during debugging
#import nodetree

#if already not imported
try:
    print("trying")
    bpy.data.node_groups["Realise instances custom"]
except KeyError:
    print("KeyError")
    
    # blend file name
#    file_path =  os.path.abspath("needednodes.blend")   #for final build
    file_path = "D:\\blender and game assets\\blender files\\2022 made files"\
    +"\\addon\\needednodes.blend" #for debug build
    inner_path = "NodeTree"   # type 
    object_name = "Realise instances custom" # name

    bpy.ops.wm.append(
        filepath=os.path.join(file_path, inner_path, object_name),
        directory=os.path.join(file_path, inner_path),
        filename=object_name
        )
else:
    print("no error")
    

def spacing(nooflines,noofcharacters=100):
    for i in range(nooflines):
        print("-"*noofcharacters);
        
def printattr(obj): #prints names of attributes of an object
    for i in dir(obj):
        print(i)

def printattr2(obj): #prints name-value pairs of attributes of an object
    for i in inspect.getmembers(obj):
        print(i)

def duplicate(obj, data=True, actions=True, collection=None): 
    #copies an object with data, animation data and places it in the active collection 
    obj_copy = obj.copy()
    if data:
        obj_copy.data = obj_copy.data.copy()
    if actions and obj_copy.animation_data:
        obj_copy.animation_data.action = obj_copy.animation_data.action.copy()

    bpy.context.collection.objects.link(obj_copy)
    return obj_copy

def fixgeometrynodes(geometrynodesmodifier):
    nodes = geometrynodesmodifier.node_group
    for node in nodes.nodes:
        pass
        
        
def main():
    nodetree.nodetree()
    ctx = bpy.context
    active_obj = ctx.active_object #get active object
    modifiers = active_obj.modifiers #get modifiers list of active object

    #currently assuming only one geometry nodes modifier(no stack)
    #loop through all modifiers of active object
    for index,modifier in enumerate(modifiers):
        
        #if it is a geometry node
        if modifier.type == "NODES":
            print("got it")
            
            #create a copy of the object,materials and geometry nodes
#            copied_obj=duplicate(active_obj)

            #get geometry nodes modifier of copied object
#            copied_modifier = copied_obj.modifiers[index]
            #fix the modifier
            fixgeometrynodes(modifier) #for debugging, change to copied_modifier in final build
            break
        else:
            print("didn't get")
            
            
spacing(10)
print("start")
#main()
        
        

  