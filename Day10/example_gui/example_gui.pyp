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
from c4d import documents

doc: c4d.documents.BaseDocument


# Be sure to use a unique ID obtained from www.plugincafe.com
PLUGIN_ID = 1234897

USER_INPUT = "C4H10"

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
	def CreateInstance(self, name:str, RefrencObject, parent, position=c4d.Vector(), rotation=c4d.Vector()):
		instance = c4d.BaseObject(c4d.Oinstance)
		doc.InsertObject(instance, parent, None)
		instance.SetName(name)
		instance.SetRefrenceObject(RefrencObject)
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
		# Create the material for the atom and connection
		matBlack = self.CreateMaterial('Black', c4d.Vector(0.1, 0.1, 0.1))
		matWhite = self.CreateMaterial('White', c4d.Vector(1, 1, 1))
		matGrey = self.CreateMaterial('Grey', c4d.Vector(0.5, 0.5, 0.5))
		#creat a hydrogen atom and a carbon atom
		hydrogen = self.CreateAtom('H', 50, null1, matWhite)
		carbon = self.CreateAtom('C', 100, null1, matBlack)
		#creat a connection object
		connection = self.CreateConnection('connection', 25, 100, null1, matGrey)
		return (null1, matBlack, matWhite, matGrey, carbon, hydrogen, connection)
		

class MoleculeLinearAlkane(Molecule):
	def Generate(self):
		# TODO: Implement
		self.CreateLibrary("Library", "Black", "White", "Grey", "Carbon", "Hydrogen", "Connection")
		print('Generating linear alkane: mIdx = ', self.moleculeIdx)
		self.CreatNull(str(self.moleculeIdx))
	
		pass

class MoleculeCyclicAlkane(Molecule):
	def Generate(self):
		# TODO: Implement
		print('Generating cyclic alkane: mIdx = ', self.moleculeIdx)
		pass




def CreateMolecule(userInput: str):
	# checksuser input
	# returns either LA or CA (or None if invalid)
 
	# TODO: Implement
	if 1 == 1:
		return MoleculeLinearAlkane(3)
	elif 2 == 2:
		return MoleculeCyclicAlkane(4)
	return None

class ExampleDialog(c4d.gui.GeDialog):

	
	def CreateLayout(self):
		"""This Method is called automatically when Cinema 4D Create the Layout (display) of the Dialog."""
		# Defines the title of the Dialog
		self.SetTitle("This is a Molecule Creator5")

		# Creates a button to create a molecule	
		# Creates a Ok and Cancel Button
		self.AddDlgGroup(c4d.DLG_OK | c4d.DLG_CANCEL)
		#Change the name of the Ok button to "Create"
		self.SetString(c4d.DLG_OK, "Create")
		# Add a description
		self.AddStaticText(1000, c4d.BFH_LEFT, name="This is a molecule creator5")
		# Add a separator
		self.AddSeparatorH(100)
		return True

	def Command(self, messageId, bc):
		"""This Method is called automatically when the user clicks on a gadget and/or changes its value this function will be called.
		It is also called when a string menu item is selected.

		Args:
			messageId (int): The ID of the gadget that triggered the event.
			bc (c4d.BaseContainer): The original message container.

		Returns:
			bool: False if there was an error, otherwise True.
		"""
		global doc
		# User click on Ok buttonG
		if messageId == c4d.DLG_OK:
			doc = documents.GetActiveDocument()
			print("User created propan2")
			# Creates a cube in cinema 4D when the user click on the Create button
			
			molecule = CreateMolecule(USER_INPUT)
			molecule.Generate()

			# Close the Dialog when the user click on the Create button
			self.Close()

			c4d.EventAdd()
			return True
		

		# User click on Cancel button
		elif messageId == c4d.DLG_CANCEL:
			print("User Click on Cancel")

			# Close the Dialog
			self.Close()
			return True

		return True
	
	# #when the user clicks on the Creat button a cube is created
	# def CreateMolecule(self):
	# 	active_doc = documents.GetActiveDocument()  # Get the active document
	# 	# Create a cube
	# 	cube = c4d.BaseObject(c4d.Ocube)
	# 	# Insert the cube into the document
	# 	active_doc.InsertObject(cube)
	# 	# Update the Cinema 4D UI
	# 	c4d.EventAdd()
	# 	return True

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
									  str="Py-CommandData Dialog",
									  info=0,
									  help="Display a basic GUI",
									  dat=ExampleDialogCommand(),
									  icon=None)