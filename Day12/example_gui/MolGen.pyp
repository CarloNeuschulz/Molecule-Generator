"""
Copyright: MAXON Computer GmbH
Author: Maxime Adam

Description:
	- Creates a Dialog which display 2 buttons OK and Cancel.

Class/method highlighted:
	- c4d.plugins.CommandData
	- CommandData.Execute()
	- c4d.gui.GeDialog
	- GeDialog.CreateLayout()
	- GeDialog.Command()
"""
import c4d
import math
from c4d import documents
from c4d import gui

doc: c4d.documents.BaseDocument


# Be sure to use a unique ID obtained from www.plugincafe.com
PLUGIN_ID = 1234897

USER_INPUT = "C4H10"
CONNECTION_LENGTH = 450

class Molecule:
	def __init__(self, moleculeIdx: int):
		self.moleculeIdx = moleculeIdx

	def Generate(self):
		print('Generating molecule is happening in child class')
	
	def DegToRad(self, degVector: c4d.Vector)->c4d.Vector:
		# Convert degrees to radians
		radX = c4d.utils.DegToRad(degVector.x)
		radY = c4d.utils.DegToRad(degVector.y)
		radZ = c4d.utils.DegToRad(degVector.z)
		return c4d.Vector(radX, radY, radZ)

	#Creats the material for the molecule
	def CreateMaterial(self, name:str, color: c4d.Vector):
		mat = c4d.BaseMaterial(c4d.Mmaterial) # Initialize a material
		mat.SetName(name) # Set the name of the material
		mat[c4d.MATERIAL_COLOR_COLOR] = color # Set the color of the material
		doc.InsertMaterial(mat) # Insert the material to the document
		return mat # Return the material
	#Inserts the materialTag to the object
	def InsertMaterialTag(self, op, m):
		tag = c4d.BaseTag(5616) # Initialize a material tag
		tag[c4d.TEXTURETAG_MATERIAL] = m # Assign material to the material tag
		tag[c4d.TEXTURETAG_PROJECTION] = 6 #UVW Mapping
		op.InsertTag(tag) # Insert tag to the object
		return tag # Return the tag

	#creats the atom object
	def CreateAtom(self, name:str, radius, parent, material):
		atom = c4d.BaseObject(c4d.Osphere) # Initialize a sphere object
		doc.InsertObject(atom, parent, None) # Insert the sphere to the document
		self.InsertMaterialTag(atom, material) # Insert the material tag to the sphere
		atom[c4d.PRIM_SPHERE_RAD] = radius # Set the radius of the sphere
		atom.SetName(name) # Set the name of the sphere
		return atom # Return the sphere object
	
	#creats the connection object
	def CreateConnection(self, name:str, radius, length, parent, material):
		connection = c4d.BaseObject(c4d.Ocylinder)
		doc.InsertObject(connection, parent, None)
		connection.SetName(name)
		connection[c4d.PRIM_CYLINDER_RADIUS] = radius
		connection[c4d.PRIM_CYLINDER_HEIGHT] = length
		connection.InsertUnder(parent)
		self.InsertMaterialTag(connection, material)
		return connection
	
	#creats the instance object of the molecule
	def CreatInstance(self, name:str, RefrencObject, parent, position=c4d.Vector(), rotation=c4d.Vector()):
		instance = c4d.BaseObject(c4d.Oinstance)
		doc.InsertObject(instance, parent, None)
		instance.SetName(name)
		instance.SetReferenceObject(RefrencObject)
		instance.SetAbsPos(position)
		radians = self.DegToRad(rotation)
		instance.SetRelRot(radians)
		instance.InsertUnder(parent)
		return instance

	# Creates a null object in the scene
	def CreatNull(self, name:str,):
		null = c4d.BaseObject(c4d.Onull)
		doc.InsertObject(null, None, None)
		null.SetName(name)
		return null

	#creats a library named "lib" that has the atom, connection and material as a child
	def CreateLibrary(self, null1, matBlack, matWhite, matGrey, carbon, hydrogen, connection):
		null1 = self.CreatNull('lib')
		#Sets the null "lib" object invisible in the editor and renderer
		null1.SetEditorMode(c4d.MODE_OFF)
		null1.SetRenderMode(c4d.MODE_OFF)

		self.libraryParent = null1
		# Create the material for the atom and connection
		matBlack = self.CreateMaterial('Black', c4d.Vector(0.1, 0.1, 0.1))
		matWhite = self.CreateMaterial('White', c4d.Vector(1, 1, 1))
		matGrey = self.CreateMaterial('Grey', c4d.Vector(0.5, 0.5, 0.5))
		#creat a hydrogen atom and a carbon atom
		self.hydrogen = self.CreateAtom('H', 50, null1, matWhite)
		self.carbon = self.CreateAtom('C', 100, null1, matBlack)
		#creat a connection object
		self.connection = self.CreateConnection('connection', 20, CONNECTION_LENGTH, null1, matGrey)

	def CreatIntermediateBlock(self, carbonlibrary, hydrogenLib, connectLib):
		#Creats null object named "Intermediateblock"
		intermediateBlockParent = self.CreatNull('Intermediateblock')
		# Creates the intermediate block that consists of instance objects
		carbon = self.CreatInstance('Carbon', carbonlibrary, intermediateBlockParent, c4d.Vector(0, 0, 0), c4d.Vector(0, 0, 0))	
		hydrogen1 = self.CreatInstance('Hydrogen1', hydrogenLib, intermediateBlockParent, c4d.Vector(460, 0, 0), c4d.Vector(0, 0, 0))
		hydrogen2 = self.CreatInstance('Hydrogen2', hydrogenLib, intermediateBlockParent, c4d.Vector(0, 460, 0), c4d.Vector(0, 0, 0))
		connection1 = self.CreatInstance('Connection1', connectLib, intermediateBlockParent, c4d.Vector(195, 0, 0), c4d.Vector(0, 0, 90))
		connection2 = self.CreatInstance('Connection2', connectLib, intermediateBlockParent, c4d.Vector(0, 195, 0), c4d.Vector(0, 0, 0))
		return intermediateBlockParent
	
	def CreatConnectionBlock(self, connectLib):
		#Creats null object named "Connectionblock"
		connectionBlockParent = self.CreatNull('Connectionblock')
		# Creates the connection block that consists of instance objects
		connection1 = self.CreatInstance('Connection1', connectLib, connectionBlockParent, c4d.Vector(0, 0, 0), c4d.Vector(0, 0, 0))
		return connectionBlockParent

class MoleculeLinearAlkane(Molecule):
	def CreateEndingBlock(self, carbonlibrary, hydrogenLib, connectLib):
		#Creats null object named "Endingblock"
		endingBlockParent = self.CreatNull('Endingblock')
		# Creates the ending block that consists of instance objects
		carbon = self.CreatInstance('Carbon', carbonlibrary, endingBlockParent, c4d.Vector(0, 0, 0), c4d.Vector(0, 0, 0))	
		hydrogen1 = self.CreatInstance('Hydrogen1', hydrogenLib, endingBlockParent, c4d.Vector(460, 0, 0), c4d.Vector(0, 0, 0))
		hydrogen2 = self.CreatInstance('Hydrogen2', hydrogenLib, endingBlockParent, c4d.Vector(0, 460, 0), c4d.Vector(0, 0, 0))
		hydrogen3 = self.CreatInstance('Hydrogen3', hydrogenLib, endingBlockParent, c4d.Vector(0, 0, 460), c4d.Vector(0, 0, 0))
		connection1 = self.CreatInstance('Connection1', connectLib, endingBlockParent, c4d.Vector(195, 0, 0), c4d.Vector(0, 0, 90))   
		connection2 = self.CreatInstance('Connection2', connectLib, endingBlockParent, c4d.Vector(0, 195, 0), c4d.Vector(0, 0, 0))
		connection3 = self.CreatInstance('Connection3', connectLib, endingBlockParent, c4d.Vector(0, 0, 195), c4d.Vector(0, 90, 0))
		return endingBlockParent
	
	def CreatMetheanBlock(self, carbonlibrary, hydrogenLib, connectLib):
		#Creats null object named "Metheanblock"
		methanBlockParent = self.CreatNull('Metheanblock')
		# Creates the methean block that consists of instance objects
		carbon = self.CreatInstance('Carbon', carbonlibrary, methanBlockParent, c4d.Vector(0, 0, 0), c4d.Vector(0, 0, 0))	
		hydrogen1 = self.CreatInstance('Hydrogen1', hydrogenLib, methanBlockParent, c4d.Vector(-460, 0, 0), c4d.Vector(0, 0, 0))
		hydrogen2 = self.CreatInstance('Hydrogen2', hydrogenLib, methanBlockParent, c4d.Vector(0, -460, 0), c4d.Vector(0, 0, 0))
		hydrogen3 = self.CreatInstance('Hydrogen3', hydrogenLib, methanBlockParent, c4d.Vector(0, 0, -460), c4d.Vector(0, 0, 0))
		hydrogen4 = self.CreatInstance('Hydrogen4', hydrogenLib, methanBlockParent, c4d.Vector(0, 0, 460), c4d.Vector(0, 0, 0))
		hydrogen5 = self.CreatInstance('Hydrogen5', hydrogenLib, methanBlockParent, c4d.Vector(0, 460, 0), c4d.Vector(0, 0, 0))
		hydrogen6 = self.CreatInstance('Hydrogen6', hydrogenLib, methanBlockParent, c4d.Vector(460, 0, 0), c4d.Vector(0, 0, 0))
		connection1 = self.CreatInstance('Connection1', connectLib, methanBlockParent, c4d.Vector(195, 0, 0), c4d.Vector(0, 0, 90))   
		connection2 = self.CreatInstance('Connection2', connectLib, methanBlockParent, c4d.Vector(0, 195, 0), c4d.Vector(0, 0, 0))
		connection3 = self.CreatInstance('Connection3', connectLib, methanBlockParent, c4d.Vector(0, 0, 195), c4d.Vector(0, 90, 0))
		connection4 = self.CreatInstance('Connection4', connectLib, methanBlockParent, c4d.Vector(0, 0, -195), c4d.Vector(0, 90, 0))
		connection5 = self.CreatInstance('Connection5', connectLib, methanBlockParent, c4d.Vector(0, -195, 0), c4d.Vector(0, 0, 0))
		connection6 = self.CreatInstance('Connection6', connectLib, methanBlockParent, c4d.Vector(-195, 0, 0), c4d.Vector(0, 0, 90))
		return methanBlockParent
	
	def Generate(self):
		# TODO: Implement
		self.CreateLibrary("Library", "Black", "White", "Grey", "Carbon", "Hydrogen", "Connection")
		print('Generating linear alkane: mIdx = ', self.moleculeIdx)
		self.CreatNull(str(self.moleculeIdx))
		
		numberOfIntermediateBlocks = self.moleculeIdx - 2 #defines how many intermediate blocks will be created based on the number of molecules
		numberOfConnectionBlocks = self.moleculeIdx - 1 #defines how many connection blocks will be created based on the number of molecules
		
		#creating a methan molecule
		if self.moleculeIdx == 1:
			methan = self.CreatMetheanBlock(self.carbon, self.hydrogen, self.connection)
			methan.SetAbsPos(c4d.Vector(0, 0, 0))
			methan.SetRelRot(self.DegToRad(c4d.Vector(0, 0, 0)))
			return
		
		#creating a ethan molecule
		if self.moleculeIdx == 2:
			ethan = self.CreateEndingBlock(self.carbon, self.hydrogen, self.connection)
			ethan.SetAbsPos(c4d.Vector(0, 0, 0))
			ethan.SetRelRot(self.DegToRad(c4d.Vector(144.7356, -30, 35.2644)))
			ethan2 = self.CreateEndingBlock(self.carbon, self.hydrogen, self.connection)
			ethan2.SetAbsPos(c4d.Vector(400, 0, 0))
			ethan2.SetRelRot(self.DegToRad(c4d.Vector(324.7356, -30, 35.2644)))
			#creates the connectionBLocks for the ethan molecule
			connectionBlock = self.CreatConnectionBlock(self.connection)
			connectionBlock.SetAbsPos(c4d.Vector(200, 0, 0))
			connectionBlock.SetRelRot(self.DegToRad(c4d.Vector(0, 0, 90)))
			return
		
		# Creating the starting- and ending- block
		startingBlock = self.CreateEndingBlock(self.carbon, self.hydrogen, self.connection)
		startingBlock.SetAbsPos(c4d.Vector(0, 0, 0))
		startingBlock.SetRelRot(self.DegToRad(c4d.Vector(144.7356, -30, 35.2644)))

		x=(numberOfIntermediateBlocks+1)*200
		endingBlock = self.CreateEndingBlock(self.carbon, self.hydrogen, self.connection)
		endingBlock.SetAbsPos(c4d.Vector(x, 400, 0))
		endingBlock.SetRelRot(self.DegToRad(c4d.Vector(324.7356, -30, 35.2644 ))) #sets the rotation of the ending block
		#if the number of molecules is even, then the ending block will be placed 400 units up on the y-axis
		#else the ending block will be placed 400 units down on the y-axis
		if numberOfIntermediateBlocks % 2 == 0:
			endingBlock.SetAbsPos(c4d.Vector(x, 400, 0))
		else:
			endingBlock.SetAbsPos(c4d.Vector(x, 0, 0))

			#loop for creating the intermediate blocks based on the number of "molecule index -2" see in line 129
		for i in range(numberOfIntermediateBlocks):
			x=(i+1)*200
			isEven = (i % 2) == 0 #checks if the number of intermediate blocks is even or odd
			intermediateBlock = self.CreatIntermediateBlock(self.carbon, self.hydrogen, self.connection)
			if isEven: 	#checks if the number is even, then it places the intermediate block 200 units up on the y-axis and 200 units to the right on the x-axis
				intermediateBlock.SetAbsPos(c4d.Vector(x, 400, 0))
				intermediateBlock.SetRelRot(self.DegToRad(c4d.Vector(0, 0, 315)))
			else: 	#if the number is odd, then it places the intermediate block 200 units down on the y-axis and duble the amount of units to the right on the x-axis
				intermediateBlock.SetAbsPos(c4d.Vector(x, 0, 0))
				intermediateBlock.SetRelRot(self.DegToRad(c4d.Vector(0, 0, 135)))
		#if the numberOfIntermediateBlocks is even rotate the intermediateBlock 90 degrees on the y-axis, els rotate the intermediateBlock 180 degrees on the z-axis
			if isEven:
				intermediateBlock.SetRelRot(self.DegToRad(c4d.Vector(90, 0, 315)))
			else:
				intermediateBlock.SetRelRot(self.DegToRad(c4d.Vector(90, 0, 135)))

		#creates the connectionBLocks based on the number of "molecule index -1" see in line 130
		for i in range(numberOfConnectionBlocks):
			x=(i*200+200/2)
			connectionBlock = self.CreatConnectionBlock(self.connection)
			connectionBlock.SetAbsPos(c4d.Vector(x, 200, 0))
			connectionBlock.SetRelRot(self.DegToRad(c4d.Vector(0, 0, 0)))
			#rotates the connectionblock based on if the numberOfConnectionBlocks is even or odd
			if i % 2 == 0:
				connectionBlock.SetRelRot(self.DegToRad(c4d.Vector(0, 0, -330)))
			else:
				connectionBlock.SetRelRot(self.DegToRad(c4d.Vector(0, 0, 330)))
		return
			
	pass

class MoleculeCyclicAlkane(Molecule):
	def Generate(self):
		# TODO: Implement
		#Creats the library for creating cyclic alkane
		self.CreateLibrary("Library", "Black", "White", "Grey", "Carbon", "Hydrogen", "Connection")
		print('Generating cyclic alkane: mIdx = ', self.moleculeIdx)
		self.CreatNull(str(self.moleculeIdx)) #add later the name of the molecule (the userInput)

		#Defines the math needed to know how many connections and intermediate blocks will be needed.
		numberOfIntermediateBlocks = self.moleculeIdx
		numberOfConnectionBlocks = self.moleculeIdx
		#defines the math needed to know where to position the intermidiate blocks
		#For the cyclic alkane, the intermediate blocks will be placed in an imaginery circle
		#The radius of the circle is 200 units
		#The molecules will be placed 100 units from the center of the circle (definign the radius), the center is at 0,0,0
		#The angle between each intermediate block is 360/moleculeIdx
		alphaDeg = 360/numberOfIntermediateBlocks
		alphaRad = c4d.utils.DegToRad(alphaDeg)
		
		lastRotation = alphaDeg #defines the last rotation of the intermediate block
		#A for loop will be used to create the intermediate blocks based on the number of molecules	(moleculeIdx/numberOfIntermediateBlocks)
		for i in range(numberOfIntermediateBlocks):

			molRadius = CONNECTION_LENGTH / math.sqrt(2*(1 - math.cos(alphaRad)))
			# molRadius = 200

			currentAlphaRad = i * alphaRad
			sn, cs = c4d.utils.SinCos(currentAlphaRad)
			y = molRadius * sn
			x = molRadius * cs
			print(x, y)

			rotation = lastRotation - alphaDeg 

			#creates the connectionBLocks based on the number of "molecule index" 
			connectionBlock = self.CreatConnectionBlock(self.connection)
			#Sets the conectionblock 225 units down on the y axis
			connectionBlock.SetAbsPos(c4d.Vector(0, -CONNECTION_LENGTH/2, 0))

			#creats a null object named "PosOffset" and places it in the center of the circle
			posOffset = self.CreatNull('PosOffset'+str(i))
			#inserts the connectionblock under the Null object known as "PosOffset"
			connectionBlock.InsertUnder(posOffset)

			# posOffset.SetAbsPos(c4d.Vector(x, y, 0))
			#rotates the "PosOffset" -60 degrees on the z-axis
			# posOffset[c4d.ID_BASEOBJECT_ROTATION_ORDER] = c4d.ID_BASEOBJECT_ROTATION_ORDER_XYZ
			

			# # Set the PosOffset position to the intermediateBlock position
			# posOffset.SetAbsPos(intermediateBlock.GetAbsPos())


			#Creates the first intermediate block with sn, cs, x and y and repeats it for the number of molecules
			intermediateBlock = self.CreatIntermediateBlock(self.carbon, self.hydrogen, self.connection)

			
			intermediateBlock[c4d.ID_BASEOBJECT_ROTATION_ORDER] = c4d.ID_BASEOBJECT_ROTATION_ORDER_XYZ
			#rotates the intermediateBlock 45 degres on the z-axis for each new intermediateBlock
			# intermediateBlock.SetRelRot(self.DegToRad(c4d.Vector(-90, -45, 0)))
			intermediateBlock.SetRelRot(self.DegToRad(c4d.Vector(-90, -45, rotation)))
			#rotates the following intermediateBlock 45 degres on the z-axis for each new intermediateBlock
			
			intermediateBlock.SetAbsPos(c4d.Vector(x, y, 0))	

			
			# Set the PosOffset position to the intermediateBlock position
			posOffset.SetAbsPos(intermediateBlock.GetAbsPos())
			posOffset.SetRelRot(self.DegToRad(c4d.Vector(0, 0, rotation + alphaDeg / 2)))
			# posOffset.InsertUnder(intermediateBlock)

			lastRotation = rotation #updates the last rotation to the current rotation


# Parses the user's input and returns the molecule index (or -1 if invalid)
def ParseUserInputAndCreateMolecule(userInput: str):
	# return MoleculeCyclicAlkane(354)
	# Check if the first user input is an uppercase "C"
	if userInput[0] != 'C':
		print("Invalid input: first character must be 'C'")
		return None

	# Find the index of 'H' in the userInput
	hIndex = userInput.find('H')

	# Check if there is an 'H' in the userInput
	if hIndex == -1:
		print("Invalid input: no 'H' found")
		return None
	
	# Check if the input is "C2H4"
	if userInput == 'C2H4':
		print("Invalid input: this molecule does not exist")
		return None

	# Check if there is no number between 'C' and 'H' and the number after 'H' is not 4
	if hIndex == 1:
		if userInput[1:] == 'H4':
			return MoleculeLinearAlkane(1)
		else:
			print("Invalid input: the number after 'H' should be 4")
			return None


	# Extract the number following the 'C' and before the 'H'
	moleculeIdx = int(userInput[1:hIndex])

	# Extract the numbers after 'C' and 'H'
	cNumber = int(userInput[1:hIndex])
	hNumber = int(userInput[hIndex+1:])

	# Extract the numbers after 'C' and 'H'
	cNumber = int(userInput[1:hIndex])
	hNumber = int(userInput[hIndex+1:])

	# Check if the number after 'H' is twice the number after 'C'
	if hNumber == cNumber * 2:
		# If the input is valid, return a new MoleculeCyclicAlkane with the number after 'C' as the molecule index
		return MoleculeCyclicAlkane(cNumber)
	elif hNumber == cNumber * 2 + 2:
		# If the input is valid, return a new MoleculeLinearAlkane with the number after 'C' as the molecule index
		return MoleculeLinearAlkane(cNumber)
	else:
		print("Invalid input: the number after 'H' should be twice the number after 'C' for cyclic alkane or twice the number after 'C' plus 2 for linear alkane")
		return None
	
	# returns either LA or CA (or None if invalid)
 
	# # TODO: Implement
	# if 1 == 1:
	# 	return MoleculeLinearAlkane(3)
	# elif 2 == 2:
	# 	return MoleculeCyclicAlkane(4)
	#return MoleculeLinearAlkane(3)
	#return None


class ExampleDialog(c4d.gui.GeDialog):
	TEXT_FIELD_ID = 1000
	CREATE_BUTTON_ID = 1001
	DELET_BUTTON_ID = 1002
	HELP_BUTTON_ID = 1003

	def CreateLayout(self):
		#Adds a text that tells the user to write the formula in the text field
		self.SetTitle("Molecule Creator")
		self.AddEditText(self.TEXT_FIELD_ID, c4d.BFH_SCALEFIT, initw=300)
		self.SetString(self.TEXT_FIELD_ID, "Write here your Formular, z.B: C4H8 / C4H10")  # Default text
		self.AddSeparatorH(c4d.BFH_SCALE)
		self.AddButton(self.CREATE_BUTTON_ID, c4d.BFH_CENTER, name="Create Molecule")
		self.AddSeparatorH(c4d.BFH_SCALE)
		self.AddButton(self.DELET_BUTTON_ID, c4d.BFH_CENTER, name="Delete Everything")
		self.AddSeparatorH(c4d.BFH_SCALE)
		self.AddButton(self.HELP_BUTTON_ID, c4d.BFH_CENTER, name="Help?")
		return True

	def delete_all_objects(self): #takes all objects in the active document and delets them
		global doc
		doc = documents.GetActiveDocument()
		allObjects = doc.GetObjects()
		for obj in allObjects:
			obj.Remove()
		
		allMats = doc.GetMaterials()
		for obj in allMats:
			obj.Remove()


		c4d.EventAdd()  # Notify Cinema 4D that the document has been changed

	def Command(self, id, msg):
		if id == self.HELP_BUTTON_ID:
			c4d.gui.MessageDialog("""
			Here is some information on how to use the plugin!	
						 			
			1. Write the formula of the molecule you want to create in the text	 
			field.	
			2. Click on the "Create Molecule" button to create the molecule.	
			3. Click on the "Delete Everything" button to delete all objects in the 	
			scene.	
						 			
			4. The plugin can create linear alkanes and cyclic alkanes.	
			5. For linear alkanes, the formula should be in the form CnH2n+2.	
			6. For cyclic alkanes, the formula should be in the form CnH2n.	
			7. "n" is the number of carbon atoms in the molecule.	
										
			8. For example, to create a propane molecule, you should write C3H8.	
			9. For cyclopropane, you should write C3H6.	
			10. It is important that the formula is correct, otherwise the molecule 	
			will not be created.	
			11. The "Letters" have to be uppercase and the numbers have to be 	
			mathamatically correct.	
										
			12. The plugin will create the molecule in the center of the scene.	
							
			13. If you have any questions, feel free to ask per email under 	
			"c_neusschulz@maxon.net". (you can also report bugs here!)	
							
			Enjoy! :)""")
		# if id == self.CREATE_BUTTON_ID:
		# 	userInput = self.GetString(self.TEXT_FIELD_ID)
		# 	molecule = ParseUserInputAndCreateMolecule(userInput)
		# 	if molecule is not None:
		# 		molecule.CreateMolecule() #"""here is a problem with the CreateMolecule function, it is not defined in the Molecule class."""
		global doc
		if id == self.CREATE_BUTTON_ID:
			doc = documents.GetActiveDocument()

			# Get the text entered by the user
			userInput = self.GetString(self.TEXT_FIELD_ID)

			# Parse the user's input and create the molecule
			molecule = ParseUserInputAndCreateMolecule(userInput)
			if molecule is None:
				gui.MessageDialog('''Invalid input! 
Please enter a valid formula (e.g. C2H6, C3H8, C4H10, ...)''')
			else:
				molecule.Generate()
				c4d.EventAdd()
		elif id == self.DELET_BUTTON_ID:
			self.delete_all_objects()
		
		return True	


class ExampleDialogCommand(c4d.plugins.CommandData):
	"""Command Data class that holds the ExampleDialog instance."""
	dialog = None
	
	def Execute(self, doc):
		"""Called when the user executes a command via either CallCommand() or a click on the Command from the extension menu.

		Args:
			doc (c4d.documents.BaseDocument): The current active document.

		Returns:
			bool: True if the command success.
		"""
		# Creates the dialog if its not already exists
		if self.dialog is None:
			self.dialog = ExampleDialog()

		# Opens the dialog
		return self.dialog.Open(dlgtype=c4d.DLG_TYPE_ASYNC, pluginid=PLUGIN_ID, defaultw=400, defaulth=32)

	def RestoreLayout(self, sec_ref):
		"""Used to restore an asynchronous dialog that has been placed in the users layout.

		Args:
			sec_ref (PyCObject): The data that needs to be passed to the dialog.

		Returns:
			bool: True if the restore success
		"""
		# Creates the dialog if its not already exists
		if self.dialog is None:
			self.dialog = ExampleDialog()

		# Restores the layout
		return self.dialog.Restore(pluginid=PLUGIN_ID, secret=sec_ref)


# main
if __name__ == "__main__":
	# Registers the plugin
	c4d.plugins.RegisterCommandPlugin(id=PLUGIN_ID,
									  str="Molecule Creator Plugin",
									  info=0,
									  help="Display a basic GUI",
									  dat=ExampleDialogCommand(),
									  icon=None)