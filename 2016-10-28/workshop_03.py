from pyplasm import *
import math

def generate_steps(stepNumber, tread, riser, stepWidth):
	"""
	generate_steps is an helper function that given a number of steps, a tread value, 
	a riser value and the step's width, generates a list containing the HPC models useful to
	draw a stair, The first step is generated as a CUBOID, meanwhile the other are generated
	using MKPOL function in order to obtain the ramp underneath the stair.
	@param stepNumber: the number of the steps that the stair needs to have
	@param tread: the tread value between two steps
	@param riser: the riser value between two steps
	@param stepWidth: the width of a single step, applied to the whole stair
	@return steps: a list containing the entire set of steps that compose the stair
	"""
	steps = []
	step2d = MKPOL([[[tread, 0],[tread, riser*2], [tread*2, riser*2], [tread*2, riser]], [[1,2,3,4]], None])
	firstStep = CUBOID([tread, riser, stepWidth])
	steps.append(firstStep)
	for i in range(int(stepNumber-1)):
		steps.append(T([1,2])([(tread*i), riser*i])(PROD([step2d, Q(stepWidth)])))
	return steps

def generate_walls(wallThickness, dx, dy, dz):
	"""
	generate_walls is a function that, given a wall thickness, and three value representing the
	dimensions of the walls, generates a list containing the HPC models useful to draw the walls that define
	the environment in which the stairs are colocated.
	@param wallThickness: the thickness of the walls
	@param dx: the dimension of the wall, X-Axis
	@param dy: the dimension of the wall, Y-Axis
	@param dz: the dimension of the wall, Z-Axis
	@return walls: a list containing the set of walls that defines the environment
	"""
	walls = []
	wall = CUBOID([dx,dz,wallThickness])
	wall2 = R([1,3])(PI/2)(CUBOID([dy-(wallThickness*2),dz,wallThickness]))
	wall2 = T([1,3])([dx,wallThickness])(wall2)
	wall3 = T([3])([dy-wallThickness-.05])(wall)
	walls.append(wall)
	walls.append(wall2)
	walls.append(wall3)
	return walls

def scale_structure(structure, dx, dy, dz):
	"""
	scale_structure is a function that, given an HPC model of a structure and three values representing 
	the dimension that the structure needs to have, return the structure scaled according to the three dimensions given.
	The transformation is obtained through the use of a linear transformation and a scaling operation.
	@param structure: the HPC model of the structure to transform
	@param dx: desired dimension of the structure, X-Axis
	@param dy: desired dimension of the structure, Y-Axis
	@param dz: desired dimension of the structure, Z-Axis
	@return transformed: the HPC model of the transformed structure
	"""
	transformation = MAT([[1,0,0],[0,dx/SIZE([1])(structure)[0],0],[0,0,1]])
	transformed = STRUCT([transformation,structure])
	transformed = STRUCT([S(3)(dz/SIZE([3])(structure)[0]),transformed]) 
	return transformed

def ggpl_quarter_turn_stairs(dx, dy, dz):
	"""
	ggpl_quarter_turn_stairs is a function that given three values representing the three dimensions 
	return an HPC model of an environment containing a quarter turn stairs. Inside the function some values
	hard-coded such as the wallThickness, the riser value, the tread value and the height of every portion 
	of the whole stair structure, however these values can be changed in the first part of the function obtaining
	a different kind of stair due to the fact that the entire structure is generated accordingly to these values.
	The structure is generated with different axes references in order to ease the process of generating it,
	the axes are changed correctly at the end of the function, before returning the result.
	The numbers of steps in a stair is ceiled in order to ease the generation of the according stair part, this 
	require further scaling and transformation to compensate the loss or the generations of steps.
	@param dx: desired dimension of the structure, X-Axis
	@param dy: desired dimension of the structure, Y-Axis
	@param dz: desired dimension of the structure, Z-Axis
	@return result: the generated HPC model containg the stair and the wall useful to support it
	"""
	#defining the essentials values
	wallThickness = 0.15
	riser = .25
	tread = .30
	lengthOfFlight = dz - (riser*2) #two platforms

	#defining the ramps length according to the length of flight
	firstRamp = lengthOfFlight/5. *2
	secondRamp = lengthOfFlight/5.
	thirdRamp = lengthOfFlight/5. * 2

	#calculating the numbers of steps
	stepNumberFirst = math.ceil(firstRamp / riser)
	stepNumberSecond = math.ceil(secondRamp / riser) 
	stepNumberThird = math.ceil(thirdRamp / riser)

	#variable that will contain all stair's models
	stairs = []

	#calculating the division of the space, X-Axis
	firstPlatformX = dx / 3.

	#calculating the division of the space, Y-Axis
	firstPlatformY = (dy-wallThickness) - tread * stepNumberFirst
	secondPlatformY = (dy-wallThickness) - tread * stepNumberSecond

	#generating the first stair part
	firstStairs = generate_steps(stepNumberFirst, tread, riser, firstPlatformX)
	firstStairs = T([3])([wallThickness])(STRUCT(firstStairs))
	stairs.append(firstStairs)

	#generating the first platform
	platform = CUBOID([firstPlatformY, riser, firstPlatformX])
	stairs.append(T([1,2,3])([tread*stepNumberFirst, riser*stepNumberFirst-riser,wallThickness])(platform))

	#generating the second stair part
	secondStair = generate_steps(stepNumberSecond, tread, riser, firstPlatformY)[1:]
	secondStair = R([1,3])(PI/2)(STRUCT(secondStair))
	secondStair = T([1,2,3])([dy-wallThickness, riser*stepNumberFirst-riser, firstPlatformX-tread+wallThickness])(secondStair)
	stairs.append(secondStair)

	#generating the second platform
	stairs.append(T([1,2,3])([tread*stepNumberFirst, (riser*stepNumberFirst)-(riser*2)+(riser*stepNumberSecond), (firstPlatformX -tread + tread*stepNumberSecond+wallThickness)])(platform))

	#generating the third stair part
	thirdStair = generate_steps(stepNumberThird, tread, riser, firstPlatformX)[1:]
	thirdStair = R([1,3])(PI)(STRUCT(thirdStair))
	thirdStair = T([1,2,3])([tread*stepNumberFirst + tread, (riser*stepNumberFirst)-(riser*2)+(riser*stepNumberSecond), ((firstPlatformX*2) -tread + tread*stepNumberSecond+wallThickness)])(thirdStair)
	stairs.append(thirdStair)

	#generating the last platform
	lastPlatform = CUBOID([tread, riser, firstPlatformX])
	lastPlatform = T([2,3])([riser*stepNumberFirst - riser*3 + riser*stepNumberSecond + riser*stepNumberThird, ((firstPlatformX*2) -tread -firstPlatformX + tread*stepNumberSecond+wallThickness)])(lastPlatform)
	stairs.append(lastPlatform)

	#generating the box of the entire structure
	box = SKEL_1(BOX([1,2,3])(CUBOID([dy,dz,dx])))

	#generating walls and stairs
	walls = generate_walls(wallThickness,stepNumberFirst*tread+firstPlatformY+wallThickness,(firstPlatformX*2 + stepNumberSecond*tread),riser*stepNumberFirst - riser*2 + riser*stepNumberSecond + riser*stepNumberThird)
	polyWalls = STRUCT(walls)
	polyStairs = STRUCT(stairs)

	#correction of the axes
	result = MAP([S3,S1,S2])(STRUCT([polyWalls,polyStairs]))
	box = MAP([S3,S1,S2])(STRUCT([box]))

	#last compensation and scaling
	result = scale_structure(result, dx, dy, dz)

	#assembling the whole structure
	result = STRUCT([result,box])
	return result

VIEW(ggpl_quarter_turn_stairs(4,4,3.5))