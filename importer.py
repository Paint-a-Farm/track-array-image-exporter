import bpy
import struct
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty
from bpy.types import Operator


class ImportTrackArray(Operator, ImportHelper):
    """Import a TrackArray Image as Bezier Curve"""
    bl_idname = "track.import_array"  # important since its how bpy.ops.import_test.some_data is constructed
    bl_label = "Import TrackArray Image"

    # ExportHelper mixin class uses this
    filepath = 'trackArray.dds'
    filename_ext = ".dds"

    filter_glob: StringProperty(
        default="*.dds",
        options={'HIDDEN'},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )

    def execute(self, context):

        with open(self.filepath, "rb") as file:
            magic = file.read(4)
            if magic != b'DDS ':
                self.report(
                    {'ERROR'}, 'Select a valid TrackArray Image to import. File is not a DDS image.')
                return{'FINISHED'}

            file.seek(12)
            height = int.from_bytes(file.read(4), 'little')
            if height != 1:
                self.report(
                    {'ERROR'}, 'Select a valid TrackArray Image to import. Invalid image found (height>1).')
                return{'FINISHED'}

            bytes = file.read(4)

            length = int.from_bytes(bytes, 'little')
            print(length)
            file.seek(140)
            bytes = file.read(4)
            arraysize = int.from_bytes(bytes, 'little')
            print('arraysize', arraysize)
            file.seek(148)

            for j in range((arraysize//2)):
                print('j', j)
                positions = list()
                rotations = list()

                for i in range(length):
                    bytes = file.read(2)
                    x = struct.unpack('e', bytes)[0]
#                    print('x',x)
                    bytes = file.read(2)
                    y = struct.unpack('e', bytes)[0]
#                    print('y',y)
                    bytes = file.read(2)
                    z = struct.unpack('e', bytes)[0]
#                    print('z',z)
                    bytes = file.read(2)
                    positions.append((x, -z, y))

                for i in range(length):
                    bytes = file.read(2)
                    w = struct.unpack('e', bytes)[0]
#                    print('x',x)
                    bytes = file.read(2)
                    z = -struct.unpack('e', bytes)[0]
#                    print('y',y)
                    bytes = file.read(2)
                    y = struct.unpack('e', bytes)[0]
#                    print('z',z)
                    bytes = file.read(2)
                    x = -struct.unpack('e', bytes)[0]
                    rotations.append((w, x, y, z))

                # create the Curve Datablock
                curveData = bpy.data.curves.new('curve', type='CURVE')
                curveData.dimensions = '3D'
                curveData.resolution_u = 2

                # map coords to spline
                polyline = curveData.splines.new('BEZIER')
                print(len(positions))
                polyline.bezier_points.add(len(positions)-1)

                for i, position in enumerate(positions):
                    #polyline.bezier_points[i].co = (x, y, z, 1)
                    polyline.bezier_points[i].co = position
                    polyline.bezier_points[i].handle_left = position
                    polyline.bezier_points[i].handle_right = position
                    polyline.bezier_points[i].handle_right_type = 'AUTO'
                    polyline.bezier_points[i].handle_left_type = 'AUTO'

                polyline.use_cyclic_u = True

                # create Object
                curveOB = bpy.data.objects.new('curve', curveData)

                # attach to scene and validate context
                bpy.context.collection.objects.link(curveOB)

        return{'FINISHED'}
