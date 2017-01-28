from pyplasm import *
from src import workshop_10 as house
from src import workshop_07 as windoor 
import glob
import csv
import random

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

"""TEST purpose
def build_house_battery(n, squared = False):

	battery = []
	for i in range(1):

		houseModel = CUBOID([17.79287338256836, 18.63495445251465, 9.000055313110352])
		xSize = SIZE([1])(houseModel)[0]
		ySize = SIZE([2])(houseModel)[0]
		battery.append(BOX([1,2,3])(houseModel))
		battery.append(T([2])([ySize*1.2]))

	if squared:
		squared = []
		squared.append(houseModel)
		squared.append(T([2])([ySize*1.2])(houseModel))
		squared.append(T([1])([xSize*1.2])(houseModel))
		squared.append(T([1,2])([xSize*1.2,ySize*1.2])(houseModel))
		return STRUCT(squared)
	return STRUCT(battery*n)
"""
def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n+1]

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

		strada = OFFSET([2,2])(STRUCT([STRUCT(curve2)]))
		strada = PROD([strada, Q(.1)])
		#strada = MATERIAL([.1,.1,.1,.2,  0,0,0,1,  0,0,0,1, 0,0,0,1, 10])(strada)

		bezierList.append(strada)
		points = []

	return STRUCT(bezierList)

strada = draw_bezier()
box = BOX([1,2])(strada)
#box = MATERIAL([0,.44,.031,.2,  0,0,0,1,  0,0,0,1, 0,0,0,1, 100])(box)
base = S([1,2])([1.45,1.45])(STRUCT([box, strada]))



#houseModel = BOX([1,2,3])(house.build_house(1))
#houseModel2 = BOX([1,2,3])(R([1,2])(PI)(house.build_house(1)))
#houseBattery = [houseModel, T([2])([20])] * 6
#houseBattery2 = [houseModel2, T([2])([20])] * 3
#houseBattery = R([1,2])(-PI/2.44)(STRUCT(houseBattery))
houseBattery = R([1,2])(-PI/2.44)(build_house_battery(6))
houseBattery2 = R([1,2])(PI/10)(build_house_battery(3))
houseBattery3 = R([1,2])(PI/2.5)(build_house_battery(3))
houseBattery4 = R([1,2])(-PI+PI/5.)(build_house_battery(5))
houseBattery5 = R([1,2])(PI/5.)(build_house_battery(5))
houseBattery6 = R([1,2])(-PI+PI/5.)(build_house_battery(4))
houseBattery7 = R([1,2])(PI/5.)(build_house_battery(5))
houseBattery8 = R([1,2])(PI/8.)(build_house_battery(0,True))
houseBattery9 = R([1,2])(-PI/2.60)(build_house_battery(3))
modello = STRUCT([base, T([1,2])([150,262])(houseBattery), 
T([1,2])([245,300])(houseBattery2), 
T([1,2])([204,353])(houseBattery3), 
T([1,2])([97,366])(houseBattery4),
T([1,2])([170,285])(houseBattery5),
T([1,2])([53,330])(houseBattery6),
T([1,2])([120,257])(houseBattery7),
T([1,2])([193,285])(houseBattery8),
T([1,2])([80,235])(houseBattery9)])
#modello = STRUCT([base, T([1,2])([193,285])(houseBattery8)])


VIEW(modello)