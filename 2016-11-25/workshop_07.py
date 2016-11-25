from pyplasm import *

XWindow = [.3,.2,.1,.5,.4]
YWindow = [.3,.3,.2,.1,.1]
occurrencyWindow = [[True, True, True, True, True],
			  [True, False, True, False, True],
			  [True, True, True, True, True],
			  [True, False, True, False, True],
			  [True, True, True, True, True]]

YDoor = [.1, .2, .02, .2, .02, .2, .3, .2, .02, .2 ,.02, .2, .1]
XDoor = [.1, .2, .02, .2, .02, 1, .02, .2, .02, .2, .1]
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

def circle(r):
	def circle0(p):
		alpha = p[0]
		return [r*COS(alpha), r*SIN(alpha)]
	return circle0

def filterCells(ukpol):
	print ukpol[1]
	for cell_index in range(len(ukpol[1])):
		for vertex in ukpol[1][cell_index]:
			if (ukpol[0][vertex-1][1] < -0.1):
				ukpol[1][cell_index] = [0,0]
	return MKPOL([ukpol[0], ukpol[1], 1])

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


def window_main(X,Y,occurrency):
	def window0(dx,dy,dz):
		arc = CIRCLE(dx/2.)([14,2])
		arc = filterCells(UKPOL(SKEL_1(arc)))
		arc = OFFSET([.1,.1,.1])(arc)
		arc = MAP([S1,S3,S2])(arc)
		arc = S(3)(.5)(arc)
		dz = dz - SIZE([3])(arc)[0]
		arc = T([1,3])([dx/2., dz])(arc)
		arc = S(2)(dy/SIZE([2])(arc)[0])(arc)
		resizeXY(X,Y,occurrency, dx, dz)
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
		result.append(BOX([dx,dz,dy]))
		res = STRUCT(result)
		res = PROD([res, Q(dy)])
		res = MAP([S1,S3,S2])(res)
		print sum(X)
		print sum(Y)
		VIEW(STRUCT([res, arc]))
	return window0


def door_main(XDoor,YDoor,occurrency):
	def door0(dx,dy,dz):
		result = []
		circle_door = MAP(circle(sum(YDoor[4:9])/2.*.95))(INTERVALS(2*PI)(50))
		print(YDoor[4:9])
		print(sum(YDoor[4:9])/2.)
		circle_door = JOIN(circle_door)
		circle_door = PROD([circle_door, Q(dy/4.)])
		circle_door = MAP([S1,S3,S2])(circle_door)
		circle_door = T([1,2,3])([dx/2., dy-dy/4.+0.001, dz/2.])(circle_door)
		for x_index in range(len(XDoor)):
			y_quotes = []
			x_sum = sum(XDoor[:x_index])
			for y_index in range(len(YDoor)):
				if(occurrency[x_index][y_index] == False):
					y_quotes.append(-YDoor[y_index])
				else:
					y_quotes.append(YDoor[y_index])
			result.append(PROD([ QUOTE([-x_sum, XDoor[x_index]]), QUOTE(y_quotes)]))
		result.append(BOX([dx,dz,dy]))
		res = STRUCT(result)
		res = PROD([res, Q(dy)])
		res = MAP([S2,S3,S1])(res)
		res = S([1,2,3])([dx/SIZE([1])(res)[0], dy/SIZE([2])(res)[0], dz/SIZE([3])(res)[0]]) (res)
		door = STRUCT([res, circle_door])
		door = TEXTURE(["iron.jpg", True, False, 1, 1, 0, 1, 1])(door)
		glass = CUBOID([SIZE([1])(res)[0]*0.94,dy/4.*.94,SIZE([3])(res)[0]*0.94])
		glass = T([1,2,3])([dx*0.05, dy/7.+dy*0.05, dz*0.05])(glass)
		glass = TEXTURE(["vetro.jpg"])(glass)
		refiner = CUBOID([dx/30, dy/20,dz])
		refiner = T([1,2])([dx/2.-dx/60,dy])(refiner)
		refiner = TEXTURE(["iron.jpg", True, False, 1, 1, 0, 1, 1])(refiner)
		handle1 = T(3)(.15)(CUBOID([.05,.02,.2]))
		handle2 = CUBOID([.05,.02,.05])
		handle3 = T([1,2])([.01,.02])(CUBOID([.03,.02,.2]))
		handles = TEXTURE("bronze.jpg")(STRUCT([handle3, handle2, handle1]))
		handles = T([1,2,3])([dx/2.-2*SIZE([1])(handles)[0],dy, dz/2.-1.5*SIZE([3])(handles)[0]])(handles)
		finalDoor = S([1,2,3])([dx/SIZE([1])(res)[0], dy/SIZE([2])(res)[0], dz/SIZE([3])(res)[0]]) (STRUCT([door, glass, refiner, handles]))
		VIEW(finalDoor)
	return door0

window_main(XWindow,YWindow,occurrencyWindow)(3,.2,2)
#door_main(XDoor, YDoor, occurencyDoor)(1.8, .4, 3)