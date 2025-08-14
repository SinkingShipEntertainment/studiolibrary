"""userSetup for Studio Library."""

# SSE Imports
from asset_manager.api import am
import studiolibrary

# Set a shared project library everyone can view and modify.
shared_path = am.get_animation_library_shared_root()
libraries = [{"name":"Shared", "path":shared_path, "default":True}]
studiolibrary.setLibraries(libraries)
