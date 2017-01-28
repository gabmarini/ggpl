from pyplasm import *
import workshop_03 as ladder
import workshop_07 as windoor 
import workshop_08 as house
import workshop_09 as roof
import csv


XWindow = [.1,.5,.05,.5,.2,.5,.05,.5,.1]
YWindow = [.15,.9,.1,.9,.2,.9,.1,1.4,.1]
occurrencyWindow = [[True]*9,
					[True,False,True,False,True,False,True,False,True],
					[True]*9,
					[True,False,True,False,True,False,True,False,True],
					[True]*9,
					[True,False,True,False,True,False,True,False,True],
					[True]*9,
					[True,False,True,False,True,False,True,False,True],
					[True]*9]


YDoor = [.2, .2, .1, .4, .1, .2, .3, .2, .1, .4 ,.1, .2, .2]
XDoor = [.4, .3, .04, .6, .05, 1.4, .04, .3, .04, .5, .3]
occurrencyDoor = [[True, True, True, True, True, True, True, True, True, True, True, True, True],
				[True, False, False, False, False, False, True, False, False, False, False, False, True],
				[True, False, True, True, True, True, True, True, True, True, True, False, True], 
				[True, False, True, False, False, False, True, False, False, False, True, False, True],
				[True, False, True, False, True, True, True, True, True, False, True, False, True],
				[True, False, True, False, True, False, True, False, True, False, True, False, True], 
				[True, False, True, False, True, True, True, True, True, False, True, False, True],
				[True, False, True, False, False, False, True, False, False, False, True, False, True],
				[True, False, True, True, True, True, True, True, True, True, True, False, True],
				[True, False, False, False, False, False, True, False, False, False, False, False, True],
				[True, True, True, True, True, True, True, True, True, True, True, True, True]]


factors = []

def multistorey_house(type, nStorey):
	"""
	buildMultiStorey accept the number of storey in the building.
	"""
	def renderWindows(XWindow, YWindow, occurrencyWindow, windowModel = False):
		"""
		renderWindows accept the window's cells and the occurrency, and optionally a window generating function 
		"""
		def renderDoors(XDoor, YDoor, occurrencyDoor, doorModel = False):
			"""
			renderWindows accept the door's cells and the occurrency, and optionally a door generating function 
			"""
			def renderRoof(vertices, pitchAngle, height):
				"""
				renderRoof accept the vertices of the base roof, a pitch angle and the desired height 
				of the roof
				"""
				def renderLadder(ladderHeight, interStep, riser):
					"""
					renderLadder is the inner function used to assembly all together, it takes the 
					desired height of the ladder, an interstep between two step and a riser for the single
					step.
					"""

					#building the ladder model and the ladder box
					ladderModel = ladder.make_ladder(ladderHeight, interStep, riser)
					with open("lines/house" + str(type) + "/" + "ladder.lines", "rb") as ladderFile:
						reader = csv.reader(ladderFile, delimiter=",")
						row = next(reader)
						ladderModel = T([1,2])([float(row[0])*factors[0], float(row[1])*factors[1]])(ladderModel)
					ladderBOX = CUBOID([SIZE([1])(ladderModel)[0]/factors[0],SIZE([2])(ladderModel)[0]/factors[1], SIZE([3])(ladderModel)[0]/factors[2]])
					ladderBOX = T([1,2])([float(row[0])-SIZE([1])(ladderBOX)[0]/2., float(row[1])-SIZE([2])(ladderBOX)[0]/2.])(ladderBOX)

					#building roof model
					if isinstance(vertices, basestring):
						with open("lines/house" + str(type) + "/" + vertices + ".lines", "rb") as file:
							reader = csv.reader(file, delimiter=",")
							newVertices = []
							for row in reader:
								newVertices.append([float(row[0]), float(row[1])])
					if newVertices:
						roofModel = roof.roofBuilder(newVertices, pitchAngle, height)
					else:
						roofModel = roof.roofBuilder(vertices, pitchAngle, height)
					roofModel = T([3])([nStorey*3/factors[2]])(roofModel)
					roofModel = S([1,2,3])([factors[0]*1.09,factors[1]*1.09,factors[2]])(roofModel)
					roofModel = T([1,2])([-SIZE([1])(roofModel)[0]*0.05,-SIZE([2])(roofModel)[0]*0.05]) (roofModel)

					#building full house model with windows and doors
					fullHouse = []
					for story in range(nStorey):
						houseModel = house.build_house(type, story, windowModel, doorModel, ladderBOX)
						fullHouse.append(houseModel)
						fullHouse.append(T([3])([3]))
					fullHouse = STRUCT(fullHouse)

					#returning the result
					return STRUCT([roofModel, ladderModel, fullHouse])

				return renderLadder

			return renderRoof

		return renderDoors

	return renderWindows

def build_house(type):

	#defining scaling factors
	externalWalls = house.generate_2D_walls("house" + str(type) + "/" + "muriesterni0")
	xfactor = 15/SIZE([1])(externalWalls)[0]
	yfactor = 15.1/SIZE([2])(externalWalls)[0]
	zfactor = xfactor

	del factors[:]

	factors.append(xfactor)
	factors.append(yfactor)
	factors.append(zfactor)

	return (multistorey_house(type, 2)
	(XWindow,YWindow,occurrencyWindow,windoor.window(XWindow, YWindow, occurrencyWindow))
	(XDoor,YDoor,occurrencyDoor, windoor.door(XDoor, YDoor, occurrencyDoor))
	("muriesterni0",PI/5.,3/zfactor)
	(3.,.20,.04)
	)
