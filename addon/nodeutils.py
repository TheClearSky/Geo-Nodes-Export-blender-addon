import bpy
import copy

def midpoint(vec1,vec2):
    #returns midpoint of 2 vectors,as a new vector
    return vec1 + ((vec2-vec1)/2)

def calculateabsolutelocation(node):
    #calculates the absolute location relative to world frame
    location = copy.deepcopy(node.location)
    while node.parent:
        node = node.parent
        location += node.location
    return location

def midpointofnodes(node1,node2):
    #returns midpoint of 2 nodes,as a new vector
#    return midpoint(node1.location,node2.location)
    return midpoint(calculateabsolutelocation(node1),calculateabsolutelocation(node2))
    
def sum2vectornodesockets(node_group,node1,node2,node1_output_index,node2_output_index):
    
    if node1_output_index >= len(node1.outputs):
        raise IndexError("node1_output_index is out of range of node1's outputs")
        
    if node2_output_index >= len(node2.outputs):
        raise IndexError("node2_output_index is out of range of node2's outputs")
    
    if node1.outputs[node1_output_index].bl_idname != "NodeSocketVector":
        raise TypeError("nodesocket of node1 isn't of type vector")
    
    if node2.outputs[node2_output_index].bl_idname != "NodeSocketVector":
        raise TypeError("nodesocket of node2 isn't of type vector")
    
    #create a new Vector Math in ADD mode
    node_to_add = node_group.nodes.new("ShaderNodeVectorMath")
    node_to_add.operation="ADD"

    #connect the correspomding sockets
    connectnodes(node_group,node1,node_to_add,node1_output_index,0)
    connectnodes(node_group,node2,node_to_add,node2_output_index,1)
    
    #change the location to a twice ahead(x) of the centre of 2 nodes 
    node_to_add.location = midpointofnodes(node1,node2)
    node_to_add.location.x += abs(node1.location.x-node2.location.x)
    return node_to_add

    
    
def addnodebetweenconnected(node_group,left_node,node_to_add,right_node):
#def addnodebetweenconnected(node_group,left_node,right_node):
    '''
    adds a node between 2 connected nodes, 
    the first (lowest index left_node) connection between the left and right 
    node is broken and replaced by first compatible input and output node of the new node
    returns true if it was succesful
    returns false and reverts back the changes to before calling the function if it failed
    '''

    #keeps track of lowest index of left node outputs connected to right node
    lowest_index = len(left_node.outputs)
    lowest_index_link = None
    
    #check all links in node group
    for link in node_group.links:
        
        #if a connection found between left and right node
        if(link.from_node == left_node) and(link.to_node == right_node):
                
            #loop through all outputs in left node until previous topmost found
            for j in range(lowest_index):
                
                #if another link was found, it must be the new topmost
                if link.from_socket == left_node.outputs[j]:
                    
                    #update the lowest index and link to new topmost
                    lowest_index = j
                    lowest_index_link = link
                    
    #found a connection
    if lowest_index < len(left_node.outputs):
        # print("found a connection")
        connection_type = link.from_socket.type
        new_node_input_index = -1
        new_node_output_index = -1
        found = False
        
        #finding same data type in new node's inputs
        for i,socket in enumerate(node_to_add.inputs):
            if socket.type == connection_type:
                found = True
                new_node_input_index = i
                break
            
        if not found:
            #couldn't find, connection not possible
            print("suitable new node input not found- Datatype mismatch")
            return False
        
        found = False
        
        #finding same data type in new node's outputs
        for i,socket in enumerate(node_to_add.outputs):
            if socket.type == connection_type:
                found = True
                new_node_output_index = i
                break
            
        if not found:
            #couldn't find, connection not possible
            print("suitable new node output not found- Datatype mismatch")
            return False
        
        right_node_input_index = -1
        #finding the index of existing connection in right node's inputs
        for i,socket in enumerate(right_node.inputs):
            
            if lowest_index_link.to_socket == socket:
                right_node_input_index = i
                break
        #no need to check if we found, because a connection was already found earlier
        
        #cut the already existing link
        node_group.links.remove(lowest_index_link)  
        
        #add the new links 
        addnodebetween(node_group,left_node,node_to_add,right_node,lowest_index\
        ,new_node_input_index,new_node_output_index,right_node_input_index)
        
        #change the new link's location to between(midpoint) the left and right link
        node_to_add.location = midpointofnodes(left_node,right_node)
        return True
    
    #no connection found  
    else:
        # print("no connections found")
        return False
    

def addnodebetween(node_group,left_node,node_to_add,right_node,left_node_output_indices\
    ,new_node_input_indices,new_node_output_indices,right_node_input_indices):
    '''
    Adds a node(node to add) between 2 nodes,left_node and right_node
    indices to connect can be defined in 2 ways, either as a list(for multiple links)
    and as a single number. Left connections(from left node to new node) and 
    right connections(from new node to right node) can both be separately
    given as any combination of list or int
    '''
    
    connectnodes(node_group,left_node,node_to_add,left_node_output_indices\
    ,new_node_input_indices)
    connectnodes(node_group,node_to_add,right_node,new_node_output_indices\
    ,right_node_input_indices)
        
    #change the new link's location to between(midpoint) the left and right link
    node_to_add.location = midpointofnodes(left_node,right_node)
     
def connectnodes(node_group,left_node,right_node,left_node_output_indices,right_node_input_indices):
    
    if isinstance(left_node_output_indices,list): #if many links
        
        #link all of them
        for left_out,right_in in zip(left_node_output_indices,right_node_input_indices):
            node_group.links.new(right_node.inputs[right_in],left_node.outputs[left_out])
            
    else:#if single link
        
        #link it
        node_group.links.new(right_node.inputs[right_node_input_indices],\
        left_node.outputs[left_node_output_indices])