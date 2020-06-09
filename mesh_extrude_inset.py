bl_info = {
    "name": "Extrude and Inset",
    "author": "Alfonso Annarumam",
    "version": (0, 1),
    "blender": (2, 80, 0),
    "location": "View3D > Menu -> Face",
    "description": "Inset and Extrude with more option ",
    "warning": "",
    "wiki_url": "",
    "category": "Mesh",
    }


import bpy
import bmesh
from bpy.props import IntProperty, FloatProperty
from mathutils import Vector
def main(context,thickness,extrude,loop,thick_loop):
    obj = bpy.context.edit_object
    me = obj.data
    faces = []
    normals = []
    verts = []
    # Get a BMesh representation
    bm = bmesh.from_edit_mesh(me)
    for f in bm.faces:
        if f.select:
            faces.append(f)
            
    #face = bm.faces.active
        

    if thickness > 0.0:
        for tl in range(0,thick_loop+1):
            bmesh.ops.inset_region(bm, faces = faces, thickness=(thickness/(thick_loop+1)), depth=0, use_even_offset=True)
    if abs(extrude) > 0.0:
        
        #verts.append(v for f in face for v in f.verts)
        for l in range(0,loop+1):
            bmesh.ops.inset_region(bm, faces = faces, thickness=0, depth=0, use_even_offset=True)
            for f in faces:
                if f.select:
                    normals.append(f.normal)
                    for v in f.verts:
                        if v not in verts:
                            verts.append(v)
            normal = sum(normals, Vector()) / len(normals)
            
            bmesh.ops.translate(bm, verts = verts, vec = normal * (extrude/(loop+1)))
            verts = []
            #print(geom)
    # Show the updates in the viewport
    # and recalculate n-gon tessellation.
    bmesh.update_edit_mesh(me, True)


class Mesh_OT_Extrude_Inset(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "mesh.extrude_inset"
    bl_label = "Extrude and Inset"
    bl_options = {'REGISTER', 'UNDO'}
    
    
    thickness : FloatProperty(name="Inset", default=0.0)
    thick_loop : IntProperty(name="Inset Loops", default=0, min=0)
    extrude : FloatProperty(name="Extrude", default=0.0)
    loop : IntProperty(name="Extrude Loops", default=0, min=0)
    
    
    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        #print("esegui")
        main(context,self.thickness,self.extrude,self.loop,self.thick_loop)
        return {'FINISHED'}

def menu_func(self, context):
    
    layout = self.layout
    layout.operator("mesh.extrude_inset")

def register():
    bpy.utils.register_class(Mesh_OT_Extrude_Inset)
    bpy.types.VIEW3D_MT_edit_mesh_faces.append(menu_func)

def unregister():
    bpy.utils.unregister_class(Mesh_OT_Extrude_Inset)
    bpy.types.VIEW3D_MT_edit_mesh_faces.remove(menu_func)

if __name__ == "__main__":
    register()

   