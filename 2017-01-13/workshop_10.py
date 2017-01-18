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

			def RenderRoof(vertices, pitchAngle, height):

				if isinstance(vertices, basestring):
					with open("lines/" + vertices + ".lines", "rb") as file:
						reader = csv.reader(file, delimiter=",")
						vertices = []
						for row in reader:
							vertices.append([float(row[0]), float(row[1])])
				roofModel = roof.roofBuilder(vertices, pitchAngle, height)
				roofModel = T([3])([nStorey*3/zfactor])(roofModel)
				roofModel = S([1,2,3])([xfactor*1.02,yfactor*1.02,zfactor])(roofModel)

				full_house = []
				for story in range(nStorey):
					h = house.build_house(story, windowModel, doorModel)
					full_house.append(h)
					full_house.append(T([3])([3]))
				return STRUCT([roofModel] + full_house)

			return RenderRoof
		return renderDoors

	return renderWindows
		
#VIEW(STRUCT([placeAndRenderRoof("muriesterni",PI/3,1.5/xfactor),renderWindowsAndDoors()]))
#VIEW(STRUCT([renderWindowsAndDoors()]))
VIEW((buildMultiStorey(2)
	(XWindow,YWindow,occurrencyWindow,windoor.window(XWindow, YWindow, occurrencyWindow))
	(XDoor,YDoor,occurrencyDoor, windoor.door(XDoor, YDoor, occurrencyDoor))
	("muriesterni0",PI/5.,2.5/xfactor)
	))