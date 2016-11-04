from pyplasm import *
import numpy

"""
roundCoordinates is a function that given a list of vertices, round the coordinates of every vertex,
if the vertex has a coordinate smaller than 0.001 it will be rounded to 0, alternatively it will
be rounded to the first decimal.
@param vertsList: a list containing vertices
"""
def roundCoordinates(vertsList):
	for j in range(len(vertsList)):
		for i in range(len(vertsList[j])):
			if(abs(vertsList[j][i]) < 0.001):
				vertsList[j][i] = 0
			else:
				vertsList[j][i] = round(vertsList[j][i],1)

"""
point2Cells is a function that given the result of UKPOL() function, build a dictionary in which every key
represent a vertex, and every value represent the list of incident faces on the vertex.
@param listUkpol: result of UKPOL() function call
@return dictionary: dictionary cointaining key and values as described above (vertex:[faces])
""" 
def point2Cells(listUkpol):
	dictionary = {}
	verts = listUkpol[0]
	roundCoordinates(verts)
	cells = listUkpol[1]
	for cell in cells:
		for label in cell:
			point = str(verts[int(label)-1])
			if(point not in dictionary):
				dictionary[point] = []
			dictionary[point].append(label)
	return dictionary

"""
planarSurfaces is a function that given a list of vertices and the corrisponding 
list of convex cells, check the complanarity of the vertices composing every convex cells.
@see https://en.wikipedia.org/wiki/Coplanarity: for better understanding about the resolution method adopted
@param verts: list of vertices
@param cells: list of convex cells, according to the list of vertices passed as first argument
@return Boolean: True if every face is composed by coplanar vertices, False otherwise

"""
def planarSurfaces(verts, cells):
	#rounding coordinates 
	roundCoordinates(verts)

	for cell in cells:
		if(len(cell) > 3):
			#building matrix
			matrix = []
			lastpoint = cell[-1]
			for label in cell:
				point = verts[int(label)-1]
				row = []
				for i in range(len(point)):
					row.append(point[i]-verts[lastpoint-1][i])
				matrix.append(row)
			#calculating matrix rank
			A = numpy.matrix(matrix)
			dim = numpy.linalg.matrix_rank(A)
			#the points are coplanar if the matrix has rank 2 or less
			if(dim > 2):
				return False
	return True
"""
removeBaseCells is a function that given a list of vertices and the corrisponding list of convex 
cells, removes the cells in which every vertex, that compose the convex cells, has a Z-coordinate of value 0.
This function is used to create an opened roof on the bottom side.
@param verts: list of vertices
@param cells: list of convex cells, according to the list of vertices passed as first argument
@return cleaned: list of convex cells without the cells described above
"""
def removeBaseCells(cells, verts):
	cleaned = []
	for i in range(len(cells)-1):
		isBaseCell = True
		for pointIndex in cells[i]:
			if(verts[pointIndex-1][2] != 0):
				isBaseCell = False
		if(not isBaseCell):
			cleaned.append(cells[i])
	return cleaned
"""
ggpl_L_and_U_roof_builder is a function that given a list of vertices and the corrisponding list of convex 
cells, build an HPC model of a L/U roof and of its beam structure.
@param verts: list of vertices
@param cells: list of convex cells, according to the list of vertices passed as first argument
@return HPCmodel: the HPC model of the roof and its beam structure
"""
def ggpl_L_and_U_roof_builder(verts, cells):

	if(not planarSurfaces(verts, cells)):
		return None

	#roofModel used to construct the beam structure
	roofModel = MKPOL([verts,cells, None])

	#cleaning the cells
	cells = removeBaseCells(cells,verts)

	#building top roof
	roof = MKPOL([verts,cells,None])
	roof = OFFSET([.1,.1,.1])(roof)
	roof = T([3])([.1])(roof)
	roof = COLOR(Color4f([1/255., 61/255., 31/255.,1]))(roof)

	#building beam structure
	beams = OFFSET([.1,.1,.1])(SKEL_1(roofModel))
	beams = S([3])(.95)(beams)
	beams = COLOR(Color4f([132/255., 54/255., 9/255.,1]))(beams)

	#returning the result roof+beams
	return STRUCT([roof,beams])



#verts = [[0,0,0],[0,3,0],[6,3,0],[6,9,0],[9,9,0],[9,0,0],[1.5,1.5,2],[7.5,1.5,2],[7.5,7.5,2]]
#cells = [[1,7,2],[2,7,8,3],[3,8,9,4],[4,9,5],[8,6,5,9],[1,6,8,7],[1,6,3,2],[3,6,5,4]]
verts = [[0,0,0], [0,10,0],[6,10,0],[6,8,0],[3,8,0],[3,4,0],[6,4,0],[6,0,0],[5,2,2],[1,2,2],[1,9,2],[5,9,2]]
cells = [[9,8,7],[7,6,10,9],[9,10,1,8],[1,10,11,2],[2,11,12,3],[3,12,4],[4,12,11,5],[5,11,10,6],[8,7,6,1],[1,6,5,2],[2,5,4,3]]
#verts = [[0,0,0],[6,0,0],[6,-12,0],[3,-12,0],[3,-3,0],[0,-3,0],[1.5,-1.5,3],[4.5,-1.5,3],[4.5,-10.5,3]]
#cells = [[1,7,6],[2,8,7,1],[2,3,9,8],[4,3,9],[4,9,8,5],[5,8,7,6],[6,5,2,1],[5,4,3,2]]
VIEW(ggpl_L_and_U_roof_builder(verts,cells))
