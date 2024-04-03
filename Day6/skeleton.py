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



def CreateLibrary():
	hObject = ...
	oObject = ...
	cObject = ...

	hMaterial = ...
	oMaterial = ...
	cMaterial = ...

	return (hObject, oObject, cObject, hMaterial, oMaterial, cMaterial)

def CreateEndingBlock(...):
	# Creates the ending block that consists of instance objects
	carbonAtom =
	hzdrogen1
	hydrogen2
	...
	pass

def CreateIntermediateBlock(...):
	# Creates the intermediate block
	pass

# def CreateConnection(...):
# 	# Creates the connection between the blocks
# 	pass
	
def CreateMolecule(moleculeIdx: int):
	# for i in range(3):
	# 	print('Index: ', i)

	# Preparation step: Creating library
	(hObject, oObject, cObject, hMaterial, oMaterial, cMaterial) = CreateLibrary()


	# Creating the blocks
	startingBlock = CreateEndingBlock(...)
	return
	endingBlock = CreateEndingBlock(...)

	# Multiple times
	intermediateBlock = CreateIntermediateBlock(...)


	# Placing and connection the blocks
	# TODO: (Carlo) moving the blocks into the correct position and rotate them properly


def main():
	CreateMolecule(4)

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