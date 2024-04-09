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