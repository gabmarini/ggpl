from pyplasm import * 
from sympy import *
import numpy as np
from random import randint

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
	partialPlane = ROTN([angle, [line[1][0] - line[0][0], line[1][1]-line[0][1],0]])(partialPlane)
	#partialPlane = ROTN([-angle, [line[1][0] - line[0][0], line[1][1]-line[0][1],0]])(partialPlane)
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

def sympyPlaneFromLine(angle, line):
	"""
	sympyPlaneFromLine is a function that given a line and an angle, return the sympy object
	representing the plane cutted by the line, the plane contain both the former and the latter point of the line.
	@param angle: the rotation that describe a particular plane
	@param line: the line used to describe the boundle of planes
	@return plane: a sympy Plane object
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

	return Plane((x1, y1, z1), (x2, y2, z2), (x3, y3, z3))

def calculateHeight(planes, p1, p2, minimum):
	"""
	calculateHeight is a function that given a list of planes (pitches), two points (a 3D line), 
	and a current minimum height, return the minimum height value of the roof in order to 
	disallow pitch intersections in case of high roof height values.
	@param planes: the planes to check against
	@param p1: former point of the 3D line
	@param p2: latter point of the 3D line
	@param minimum: current roof height minimum
	@return minimum height of the roof that disallow pitch intersections 
	"""
	L = Line3D(Point3D(p1[0], p1[1], p1[2]), Point3D(p2[0], p2[1], p2[2]))
	heights = []
	for plane in planes:
		heights.append(round((plane.intersection(L)[0][2]).evalf(), 2))
	heights = [x for x in heights if x > 0]
	return minimum if minimum < min(heights) and minimum != 0 else min(heights)


def roofBuilder(verts, angle, height):
	"""
	roofBuilder is a function that given a list of vertices (roof bottom), an angle and an height, 
	return an HPC model of a mansard roof.
	@param verts: the vertices that define the shape of the roof bottom
	@param angle: the angle used to rotate the roof pitches
	@param height: the desired height of the roof
	@return roof: the HPC model of the generated roof
	"""
	
	
	lines = list2CoupledList(verts)

	roofBase = SOLIDIFY(POLYLINE(verts + [verts[0]]))
	roofBase = TEXTURE("texture/wood.jpg")(roofBase)


	sympyPlanes = []
	planes = []
	for line in lines: 
		planes.append(planeFromLine(angle,line))
		sympyPlanes.append(sympyPlaneFromLine(angle,line))

	#considering planes as couples
	couplePlanes = list2CoupledList(planes)

	linesEquations = []

	#calculating lines equations through planes intersections
	for couple in couplePlanes:
		x, y, z = symbols('x y z')
		solved = solve([Eq(couple[0][0]*x+couple[0][1]*y+couple[0][2]*z, couple[0][3]),
			Eq(couple[1][0]*x+couple[1][1]*y+couple[1][2]*z, couple[1][3])])
		linesEquations.append(solved)

	coupleLines = list2CoupledList(linesEquations)
	roofPitch = []
	roofHeight = height

	#calculating roof height
	for couple in coupleLines:
		base1 = [round(float((couple[0])[x].subs(z,0)),1),round(float((couple[0])[y].subs(z,0)),1),0]
		top1 = [round(float((couple[0])[x].subs(z,1)),1),round(float((couple[0])[y].subs(z,1)),1),1]
		#roofHeight = calculateHeight(sympyPlanes, base1, top1, roofHeight)

	#building roof pitches
	pitchTexture = str(randint(1,5))
	for couple in coupleLines:
		base1 = [round(float((couple[0])[x].subs(z,0)),2),round(float((couple[0])[y].subs(z,0)),2),0]
		base2 = [round(float((couple[1])[x].subs(z,0)),2),round(float((couple[1])[y].subs(z,0)),2),0]
		top1 = [round(float((couple[0])[x].subs(z,roofHeight)),2),round(float((couple[0])[y].subs(z,roofHeight)),2),round(roofHeight,2)]
		top2 = [round(float((couple[1])[x].subs(z,roofHeight)),2),round(float((couple[1])[y].subs(z,roofHeight)),2),round(roofHeight,2)]
		points = [base1, top1, top2, base2, base1]
		faces = [[1,2,3,4,5]]
		roofPitch.append(COLOR(Color4f([61/255.,61/255., 41/255.]))(TEXTURE("texture/roof" + pitchTexture + ".jpg")(MKPOL([points, faces, 1]))))

	#building rooftop
	roofTop = []
	for equation in linesEquations:
		roofTop.append([round(float(equation[x].subs(z,roofHeight)),2), round(float(equation[y].subs(z,roofHeight)),2)])

	roofTop.append(roofTop[0])
	terrace = T([3])([roofHeight])(SOLIDIFY(POLYLINE(roofTop)))

	roofPitch = STRUCT(roofPitch)

	return STRUCT([TEXTURE("texture/surface" + str(randint(1,10)) + ".jpg")(terrace), roofBase, roofPitch])

#roof vertices
v1 = [0,0]
v2 = [7,0]
v3 = [7,5]
v4 = [6,5]
v5 = [7,7]
v6 = [3,8]
v7 = [0,7]

roofHeight = 2

angle = PI/3.

#VIEW(roofBuilder([v1,v2,v3,v4,v5,v6,v7], angle, roofHeight))
