import bpy
#for debugging, disable in build
# fixgeoandmat = bpy.data.texts["Exporttogltfcustom.py"].as_module() 

#for build, disable during debugging
from . import fixgeoandmat

#for debugging, disable in build
# prepareforbaking = bpy.data.texts["prepareforbakings.py"].as_module() 

#for build, disable during debugging
from . import prepareforbaking

import textwrap
 
def rowlabelmultiline(context, text, parent):
    '''Creates row labels in panel depending on width of panel
    effectively giving multiline text with wrap'''
    chars = int(context.region.width / 7)   # 7 pix on 1 character
    wrapper = textwrap.TextWrapper(width=chars)
    text_lines = wrapper.wrap(text=text)
    for text_line in text_lines:
        row = parent.row()
        row.label(text=text_line)


class TOOLS_OT_FixGeoAndMatOperator(bpy.types.Operator):
    '''Makes a copy of the object and changes the geo nodes and mats of copy to keep looks identical\
while supporting instance realisation'''
    bl_idname = 'gne.fixgeoandmat'
    bl_label = 'Fix Geo Nodes and Materials'
    bl_options = {"REGISTER", "UNDO"}
    
    def execute(self, context):

        fixgeoandmat.main()
            
        return {'FINISHED'}

class TOOLS_PT_GeoNodesExport(bpy.types.Panel):
    '''draws a panel in n-panel for fixing geo and mats'''
    
    bl_label = "Fix Geometry Node Tree"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Geo Nodes Export'
    
    def draw(self,context):
        col = self.layout.column()
        text="Step 1) Select the object you want to export and click the button below. Make sure there are no nodegroups in your geometry node tree, if there are, ungroup all of them"

        rowlabelmultiline(context=context,text=text,parent=col)

        col.operator(TOOLS_OT_FixGeoAndMatOperator.bl_idname\
        , text=TOOLS_OT_FixGeoAndMatOperator.bl_label)
        
PROPS = [
    ('image_name', bpy.props.StringProperty(name='Image Name', default='new_image')),
    ('bakedimageheight', bpy.props.IntProperty(name='Image Height(px)', default=512)),
    ('bakedimagewidth', bpy.props.IntProperty(name='Image Width(px)', default=512)),
    ('alpha', bpy.props.BoolProperty(name='Alpha', default=True)),
    
]
       
class TOOLS_OT_PrepareForBakingOperator(bpy.types.Operator):
    '''Makes a new image, adds this image as image texture to all linked materials and selects them.\
UV unwraps(smart uv project) the mesh'''
    bl_idname = 'gne.prepareforbaking'
    bl_label = 'Prepare For Baking'
    bl_options = {"REGISTER", "UNDO"}
    
    def execute(self, context):

        prepareforbaking.main(context.scene.image_name,context.scene.bakedimageheight\
        ,context.scene.bakedimagewidth,context.scene.alpha)
            
        return {'FINISHED'}

class TOOLS_PT_PrepareForBaking(bpy.types.Panel):
    '''draws a panel in n-panel'''
    
    bl_label = "Prepare For Baking"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Geo Nodes Export'
    
    def draw(self,context):
        col = self.layout.column()
        
        text="Step 2) The above step created a copy of the selected object, select this copied object, choose your settings and click the button below (will create a new image).Make sure you are using generated coordinates if you are using texture coordinates. If you are using object coordinates, you can convert generated to object by subtracting 0.5 and then multiplying by 2 (if object's origin is in center)"

        rowlabelmultiline(context=context,text=text,parent=col)
        
        for (prop_name, _) in PROPS:
            row = col.row()
            row.prop(context.scene, prop_name)
            
        col.operator(TOOLS_OT_PrepareForBakingOperator.bl_idname\
        , text=TOOLS_OT_PrepareForBakingOperator.bl_label)

        text="Step 3) (Manual Step, Depends on use case) Modify the shaders according to your needs on the copied object (if needed). Change your render engine to cycles, scroll down, choose your settings, then hit bake. Connect the image textures(newly created and set to active) in every material linked to the copied object, to the appropriate color/normal/emit/etc channel and then do export"

        rowlabelmultiline(context=context,text=text,parent=col)
        
CLASSES = [
    TOOLS_OT_FixGeoAndMatOperator,TOOLS_PT_GeoNodesExport,TOOLS_OT_PrepareForBakingOperator,
     TOOLS_PT_PrepareForBaking
]
