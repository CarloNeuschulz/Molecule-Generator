import c4d
import typing
import mxutils
from c4d import gui
doc: c4d.documents.BaseDocument
op: typing.Optional[c4d.BaseObject]

# Define the molecules available in the dropdown
MOLECULES = {
    "H2O": "h2o",
    # Add more molecules as needed
}

class MyDialog(gui.GeDialog):
    def CreateLayout(self):
        # Add dropdown to select molecule
        self.AddComboBox(1000, c4d.BFH_SCALEFIT | c4d.BFH_LEFT, 200, 20, initw=100, specialalign=False)
        for name in MOLECULES.keys():
            self.AddChild(1000, 0, name)

        # Add button to create selected molecule
        self.AddButton(1001, c4d.BFH_CENTER, name="H2O")

        return True

    def Command(self, id, msg):
        if id == 1001:  # Create button pressed
            # Get selected molecule from dropdown
            index = self.GetLong(1000)
            molecule_name = self.GetString(1000, index)

            # Call function to create selected molecule
            self.create_molecule(molecule_name)
            exec(molecule + 
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

   
    if __name__=='__main__':
        main())  
            # Execute the main function of the molecule script
            c4d.EventAdd()  # Update the scene

def main():
    # Create a dialog instance
    dlg = MyDialog()
    # Open the dialog
    dlg.Open(c4d.DLG_TYPE_MODAL_RESIZEABLE)

if __name__ == '__main__':
    main()
