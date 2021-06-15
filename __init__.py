if "bpy" in locals():
    import importlib
    importlib.reload(exporter)
    importlib.reload(importer)
else:
    from . import exporter
    from . import importer

import bpy

bl_info = {
    "name": "TrackArray Image Importer/Exporter for Farming Simulator 19",
    "description": "Import and Exports TrackArray Images for use with 3D tracks in Farming Simulator 19",
    "blender": (2, 80, 0),
    "category": "Import-Export",
    "author": "Paint-a-Farm | Kim Brandwijk",
    "version": (1,0),
    "location": "File > Import/Export > TrackArray Image (.dds)"
}

def menu_func_export(self, context):
    self.layout.operator(exporter.ExportTrackArray.bl_idname, text="TrackArray Image (.dds)")

def menu_func_import(self, context):
    self.layout.operator(importer.ImportTrackArray.bl_idname, text="TrackArray Image (.dds)")

def register():
    bpy.utils.register_class(exporter.ExportTrackArray)
    bpy.utils.register_class(importer.ImportTrackArray)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)

def unregister():
    bpy.utils.unregister_class(exporter.ExportTrackArray)
    bpy.utils.unregister_class(importer.ImportTrackArray)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_import)

if __name__ == "__main__":
    register()