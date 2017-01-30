from pyplasm import *
from src import workshop_10 as house
from src import tree
import glob
import csv
import random

#MATERIAL function to apply in order to create a water-like effect
waterify = MATERIAL([0,.2,.6,1, 0,.2,.4,.1, 1,1,1,1, 0,0,0,1, 100])

def box_max_min(boxVerts):
	"""
	box_max_min is a function that given a list of vertices, return two vertices, the ones
	visible and not covered by the plastic's borders. The former is the vertex with
	minimum X and Y values, meanwhile the latter is the one with maximum X and Y
	values, together they describe a 2D box used to put in place the trees.
	@param boxVerts: a list of vertices
	@return p1,p2: two points describing a 2D box in XY plane (z = 0)
	"""
	ymax = max([v[1] for v in boxVerts])
	ymin = min([v[1] for v in boxVerts])
	xmax = max([v[0] for v in boxVerts])
	xmin = min([v[0] for v in boxVerts])
	return (xmin+2,ymin+2),(xmax-2,ymax-2)

def is_in_box(boxMinV, boxMaxV, point):
	"""
	is_in_box is a function that given a 2 points describing a box in XY plane, return True
	if the third point passed as parameter is contained inside the box, False otherwise.
	@param boxMinV: the vertex with	minimum X and Y values 
	@param the vertex with maximum X and Y values
	@param point: is the vertex to be verified
	@return boolean: True if the point is contained in the box, False otherwise
	"""
	return point[0] > boxMinV[0] and point[1] > boxMinV[1] and point[0] < boxMaxV[0] and point[1] < boxMaxV[1]


def build_district(n, squared = False):
	"""
	build_district is a function that given a number and an optional boolean parameter,
	return a district of N houses if squared is false (or not passed).
	If the second parameter is not False, 4 houses will be produced, arranged in 
	a square, one house for every vertex of the square.
	@param n: number of houses that need to be built.
	@param squared: if the houses need to be arranged as a square,
	actually override the first parameter to 4.
	@return district: the HPC model of the district
	"""
	district = []

	if squared:
		squared = []
		houseModel = house.build_house(random.randint(1,2))
		xSize = SIZE([1])(houseModel)[0]
		ySize = SIZE([2])(houseModel)[0]
		squared.append(houseModel)
		houseModel = house.build_house(random.randint(1,2))
		xSize = SIZE([1])(houseModel)[0]
		ySize = SIZE([2])(houseModel)[0]
		squared.append(T([2])([ySize*1.2])(houseModel))
		houseModel = house.build_house(random.randint(1,2))
		xSize = SIZE([1])(houseModel)[0]
		ySize = SIZE([2])(houseModel)[0]
		squared.append(T([1])([xSize*1.2])(houseModel))
		houseModel = house.build_house(random.randint(1,2))
		xSize = SIZE([1])(houseModel)[0]
		ySize = SIZE([2])(houseModel)[0]
		squared.append(T([1,2])([xSize*1.2,ySize*1.2])(houseModel))
		return STRUCT(squared)

	for i in range(n):
		houseModel = house.build_house(random.randint(1,2))
		xSize = SIZE([1])(houseModel)[0]
		ySize = SIZE([2])(houseModel)[0]
		houseModel = T([2])([ySize*i*1.2])(houseModel)
		district.append((houseModel))

	return STRUCT(district)


def build_district(n, squared = False):
	battery = []
	for i in range(1):
		if random.randint(0,1) == 0:
			houseModel = CUBOID([17.79287338256836, 18.63495445251465, 9.000055313110352])
		else:
			houseModel  = CUBOID([16.35014533996582, 19.027542114257812, 9.0])
		xSize = SIZE([1])(houseModel)[0]
		ySize = SIZE([2])(houseModel)[0]
		battery.append(BOX([1,2,3])(houseModel))
		battery.append(T([2])([ySize*1.15]))
	if squared:
		squared = []
		squared.append(houseModel)
		squared.append(T([2])([ySize*1.2])(houseModel))
		squared.append(T([1])([xSize*1.2])(houseModel))
		squared.append(T([1,2])([xSize*1.2,ySize*1.2])(houseModel))
		return STRUCT(squared)
	return STRUCT(battery*n)

def position_trees(box):
	"""
	position_trees is a function that given an hpc model of a box on XY plane reads 
	a .lines file and return a list of HPC models representing a bunch of trees. 
	A tree is created at the beginning and the end of every line in the .lines file. 
	A tree isn't created if it will result outside the box or on the plastic border. 
	The trees are slightly randomized in shape and colors.
	@param box: the box in which the trees will be positioned.
	@return trees: a list of tree hpc models
	"""
	boxMinV,boxMaxV = box_max_min(UKPOL(S([1,2])([1.45,1.45])(box))[0])
	treeList = []
	with open("lines/trees.lines") as trees:
		reader = csv.reader(trees, delimiter=",")
		for row in reader:
			if is_in_box(boxMinV, boxMaxV, [float(row[0])*1.45, float(row[1])*1.45]):
				treeModel = T([1,2])([float(row[0])*1.45, float(row[1])*1.45])(tree.render_tree())
				treeList.append(treeModel)
			if is_in_box(boxMinV, boxMaxV, [float(row[2])*1.45, float(row[3])*1.45]):
				treeModel = T([1,2])([float(row[2])*1.45, float(row[3])*1.45])(tree.render_tree())
				treeList.append(treeModel)
	return STRUCT(treeList)

def chunks(l, n):
    """Yield successive n+1-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n+1]

def draw_beziers():
	"""
	draw_beziers is a function that reads a bunch of .lines file and generate the 
	related bezier's curves, every curve is built 2 time, the former is 
	used in order to draw the road, meanwhile the latter is used for the sidewalk.
	@return roads: the HPC model of the roads plus the sidewalks
	"""
	points = []
	bezierList = []
	filelist = glob.glob("lines/bezier*.lines")
	for file in filelist:
		with open(str(file)) as bez:
			reader = csv.reader(bez, delimiter=",")
			for row in reader:
				points.append([float(row[2]), float(row[3])])
		newPoints = list(chunks(points, 2))
		if str(file) == "lines/bezier.lines":
			newPoints[-1] = newPoints[-1] + [newPoints[0][0]]
		curves = []

		for points in newPoints:
			curve = MAP(BEZIER(S1)(points))(INTERVALS(1)(64))
			curves.append(curve)

		road = OFFSET([2,2])(STRUCT(curves))
		sidewalk = OFFSET([3,3]) (STRUCT(curves))
		sidewalk = T([1,2])([-.5,-.5])(sidewalk)
		road = PROD([road, Q(.1)])
		sidewalk = PROD([sidewalk, Q(.05)])
		road = MATERIAL([.1,.1,.1,.2,  0,0,0,1,  0,0,0,1, 0,0,0,1, 10])(road)
		bezierList.append(road)
		bezierList.append(sidewalk)
		points = []

	return STRUCT(bezierList)

def suburban_neighborhood():
	"""
	suburban_neighborhood is a function that generate an HPC model of the entire neighborhood,
	although it won't take any argument it's capable of generating a different scenario
	every time it is launched. Due to the randomization used it can generate hundreds
	of different trees and theoretically thousands of different house (starting 
	from two different type of house).
	It generate districts, roads, sidewalks, trees, rivers and the plastic box
	and borders.
	@return neighborhood: the HPC model of the neighborhood.
	"""

	#building roads and sidewalks
	roads = draw_beziers()

	#building box and border
	box = BOX([1,2])(roads)
	box = MATERIAL([0,0,0,1,  0,.1,0,1,  0,.1,0,1, 0,0,0,1, 0])(box)
	border = PROD([T([1,2])([-1,-1])(OFFSET([2,2])(SKEL_1(box))),Q(2)])
	border = MATERIAL([0.53,.3,0,.1,  0,0,0,1,  0.53,.3,0,.8, 0,0,0,1, 100])(border)

	#building rivers
	boxMinV,boxMaxV = box_max_min(UKPOL((JOIN(SKEL_1(border))))[0])

	points = [[[boxMaxV[0],boxMinV[1]], [boxMaxV[0],boxMinV[1]+.75*i], [boxMaxV[0]-2.5*i,boxMinV[1]]] for i in xrange(1,32)]
	points2 = [[[boxMinV[0],boxMaxV[1]], [boxMinV[0],boxMaxV[1]-.75*i], [boxMinV[0]+.85*i,boxMaxV[1]]] for i in xrange(1,45)]

	rivers = [MKPOL([ps,[[1,2,3]],1]) for ps in points]
	rivers2 = [MKPOL([ps,[[1,2,3]],1]) for ps in points2]

	riversModel = [waterify(T([3])([.005*i+1])(fiume)) for i,fiume in enumerate(rivers,0)]
	riversModel2 = [waterify(T([3])([.005*i+1])(fiume)) for i,fiume in enumerate(rivers2,0)]

	#assebling the base
	base = S([1,2])([1.45,1.45])(STRUCT([box, roads, border, STRUCT(riversModel + riversModel2)]))
	
	#building every single district
	district = R([1,2])(-PI/2.44)(build_district(6))
	district2 = R([1,2])(PI/10)(build_district(3))
	district3 = R([1,2])(PI/2.5)(build_district(3))
	district4 = R([1,2])(-PI+PI/5.)(build_district(5))
	district5 = R([1,2])(PI/5.)(build_district(5))
	district6 = R([1,2])(-PI+PI/5.)(build_district(4))
	district7 = R([1,2])(PI/5.)(build_district(5))
	district8 = R([1,2])(PI/8.)(build_district(0,True))
	district9 = R([1,2])(-PI/2.60)(build_district(3))
	district10 = R([1,2])(-PI/2.44)(build_district(6))
	district11 = R([1,2])(-PI/3.5)(build_district(3))

	#building the entire neighborhood
	model = STRUCT([base, T([1,2])([150,262])(district), 
	T([1,2])([245,300])(district2), 
	T([1,2])([204,353])(district3), 
	T([1,2])([97,366])(district4),
	T([1,2])([170,285])(district5),
	T([1,2])([53,330])(district6),
	T([1,2])([120,257])(district7),
	T([1,2])([193,285])(district8),
	T([1,2])([80,235])(district9),
	T([1,2])([168,217])(district10),
	T([1,2])([38,362])(district11)])

	#building trees
	trees = position_trees(box)

	#assembling all together
	neighborhood = STRUCT([model, trees])
	
	#translating back to the origin	
	boxMinV,boxMaxV = box_max_min(UKPOL(S([1,2])([1.45,1.45])(JOIN(SKEL_1(border))))[0])
	neighborhood = T([1,2])([-boxMinV[0], -boxMinV[1]])(neighborhood)

	#returning the result
	return neighborhood

VIEW(suburban_neighborhood())