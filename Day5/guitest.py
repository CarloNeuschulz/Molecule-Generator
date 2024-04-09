import c4d
from c4d import gui
import typing
import mxutils

class MyDialog(gui.GeDialog):
    def CreateLayout(self):
        # Add a button to the dialog
        self.AddButton(1000, c4d.BFH_CENTER, name="Create Model")
        return True

    def Command(self, id, msg):
        if id == 1000:  # Button ID
            # Call your function to create the model
            self.create_model()
        return True

    def create_model(self):
        # Insert your model creation script here
        # Your existing model creation script

        
        # Accessing Cinema 4D's active document
        doc = c4d.documents.GetActiveDocument()

        def foo():
            return {
                "a": mxutils.CheckType(c4d.BaseObject(c4d.Osphere)),
                "b": mxutils.CheckType(c4d.BaseObject(c4d.Ocylinder))
            }

        def CreateMaterial(name: str, color: c4d.Vector) -> c4d.BaseMaterial:
            mat = c4d.BaseMaterial(c4d.Mmaterial)
            mat.SetName(name)
            mat[c4d.MATERIAL_COLOR_COLOR] = color
            doc.InsertMaterial(mat)
            return mat

        def InsertMaterialTag(op, m):
            tag = c4d.BaseTag(5616)
            tag[c4d.TEXTURETAG_MATERIAL] = m
            tag[c4d.TEXTURETAG_PROJECTION] = 6  # UVW Mapping
            op.InsertTag(tag)
        
        def CreateAtom(name, radius, parent):
            atom = c4d.BaseObject(c4d.Osphere)
            doc.InsertObject(atom, None, None)
            atom.SetName(name)
            atom[c4d.PRIM_SPHERE_RAD] = radius

        def CreateNull(name):
            # TODO: (Carlo) put implementation here
            pass

        def CreateInstance(name, referenceObjecet, parentObject):
            # TODO: (Carlo) put implementation here
            pass

        
        # Creating Library
        oxygen = CreateAtom('Oxygen', 100)
        hydrogen = CreateAtom('Hydrogen', 50)
        connect = CreatConnection('Connection', 20)
        null = CreateNull('Library')
        
        # Creating H2O

        #null1 = mxutils.CheckType(c4d.BaseObject(c4d.Onull))
        # doc.InsertObject(null1, None, None)
        #null1.SetName("H2O")

        null1 = CreateNull("h2o")

        instance = mxutils.CheckType(c4d.InstanceObject())
        doc.InsertObject(instance, null1, None)
        instance.SetName("Oxygen")
        doc.SetActiveObject(instance)
        instance.SetReferenceObject(oxygen)

        m = c4d.Matrix(v1=c4d.Vector(0, 1, 0),
                        v2=c4d.Vector(-1, 0, 0),
                        v3=c4d.Vector(0, 0, 1))
        instance = CreateInstance(name, oxygen, null1, pos, m)

        # hydrogen = mxutils.CheckType(c4d.BaseObject(c4d.Osphere))
        # doc.InsertObject(hydrogen, None, None)
        # hydrogen.SetName("hydrogen")
        # hydrogen[c4d.PRIM_SPHERE_RAD] = 50
        

        instance1 = mxutils.CheckType(c4d.InstanceObject())
        doc.InsertObject(instance1, null1, None)
        instance1.SetName("hydrogen")
        x_pos = 340
        y_pos = 0
        z_pos = 0
        instance1.SetAbsPos(c4d.Vector(x_pos, y_pos, z_pos))
        doc.SetActiveObject(instance1)
        instance1.SetReferenceObject(hydrogen)

        instance2 = mxutils.CheckType(c4d.InstanceObject())
        doc.InsertObject(instance2, null1, None)
        instance2.SetName("hydrogen2")
        x_pos = 0
        y_pos = 340
        z_pos = 0
        instance2.SetAbsPos(c4d.Vector(x_pos, y_pos, z_pos))
        doc.SetActiveObject(instance2)
        instance2.SetReferenceObject(hydrogen)

        connect = mxutils.CheckType(c4d.BaseObject(c4d.Ocylinder))
        doc.InsertObject(connect, None, None)
        connect.SetName("connect")
        m = c4d.Matrix(v1=c4d.Vector(0, 1, 0),
                        v2=c4d.Vector(-1, 0, 0),
                        v3=c4d.Vector(0, 0, 1))
        connect.SetMl(m)
        x_pos = 195
        y_pos = 0
        z_pos = 0
        connect.SetAbsPos(c4d.Vector(x_pos, y_pos, z_pos))
        connect[c4d.PRIM_CYLINDER_RADIUS] = 20

        instance1 = mxutils.CheckType(c4d.InstanceObject())
        doc.InsertObject(instance1, null1, None)
        instance1.SetName("connect")
        m = c4d.Matrix(v1=c4d.Vector(0, 1, 0),
                        v2=c4d.Vector(-1, 0, 0),
                        v3=c4d.Vector(0, 0, 1))
        instance1.SetMl(m)
        x_pos = 195
        y_pos = 0
        z_pos = 0
        instance1.SetAbsPos(c4d.Vector(x_pos, y_pos, z_pos))
        doc.SetActiveObject(instance1)
        instance1.SetReferenceObject(connect)

        instance2 = mxutils.CheckType(c4d.InstanceObject())
        doc.InsertObject(instance2, null1, None)
        instance2.SetName("connect2")
        x_pos = 0
        y_pos = 195
        z_pos = 0
        instance2.SetAbsPos(c4d.Vector(x_pos, y_pos, z_pos))
        # Makes instance object active (selected)
        doc.SetActiveObject(instance2)
        #Asseses the connect to the instance2 object
        instance2.SetReferenceObject(connect)
                



        #creats a null object called "Liabry"
        null = mxutils.CheckType(c4d.BaseObject(c4d.Onull))
        #Sets the position of the null object to 0/0/350
        null.SetAbsPos(c4d.Vector(0, 0, 350))
            #Sets the name of the null object to "Liabry"
        null.SetName("Liabry")
        #Adds the cylinder, the two spheres to the null object
        doc.InsertObject(null, None, None)
        connect.InsertUnder(null)
        oxygen.InsertUnder(null)
        hydrogen.InsertUnder(null)


        #Creates materials for the spheres and the cylinder
        matRed = CreateMaterial('Red', c4d.Vector(1, 0, 0))
        matWhite = CreateMaterial('White', c4d.Vector(1, 1, 1))
        matGrey = CreateMaterial('Grey', c4d.Vector(0.5, 0.5, 0.5))

        InsertMaterialTag(oxygen, matRed)
        InsertMaterialTag(hydrogen, matWhite)
        InsertMaterialTag(connect, matGrey)


        #Sets the null "libary" object to be invisible in the editor and renderer
        null.SetEditorMode(c4d.MODE_OFF)
        null.SetRenderMode(c4d.MODE_OFF)

        self.Close()


def main():
    # Create a dialog instance
    dlg = MyDialog()
    # Open the dialog
    dlg.Open(c4d.DLG_TYPE_MODAL_RESIZEABLE)

    #update the scene
    c4d.EventAdd()

if __name__ == '__main__':
    main()