import bpy
import inspect

def spacing(nooflines,noofcharacters=100):
    for i in range(nooflines):
        print("-"*noofcharacters);
        
def printattr(obj): #prints names of attributes of an object
    for i in dir(obj):
        print(i)

def printattr2(obj): #prints name-value pairs of attributes of an object
    for i in inspect.getmembers(obj):
        print(i)

def getmaterials(object,geometrynodesmodifier):
    #returns all the materials linked to this object in a list
    
    materials = []
    #get the nodes of this node group
    nodes = geometrynodesmodifier.node_group
    
    #case 1: material is set using set material node
    found = False
    for node in nodes.nodes:
        if node.bl_idname == "GeometryNodeSetMaterial":
            found = True
            
            #add the material to the list
            materials.append(node.inputs[2].default_value)
            
            
    #case 2: material is set by active material
    if not found:
        
        #copy the material
        materials.append(object.active_material)
    
    return materials
              
def main(image_name="new_image",bakedimagewidth=512,bakedimageheight=512,alpha=True):

    ctx = bpy.context
    active_obj = ctx.active_object #get active object
    modifiers = active_obj.modifiers #get modifiers list of active object

    #currently assuming only one geometry nodes modifier(no stack)
    #loop through all modifiers of active object
    for index,modifier in enumerate(modifiers):
        
        #if it is a geometry node
        if modifier.type == "NODES":
            
            #apply the modifier
            try:
                modifiers.active = modifier
                bpy.ops.object.modifier_apply(modifier=modifier.name)
            except RuntimeError:
                print(f"Error applying {modifier.name} to {active_obj.name}")
                
            #create an image the bake the textures into
            image = bpy.data.images.new(image_name,bakedimagewidth,bakedimageheight,alpha=alpha)
            
            #get all the linked materials
            materials = getmaterials(active_obj,modifier)
            for material in materials:
                
                #add a new image texture node in every material
                nodes = material.node_tree
                image_node = nodes.nodes.new("ShaderNodeTexImage")
                
                #make the image texture node active and assign it the new image
                nodes.nodes.active = image_node
                image_node.image = image
        
#        lm =  active_obj.data.uv_layers.get("LightMap")
#        if not lm:
#            lm = active_obj.data.uv_layers.new(name="LightMap")
#        lm.active = True
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.select_all(action='SELECT') # for all faces
#        bpy.ops.mesh.uv_texture_add()
        bpy.ops.uv.smart_project(angle_limit=1.15192\
        , island_margin=0.01, area_weight=0.00)
#        bpy.ops.uv.lightmap_pack()
        bpy.ops.object.editmode_toggle()
                
            
                
    
if __name__ == "__main__":      
    spacing(10)
    main()
            