import bpy
from . import panel_ui
from . import nodeutils
from . import fixgeoandmat
from . import prepareforbaking
#import bpy and every other addon file

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

#data about this addon
bl_info = {
    "name" : "Geo Nodes Export",
    "author" : "Deepak Prasad",
    "description" : "An addon to convert geonodes to export friendly format using texture baking",
    "blender" : (3, 1, 0),
    "version" : (1, 0, 0),
    "location" : "3D View > N-Panel > Geo Nodes Export",
    "warning" : "",
    "category" : "Import Export"
}

#register and unregister all classes and pros(they are imported from panel_ui.py)
def register():
    print(f'Enabled {bl_info["name"]}')
    
    for (prop_name, prop_value) in panel_ui.PROPS:
        setattr(bpy.types.Scene, prop_name, prop_value)
        
    for klass in panel_ui.CLASSES:
        bpy.utils.register_class(klass)

def unregister():
    print(f'Disabled {bl_info["name"]}') 
    
    for (prop_name, _) in panel_ui.PROPS:
        delattr(bpy.types.Scene, prop_name)
        
    for klass in reversed(panel_ui.CLASSES):
        bpy.utils.unregister_class(klass)

