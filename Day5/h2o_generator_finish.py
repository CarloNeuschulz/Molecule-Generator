import c4d
import typing
import mxutils
from c4d import gui
doc: c4d.documents.BaseDocument
op: typing.Optional[c4d.BaseObject]
def foo():
	return {
        "a": mxutils.CheckType(c4d.BaseObject(c4d.Osphere)),
         "b": mxutils.CheckType(c4d.BaseObject(c4d.Ocylinder))}

def CreateMaterial(name, color):
    mat = c4d.BaseMaterial(c4d.Mmaterial) # Initialize a material
    mat.SetName(name) # Set the name of the material
    mat[c4d.MATERIAL_COLOR_COLOR] = color # Set the color of the material
    doc.InsertMaterial(mat) # Insert the material to the document
    return mat

def InsertMaterialTag(op, m):
    tag = c4d.BaseTag(5616) # Initialize a material tag
    tag[c4d.TEXTURETAG_MATERIAL] = m # Assign material to the material tag
    tag[c4d.TEXTURETAG_PROJECTION] = 6 #UVW Mapping
    op.InsertTag(tag) # Insert tag to the object

def CreatAtom(name:str, radius, parent, material):
     atom = c4d.BaseObject(c4d.Osphere)
     doc.InsertObject(atom, None, None)
     atom.SetName(name)
     atom[c4d.PRIM_SPHERE_RAD] = radius
     atom.InsertUnder(parent) #inserts the atom/model under the null object known as "Library"
     InsertMaterialTag(atom, material) #materials created down in line 220-222, allows to select the material
     return atom

def CreatConnection(name:str, radius, parent, material):
    connection = c4d.BaseObject(c4d.Ocylinder)
    doc.InsertObject(connection, None, None)
    connection.SetName(name)
    connection[c4d.PRIM_CYLINDER_RADIUS] = radius
    connection.InsertUnder(parent) #Inserts the atom/model under the null object known as "Library"
    InsertMaterialTag(connection, material) ##materials created down in line 220-222, allows to select the material
    return connection

def CreatNull(name:str):
     null = c4d.BaseObject(c4d.Onull)
     doc.InsertObject(null, None, None)
     null.SetName(name)
     return null

def CreatInstance(name:str, RefrencObject, parent, position = c4d.Vector(), rotation = c4d.Vector()):
     instance = c4d.BaseObject(c4d.Oinstance)
     doc.InsertObject(instance, None, None)
     instance.SetName(name)
     instance.SetReferenceObject(RefrencObject) #sets the refrence object for the instance, is able to select one of the library object as a refrence object.
     instance.SetAbsPos(position) #sets tha position of the object, able to use matrix for more specific positions.
     radX = c4d.utils.DegToRad(rotation.x)
     radY = c4d.utils.DegToRad(rotation.y)
     radZ = c4d.utils.DegToRad(rotation.z)
     radians = c4d.Vector(radX, radY, radZ)
     instance.SetRelRot(radians) #Changes degree to radiant and sets the radiant of the object.
     instance.InsertUnder(parent)

def main():

    #creating "Library"
    null = CreatNull('Library') #creats the nullobject/library, that NEEDS TO BE PUT FIRST otherwise nothing will work, why i dunn know.
    #Creates materials for the atoms and the connections
    matRed = CreateMaterial('Red', c4d.Vector(1, 0, 0))
    matWhite = CreateMaterial('White', c4d.Vector(1, 1, 1))
    matGrey = CreateMaterial('Grey', c4d.Vector(0.5, 0.5, 0.5))

    #dont actually need this anymore but i will keep it anyway in the extrem that nothing will work and i need to go back a few steps
    # InsertMaterialTag(oxygen, matRed)
    # InsertMaterialTag(hydrogen, matWhite)
    # InsertMaterialTag(connect, matGrey)

    #this can technicaly be later to make everything more butiful, but i will leav it there --> its broken
    #Sets the null "libary" object to be invisible in the editor and renderer
    null.SetEditorMode(c4d.MODE_OFF)
    null.SetRenderMode(c4d.MODE_OFF)

    #creats the atoms and connection based on the values given above. 
    oxygen = CreatAtom('Oxygen', 100, null, matRed)
    hydrogen = CreatAtom('Hydrogen', 50, null, matWhite)
    connect = CreatConnection('Connection', 20, null, matGrey)


    #Creating "h2o", creats the library and the instances that gets the given atoms and connections as refrenceobjects
    null1 = CreatNull("h2o")
    instance = CreatInstance('Oxygen', oxygen, null1, position = c4d.Vector(0, 0, 0), rotation = c4d.Vector(0, 0, 0) )
    instance = CreatInstance('Connection1', connect, null1, position = c4d.Vector(195, 0, 0), rotation=c4d.Vector(0, 0, 90))
    instance = CreatInstance('Connection2', connect, null1, position=c4d.Vector(0, 195, 0), rotation=c4d.Vector(0, 0, 0,))
    instance = CreatInstance('Hydrogen1', hydrogen, null1, position=c4d.Vector(300, 0, 0), rotation=c4d.Vector(0, 0, 0,))
    instance = CreatInstance('Hydrogen2', hydrogen, null1, position=c4d.Vector(0, 300, 0), rotation=c4d.Vector(0, 0, 0))

# def CreatInstance2(name:str, RefrencObject, parent, position = c4d.Vector(), rotation = c4d.Vector()):
#      """
#      Creates instance given blah blha blah
#      rotation is expecteed in degrees
#      """
#      instance = c4d.BaseObject(c4d.Oinstance)
#      doc.InsertObject(instance, None, None)
#      instance.SetName(name)
#      instance.SetReferenceObject(RefrencObject)
#      instance.SetAbsPos(position)
#      # instance.SetMl(matrix)
#      instance.SetRelRot(c4d.utils.DegToRad(rotation))
#      instance.InsersUnder(parent)
    
    # # Creates "Oxygen" a sphere at 0/0/0 with a radius of 100
    # oxygen = mxutils.CheckType(c4d.BaseObject(c4d.Osphere))
    # #Inserts the sphere into the active document
    # doc.InsertObject(oxygen, None, None)
    # oxygen.SetName("Oxygen")
    # #creats a null object called "H2O"
    # null1 = mxutils.CheckType(c4d.BaseObject(c4d.Onull))
    # #Inserts the null object into the active document
    # doc.InsertObject(null1, None, None)
		# #Sets the name of the null object to "H2O"
    # null1.SetName("H2O")   
    # #Creats instance object of the sphere
    # instance = mxutils.CheckType(c4d.InstanceObject())
    # #Inserts the instance object of the sphere into the active document
    # doc.InsertObject(instance, null1, None)
    # #rename instance to "Oxygen"
    # instance.SetName("Oxygen")
    # # Makes instance object active (selected)
    # doc.SetActiveObject(instance)
    # # Sets the instance reference object to the created cube
    # instance.SetReferenceObject(oxygen)


	  # # #creats "Hydrogen" a sphere at 0/0/0 with a radius of 50
    # # hydrogen = mxutils.CheckType(c4d.BaseObject(c4d.Osphere))
	  # # #Inserts the "hydrogene" sphere into the active document
    # # doc.InsertObject(hydrogen, None, None)
    # # hydrogen.SetName("hydrogen")
	  # # #sets the radius of the "hydrogen" sphere to 50
    # # hydrogen[c4d.PRIM_SPHERE_RAD] = 50
	  # # #creats instance object of the "hydrogen" sphere
    # instance1 = mxutils.CheckType(c4d.InstanceObject())
		# #Inserts the instance object of the "hydrogen" sphere into the active document
    # doc.InsertObject(instance1, null1, None)
    # #rename instance to "hydrogen"
    # instance1.SetName("hydrogen")
    # #sets the position of the instance1 on the x axis to 340/0/0
    # x_pos = 340
    # y_pos = 0
    # z_pos = 0
    # instance1.SetAbsPos(c4d.Vector(x_pos, y_pos, z_pos))
    # # Makes instance object active (selected)
    # doc.SetActiveObject(instance1)
    # # Sets the instance reference object to the created cube
    # instance1.SetReferenceObject(hydrogen)
    # #creats instance2 object of the "hydrogen" sphere
    # instance2 = mxutils.CheckType(c4d.InstanceObject())
    # #Inserts the instance2 object of the "hydrogen" sphere into the active document
    # doc.InsertObject(instance2, null1, None)
    # #rename instance to "hydrogen2"
    # instance2.SetName("hydrogen2")
    # #sets the position of the instance2 on the y axis to 0/340/0
    # x_pos = 0
    # y_pos = 340
    # z_pos = 0
    # instance2.SetAbsPos(c4d.Vector(x_pos, y_pos, z_pos))
    # # Makes instance object active (selected)
    # doc.SetActiveObject(instance2)
    # # Sets the instance2 reference object to the created "hydrogen" sphere
    # instance2.SetReferenceObject(hydrogen)





    # #Creats a connection line as a cylinder
    # connect = mxutils.CheckType(c4d.BaseObject(c4d.Ocylinder))
    # #Inserts the cylinder into the active document
    # doc.InsertObject(connect, None, None)
    # connect.SetName("connect")
    # #Sets the position of the cylinder to the sphere
    # m = c4d.Matrix(v1=c4d.Vector( 0, 1, 0),
    #             	v2=c4d.Vector(-1, 0, 0),
    #             	v3=c4d.Vector( 0, 0, 1))
    # connect.SetMl(m)
    # connect: c4d.BaseObject
    # connect.SetRelRot(c4d.Vector(0, 0, c4d.utils.DegToRad(45)))
	  # # Set the position of the cylinder
    # x_pos = 195
    # y_pos = 0
    # z_pos = 0
    # connect.SetAbsPos(c4d.Vector(x_pos, y_pos, z_pos))
	  # #Set the radius of the cylinder to 20
    # connect[c4d.PRIM_CYLINDER_RADIUS] = 20
	  # #creats a instance object of the cylinder
    # instance1 = mxutils.CheckType(c4d.InstanceObject())
		# #Inserts the instance object of the cylinder into the active document
    # doc.InsertObject(instance1, null1, None)
    # #rename instance to "connect"
    # instance1.SetName("connect")
    # #Sets the position of the instance1 to the sphere
    # m = c4d.Matrix(v1=c4d.Vector( 0, 1, 0),
    #             	v2=c4d.Vector(-1, 0, 0),
    #             	v3=c4d.Vector( 0, 0, 1))
    # instance1.SetMl(m)
	  # # Set the position of the instance1
    # x_pos = 195
    # y_pos = 0
    # z_pos = 0
    # instance1.SetAbsPos(c4d.Vector(x_pos, y_pos, z_pos))
    # # Makes instance object active (selected)
    # doc.SetActiveObject(instance1)
    # # Sets the instance reference object to the created cylinder "connect"
    # instance1.SetReferenceObject(connect)
    # #creats a second instance object of the cylinder
    # instance2 = mxutils.CheckType(c4d.InstanceObject())
    # #Inserts the instance object of the cylinder into the active document
    # doc.InsertObject(instance2, null1, None)
    # #rename instance to "connect2"
    # instance2.SetName("connect2")
	  # # Set the position of the instance2
    # x_pos = 0
    # y_pos = 195
    # z_pos = 0
    # instance2.SetAbsPos(c4d.Vector(x_pos, y_pos, z_pos))
    # # Makes instance object active (selected)
    # doc.SetActiveObject(instance2)
    # #Asseses the connect to the instance2 object
    # instance2.SetReferenceObject(connect)
                   
  


	  # #creats a null object called "Liabry"
    # null = mxutils.CheckType(c4d.BaseObject(c4d.Onull))
    # #Sets the position of the null object to 0/0/350
    # null.SetAbsPos(c4d.Vector(0, 0, 350))
    # #Sets the name of the null object to "Liabry"
    # null.SetName("Liabry")
	  # #Adds the cylinder, the two spheres to the null object
    # doc.InsertObject(null, None, None)
    # connect.InsertUnder(null)
    # oxygen.InsertUnder(null)
    # hydrogen.InsertUnder(null)



    
    
    #update the scene
    c4d.EventAdd()



if __name__=='__main__':
    main()

"""
def CreateH2O():


def main():
    CreateH2O()
    
    #update the scene
    c4d.EventAdd()
"""