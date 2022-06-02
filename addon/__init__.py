from panel_ui import *
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

bl_info = {
    "name" : "Geo Nodes Export",
    "author" : "Deepak Prasad",
    "description" : "An addon to convert geonodes to export friendly format using texture baking",
    "blender" : (3, 1, 0),
    "version" : (1, 0, 0),
    "location" : "3D View > N-Panel > Geo Nodes Export",
    "warning" : "",
    "category" : "Geometry Nodes"
}

def register():
    print('registered') # just for debug
    
    for (prop_name, prop_value) in PROPS:
        setattr(bpy.types.Scene, prop_name, prop_value)
        
    for klass in CLASSES:
        bpy.utils.register_class(klass)

def unregister():
    print('unregistered') # just for debug
    
    for (prop_name, _) in PROPS:
        delattr(bpy.types.Scene, prop_name)
        
    for klass in reversed(CLASSES):
        bpy.utils.unregister_class(klass)

