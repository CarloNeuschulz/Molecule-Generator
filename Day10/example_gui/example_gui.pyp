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


# Be sure to use a unique ID obtained from www.plugincafe.com
PLUGIN_ID = 1234897


class ExampleDialog(c4d.gui.GeDialog):

	
	def CreateLayout(self):
		"""This Method is called automatically when Cinema 4D Create the Layout (display) of the Dialog."""
		# Defines the title of the Dialog
		self.SetTitle("This is a Molecule Creator2")

		# Creates a button to create a molecule	
		# Creates a Ok and Cancel Button
		self.AddDlgGroup(c4d.DLG_OK | c4d.DLG_CANCEL)
		#Change the name of the Ok button to "Create"
		self.SetString(c4d.DLG_OK, "Create")
		# Add a description
		self.AddStaticText(1000, c4d.BFH_LEFT, name="This is a molecule creator2")
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
		# User click on Ok buttonG
		if messageId == c4d.DLG_OK:
			print("User created propan2")
			# Creates a cube in cinema 4D when the user click on the Create button
			self.CreateMolecule()
			# Close the Dialog when the user click on the Create button
			self.Close()

			return True
		

		# User click on Cancel button
		elif messageId == c4d.DLG_CANCEL:
			print("User Click on Cancel")

			# Close the Dialog
			self.Close()
			return True

		return True
	
	#when the user clicks on the Creat button a cube is created
	def CreateMolecule(self):
		active_doc = documents.GetActiveDocument()  # Get the active document
		# Create a cube
		cube = c4d.BaseObject(c4d.Ocube)
		# Insert the cube into the document
		active_doc.InsertObject(cube)
		# Update the Cinema 4D UI
		c4d.EventAdd()
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
									  str="Py-CommandData Dialog",
									  info=0,
									  help="Display a basic GUI",
									  dat=ExampleDialogCommand(),
									  icon=None)