import Exporttogltfcustom
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
    "name" : "geoexportfriendly",
    "author" : "Deepak Prasad",
    "description" : "An addon to convert geonodes to export friendly format using texture baking",
    "blender" : (3, 1, 2),
    "version" : (1, 0, 0),
    "location" : "",
    "warning" : "",
    "category" : "Generic"
}

def register():
    Exporttogltfcustom.main()

def unregister():
    pass
