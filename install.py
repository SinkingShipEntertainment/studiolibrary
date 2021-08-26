# Copyright 2017 by Kurt Rathjen. All Rights Reserved.
#
# This library is free software: you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation, either
# version 3 of the License, or (at your option) any later version.
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
# You should have received a copy of the GNU Lesser General Public
# License along with this library. If not, see <http://www.gnu.org/licenses/>.
"""
Drag and drop for Maya 2018+
"""
import os
import sys

try:
    import maya.mel
    import maya.cmds
    isMaya = True
except ImportError:
    isMaya = False

def onMayaDroppedPythonFile(*args, **kwargs):
    """This function is only supported since Maya 2017 Update 3"""
    pass

def remove_library_shelf_tool(parent_shelf):
    '''
    Removes the Duplicate Shelf Tool if there is
    '''
    all_shelf_buttons = maya.cmds.shelfLayout(parent_shelf, query=True, childArray=True)

    labels = [maya.cmds.shelfButton(button_name, query=True, label=True) for button_name in all_shelf_buttons if 'separator' not in button_name]
    library_count = labels.count('Studio Library')
    #print("Libraries = %s" % library_count)

    if library_count <= 1:
        return

    for button_name in all_shelf_buttons:
        # --------------------------------------------------------
        #Shelfs may have separators and these aren't buttons
        #and will be an error asked to be one
        # --------------------------------------------------------

        if 'separator' not in button_name:
            label = maya.cmds.shelfButton(button_name, query=True, label=True)
            if label == 'Studio Library':
                maya.cmds.deleteUI(button_name)
                break


def sse_studio_library():
    # -----------------------------------
    # Studio Library
    # www.studiolibrary.com
    #
    # Sinking Ship Database Paths
    # -----------------------------------

    import os
    import sys

    # SSE Imports
    from asset_manager.api import am

    srcPath = os.path.join(os.path.dirname(__file__), 'src')

    if not os.path.exists(srcPath):
        raise IOError(r'The source path %s does not exist!' % srcPath)

    if srcPath not in sys.path:
        sys.path.insert(0, srcPath)

    import studiolibrary

    # TODO: Make sure that the folder location is created if its not there
    shared_path = am.get_animation_library_shared_root()

    # List of paths that users will have access to.
    # These paths will be based on the project

    libraries = [
    {"name":"Shared", "path":shared_path, "default":True, "theme":{"accentColor":"rgb(128,128,0)"}},
    ]

    studiolibrary.setLibraries(libraries)
    studiolibrary.main()

def _onMayaDropped():
    """Dragging and dropping this file into the scene executes the file."""

    srcPath = os.path.join(os.path.dirname(__file__), 'src')
    iconPath = os.path.join(srcPath, 'studiolibrary', 'resource', 'icons', 'icon.png')

    srcPath = os.path.normpath(srcPath)
    iconPath = os.path.normpath(iconPath)

    if not os.path.exists(iconPath):
        raise IOError('Cannot find ' + iconPath)

    for path in sys.path:
        if os.path.exists(path + '/studiolibrary/__init__.py'):
            maya.cmds.warning('Studio Library is already installed at ' + path)

    shelf = maya.mel.eval('$gShelfTopLevel=$gShelfTopLevel')
    parent = maya.cmds.tabLayout(shelf, query=True, selectTab=True)

    maya.cmds.shelfButton(
        command=sse_studio_library,
        annotation='Studio Library',
        sourceType='python',
        label="Studio Library",
        image=iconPath,
        image1=iconPath,
        parent=parent
    )

    remove_library_shelf_tool(parent)

if isMaya:
    _onMayaDropped()
