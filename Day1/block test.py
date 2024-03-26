import c4d
import typing

doc: c4d.documents.BaseDocument
op: typing.Optional[c4d.BaseObject]

def ConstructPolygonObject() -> None:

	print ("\n\n--- ConstructPolygonObject Example -----------------------------------------------")
	

	cube = c4d.PolygonObject(pcnt=8, vcnt=6)
	if not isinstance(cube, c4d.PolygonObject):
		raise MemoryError("Could not allocate polygon object.")
	points = cube.GetAllPoints()
	

	mg = cube.GetMg()

	polygons = cube.GetAllPolygons()

	print (f"\nPoints and polygons of '{cube.GetName()}' after allocation:")
	print(f"{cube.GetAllPoints() = }")
	print(f"{cube.GetAllPolygons() = }")


	size = 200.0

	points = [
		c4d.Vector(0, size, 0),            # Point 0
		c4d.Vector(size, size, 0),         # Point 1
		c4d.Vector(size, size, size),      # Point 2
		c4d.Vector(0, size, size),         # Point 3
		c4d.Vector(0, 0, 0),               # Point 4
		c4d.Vector(size, 0, 0),            # Point 5
		c4d.Vector(size, 0, size),         # Point 6
		c4d.Vector(0, 0, size),            # Point 7
	]

	quad = c4d.CPolygon(0, 1, 2, 3)

	print (f"\n{quad.a = }, {quad.b = }, {quad.c = }, {quad.d = }")

	inverted = c4d.CPolygon(3, 2, 1, 0)

	tri = c4d.CPolygon(0, 1, 2, 2)

	polygons = [
		c4d.CPolygon(3, 2, 1, 0),

		c4d.CPolygon(4, 5, 6, 7),

		c4d.CPolygon(0, 4, 7, 3),

		c4d.CPolygon(1, 2, 6, 5),

		c4d.CPolygon(0, 1, 5, 4),

		c4d.CPolygon(3, 7, 6, 2),
	]

	cube.SetAllPoints(points)

	for i, cpoly in enumerate(polygons):
		cube.SetPolygon(i, cpoly)

	cube.Message(c4d.MSG_UPDATE)

	print (f"\nPoints and polygons of '{cube.GetName()}' after modification:")
	print(f"{cube.GetAllPoints() = }")
	print(f"{cube.GetAllPolygons() = }")

	return cube

def main(doc: c4d.documents.BaseDocument) -> None:
	# op[c4d.PRIM_CUBE_LEN,c4d.VECTOR_X] = 400
	# c4d.EventAdd()
	# return

	cube = ConstructPolygonObject()

	if not doc.StartUndo():
		raise RuntimeError("Could not open undo stack.")

	doc.InsertObject(cube)

	if not doc.AddUndo(c4d.UNDOTYPE_NEWOBJ, cube):
		raise RuntimeError("Could not add undo item.")

	if not doc.EndUndo():
		raise RuntimeError("Could not close undo stack.")

	#doc.SetMode(c4d.Mpolygons)
	doc.SetActiveObject(cube, c4d.SELECTION_NEW)

	c4d.EventAdd()
if __name__ == '__main__':
	c4d.CallCommand(13957)
main(doc)