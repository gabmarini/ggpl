from pyplasm import * 
from sympy import *
import numpy as np

def list2CoupledList(startList):
	"""
	list2CoupledList is a function that given a starting list, return a list containing, for every element in the 
	starting list, a couple (list) made by the original element and its successor, if the original element
	is the last of the original list, the first element of the original list is used as successor.
	E.g. [1,2,3] -> [[1,2],[2,3],[3,1]]
	@param startList: starting list
	@return coupledList: the list containing the couples generated as described above
	"""
	coupledList = []
	for index in range(len(startList)-1):
		coupledList.append([startList[index],startList[index+1]])
	coupledList.append([startList[-1], startList[0]])
	return coupledList

def planeFromLine(angle, line):
	"""
	planeFromLine is a function that given a line and an angle, return the 4 coefficients that describe a plane passing
	through the line, the plane contain both the former and the latter point of the line.
	@param angle: the rotation that describe a particular plane
	@param line: the line used to describe the boundle of planes
	@return planesParam: a list containing the 4 coefficients that describe a plane
	"""

	partialPlane = PROD([POLYLINE(line), QUOTE([2])])
	partialPlane = T([1,2])([-line[0][0], -line[0][1]])(partialPlane)
	partialPlane = ROTN([-angle, [line[1][0] - line[0][0], line[1][1]-line[0][1],0]])(partialPlane)
	partialPlane = T([1,2])([+line[0][0], +line[0][1]])(partialPlane)

	#obtaining 3 points
	points = []
	points.append(UKPOL(partialPlane)[0][0])
	points.append(UKPOL(partialPlane)[0][1])
	points.append(UKPOL(partialPlane)[0][2])

	x1 = points[0][0]
	x2 = points[1][0]
	x3 = points[2][0]
	y1 = points[0][1]
	y2 = points[1][1]
	y3 = points[2][1]
	z1 = points[0][2]
	z2 = points[1][2]
	z3 = points[2][2]

	#calculating the three vectors
	p1 = np.array([x1, y1, z1])
	p2 = np.array([x2, y2, z2])
	p3 = np.array([x3, y3, z3])

	v1 = p3 - p1
	v2 = p2 - p1
	# the cross product is a vector normal to the plane
	cp = np.cross(v1, v2)
	a, b, c = cp

	# This evaluates a * x3 + b * y3 + c * z3 which equals d
	d = np.dot(cp, p3)

	return [a,b,c,d]

def roofBuilder(verts, angle, height):
	"""
	roofBuilder is a function that given a list of vertices (roof bottom), an angle and an height, 
	return an HPC model of a roof.
	@param verts: the vertices that define the shape of the roof bottom
	@param angle: the angle used to rotate the roof pitches
	@param height: the desired height of the roof
	@return roof: the HPC model of the generated roof
	"""

	lines = list2CoupledList(verts)

	roofBase = SOLIDIFY(POLYLINE(verts + [verts[0]]))

	planes = []
	for line in lines: 
		planes.append(planeFromLine(angle,line))

	#considering planes as couples
	couplePlanes = list2CoupledList(planes)

	roofTop = []
	linesEquations = []

	#calculating lines equations through planes intersections
	for couple in couplePlanes:
		x, y, z = symbols('x y z')
		solved = solve([Eq(couple[0][0]*x+couple[0][1]*y+couple[0][2]*z, couple[0][3]),
			Eq(couple[1][0]*x+couple[1][1]*y+couple[1][2]*z, couple[1][3])])
		linesEquations.append(solved)
		roofTop.append([round(float(solved[x].subs(z,roofHeight)),2), round(float(solved[y].subs(z,roofHeight)),2)])

	roofTop.append(roofTop[0])
	terrace = T([3])([roofHeight])(SOLIDIFY(POLYLINE(roofTop)))

	coupleLines = list2CoupledList(linesEquations)
	roofPitch = []

	#building roof pitches
	for couple in coupleLines:
		base1 = [round(float((couple[0])[x].subs(z,0)),2),round(float((couple[0])[y].subs(z,0)),2),0]
		base2 = [round(float((couple[1])[x].subs(z,0)),2),round(float((couple[1])[y].subs(z,0)),2),0]
		top1 = [round(float((couple[0])[x].subs(z,roofHeight)),2),round(float((couple[0])[y].subs(z,roofHeight)),2),roofHeight]
		top2 = [round(float((couple[1])[x].subs(z,roofHeight)),2),round(float((couple[1])[y].subs(z,roofHeight)),2),roofHeight]
		points = [base1, base2, top2, top1, base1]
		faces = [[1,2,3,4]]
		roofPitch.append(TEXTURE("textures/roof.jpg")(MKPOL([points, faces, 1])))

	roofPitch = STRUCT(roofPitch)

	return STRUCT([TEXTURE("textures/surface.jpg")(terrace), roofBase, roofPitch])

#roof vertices
v1 = [0,0]
v2 = [7,0]
v3 = [7,5]
v4 = [6,5]
v5 = [7,7]
v6 = [3,8]
v7 = [0,7]

roofHeight = 1

angle = PI/3.

VIEW(roofBuilder([v1,v2,v3,v4,v5,v6,v7], angle, roofHeight))
