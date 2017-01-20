from pyplasm import *
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
			#appending vertices representing the polygon's base
			basePolygon.append([float(row[0]),float(row[1])])
			#every 4 points build a 2D-cuboid, rinse and repeat
			if(acc == 4):
				wannaBeHoles.append(MKPOL([basePolygon,[[1,2,3,4]],None]))
				basePolygon = []
				acc = 0
		#building 3D "wanna-be" holes
	wannaBeHoles = STRUCT(wannaBeHoles)
	return wannaBeHoles


def generate_windows_special_hole_models(linesFileName, modelBuilder, height):
	"""
	generate_windows_special_hole_models is a function that given a .lines's file name, a model builder function
	and a wall height, generate a couple containing two lists: the former contain the windows models, the latter
	contain the windows model used to generate the holes in the walls.
	@param linesFileName: the file name of .lines file containing lines used to place windows models
	@param modelBuilder: the windows's generator function
	@param height: the wall height used to position the models
	@return (models, holes): models contain the actual models of the windows meanwhile, holes contain
	the convex hulls of the corresponding element in models list
	"""
	with open("lines/"+ linesFileName + ".lines", "rb") as file:
		reader = csv.reader(file, delimiter=",")
		holes = []
		models = []
		xMin = 100000000
		xMax = 0
		yMin = 100000000
		yMax = 0
		for row in reader:
			xMin = min(xMin, float(row[0]), float(row[2]))
			xMax = max(xMax, float(row[0]), float(row[2]))
			yMin = min(yMin, float(row[1]), float(row[3]))
			yMax = max(yMax, float(row[1]), float(row[3]))
			if float(row[0]) != float(row[2]):
				model = modelBuilder(xMax-xMin,19.5,height/2.)
				model = T([1,2,3])([xMin,yMin*.99, height/4.])(model)
			else:
				model = modelBuilder(yMax-yMin,19.5,height/2.)
				model = R([1,2])(-PI/2.)(model)
				model = T([2])([yMax-yMin])(model)
				model = T([1,2,3])([xMin*.99,yMin, height/4.])(model)
			holes.append(JOIN(SKEL_1(model)))
			models.append(model)
			xMin = 100000000
			xMax = 0
			yMin = 100000000
			yMax = 0
	holes = STRUCT(holes)
	models = STRUCT(models)
	return (models, holes)

def generate_doors_special_hole_models(linesFileName, modelBuilder, height):
	"""
	generate_doors_special_hole_models is a function that given a .lines's file name, a model builder function
	and a wall height, generate a couple containing two lists: the former contain the doors models, the latter
	contain the doors model used to generate the holes in the walls.
	@param linesFileName: the file name of .lines file containing lines used to place doors models
	@param modelBuilder: the doors's generator function
	@param height: the wall height used to position the models
	@return (models, holes): models contain the actual models of the windows meanwhile, holes contain
	the convex hulls of the corresponding element in models list
	"""
	with open("lines/"+ linesFileName + ".lines", "rb") as file:
		reader = csv.reader(file, delimiter=",")
		holes = []
		models = []
		xMin = 100000000
		xMax = 0
		yMin = 100000000
		yMax = 0
		for row in reader:
			xMin = min(xMin, float(row[0]), float(row[2]))
			xMax = max(xMax, float(row[0]), float(row[2]))
			yMin = min(yMin, float(row[1]), float(row[3]))
			yMax = max(yMax, float(row[1]), float(row[3]))
			if float(row[0]) != float(row[2]):
				model = modelBuilder(xMax-xMin,19,3*height/4.)
				model = T([1,2])([xMin,yMin*.99])(model)
			else:
				model = modelBuilder(yMax-yMin,19,3*height/4.)
				model = R([1,2])(-PI/2.)(model)
				model = T([2])([yMax-yMin])(model)
				model = T([1,2])([xMin*.99,yMin])(model)
			holes.append(JOIN(SKEL_1(model)))
			models.append(model)
			xMin = 100000000
			xMax = 0
			yMin = 100000000
			yMax = 0
	holes = STRUCT(holes)
	models = STRUCT(models)
	return (models, holes)


def texturized_floors(story, ladderModel = False):
	"""
	texturized_floors is a function that return a list of HPC models, in particular models of the different floors that are
	present in the building, including the external floors. two params are accepted, the current story generated and
	eventually the ladder model used to generate hole in the floors, however this function build all the floors of 4 
	type of environments: livingroom, bathroom, bedroom, terrace.
	Moreover, in order to generate correctly all the floors, the following files are needed: bedroomKX.lines, 
	where X is an integer > 0, bathroomKY.lines where Y is an integer > 0, livingroomKZ.lines where Z in an integer > 0, 
	terrace_surfaceKW.lines where W is an integer > 0. It actually possible to have a series of file 
	(e.g. bathroom1.lines, bathroom2.lines, ecc...), K is the number corresponding to the current story. 
	In addition, this function could add some fancy random texture to the 	generated floors (up to 6 for every category)
	@param story: current story
	@param ladderModel: the ladder model used to calculate the holes in the floor 
	@return res: list of HPCs representing all the floors generated with their texture if any
	"""
	res = []
	def build_floor(roomType, texturePrefix):
		counter = 1
		result = []
		while True:
			if os.path.isfile("lines/" + roomType + str(story) + str(counter) + ".lines"):
				with open("lines/" + roomType + str(story) + str(counter) + ".lines", "rb") as file:
					reader = csv.reader(file, delimiter=",")
					polylineList = []
					for row in reader:
						polylineList.append(POLYLINE([[float(row[0]), float(row[1])],[float(row[2]), float(row[3])]]))
				floor = PROD([SOLIDIFY(STRUCT(polylineList)),Q(.5)])
				ladderHole = T([3])([-1])(ladderModel)
				if(story != 0 and ladderModel):
					floor = DIFFERENCE([floor, ladderHole])
				result.append(TEXTURE("texture/" + texturePrefix+str(randint(1,6))+".jpg")(floor))
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


def build_house(story, windowsGenerationFunction = False, doorsGenerationFunction = False, ladderModel = False):
	"""
	texturized_floors is a function that return a list of HPC models, in particular models of the different floors that are
	present in the building, including the external floors. No params are formally required, however this function build all
	the floors of 4 type of environments: livingroom, bathroom, bedroom, terrace.
	Moreover, in order to generate correctly all the floors, the following files are needed: bedroomX.lines, 
	where X is an integer > 0, bathroomY.lines where Y is an integer > 0, livingroomZ.lines where Z in an integer > 0, 
	terrace_surfaceW.lines where W is an integer > 0. It actually possible to have a series of file 
	(e.g. bathroom1.lines, bathroom2.lines, ecc...). In addtion, this function could add some fancy random texture to the 
	generated floors (up to 6 for every category)
	@return res: list of HPCs representing all the floors generated with their texture if any
	"""
	#generating 2D external walls
	externalWalls = generate_2D_walls("muriesterni"+str(story))

	#defining scaling factors
	xfactor = 15/SIZE([1])(externalWalls)[0]
	yfactor = 15.1/SIZE([2])(externalWalls)[0]
	zfactor = xfactor

	#building external 3D-walls
	walls = OFFSET([12,12])(externalWalls)
	walls = PROD([walls, Q(3/xfactor)])

	#generating internal 2D-walls
	internalWalls = generate_2D_walls("muriinterni"+str(story))

	#building internal 3D-walls
	internals = OFFSET([7,7])(internalWalls)
	internals = PROD([internals, Q(3/xfactor)])

	#building 3D-doors holes
	if(not doorsGenerationFunction):
		doors = generate_hole_models("porte"+str(story))
		doors = PROD([doors, Q(2.5/xfactor)])
	else:
		doors = generate_doors_special_hole_models("porte_model"+str(story), doorsGenerationFunction, 3/zfactor)

	#building 3D-windows holes
	if(not windowsGenerationFunction):
		windows = generate_hole_models("finestre"+str(story))
		windows = PROD([windows, Q(SIZE([3])(walls)[0]/2.)])
		windows = T(3)(SIZE([3])(walls)[0]/4.)(windows)
	else:
		windows = generate_windows_special_hole_models("finestre_model"+str(story),windowsGenerationFunction,4/zfactor)

	#building 2D-model of the terrace walls
	terrace_walls = generate_2D_walls("terrace_walls"+str(story))
	terrace_walls = OFFSET([5,5])(terrace_walls)

	#building 3D-model of the terrace walls with some fancy texture addition
	terrace_walls = PROD([terrace_walls, Q(1.5/xfactor)])
	terrace_walls = TEXTURE(["texture/wood2.jpg",True,True,10,10,PI/2.,200,200,100,100])(terrace_walls)

	#building the frame assembling the external walls and the interior walls
	frame = STRUCT([walls, internals])

	#breaking the walls in order to put some windows and doors
	if (not windowsGenerationFunction and not doorsGenerationFunction):
		exteriors = DIFFERENCE([walls, windows, doors])
		interiors = DIFFERENCE([internals, doors, windows])
	if (windowsGenerationFunction and not doorsGenerationFunction): 
		exteriors = DIFFERENCE([walls, doors, windows[1]])
		interiors = DIFFERENCE([internals, doors, windows[1]])
	if (not windowsGenerationFunction and doorsGenerationFunction):
		exteriors = DIFFERENCE([walls, doors[1], windows])
		interiors = DIFFERENCE([internals, doors[1], windows])
	if (windowsGenerationFunction and doorsGenerationFunction):
		exteriors = DIFFERENCE([walls, doors[1], windows[1]])
		interiors = DIFFERENCE([internals, doors[1], windows[1]])
		

	#adding some fancy texture to the walls
	exteriors = TEXTURE(["texture/wood_surface.jpg",True,True,10,10,-PI/2.,1,1])(exteriors)
	interiors = TEXTURE(["texture/wood1.jpg",True,True,1,1,PI/2.,5,5])(interiors)

	#building the floors
	floor = STRUCT(texturized_floors(story, ladderModel))
	#floor = CUBOID([0,0,0])

	#scaling and assembling all together
	if (not windowsGenerationFunction and not doorsGenerationFunction):	
		house = S([1,2,3])([xfactor,yfactor, zfactor])(STRUCT([interiors, exteriors, terrace_walls, floor]))
	if (windowsGenerationFunction and not doorsGenerationFunction):
		house = S([1,2,3])([xfactor,yfactor, zfactor])(STRUCT([interiors, exteriors, terrace_walls, floor, windows[0]]))
	if (not windowsGenerationFunction and doorsGenerationFunction):
		house = S([1,2,3])([xfactor,yfactor, zfactor])(STRUCT([interiors, exteriors, terrace_walls, floor, doors[0]]))
	if (windowsGenerationFunction and doorsGenerationFunction):
		house = S([1,2,3])([xfactor,yfactor, zfactor])(STRUCT([interiors, exteriors, terrace_walls, floor, windows[0], doors[0]]))



	return house