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
         
    #return c4d.BaseMaterial(c4d.Mmaterial)

def InsertMaterialTag(op, m):
    tag = c4d.BaseTag(5616) # Initialize a material tag
    tag[c4d.TEXTURETAG_MATERIAL] = m # Assign material to the material tag
    tag[c4d.TEXTURETAG_PROJECTION] = 6 #UVW Mapping
    op.InsertTag(tag) # Insert tag to the object

def main():
    # Creates "Oxygen" a sphere at 0/0/0 with a radius of 100
    oxygen = mxutils.CheckType(c4d.BaseObject(c4d.Osphere))
    #Inserts the sphere into the active document
    doc.InsertObject(oxygen, None, None)
    oxygen.SetName("Oxygen")
    #creats a null object called "H2O"
    null1 = mxutils.CheckType(c4d.BaseObject(c4d.Onull))
    #Inserts the null object into the active document
    doc.InsertObject(null1, None, None)
		#Sets the name of the null object to "H2O"
    null1.SetName("H2O")   
    #Creats instance object of the sphere
    instance = mxutils.CheckType(c4d.InstanceObject())
    #Inserts the instance object of the sphere into the active document
    doc.InsertObject(instance, null1, None)
    #rename instance to "Oxygen"
    instance.SetName("Oxygen")
    # Makes instance object active (selected)
    doc.SetActiveObject(instance)
    # Sets the instance reference object to the created cube
    instance.SetReferenceObject(oxygen)


	  #creats "Hydrogen" a sphere at 0/0/0 with a radius of 50
    hydrogen = mxutils.CheckType(c4d.BaseObject(c4d.Osphere))
	  #Inserts the "hydrogene" sphere into the active document
    doc.InsertObject(hydrogen, None, None)
    hydrogen.SetName("hydrogen")
	  #sets the radius of the "hydrogen" sphere to 50
    hydrogen[c4d.PRIM_SPHERE_RAD] = 50
	  #creats instance object of the "hydrogen" sphere
    instance1 = mxutils.CheckType(c4d.InstanceObject())
		#Inserts the instance object of the "hydrogen" sphere into the active document
    doc.InsertObject(instance1, null1, None)
    #rename instance to "hydrogen"
    instance1.SetName("hydrogen")
    #sets the position of the instance1 on the x axis to 340/0/0
    x_pos = 340
    y_pos = 0
    z_pos = 0
    instance1.SetAbsPos(c4d.Vector(x_pos, y_pos, z_pos))
    # Makes instance object active (selected)
    doc.SetActiveObject(instance1)
    # Sets the instance reference object to the created cube
    instance1.SetReferenceObject(hydrogen)
    #creats instance2 object of the "hydrogen" sphere
    instance2 = mxutils.CheckType(c4d.InstanceObject())
    #Inserts the instance2 object of the "hydrogen" sphere into the active document
    doc.InsertObject(instance2, null1, None)
    #rename instance to "hydrogen2"
    instance2.SetName("hydrogen2")
    #sets the position of the instance2 on the y axis to 0/340/0
    x_pos = 0
    y_pos = 340
    z_pos = 0
    instance2.SetAbsPos(c4d.Vector(x_pos, y_pos, z_pos))
    # Makes instance object active (selected)
    doc.SetActiveObject(instance2)
    # Sets the instance2 reference object to the created "hydrogen" sphere
    instance2.SetReferenceObject(hydrogen)





    #Creats a connection line as a cylinder
    connect = mxutils.CheckType(c4d.BaseObject(c4d.Ocylinder))
    #Inserts the cylinder into the active document
    doc.InsertObject(connect, None, None)
    connect.SetName("connect")
    #Sets the position of the cylinder to the sphere
    m = c4d.Matrix(v1=c4d.Vector( 0, 1, 0),
                	v2=c4d.Vector(-1, 0, 0),
                	v3=c4d.Vector( 0, 0, 1))
    connect.SetMl(m)
	  # Set the position of the cylinder
    x_pos = 195
    y_pos = 0
    z_pos = 0
    connect.SetAbsPos(c4d.Vector(x_pos, y_pos, z_pos))
	  #Set the radius of the cylinder to 20
    connect[c4d.PRIM_CYLINDER_RADIUS] = 20
	  #creats a instance object of the cylinder
    instance1 = mxutils.CheckType(c4d.InstanceObject())
		#Inserts the instance object of the cylinder into the active document
    doc.InsertObject(instance1, null1, None)
    #rename instance to "connect"
    instance1.SetName("connect")
    #Sets the position of the instance1 to the sphere
    m = c4d.Matrix(v1=c4d.Vector( 0, 1, 0),
                	v2=c4d.Vector(-1, 0, 0),
                	v3=c4d.Vector( 0, 0, 1))
    instance1.SetMl(m)
	  # Set the position of the instance1
    x_pos = 195
    y_pos = 0
    z_pos = 0
    instance1.SetAbsPos(c4d.Vector(x_pos, y_pos, z_pos))
    # Makes instance object active (selected)
    doc.SetActiveObject(instance1)
    # Sets the instance reference object to the created cylinder "connect"
    instance1.SetReferenceObject(connect)
    #creats a second instance object of the cylinder
    instance2 = mxutils.CheckType(c4d.InstanceObject())
    #Inserts the instance object of the cylinder into the active document
    doc.InsertObject(instance2, null1, None)
    #rename instance to "connect2"
    instance2.SetName("connect2")
	  # Set the position of the instance2
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