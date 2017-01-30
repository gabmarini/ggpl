from pyplasm import *
from src import workshop_10 as house
from src import test
import glob
import csv
import random


def box_max_min(boxVerts):
	ymax = max([v[1] for v in boxVerts])
	ymin = min([v[1] for v in boxVerts])
	xmax = max([v[0] for v in boxVerts])
	xmin = min([v[0] for v in boxVerts])
	return (xmin+2,ymin+2),(xmax-2,ymax-2)

def is_in_box(boxMinV, boxMaxV, point):
	return point[0] > boxMinV[0] and point[1] > boxMinV[1] and point[0] < boxMaxV[0] and point[1] < boxMaxV[1]


def build_house_battery(n, squared = False):

	battery = []

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
		battery.append((houseModel))

	return STRUCT(battery)

def build_house_battery(n, squared = False):

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
	boxMinV,boxMaxV = box_max_min(UKPOL(S([1,2])([1.45,1.45])(box))[0])
	treeList = []
	with open("lines/trees.lines") as trees:
		reader = csv.reader(trees, delimiter=",")
		for row in reader:
			if is_in_box(boxMinV, boxMaxV, [float(row[0])*1.45, float(row[1])*1.45]):
				treeModel = T([1,2])([float(row[0])*1.45, float(row[1])*1.45])(test.render_tree())
				treeList.append(treeModel)
			if is_in_box(boxMinV, boxMaxV, [float(row[2])*1.45, float(row[3])*1.45]):
				treeModel = T([1,2])([float(row[2])*1.45, float(row[3])*1.45])(test.render_tree())
				treeList.append(treeModel)
	return STRUCT(treeList)

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n+1]
"""
def draw_pool():
	points = []
	bezierList = []
	with open("lines/pool.lines") as pool:
		reader = csv.reader(pool, delimiter=",")
		for row in reader:
			points.append([float(row[2]), float(row[3])])
	puntinuovi = list(chunks(points, 8))
	puntinuovi[-1] = puntinuovi[-1] + [puntinuovi[0][0]]
	curve2 = []

	for punti in puntinuovi:
		curva = MAP(BEZIER(S1)(punti))(INTERVALS(1)(64))
		curve2.append(curva)

	return STRUCT(curve2)
"""

def draw_bezier():
	points = []
	bezierList = []
	filelist = glob.glob("bezier*.lines")
	for file in filelist:
		with open(str(file)) as bez:
			reader = csv.reader(bez, delimiter=",")
			for row in reader:
				points.append([float(row[2]), float(row[3])])
		puntinuovi = list(chunks(points, 2))
		if str(file) == "bezier.lines":
			puntinuovi[-1] = puntinuovi[-1] + [puntinuovi[0][0]]
		curve2 = []

		for punti in puntinuovi:
			curva = MAP(BEZIER(S1)(punti))(INTERVALS(1)(64))
			curve2.append(curva)

		strada = OFFSET([2,2])(STRUCT(curve2))
		strada2 = OFFSET([3,3]) (STRUCT(curve2))
		strada2 = T([1,2])([-.5,-.5])(strada2)
		strada = PROD([strada, Q(.1)])
		strada2 = PROD([strada2, Q(.05)])
		strada = MATERIAL([.1,.1,.1,.2,  0,0,0,1,  0,0,0,1, 0,0,0,1, 10])(strada)
		bezierList.append(strada)
		bezierList.append(strada2)
		points = []
	return STRUCT(bezierList)

strada = draw_bezier()
box = BOX([1,2])(strada)
#box = MATERIAL([0,.44,.031,.2,  0,0,0,1,  0,0,0,1, 0,0,0,1, 100])(box)
box = MATERIAL([0,0,0,1,  0,.1,0,1,  0,.1,0,1, 0,0,0,1, 0])(box)
#box = MATERIAL([.2,.2,.2,.3,  0,0,0,1,  0,0,0,1, 0,0,0,1, 10])(box)
#print SIZE([1,2])(box)
border = PROD([T([1,2])([-1,-1])(OFFSET([2,2])(SKEL_1(box))),Q(2)])
border = MATERIAL([0.53,.3,0,.1,  0,0,0,1,  0.53,.3,0,.8, 0,0,0,1, 100])(border)

waterify = MATERIAL([0,.2,.6,1, 0,.2,.4,.2, 1,1,1,1, 0,0,0,1, 100])

boxMinV,boxMaxV = box_max_min(UKPOL((JOIN(SKEL_1(border))))[0])
points = [[[boxMaxV[0],boxMinV[1]], [boxMaxV[0],boxMinV[1]+1.5*i], [boxMaxV[0]-5*i,boxMinV[1]]] for i in xrange(1,16)]

fiumi = [MKPOL([ps,[[1,2,3]],1]) for ps in points]

result = [waterify(T([3])([.005*i+1])(fiume)) for i,fiume in enumerate(fiumi,0)]

base = S([1,2])([1.45,1.45])(STRUCT([box, strada, border, STRUCT(result)]))

VIEW(base)
houseBattery = R([1,2])(-PI/2.44)(build_house_battery(6))
houseBattery2 = R([1,2])(PI/10)(build_house_battery(3))
houseBattery3 = R([1,2])(PI/2.5)(build_house_battery(3))
houseBattery4 = R([1,2])(-PI+PI/5.)(build_house_battery(5))
houseBattery5 = R([1,2])(PI/5.)(build_house_battery(5))
houseBattery6 = R([1,2])(-PI+PI/5.)(build_house_battery(4))
houseBattery7 = R([1,2])(PI/5.)(build_house_battery(5))
houseBattery8 = R([1,2])(PI/8.)(build_house_battery(0,True))
houseBattery9 = R([1,2])(-PI/2.60)(build_house_battery(3))
houseBattery10 = R([1,2])(-PI/2.44)(build_house_battery(6))
houseBattery11 = R([1,2])(-PI/3.5)(build_house_battery(3))

modello = STRUCT([base, T([1,2])([150,262])(houseBattery), 
T([1,2])([245,300])(houseBattery2), 
T([1,2])([204,353])(houseBattery3), 
T([1,2])([97,366])(houseBattery4),
T([1,2])([170,285])(houseBattery5),
T([1,2])([53,330])(houseBattery6),
T([1,2])([120,257])(houseBattery7),
T([1,2])([193,285])(houseBattery8),
T([1,2])([80,235])(houseBattery9),
T([1,2])([167,216])(houseBattery10),
T([1,2])([38,362])(houseBattery11)])

trees = position_trees(box)


final = STRUCT([modello, trees])


boxMinV,boxMaxV = box_max_min(UKPOL(S([1,2])([1.45,1.45])(JOIN(SKEL_1(border))))[0])
final = T([1,2])([-boxMinV[0], -boxMinV[1]])(final)

VIEW(final)