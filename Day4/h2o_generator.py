import c4d
import typing
import mxutils
doc: c4d.documents.BaseDocument
op: typing.Optional[c4d.BaseObject]
def foo():
	return {
        "a": mxutils.CheckType(c4d.BaseObject(c4d.Osphere)),
         "b": mxutils.CheckType(c4d.BaseObject(c4d.Ocylinder))}
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
    instance = mxutils.CheckType(c4d.InstanceObject())

		#Inserts the instance object of the "hydrogen" sphere into the active document
    doc.InsertObject(instance, null1, None)
    #rename instance to "hydrogen"
    instance.SetName("hydrogen")
    # Makes instance object active (selected)
    doc.SetActiveObject(instance)
    # Sets the instance reference object to the created cube
    instance.SetReferenceObject(hydrogen)




    #Creats a connection line as a cylinder
    connect = mxutils.CheckType(c4d.BaseObject(c4d.Ocylinder))

        #Inserts the cylinder into the active document
    doc.InsertObject(connect, None, None)
    connect.SetName("connect")

	#creats a instance object of the cylinder
    instance = mxutils.CheckType(c4d.InstanceObject())
    
		#Inserts the instance object of the cylinder into the active document
    doc.InsertObject(instance, null1, None)
    #rename instance to "connect"
    instance.SetName("connect")
    # Makes instance object active (selected)
    doc.SetActiveObject(instance)
    # Sets the instance reference object to the created cube
    instance.SetReferenceObject(connect)



    	#Sets the position of the cylinder to the sphere
    m = c4d.Matrix(v1=c4d.Vector( 0, 1, 0),
                	v2=c4d.Vector(-1, 0, 0),
                	v3=c4d.Vector( 0, 0, 1))
    connect.SetMl(m)

	   # Set the position of the cylinder
    x_pos = 140
    y_pos = 0
    z_pos = 0
    connect.SetAbsPos(c4d.Vector(x_pos, y_pos, z_pos))

	#Set the radius of the cylinder to 20
    connect[c4d.PRIM_CYLINDER_RADIUS] = 20





		#creats a null object called "Liabry"
    null = mxutils.CheckType(c4d.BaseObject(c4d.Onull))

	#Inserts the null object into the active document
    x_pos = 0
    y_pos = 0
    z_pos = 350
    connect.SetAbsPos(c4d.Vector(x_pos, y_pos, z_pos))

	#Sets the name of the null object to "Liabry"
    null.SetName("Liabry")

	#Adds the cylinder, the two spheres to the null object
    doc.InsertObject(null, None, None)
    connect.InsertUnder(null)
    oxygen.InsertUnder(null)
    hydrogen.InsertUnder(null)




    #update the scene
    c4d.EventAdd()


if __name__=='__main__':
    main()