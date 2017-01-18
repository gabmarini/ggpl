from pyplasm import *
from src import chiocciola as ladder
from src import workshop_07 as windoor 
from src import workshop_08 as house
from src import workshop_09 as roof
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


#defining scaling factors
externalWalls = house.generate_2D_walls("muriesterni0")
xfactor = 15/SIZE([1])(externalWalls)[0]
yfactor = 15.1/SIZE([2])(externalWalls)[0]
zfactor = xfactor





def buildMultiStorey(nStorey):

	def renderWindows(XWindow, YWindow, occurrencyWindow, windowModel):

		def renderDoors(XDoor, YDoor, occurrencyDoor, doorModel):

			def renderRoof(vertices, pitchAngle, height):

				def renderLadder(ladderHeight, interStep, riser):

					ladderModel = ladder.make_ladder(ladderHeight, interStep, riser)
					with open("lines/ladder.lines", "rb") as ladderFile:
						reader = csv.reader(ladderFile, delimiter=",")
						row = next(reader)
						ladderModel = T([1,2])([float(row[0])*xfactor, float(row[1])*yfactor])(ladderModel)
					ladderBOX = CUBOID([SIZE([1])(ladderModel)[0]/xfactor,SIZE([2])(ladderModel)[0]/yfactor, SIZE([3])(ladderModel)[0]/zfactor])
					ladderBOX = T([1,2])([float(row[0])-SIZE([1])(ladderBOX)[0]/2., float(row[1])-SIZE([2])(ladderBOX)[0]/2.])(ladderBOX)

					if isinstance(vertices, basestring):
						with open("lines/" + vertices + ".lines", "rb") as file:
							reader = csv.reader(file, delimiter=",")
							newVertices = []
							for row in reader:
								newVertices.append([float(row[0]), float(row[1])])
					if newVertices:
						roofModel = roof.roofBuilder(newVertices, pitchAngle, height)
					else:
						roofModel = roof.roofBuilder(vertices, pitchAngle, height)
					roofModel = T([3])([nStorey*3/zfactor])(roofModel)
					roofModel = S([1,2,3])([xfactor*1.02,yfactor*1.02,zfactor])(roofModel)

					full_house = []
					for story in range(nStorey):
						h = house.build_house(story, windowModel, doorModel, ladderBOX)
						full_house.append(h)
						full_house.append(T([3])([3]))

				
					full_house = STRUCT(full_house)
					return STRUCT([roofModel, ladderModel, full_house])
				return renderLadder
			return renderRoof
		return renderDoors

	return renderWindows
		
VIEW((buildMultiStorey(2)
	(XWindow,YWindow,occurrencyWindow,windoor.window(XWindow, YWindow, occurrencyWindow))
	(XDoor,YDoor,occurrencyDoor, windoor.door(XDoor, YDoor, occurrencyDoor))
	("muriesterni0",PI/5.,2.5/zfactor)
	(3.,.20,.04)
	))