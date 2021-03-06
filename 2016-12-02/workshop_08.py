from pyplasm import *
from larlib import *
from random import randint
import os.path
import csv

"""
generate_2D_walls is function that given a lines file name return the 2D-HPC model of a wireframe 
representing a wall/set of walls.
@param linesFileName: the file name (except .lines) of a file containing lines used as a source, 
in order to create the walls
@return wall: the HPCs models of the generated wall/walls wireframe
"""
def generate_2D_walls(linesFileName):
	with open("lines/"+linesFileName +  ".lines", "rb") as file:
		reader = csv.reader(file, delimiter=",")
		polylineList = []
		for row in reader:
			polylineList.append(POLYLINE([[float(row[0]), float(row[1])],[float(row[2]), float(row[3])]]))
	wall = STRUCT(polylineList)
	return wall

"""
generate_hole_models ia a function that given a lines file name return the 2D-HPC model of a set of squares, 
located where there's need to be an hole in the wall.
@param linesFileName: the file name (except .lines) of a file containing lines used as a source, 
in order to create the squares
@return wannaBeHoles: the HPCs models of the generated squares
"""
def generate_hole_models(linesFileName):
	with open("lines/"+ linesFileName + ".lines", "rb") as file:
		reader = csv.reader(file, delimiter=",")
		wannaBeHoles = []
		basePolygon = []
		acc = 0
		for row in reader:
			acc = acc + 1
			#appendig vertices representing the polygon's base
			basePolygon.append([float(row[0]),float(row[1])])
			#every 4 points build a 2D-cuboid, rinse and repeat
			if(acc == 4):
				wannaBeHoles.append(MKPOL([basePolygon,[[1,2,3,4]],None]))
				basePolygon = []
				acc = 0
		#building 3D "wanna-be" holes
	wannaBeHoles = STRUCT(wannaBeHoles)
	return wannaBeHoles

"""
texturized_floors is a function that return a list of HPC models, in particular models of the different floors that are
present in the building, including the external floors. No params are formally required, however this function build all
the floors of 4 type of environment: livingroom, bathroom, bedroom, terrace.
Moreover, in order to generate correctly all the floors, the following files are needed: bedroomX.lines, 
where X is an integer > 0, bathroomY.lines where Y is an integer > 0, livingroomZ.lines where Z in an integer > 0, 
terrace_surfaceW.lines where W is an integer > 0. It actually possible to have a series of file 
(e.g. bathroom1.lines, bathroom2.lines, ecc...). In addtion, this function could add some fancy random texture to the 
generated floors (up to 6 for every category)
@return res: list of HPCs representing all the floors generated with their texture if any
"""
def texturized_floors():
	res = []
	def build_floor(roomType, texturePrefix):
		counter = 1
		result = []
		while True:
			if os.path.isfile("lines/" + roomType + str(counter) + ".lines"):
				with open("lines/" + roomType+str(counter)+".lines", "rb") as file:
					reader = csv.reader(file, delimiter=",")
					polylineList = []
					for row in reader:
						polylineList.append(POLYLINE([[float(row[0]), float(row[1])],[float(row[2]), float(row[3])]]))
				result.append(TEXTURE("texture/" + texturePrefix+str(randint(1,6))+".jpg")(SOLIDIFY(STRUCT(polylineList))))
				counter = counter + 1
			else: 
				counter = 1
				break
		return result
	res = res + build_floor("bedroom","camera")
	res = res + build_floor("bathroom", "bagno")
	res = res + build_floor("livingroom", "sala")
	res = res + build_floor("terrace_surface", "terrazzo")
	return res

"""
build_house is the function that generates all the house parts: walls and floors. It takes no argument, due to the fact
that it's parameterized thanks to the data files used in its body. This function also apply some sort of scaling in order
to transform the units of measure used in inkscape (pixels) into meters.
@return house: the HPC model of the entire house
@see generate_2D_walls
@see generate_hole_models
@see texturized_floors
"""
def build_house():

	#generating 2D external walls
	externalWalls = generate_2D_walls("muriesterni")

	#defining scaling factors
	xfactor = 15/SIZE([1])(externalWalls)[0]
	yfactor = 15.1/SIZE([2])(externalWalls)[0]
	zfactor = xfactor

	#building external 3D-walls
	walls = OFFSET([12,12])(externalWalls)
	walls = PROD([walls, Q(3/xfactor)])

	#generating internal 2D-walls
	internalWalls = generate_2D_walls("muriinterni")

	#building internal 3D-walls
	internals = OFFSET([7,7])(internalWalls)
	internals = PROD([internals, Q(3/xfactor)])

	#building 3D-doors holes
	doors = generate_hole_models("porte")
	doors = PROD([doors, Q(2.5/xfactor)])

	#building 3D-windows holes
	windows = generate_hole_models("finestre")
	windows = PROD([windows, Q(SIZE([3])(walls)[0]/2.)])
	windows = T(3)(SIZE([3])(walls)[0]/4.)(windows)

	#building 2D-model of the terrace walls
	terrace_walls = generate_2D_walls("terrace_walls")
	terrace_walls = OFFSET([5,5])(terrace_walls)

	#building 3D-model of the terrace walls with some fancy texture addition
	terrace_walls = PROD([terrace_walls, Q(1.5/xfactor)])
	terrace_walls = TEXTURE(["texture/wood2.jpg",True,True,10,10,PI/2.,20,20,10,10])(terrace_walls)

	#building the frame assembling the external walls and the interior walls
	frame = STRUCT([walls, internals])

	#breaking the walls in order to put some windows and doors
	exteriors = DIFFERENCE([walls, windows, doors])
	interiors = DIFFERENCE([internals, doors, windows])

	#adding some fancy texture to the walls
	exteriors = TEXTURE(["texture/brick.jpg",True,True,10,10,PI/2.,20,20,10,10])(exteriors)
	interiors = TEXTURE(["texture/wood.jpg",True,True,1,1,PI/2.,5,5])(interiors)

	#building the floors
	floor = STRUCT(texturized_floors())

	#scaling and assembling all together
	house = S([1,2,3])([xfactor,yfactor, zfactor])(STRUCT([interiors, exteriors, terrace_walls, floor]))

	return house

#showing the result
VIEW(build_house())