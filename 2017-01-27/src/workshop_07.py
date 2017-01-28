from pyplasm import *

#XWindow = [.2,.8,.05,.8,.2,.8,.05,.8,.2]
#YWindow = [.1,.7,.05,.7,.05,.7,.05,.7,.01]

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


#YDoor = [.1, .2, .02, .2, .02, .2, .3, .2, .02, .2 ,.02, .2, .1]
#XDoor = [.1, .2, .02, .2, .02, 1, .02, .2, .02, .2, .1]

YDoor = [.2, .2, .1, .4, .1, .2, .3, .2, .1, .4 ,.1, .2, .2]
XDoor = [.4, .3, .04, .6, .05, 1.4, .04, .3, .04, .5, .3]
occurencyDoor = [[True, True, True, True, True, True, True, True, True, True, True, True, True],
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
"""
circle is a function that, given a radius return a function that given an angle return the part 
of the circumference, defined by the angle, described by the radius.
@param r: radius of the circumference
@param p: angle of the circumference to represent
@return a part of circumference
"""
def circle(r):
	def circle0(p):
		alpha = p[0]
		return [r*COS(alpha), r*SIN(alpha)]
	return circle0

"""
removeNegativeCells is a function that given the result of a UKPOL call, remove the cells that contain
vertices with a negative Y-axis value, and return the cleaned polyhedron. 
This function is used to generate the window's upper arc.
@param ukpol: the result of a UKPOL call
@return : a polyhedron cleaned, based on the initial UKPOL
"""
def removeNegativeCells(ukpol):
	for cell_index in range(len(ukpol[1])):
		for vertex in ukpol[1][cell_index]:
			if (ukpol[0][vertex-1][1] < -0.01):
				ukpol[1][cell_index] = [0,0]
	return MKPOL([ukpol[0], ukpol[1], 1])

"""
resizeXY is a function that given three array X,Y,occurrency and two dimensions dx and dz, scale the values
contained in X and Y, in such a way that, only empty spaces are scaled and filled spaces are mantained fixed.
@param X: array of distances on X-axis, relative distance calculated on the previous point
@param Y: array of distances on Y-axis, relative distance calculated on the previous point
@param occurrency: array of occurrences defining which spaces are empty and which are filled
@param dx: given desired dimension, X-axis
@param dz: given desired dimension, Z-axis
"""
def resizeXY(X, Y, occurrency, dx, dz):
	sumY = sum(Y) 
	sumX = sum(X)
	visitedY = [False]*len(Y)
	for y_index in range(len(Y)):
		update = True
		for x_index in range(len(X)):
			if(occurrency[x_index][y_index] == False):
				update = False 
		if(update):
			sumY = sumY - Y[y_index]
			sumX = sumX - X[y_index]
			dx = dx - X[y_index]
			dz = dz - Y[y_index]

	for x_index in range(len(X)):
		modifyX = False
		for y_index in range(len(Y)):
			if(occurrency[x_index][y_index] == False and visitedY[y_index] == False):
				Y[y_index] = (dz * Y[y_index])/sumY
				visitedY[y_index] = True
				modifyX = True
			if(occurrency[x_index][y_index] == False and visitedY[y_index] == True and not modifyX):
				modifyX = True
		if(modifyX):
			X[x_index] = (dx * X[x_index])/sumX

"""
window is a main function that given three array, X, Y and occurrency, return the HPC model of the window
generated according to the three parameters. X and Y contain values of distances calculated on the previous 
segment of the axis contained respectively in each array. Occurrency is a matrix containing booleans that
map which cell is empty and which cell is filled. Window0 is an inner function useful for "scaling"
(@see resizeXY) the resulting window, according to the three parameter dx, dy, dz.
@param X: array of distances on X-axis, relative distance calculated on the previous point
@param Y: array of distances on Y-axis, relative distance calculated on the previous point
@param occurrency: array of occurrences defining which spaces are empty and which are filled
@param dx: given desired dimension, X-axis
@param dy: given desired dimension, Y-axis
@param dz: given desired dimension, Z-axis
"""
def window(X,Y,occurrency):

	def window0(dx,dy,dz):

		#generating arc and glass filler
		arc = CIRCLE(dx/2.)([14,2])
		arc = removeNegativeCells(UKPOL(SKEL_1(arc)))
		glassArc = JOIN(arc)
		glassArc = PROD([glassArc, Q(dy/4.*.94)])
		arc = OFFSET([.1,.1,.1])(arc)
		arc = MAP([S1,S3,S2])(arc)
		glassArc = MAP([S1,S3,S2])(glassArc)
		glassArc = S(3)(.8)(glassArc)
		arc = S(3)(.8)(arc)

		#calculating new space for the lower frame
		dz = dz - SIZE([3])(arc)[0]

		#completing upper arc
		arc = T([1,3])([dx/2., dz])(arc)
		arc = S(2)(dy/SIZE([2])(arc)[0])(arc)

		#generating front frame, handles and joints
		frame = CUBOID([dx/2.*.975,0.01,dz])
		framediff = S([1,3])([.95,.95])(frame)
		framediff = T([1,3])([SIZE([1])(frame)[0]*.025, SIZE([3])(frame)[0]*.025])(framediff)
		frame = DIFFERENCE([frame, framediff])
		frame = T([1,2,3])([SIZE([1])(frame)[0]*.025, dy ,SIZE([3])(frame)[0]*.025])(frame)
		frame2 = T(1)(dx/2.- SIZE([1])(frame)[0]*.025)(frame)
		joint = CYLINDER([0.02, .1])(40)
		joint = T([1,2,3])([dx - SIZE([1])(frame)[0]*.025,dy*1.02,dz/4.])(joint)
		joint2 = T([3])([dz/2.])(joint)
		handle = CUBOID([.02,.02,.015])
		handle2 = CUBOID([.02,.02,.1])
		handle2 = T([2,3])([.02,-.085])(handle2)
		handles = STRUCT([handle,handle2])
		handle = T([1,2,3])([dx/2.- SIZE([1])(frame)[0]*.025 - SIZE([1])(handles)[0], dy, 11*dz/20.])(handles)
		handle2 = T([1,2,3])([dx/2.+ SIZE([1])(frame)[0]*.025, dy, 11*dz/20.])(handles)

		#resizing empty spaces
		resizeXY(X,Y,occurrency, dx, dz)

		#building main frame
		result = []
		for x_index in range(len(X)):
			y_quotes = []
			x_sum = sum(X[:x_index])
			for y_index in range(len(Y)):
				if(occurrency[x_index][y_index] == False):
					y_quotes.append(-Y[y_index])
				else:
					y_quotes.append(Y[y_index])
			result.append(PROD([ QUOTE([-x_sum, X[x_index]]), QUOTE(y_quotes)]))

		#remapping frame's axis
		res = STRUCT(result)
		res = MAP([S1,S3,S2])(PROD([res, Q(dy)]))

		#generating glass filler for the lower frame and the upper arc
		glass = CUBOID([SIZE([1])(res)[0]*0.99,dy/4.*.99,SIZE([3])(res)[0]*0.99])
		glass = T([1,2,3])([dx*0.01, dy/7.+dy*0.01, dz*0.01])(glass)
		glass = TEXTURE(["texture/vetro2.jpg"])(glass) 
		glassArc = T([1,2,3])([dx/2., dy/7.+dy*0.05, dz])(glassArc)
		glassArc = TEXTURE(["texture/vetro2.jpg"])(glassArc)

		#adding some fancy texture to the frame, assemblig all the parts
		windowFrame = STRUCT([res, arc, frame, frame2, joint, joint2, handle, handle2])
		windowFrame = TEXTURE(["texture/wood_window.jpg"])(windowFrame)
		window = STRUCT([windowFrame, glass, glassArc])

		#global scaling
		window = S([1,2,3])([dx/SIZE([1])(window)[0], dy/SIZE([2])(window)[0], dz/SIZE([3])(window)[0]])(window)

		return window

	return window0

"""
door is a main function that given three array, X, Y and occurrency, return the HPC model of the door
generated according to the three parameters. X and Y contain values of distances calculated on the previous 
segment of the axis contained respectively in each array. Occurrency is a matrix containing booleans that
map which cell is empty and which cell is filled. Door0 is an inner function useful for scaling
the resulting door, according to the three parameter dx, dy, dz.
@param X: array of distances on X-axis, relative distance calculated on the previous point
@param Y: array of distances on Y-axis, relative distance calculated on the previous point
@param occurrency: array of occurrences defining which spaces are empty and which are filled
@param dx: given desired dimension, X-axis
@param dy: given desired dimension, Y-axis
@param dz: given desired dimension, Z-axis
"""
def door(XDoor,YDoor,occurrency):

	def door0(dx,dy,dz):

		result = []
		#creating cylinder part of the door
		circle_door = MAP(circle(sum(YDoor[4:9])/2.*.95))(INTERVALS(2*PI)(50))
		circle_door = PROD([JOIN(circle_door), Q(dy/4.)])
		circle_door = MAP([S1,S3,S2])(circle_door)
		circle_door = S([1,2,3])([dx/SIZE([1])(circle_door)[0]/2., dy/SIZE([2])(circle_door)[0]/5., dz/SIZE([3])(circle_door)[0]/5.]) (circle_door)
		circle_door = T([1,2,3])([dx/2., dy-dy/4.+0.001, dz/2.])(circle_door)

		#building main door's frame
		for x_index in range(len(XDoor)):
			y_quotes = []
			x_sum = sum(XDoor[:x_index])
			for y_index in range(len(YDoor)):
				if(occurrency[x_index][y_index] == False):
					y_quotes.append(-YDoor[y_index])
				else:
					y_quotes.append(YDoor[y_index])
			result.append(PROD([ QUOTE([-x_sum, XDoor[x_index]]), QUOTE(y_quotes)]))

		#assembling all together
		res = PROD([STRUCT(result), Q(dy)])
		res = MAP([S2,S3,S1])(res)
		res = S([1,2,3])([dx/SIZE([1])(res)[0], dy/SIZE([2])(res)[0], dz/SIZE([3])(res)[0]]) (res)
		door = TEXTURE(["texture/wood.jpg", True, False, 1, 1, 0, 1, 1])(STRUCT([res, circle_door]))

		#adding some fancy glass and iron textures
		glass = CUBOID([SIZE([1])(res)[0]*0.94,dy/4.*.94,SIZE([3])(res)[0]*0.94])
		glass = T([1,2,3])([dx*0.05, dy/7.+dy*0.05, dz*0.05])(glass)
		glass = TEXTURE(["texture/vetro.jpg"])(glass)

		#building some details
		refiner = CUBOID([dx/30, dy/20,dz])
		refiner = T([1,2])([dx/2.-dx/60,dy])(refiner)
		refiner = TEXTURE(["texture/wood.jpg", True, False, 1, 1, 0, 1, 1])(refiner)

		#building the handle
		handle1 = T(3)(.15)(CUBOID([.05,.02,.2]))
		handle2 = CUBOID([.05,.02,.05])
		handle3 = T([1,2])([.01,.02])(CUBOID([.03,.02,.2]))
		handles = TEXTURE("texture/bronze.jpg")(STRUCT([handle3, handle2, handle1]))
		handles = S([1,2,3])([20,20,20])(handles)
		handles = T([1,2,3])([dx/2.-2*SIZE([1])(handles)[0],dy, dz/2.-1.5*SIZE([3])(handles)[0]])(handles)

		#assembling all together and global scaling
		finalDoor = S([1,2,3])([dx/SIZE([1])(res)[0], dy/SIZE([2])(res)[0], dz/SIZE([3])(res)[0]]) (STRUCT([door, glass, refiner, handles]))
		
		return finalDoor

	return door0

#VIEW(window(XWindow,YWindow,occurrencyWindow)(2,.2,3))
#VIEW(window(XWindow,YWindow,occurrencyWindow)(1,.3,2))

#VIEW(door(XDoor, YDoor, occurencyDoor)(1.8, .4, 3))
#VIEW(door(XDoor, YDoor, occurencyDoor)(2.5, .3, 3))