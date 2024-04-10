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

SPACING_X = 200
SPACING_Y = 400
POSITION_h = 460

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

def CreatConnection(name:str, radius, length, parent, material):
	connection = c4d.BaseObject(c4d.Ocylinder)
	doc.InsertObject(connection, None, None)
	connection.SetName(name)
	connection[c4d.PRIM_CYLINDER_RADIUS] = radius
	connection[c4d.PRIM_CYLINDER_HEIGHT] = length
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

	#defines the connectionblock l3ength based on the spacing of the atoms using c = sqrt(a^2 + b^2)
	length = (SPACING_X**2 + SPACING_Y**2)**0.5
	#creats the atoms and connection based on the values given above. 
	carbon = CreatAtom('Carbon', 100, null, matBlack)
	hydrogen = CreatAtom('Hydrogen', 50, null, matWhite)
	connect = CreatConnection('Connection', 20, length, null, matGrey)
	return (carbon, hydrogen, connect, matBlack, matWhite, matGrey)

def CreateEndingBlock(carbonlibrary, hydrogenLib, connectLib):
	#Creats null object named "Endingblock"
	endingBlockParent = CreatNull('Endingblock')
	# Creates the ending block that consists of instance objects
	carbon = CreatInstance('Carbon', carbonlibrary, endingBlockParent, c4d.Vector(0, 0, 0), c4d.Vector(0, 0, 0))	
	hydrogen1 = CreatInstance('Hydrogen1', hydrogenLib, endingBlockParent, c4d.Vector(POSITION_h, 0, 0), c4d.Vector(0, 0, 0))
	hydrogen2 = CreatInstance('Hydrogen2', hydrogenLib, endingBlockParent, c4d.Vector(0, POSITION_h, 0), c4d.Vector(0, 0, 0))
	hydrogen3 = CreatInstance('Hydrogen3', hydrogenLib, endingBlockParent, c4d.Vector(0, 0, POSITION_h), c4d.Vector(0, 0, 0))
	connection1 = CreatInstance('Connection1', connectLib, endingBlockParent, c4d.Vector(195, 0, 0), c4d.Vector(0, 0, 90))   
	connection2 = CreatInstance('Connection2', connectLib, endingBlockParent, c4d.Vector(0, 195, 0), c4d.Vector(0, 0, 0))
	connection3 = CreatInstance('Connection3', connectLib, endingBlockParent, c4d.Vector(0, 0, 195), c4d.Vector(0, 90, 0))
	return endingBlockParent

def CreatIntermediateBlock(carbonlibrary, hydrogenLib, connectLib):
	#Creats null object named "Intermediateblock"
	intermediateBlockParent = CreatNull('Intermediateblock')
	# Creates the intermediate block that consists of instance objects
	carbon = CreatInstance('Carbon', carbonlibrary, intermediateBlockParent, c4d.Vector(0, 0, 0), c4d.Vector(0, 0, 0))	
	hydrogen1 = CreatInstance('Hydrogen1', hydrogenLib, intermediateBlockParent, c4d.Vector(POSITION_h, 0, 0), c4d.Vector(0, 0, 0))
	hydrogen2 = CreatInstance('Hydrogen2', hydrogenLib, intermediateBlockParent, c4d.Vector(0, POSITION_h, 0), c4d.Vector(0, 0, 0))
	connection1 = CreatInstance('Connection1', connectLib, intermediateBlockParent, c4d.Vector(195, 0, 0), c4d.Vector(0, 0, 90))
	connection2 = CreatInstance('Connection2', connectLib, intermediateBlockParent, c4d.Vector(0, 195, 0), c4d.Vector(0, 0, 0))
	return intermediateBlockParent

def CreatConnectionBlock(connectLib):
	#Creats null object named "Connectionblock"
	connectionBlockParent = CreatNull('Connectionblock')
	# Creates the connection block that consists of instance objects
	connection1 = CreatInstance('Connection1', connectLib, connectionBlockParent, c4d.Vector(0, 0, 0), c4d.Vector(0, 0, 0))
	return connectionBlockParent

def CreatMetheanBlock(carbonlibrary, hydrogenLib, connectLib):
	#Creats null object named "Metheanblock"
	methanBlockParent = CreatNull('Metheanblock')
	# Creates the methean block that consists of instance objects
	carbon = CreatInstance('Carbon', carbonlibrary, methanBlockParent, c4d.Vector(0, 0, 0), c4d.Vector(0, 0, 0))	
	hydrogen1 = CreatInstance('Hydrogen1', hydrogenLib, methanBlockParent, c4d.Vector(-POSITION_h, 0, 0), c4d.Vector(0, 0, 0))
	hydrogen2 = CreatInstance('Hydrogen2', hydrogenLib, methanBlockParent, c4d.Vector(0, -POSITION_h, 0), c4d.Vector(0, 0, 0))
	hydrogen3 = CreatInstance('Hydrogen3', hydrogenLib, methanBlockParent, c4d.Vector(0, 0, -POSITION_h), c4d.Vector(0, 0, 0))
	hydrogen4 = CreatInstance('Hydrogen4', hydrogenLib, methanBlockParent, c4d.Vector(0, 0, POSITION_h), c4d.Vector(0, 0, 0))
	hydrogen5 = CreatInstance('Hydrogen5', hydrogenLib, methanBlockParent, c4d.Vector(0, POSITION_h, 0), c4d.Vector(0, 0, 0))
	hydrogen6 = CreatInstance('Hydrogen6', hydrogenLib, methanBlockParent, c4d.Vector(POSITION_h, 0, 0), c4d.Vector(0, 0, 0))
	connection1 = CreatInstance('Connection1', connectLib, methanBlockParent, c4d.Vector(195, 0, 0), c4d.Vector(0, 0, 90))   
	connection2 = CreatInstance('Connection2', connectLib, methanBlockParent, c4d.Vector(0, 195, 0), c4d.Vector(0, 0, 0))
	connection3 = CreatInstance('Connection3', connectLib, methanBlockParent, c4d.Vector(0, 0, 195), c4d.Vector(0, 90, 0))
	connection4 = CreatInstance('Connection4', connectLib, methanBlockParent, c4d.Vector(0, 0, -195), c4d.Vector(0, 90, 0))
	connection5 = CreatInstance('Connection5', connectLib, methanBlockParent, c4d.Vector(0, -195, 0), c4d.Vector(0, 0, 0))
	connection6 = CreatInstance('Connection6', connectLib, methanBlockParent, c4d.Vector(-195, 0, 0), c4d.Vector(0, 0, 90))
	return methanBlockParent

def CreatMolecule(moleculeIdx: int):
	# Preparation step: Creating library
	(cLib, hLib, cnLib, matBlack, matWhite, matGrey) = Creatlibrary(null="Library", matBlack="Black", matWhite="White", matGrey="Grey", carbon="Carbon", hydrogen="Hydrogen", connect="Connection")

	numberOfIntermediateBlocks = moleculeIdx - 2 #defines how many intermediate blocks will be created based on the number of molecules
	numberOfConnectionBlocks = moleculeIdx - 1 #defines how many connection blocks will be created based on the number of molecules

	#creating a methan molecule
	if moleculeIdx == 1:
		methan = CreatMetheanBlock(cLib, hLib, cnLib)
		methan.SetAbsPos(c4d.Vector(0, 0, 0))
		methan.SetRelRot(DegToRad(c4d.Vector(0, 0, 0)))
		return
	
	#creating a ethan molecule
	if moleculeIdx == 2:
		ethan = CreateEndingBlock(cLib, hLib, cnLib)
		ethan.SetAbsPos(c4d.Vector(0, 0, 0))
		ethan.SetRelRot(DegToRad(c4d.Vector(144.7356, -30, 35.2644)))
		ethan2 = CreateEndingBlock(cLib, hLib, cnLib)
		ethan2.SetAbsPos(c4d.Vector(400, 0, 0))
		ethan2.SetRelRot(DegToRad(c4d.Vector(324.7356, -30, 35.2644)))
		#creates the connectionBLocks for the ethan molecule
		connectionBlock = CreatConnectionBlock(cnLib)
		connectionBlock.SetAbsPos(c4d.Vector(200, 0, 0))
		connectionBlock.SetRelRot(DegToRad(c4d.Vector(0, 0, 90)))
		return
	
	
	# Creating the starting- and ending- block
	startingBlock = CreateEndingBlock(cLib, hLib, cnLib)
	startingBlock.SetAbsPos(c4d.Vector(0, 0, 0))
	startingBlock.SetRelRot(DegToRad(c4d.Vector(144.7356, -30, 35.2644)))

	x=(numberOfIntermediateBlocks+1)*SPACING_X
	endingBlock = CreateEndingBlock(cLib, hLib, cnLib)
	endingBlock.SetAbsPos(c4d.Vector(x, SPACING_Y, 0))
	endingBlock.SetRelRot(DegToRad(c4d.Vector(324.7356, -30, 35.2644 ))) #sets the rotation of the ending block
	#if the number of molecules is even, then the ending block will be placed 400 units up on the y-axis
	#else the ending block will be placed 400 units down on the y-axis
	if numberOfIntermediateBlocks % 2 == 0:
		endingBlock.SetAbsPos(c4d.Vector(x, SPACING_Y, 0))
	else:
		endingBlock.SetAbsPos(c4d.Vector(x, 0, 0))
		

	

	#loop for creating the intermediate blocks based on the number of "molecule index -2" see in line 129
	for i in range(numberOfIntermediateBlocks):
		x=(i+1)*SPACING_X
		isEven = (i % 2) == 0 #checks if the number of intermediate blocks is even or odd
		intermediateBlock = CreatIntermediateBlock(cLib, hLib, cnLib)
		if isEven: 	#checks if the number is even, then it places the intermediate block 200 units up on the y-axis and 200 units to the right on the x-axis
			intermediateBlock.SetAbsPos(c4d.Vector(x, SPACING_Y, 0))
			intermediateBlock.SetRelRot(DegToRad(c4d.Vector(0, 0, 315)))
		else: 	#if the number is odd, then it places the intermediate block 200 units down on the y-axis and duble the amount of units to the right on the x-axis
			intermediateBlock.SetAbsPos(c4d.Vector(x, 0, 0))
			intermediateBlock.SetRelRot(DegToRad(c4d.Vector(0, 0, 135)))
	#if the numberOfIntermediateBlocks is even rotate the intermediateBlock 90 degrees on the y-axis, els rotate the intermediateBlock 180 degrees on the z-axis
		if isEven:
			intermediateBlock.SetRelRot(DegToRad(c4d.Vector(90, 0, 315)))
		else:
			intermediateBlock.SetRelRot(DegToRad(c4d.Vector(90, 0, 135)))

	#creates the connectionBLocks based on the number of "molecule index -1" see in line 130
	for i in range(numberOfConnectionBlocks):
		x=(i*SPACING_X+SPACING_X/2)
		connectionBlock = CreatConnectionBlock(cnLib)
		connectionBlock.SetAbsPos(c4d.Vector(x, 200, 0))
		connectionBlock.SetRelRot(DegToRad(c4d.Vector(0, 0, 0)))
		#rotates the connectionblock based on if the numberOfConnectionBlocks is even or odd
		if i % 2 == 0:
			connectionBlock.SetRelRot(DegToRad(c4d.Vector(0, 0, -330)))
		else:
			connectionBlock.SetRelRot(DegToRad(c4d.Vector(0, 0, 330)))
	return

def ParseUserInput(userInput: str) -> int:
	#Checks if the first character is the uppercase letter "C", if not it returns -1.
    if userInput[0] != 'C':
        return -1
	
    #Checks if the nex characters are numbers until the next uppercase letter "H", if not it returns -1
    moleculeIdx = 0
    for i in range(1, len(userInput)):
        if userInput[i] == 'H':
            moleculeIdx = int(userInput[1:i])
            break
        if not userInput[i].isdigit():
            return -1
		#checks if the character after the "H" is a number, that is the numbers behind "C" times "2" plus "2"
    if not userInput[i+1].isdigit() or int(userInput[i+1]) != moleculeIdx*2+2:
        return -1
	#if there is no number after the "H" it returns -1
    if i+1 == len(userInput):
        return -1
    return moleculeIdx

	

def main():

	userInput = 'C3H8' # Ask the user for the molecule

	moleculeIdx = ParseUserInput(userInput)

	if moleculeIdx == -1:
		gui.MessageDialog('''Invalid input! 
Please enter a valid formula (e.g. C2H6, C3H8, C4H10, ...)''')
		return

	# Call the function with the desired number of molecules
	# moleculeIdx = 2  #1 - Methan, 2 - Ethan, 3 - propan, 4 - butan, 5 - pentan, 6 - hexan, 7 - heptan, 8 - octan, 9 - nonan, 10 - decan "..."
	CreatMolecule(moleculeIdx)
	# Update the scene
	c4d.EventAdd()

if __name__=='__main__':
	main()