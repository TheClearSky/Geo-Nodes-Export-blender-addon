import inspect
import bpy
import os

#for debugging, disable in build
nodeutils = bpy.data.texts["nodegrouputilities.py"].as_module() 

#for build, disable during debugging
#import nodegrouputilities as nodeutils
def requirednodecheck():
    #if already not imported
    try:
        print("finding Realise instances custom node")
        bpy.data.node_groups["Realise instances custom"]
    except KeyError:
        #import it
        print("Not found:Importing it")
        
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
        print("Found")
    

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
    
    #get the nodes of this node group
    nodes = geometrynodesmodifier.node_group
    
    output_node = None
    #loop through all nodes and store the output node if found
    for node in nodes.nodes:
        if node.bl_idname == "NodeGroupOutput":
            output_node = node
            
    if not output_node:
        #if output node wasn't found, raise an exception
        raise ValueError("There's no output node in geonodes")
        


    nodedict = {}
    
    #constructing a dictionary data structure that maps a node to the previous nodes connecting it
    #it also has a "visited" bool to keep track in breadth first search later
    #
    # nodedict--+
    #           |---node
    #           +--+
    #              |---"visited" (bool)
    #              |---"links" (array of link)
    
    for link in nodes.links:
        if link.to_node not in nodedict:
            nodedict[link.to_node]={"visited":False,"links":[link]}
        else:
            nodedict[link.to_node]["links"].append(link)
            
    #breadth first search starting from output node
    queue = [output_node]
    nodedict[output_node]["visited"]=True
    
    #to keep track of path, key-node,value-parentnode
    path = {}
    
    visited_first_join_geometry = False
    visited_first_instance_on_points = False
    
    #array(list) of pairs(tuple) of left and right nodes to add nodes between
    nodes_to_add_between = []
    
    while queue:
        
        queue_front = queue.pop(0)
        
        if queue_front.bl_idname == "GeometryNodeJoinGeometry":
            
            visited_first_join_geometry = True

            #adding all the branches to adding realise instances custom node
            for link in nodedict[queue_front]["links"]:
                nodes_to_add_between.append((link.from_node,queue_front))
            
            #tracing path
            current_node = queue_front
            prev_node = None
            
            #trace until output node
            while current_node!=output_node:
                prev_node = current_node
                current_node = path[current_node]
                
                #if another join geometry found, 
                #no realise instance needed on this branch separately
                if current_node.bl_idname == "GeometryNodeJoinGeometry":
                    try:
                        nodes_to_add_between.remove((prev_node,current_node))
                    except ValueError:
                        #this branch was already taken care of by another join geometry in front
                        pass
            
            
            
            
        if (not (visited_first_join_geometry or visited_first_instance_on_points))\
        and (queue_front.bl_idname == "GeometryNodeInstanceOnPoints"):
            
            visited_first_instance_on_points = True
            
            node_to_add = nodes.nodes.new("GeometryNodeRealizeInstances")
            #tracing path
            current_node = queue_front
            prev_node = None
            while current_node!=output_node:
                prev_node = current_node
                current_node = path[current_node]
                
            nodeutils.addnodebetweenconnected(nodes,prev_node,node_to_add,current_node)
                
#        print("Queue front\t\t",queue_front)
        
        for link in nodedict[queue_front]["links"]:
            try:
                if not nodedict[link.from_node]["visited"]:
                    queue.append(link.from_node)
                    nodedict[link.from_node]["visited"]=True
                    path[link.from_node] = queue_front
            except KeyError:
                queue.append(link.from_node)
                path[link.from_node] = queue_front
                nodedict[link.from_node]={"visited":True,"links":[]}
                #reached a node that has no further incoming connections
                
    #finally adding nodes in all required places and storing them
    realise_nodes_to_add = []
    for pair in nodes_to_add_between:
        
        node_to_add = nodes.nodes.new("GeometryNodeGroup")
        node_to_add.node_tree = bpy.data.node_groups["Realise instances custom"]
#        printattr2(node_to_add)
        nodeutils.addnodebetweenconnected(nodes,pair[0],node_to_add,pair[1])
        realise_nodes_to_add.append(node_to_add)
    
    noofrealisenodes = len(realise_nodes_to_add)
    node1index = 0
    node2index = 0
    while len(realise_nodes_to_add) > 1:
        
        if realise_nodes_to_add[0].bl_idname == "GeometryNodeGroup":
            node1index = 1
        else:
            node1index = 0
            
        if realise_nodes_to_add[1].bl_idname == "GeometryNodeGroup":
            node2index = 1
        else:
            node2index = 0
    
        new_node = nodeutils.sum2vectornodesockets(nodes,realise_nodes_to_add[0]\
        ,realise_nodes_to_add[1],node1index,node2index)
        realise_nodes_to_add.pop(0)
        realise_nodes_to_add.pop(0)
        realise_nodes_to_add.append(new_node)
        
    if realise_nodes_to_add:
        
        #make a new output vector attribute to store the new co-ordinates
        texturefix = nodes.outputs.new("NodeSocketVector","texturefix") 
        
        for index,socket in enumerate(output_node.inputs):
            if socket.identifier == texturefix.identifier:
                texturefix = socket
                break
        
        if realise_nodes_to_add[0].bl_idname == "GeometryNodeGroup":
            nodes.links.new(texturefix,realise_nodes_to_add[0].outputs[1])
        else:
            nodes.links.new(texturefix,realise_nodes_to_add[0].outputs[0])
        
        subtract_node = nodes.nodes.new("ShaderNodeVectorMath")
        subtract_node.operation="SUBTRACT"
        nodeutils.addnodebetweenconnected(nodes,realise_nodes_to_add[0],subtract_node,output_node)
        vector_node = nodes.nodes.new("FunctionNodeInputVector")
        vector_node.vector.x=0.5*(noofrealisenodes-1)
        vector_node.vector.y=vector_node.vector.x
        vector_node.vector.z=vector_node.vector.x
        
        nodeutils.connectnodes(nodes,vector_node,subtract_node,0,1)
        vector_node.location=nodeutils.calculateabsolutelocation(subtract_node)
        vector_node.location.x-=500
        vector_node.location.y-=200
        texturefix_identifier_index = int(texturefix.identifier[7:])
        geometrynodesmodifier[f"Output_{texturefix_identifier_index}_attribute_name"]= "texturefix"

def fixmaterial(material):
    
    nodes = material.node_tree
    for node in nodes.nodes:
        if node.bl_idname=="ShaderNodeTexCoord":
            attr_node = nodes.nodes.new("ShaderNodeAttribute")
            attr_node.location = node.location
            attr_node.attribute_name = "texturefix"
            links = node.outputs[0].links
            for link in links:
                nodes.links.new(attr_node.outputs[1],link.to_socket)

def fixmaterials(object,geometrynodesmodifier):
    
    #get the nodes of this node group
    nodes = geometrynodesmodifier.node_group
    
    #case 1: material is set using set material node
    found = False
    for node in nodes.nodes:
        if node.bl_idname == "GeometryNodeSetMaterial":
            found = True
            
            #copy the material
            material = node.inputs[2].default_value.copy()
            node.inputs[2].default_value=material
            
            fixmaterial(material)
            
    #case 2: material is set by active material
    if not found:
        
        #copy the material
        material = object.active_material.copy()
        object.active_material = material
        
        fixmaterial(material)
            
        
def main():
    
    requirednodecheck()
    
    ctx = bpy.context
    active_obj = ctx.active_object #get active object
    modifiers = active_obj.modifiers #get modifiers list of active object

    #currently assuming only one geometry nodes modifier(no stack)
    #loop through all modifiers of active object
    for index,modifier in enumerate(modifiers):
        
        #if it is a geometry node
        if modifier.type == "NODES":
#            print("got it")
            
            #create a copy of the object,data and animation data
            #still need to copy materials and geo nodes later
            copied_obj=duplicate(active_obj)

            #get geometry nodes modifier of copied object
            copied_modifier = copied_obj.modifiers[index]
            
            #duplicate the nodetree
            new_node_tree = copied_modifier.node_group.copy()
            #add the new nodetree to the copied modifier
            copied_modifier.node_group = new_node_tree
            
            #fix the modifier
            fixgeometrynodes(copied_modifier) #for debugging, change to copied_modifier in final build
            fixmaterials(copied_obj,copied_modifier)
            break
#        else:
#            print("didn't get")
            
           
if __name__ == "__main__":   
    spacing(10)
#    print("start")
    main()