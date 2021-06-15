import bpy
import struct
from bpy_extras.io_utils import ExportHelper
from bpy.props import StringProperty
from bpy.types import Operator


class ExportTrackArray(Operator, ExportHelper):
    """Export a track armature as FS19 TrackArray Image"""
    bl_idname = "track.export_array"  # important since its how bpy.ops.import_test.some_data is constructed
    bl_label = "Export TrackArray Image"

    # ExportHelper mixin class uses this
    filepath = 'trackArray.dds'
    filename_ext = ".dds"

    filter_glob: StringProperty(
        default="*.dds",
        options={'HIDDEN'},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )

    def invoke(self, context, event):
        if bpy.context.active_object is None or bpy.context.active_object.type != 'ARMATURE':
            self.report(
                {'ERROR'}, 'Select the track ARMATURE to export the TrackArray Image')
            return{'FINISHED'}

        self.filepath = "trackArray.dds"
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def execute(self, context):

        armature = context.active_object
        pose_bones = armature.pose.bones

        width = pose_bones[-1].constraints["Spline IK"].chain_count

        positions = list()
        rotations = list()

        for pose_bone in pose_bones:
            bone_head_location = (armature.location + pose_bone.head)
            rotation_quat = (pose_bone.matrix).to_quaternion()

            positions += [(bone_head_location[0], bone_head_location[2], -bone_head_location[1], 1.0)]
            rotations += [(rotation_quat.w, -rotation_quat.z, rotation_quat.y, -rotation_quat.x)]

        positions = positions[-width:]
        rotations = rotations[-width:]

        hex_as_bytes = b"\x44\x44\x53\x20\x7C\x00\x00\x00\x0F\x10\x02\x00\x01\x00\x00\x00"
        length = width.to_bytes(4, byteorder="little")
        size = (width * 8).to_bytes(4, byteorder="little")
        rest_of_header = b"\x00\x00\x00\x00\x01\x00\x00\x00\xD9\xE8\x8A\x28\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x20\x00\x00\x00\x04\x00\x00\x00\x44\x58\x31\x30\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08\x10\x40\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0A\x00\x00\x00\x03\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00"

        posflattened = [element for tupl in positions for element in tupl]
        posbytes = struct.pack('%se' % len(posflattened), *posflattened)
        rotflattened = [element for tupl in rotations for element in tupl]
        rotbytes = struct.pack('%se' % len(rotflattened), *rotflattened)

        with open(self.filepath, "wb") as f:
            f.write(hex_as_bytes)
            f.write(length)
            f.write(size)
            f.write(rest_of_header)
            f.write(posbytes)
            f.write(rotbytes)

        return{'FINISHED'}
