import bpy
#for debugging, disable in build
# fixgeoandmat = bpy.data.texts["Exporttogltfcustom.py"].as_module() 

#for build, disable during debugging
import fixgeoandmat

#for debugging, disable in build
# prepareforbaking = bpy.data.texts["prepareforbakings.py"].as_module() 

#for build, disable during debugging
import prepareforbaking

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
    '''draws a panel in n-panel'''
    
    bl_label = "Fix Geometry Node Tree"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Geo Nodes Export'
    
    def draw(self,context):
        col = self.layout.column()
        col.operator(TOOLS_OT_FixGeoAndMatOperator.bl_idname\
        , text=TOOLS_OT_FixGeoAndMatOperator.bl_label)
        
PROPS = [
    ('image_name', bpy.props.StringProperty(name='Image Name', default='new_image')),
#    ('suffix', bpy.props.StringProperty(name='Suffix', default='Suff')),
#    ('add_version', bpy.props.BoolProperty(name='Add Version', default=False)),
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
    
    bl_label = "Fix Geometry Node Tree"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Geo Nodes Export'
    
    def draw(self,context):
        col = self.layout.column()
        for (prop_name, _) in PROPS:
            row = col.row()
            row.prop(context.scene, prop_name)
            
        col.operator(TOOLS_OT_PrepareForBakingOperator.bl_idname\
        , text=TOOLS_OT_PrepareForBakingOperator.bl_label)
        
CLASSES = [
    TOOLS_OT_FixGeoAndMatOperator,TOOLS_PT_GeoNodesExport,TOOLS_OT_PrepareForBakingOperator,
     TOOLS_PT_PrepareForBaking
]
