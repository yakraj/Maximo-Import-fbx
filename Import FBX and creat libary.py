import os
import bpy
import glob

bl_info = {
    "name": "Import FBX to libary",
    "author": "FlyCGI",
    "version": (1, 0),
    "blender": (3, 00, 0),
    "location": "View3D > Tool Shelf > FlyCGI",
    "description": "imports fbx and creats a libary",
    "warning": "",
    "doc_url": "",
    "category": "import",
    }
    



class MyProperties(bpy.types.PropertyGroup):
    my_string : bpy.props.StringProperty(name= "ImportDirectory, copied from folder ")

def main(self, context):
    scene = context.scene
    mytool = scene.my_tool
    
    dir = mytool.my_string
    
    dirnew = dir.replace(" \ ", " / ")
    
    path_to_fbx_dir = os.path.join(dirnew)
    
    #C:/Users/xxerb/Downloads/Mixamo/Farming Pack
    #C:/Users/xxerb/Downloads/Mixamo/Basic Shooter Pack
    file_list = sorted(os.listdir(path_to_fbx_dir))

    fbx_list = [item for item in file_list if item.endswith('.fbx')]


    selectedobjects = bpy.context.selected_objects
    print(selectedobjects)



    col1 = bpy.data.collections.new(name="col1") #create new coll in data
    bpy.context.scene.collection.children.link(col1)



    #link selected objects to new scene, later back to old

    currentobj = bpy.context.object
    obj_old_coll1 = currentobj.users_collection #list of all collection the obj is in
        
    col1.objects.link(currentobj) #link obj to scene
    for ob in obj_old_coll1: #unlink from all  precedent obj collections
        ob.objects.unlink(currentobj)

    Mesh = bpy.context.view_layer.objects.active
    count = 0

    for item in fbx_list:
        path_to_file = os.path.join(path_to_fbx_dir, item)
        
        print( item )
        count+=1
        print(count)
        
        
        bpy.ops.object.select_all(action='DESELECT')
            
        #creat dublicate of mesh and rename
        Mesh.select_set(True)
        bpy.context.view_layer.objects.active = Mesh
        
        bpy.ops.object.duplicate_move()
        bpy.context.view_layer.objects.active.name = item
        MeshNew = bpy.context.view_layer.objects.active
        
        #MeshNew.parent_clear(type='CLEAR_KEEP_TRANSFORM')
        bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')
        
        bpy.ops.import_scene.fbx(filepath = path_to_file, filter_glob='*.fbx', use_anim=True, use_custom_props=True, use_custom_props_enum_as_string=True, ignore_leaf_bones=False, force_connect_children=False, automatic_bone_orientation=True,)
        
        
        
        
        activearmature = bpy.context.view_layer.objects.active
        #rename active obj
        activearmature.name = item+"armt"
        #rename anim
        bpy.data.actions["Armature.001|mixamo.com|Layer0"].name = item
        
        
        
        
        activearmature = bpy.context.object #current selected objects
        
        
        #link armatures to new collection
        
        obj_old_coll = activearmature.users_collection #list of all collection the obj is in
        
        col1.objects.link(activearmature) #link obj to scene
        
        for ob in obj_old_coll: #unlink from all  precedent obj collections
            ob.objects.unlink(activearmature)
        
        
        #select the new mesh
        MeshNew.select_set(True)
        bpy.context.view_layer.objects.active = MeshNew
        #bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
        

        
        
        bpy.context.object.modifiers["Armature"].object = bpy.data.objects[item+"armt"]


        
        activearmature.select_set(True)
        #bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
        
        bpy.context.view_layer.objects.active = activearmature
        
        bpy.ops.object.parent_set(type='OBJECT', keep_transform=True)
        
        
        #move on x 1
        bpy.ops.transform.translate(
    value=(count, 0, 0),
    orient_type='GLOBAL',
    orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)),
    orient_matrix_type='GLOBAL',
    constraint_axis=(True, False, False),
    mirror=False,
    use_proportional_edit=False,
    proportional_edit_falloff='SMOOTH',
    proportional_size=1,
    use_proportional_connected=False,
    use_proportional_projected=False
)

        

        bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)


        MeshNew.asset_mark()
        MeshNew.asset_generate_preview()
        #MeshNew.modifiers["Armature"].object = bpy.data.objects[files]
        

        #move base back to original col

    bpy.ops.object.select_all(action='DESELECT')  


    Mesh.select_set(True)
    bpy.context.view_layer.objects.active = Mesh
    bpy.ops.object.move_to_collection(collection_index=1)




class ImportFBXs(bpy.types.Operator):
    #tooltip when hovering with the mouse over button
    """Import fbx, rename everything to there file name and copy active mesh onto armatures"""
    #idname to creat the operation, bpy.ops.idnameinthiscasefurr.shape_scale()
    bl_idname = "import.fbxs"
    #name of button
    bl_label = "Import FBXs"
    ##undo system
    bl_options = {'REGISTER', 'UNDO'}
    
    
    # script can only run if a curve is selected
    @classmethod
    def poll(cls, context):
        return context.active_object is not None and context.active_object.type == 'MESH' 
     

    #this triggers the "main" function above, where we wrote our code
    def execute(self, context):
        main(self, context)
        return {'FINISHED'}
    
    
    
    
    
    
    
class Importpanel(bpy.types.Panel):
    #tooltip when hovering with the mouse over button
    """Creates a Panel in the Tool Shelf"""
    #name of unfold window
    bl_label = "Import FBX batch"
    #idname to creat the operation, bpy.ops.inthiscaseOBJECT_PT_ScaleMeshToManifold.shape_scale()
    bl_idname = "OBJECT_PT_ImportFBX"
    #in wich window it should appear
    bl_space_type = 'VIEW_3D'
    #in what region, UI
    bl_region_type = 'UI'
    #name of tab, when tab already exists it puts it in the same
    bl_category = "FlyCGI"


    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool
        
        layout.prop(mytool,"my_string")
        
        row = layout.row()
        #what operator to use in button, operator was created by triggering the main function wich our code is in
        row.operator("import.fbxs")
        
        




def menu_func(self, context):
    self.layout.operator(SimpleOperator.bl_idname, text=SimpleOperator.bl_label)
    
def register():
    bpy.utils.register_class(MyProperties)
    bpy.utils.register_class(ImportFBXs)
    bpy.utils.register_class(Importpanel)
    bpy.types.Scene.my_tool = bpy.props.PointerProperty(type= MyProperties)
    
def unregister():
    bpy.utils.unregister_class(MyProperties)
    bpy.utils.unregister_class(ImportFBXs)
    bpy.utils.unregister_class(Importpanel)
    del bpy.types.Scene.my_tool
    




#idk but apperently needs it
if __name__ == "__main__":
    register()