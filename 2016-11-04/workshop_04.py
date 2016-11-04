from pyplasm import *
import numpy

def normalize_list(list_verts):
	for j in range(len(list_verts)):
		for i in range(len(list_verts[j])):
			if(abs(list_verts[j][i]) < 0.001):
				list_verts[j][i] = 0
			else:
				list_verts[j][i] = round(list_verts[j][i],1)

def makeDict(listUkpol):
	dictionary = {}
	verts = listUkpol[0]
	normalize_list(verts)
	cells = listUkpol[1]
	for cell in cells:
		for label in cell:
			point = str(verts[int(label)-1])
			if(point not in dictionary):
				dictionary[point] = []
			dictionary[point].append(label)
	return dictionary

def checkSurfacesComplanarity(verts, cells):
	normalize_list(verts)
	for cell in cells:
		if(len(cell) > 3):
			matrix = []
			lastpoint = cell[-1]
			for label in cell:
				point = verts[int(label)-1]
				row = []
				for i in range(len(point)):
					row.append(point[i]-verts[lastpoint-1][i])
				matrix.append(row)
			A = numpy.matrix(matrix)
			dim = numpy.linalg.matrix_rank(A)
			if(dim > 2):
				return False
	return True


verts = [[0,0,0],[0,3,0],[6,3,0],[6,9,0],[9,9,0],[9,0,0],[1.5,1.5,2],[7.5,1.5,2],[7.5,7.5,2]]
cells = [[1,7,2],[2,7,8,3],[3,8,9,4],[4,9,5],[8,6,5,9],[1,6,8,7],[1,6,3,2],[3,6,5,4]]
#verts = [[0,0,0],[6,0,0],[6,-12,0],[3,-12,0],[3,-3,0],[0,-3,0],[1.5,-1.5,3],[4.5,-1.5,3],[4.5,-10.5,3]]
#cells = [[1,7,6],[2,8,7,1],[2,3,9,8],[4,3,9],[4,9,8,5],[5,8,7,6],[6,5,2,1],[5,4,3,2]]
tetto = MKPOL([verts,cells, None])
tetto_sopra = MKPOL([verts,cells[:-2],None])
tetto_sopra = OFFSET([.1,.1,.1])(tetto_sopra)
tetto_sopra = T([3])([.1])(tetto_sopra)
tetto_sopra = COLOR(Color4f([1/255., 61/255., 31/255.,1]))(tetto_sopra)
travi = OFFSET([.1,.1,.1])(SKEL_1(tetto))
travi = S([3])(.95)(travi)
travi = COLOR(Color4f([132/255., 54/255., 9/255.,1]))(travi)
VIEW((STRUCT([travi, tetto_sopra])))