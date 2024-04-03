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

def DegToRad(degVector: c4d.Vector) -> c4d.Vector:
	"""Converts a vector of degrees to a vector of radians"""
	radX = c4d.utils.DegToRad(degVector.x)
	radY = c4d.utils.DegToRad(degVector.y)
	radZ = c4d.utils.DegToRad(degVector.z)
	return c4d.Vector(radX, radY, radZ)

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
	InsertMaterialTag(atom, material) #materials created down in line ###, allows to select the material
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
	radians = DegToRad(rotation)
	instance.SetRelRot(radians) #Changes degree to radiant and sets the radiant of the object.
	instance.InsertUnder(parent)
	
def Creatlibrary(null, matBlack, matWhite, matGrey, carbon, hydrogen, connect):
	#creating "Library"
	null = CreatNull('Library') #creats the nullobject/library, that NEEDS TO BE PUT FIRST otherwise nothing will work, why i dunn know.
	#Creates materials for the atoms and the connections
	matBlack = CreateMaterial('Black', c4d.Vector(0.1, 0.1, 0.1))
	matWhite = CreateMaterial('White', c4d.Vector(1, 1, 1))
	matGrey = CreateMaterial('Grey', c4d.Vector(0.5, 0.5, 0.5))

	#Sets the null "library" object to be invisible in the editor and renderer
	null.SetEditorMode(c4d.MODE_OFF)
	null.SetRenderMode(c4d.MODE_OFF)

	#creats the atoms and connection based on the values given above. 
	carbon = CreatAtom('Carbon', 100, null, matBlack)
	hydrogen = CreatAtom('Hydrogen', 50, null, matWhite)
	connect = CreatConnection('Connection', 20, null, matGrey)
	return (carbon, hydrogen, connect, matBlack, matWhite, matGrey)

def CreateEndingBlock(carbonlibrary, hydrogenLib, connectLib):
	#Creats null object named "Endingblock"
	endingBlockParent = CreatNull('Endingblock')
	# Creates the ending block that consists of instance objects
	carbon = CreatInstance('Carbon', carbonlibrary, endingBlockParent, c4d.Vector(0, 0, 0), c4d.Vector(0, 0, 0))	
	hydrogen1 = CreatInstance('Hydrogen1', hydrogenLib, endingBlockParent, c4d.Vector(340, 0, 0), c4d.Vector(0, 0, 0))
	hydrogen2 = CreatInstance('Hydrogen2', hydrogenLib, endingBlockParent, c4d.Vector(0, 340, 0), c4d.Vector(0, 0, 0))
	hydrogen3 = CreatInstance('Hydrogen3', hydrogenLib, endingBlockParent, c4d.Vector(0, 0, 340), c4d.Vector(0, 0, 0))
	connection1 = CreatInstance('Connection1', connectLib, endingBlockParent, c4d.Vector(195, 0, 0), c4d.Vector(0, 0, 90))   
	connection2 = CreatInstance('Connection2', connectLib, endingBlockParent, c4d.Vector(0, 195, 0), c4d.Vector(0, 0, 0))
	connection3 = CreatInstance('Connection3', connectLib, endingBlockParent, c4d.Vector(0, 0, 195), c4d.Vector(0, 90, 0))
	return endingBlockParent

def CreatIntermediateBlock(carbonlibrary, hydrogenLib, connectLib):
	#Creats null object named "Intermediateblock"
	intermediateBlockParent = CreatNull('Intermediateblock')
	# Creates the intermediate block that consists of instance objects
	carbon = CreatInstance('Carbon', carbonlibrary, intermediateBlockParent, c4d.Vector(0, 0, 0), c4d.Vector(0, 0, 0))	
	hydrogen1 = CreatInstance('Hydrogen1', hydrogenLib, intermediateBlockParent, c4d.Vector(340, 0, 0), c4d.Vector(0, 0, 0))
	hydrogen2 = CreatInstance('Hydrogen2', hydrogenLib, intermediateBlockParent, c4d.Vector(0, 340, 0), c4d.Vector(0, 0, 0))
	connection1 = CreatInstance('Connection1', connectLib, intermediateBlockParent, c4d.Vector(195, 0, 0), c4d.Vector(0, 0, 90))   
	connection2 = CreatInstance('Connection2', connectLib, intermediateBlockParent, c4d.Vector(0, 195, 0), c4d.Vector(0, 0, 0))
	return intermediateBlockParent

def CreatConnectionBlock(connectLib):
	#Creats null object named "Connectionblock"
	connectionBlockParent = CreatNull('Connectionblock')
	# Creates the connection block that consists of instance objects
	connection1 = CreatInstance('Connection1', connectLib, connectionBlockParent, c4d.Vector(0, 0, 0), c4d.Vector(0, 0, 0))
	return connectionBlockParent

# def IsEven(number: int) -> bool:
# 	return number % 2 == 0

def CreatMolecule(moleculeIdx: int):
	# Preparation step: Creating library
	(cLib, hLib, cnLib, matBlack, matWhite, matGrey) = Creatlibrary(null="Library", matBlack="Black", matWhite="White", matGrey="Grey", carbon="Carbon", hydrogen="Hydrogen", connect="Connection")

	numberOfIntermediateBlocks = moleculeIdx - 2 #defines how many intermediate blocks will be created based on the number of molecules
	
	# Creating the blocks using a loop
	startingBlock = CreateEndingBlock(cLib, hLib, cnLib)
	startingBlock.SetRelRot(DegToRad(c4d.Vector(144.7356, -30, 35.2644)))

	x=(numberOfIntermediateBlocks+1)*200
	endingBlock = CreateEndingBlock(cLib, hLib, cnLib)
	endingBlock.SetAbsPos(c4d.Vector(x, 0, 0))
 
	# intermediateBlock = CreatIntermediateBlock(cLib, hLib, cnLib)
	# intermediateBlock.SetAbsPos(c4d.Vector(400, 200, 0))
	
	# connectionBlock = CreatConnectionBlock(cnLib)	

	#loop for creating the intermediate blocks based on the number of "molecule index -2" see in line 129
	for i in range(numberOfIntermediateBlocks):
		x=(i+1)*200
		isEven = (i % 2) == 0 #checks if the number of intermediate blocks is even or odd
		intermediateBlock = CreatIntermediateBlock(cLib, hLib, cnLib)
		if isEven: 	#checks if the number is even, then it places the intermediate block 200 units up on the y-axis and 200 units to the right on the x-axis
			intermediateBlock.SetAbsPos(c4d.Vector(x, 200, 0))
		else: 	#if the number is odd, then it places the intermediate block 200 units down on the y-axis and duble the amount of units to the right on the x-axis
			intermediateBlock.SetAbsPos(c4d.Vector(x, -200, 0))
		
	# 	connectionBlock = CreatConnectionBlock(cnLib)	
	return

def main():
	# Call the function with the desired number of molecules
	moleculeIdx = 12  # 3 - propan, 4 - butan, 5 - pentan, 6 - hexan, 7 - heptan, 8 - octan, 9 - nonan, 10 - decan
	CreatMolecule(moleculeIdx)
	# Update the scene
	c4d.EventAdd()

if __name__=='__main__':
	main()