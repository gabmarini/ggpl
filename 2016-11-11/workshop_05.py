from pyplasm import *
import random

def draw_point_in_circle(radius, npoints):
	return [(COS(2*PI/npoints*x)*radius,SIN(2*PI/npoints*x)*radius) for x in range(0,npoints+1)]

def circle(r):
	def circle0(p):
		alpha = p[0]
		return [r*COS(alpha), r*SIN(alpha)]
	return circle0

def ggpl_table(dx,dy,dz):
	tableThickness = .05
	chairThickness = .02
	supportThickness = .03
	chairSeat = .175
	grey = Color4f([184/255., 186/255., 186/255., 1])
	seatTableDifference = (dz - tableThickness - chairThickness - supportThickness)/2.


	seat = CYLINDER([chairSeat,chairThickness])(100)

	table = CYLINDER([dx/2. - chairSeat, tableThickness])(100)
	table = T([3])([dz - tableThickness])(table)
	table = COLOR(Color4f([38/255.,226/255.,189/255.,1]))(table)

	traslations = (draw_point_in_circle((dx - 2*chairSeat)/2.,16))[::2]

	seats = []

	chairSupport = CYLINDER([.03, seatTableDifference + supportThickness])(100)
	chairSupport = COLOR(grey)(chairSupport)
	mainSupport = CYLINDER([.15, dz - tableThickness])(100)
	mainSupport = COLOR(grey)(mainSupport)

	support = CYLINDER([supportThickness/2., dx/2. - 2*chairSeat/2.])(100)
	support = MAP([S3,S2,S1])(support)
	support = T([3])(seatTableDifference/2.)(support)
	support = COLOR(grey)(support)

	supports = [support, R([1,2])(2*PI/8.)]*8

	for i in traslations:
		tempSeat = T([1,2,3])([i[0],i[1],seatTableDifference + supportThickness])(seat)
		seats.append(COLOR(Color4f([random.random()*255/255.,random.random()*255/255.,random.random()*255/255.,1]))(tempSeat))
		seats.append(T([1,2])([i[0],i[1]])(chairSupport))

	box = SKEL_1(BOX([1,2,3])(CUBOID([dx,dy,dz])))
	box = T([1,2])([-dx/2.,-dy/2.])(box)

	seats = seats + supports
	seats.append(mainSupport)
	seats.append(box)
	seats.append(table)

	return STRUCT(seats)

#for tony modify the difference between box and chair
def ggpl_chair(dx,dy,dz):
	footRadius = .05
	seatHeight = .015
	seatBackThickness = .015
	seatBackHeight = dz/6.
	sphere = SPHERE(footRadius)([40,40])
	sphere = JOIN(SKEL_1(sphere))

	chair = []

	feet = [[0 + footRadius,0 + footRadius],[dx - footRadius,0 + footRadius], [dx - footRadius, dy - footRadius], [0 + footRadius, dy - footRadius]]

	support = CYLINDER([1.3*footRadius/2.,dy - 2*footRadius])(100)
	support = MAP([S1,S3,S2])(support)
	sideSupport = T([1,2,3])([footRadius,footRadius,dz/4. - footRadius])(support)
	sideSupports = [sideSupport, T([1])([dx - 2*footRadius])(sideSupport)]
	otherSideSupport = CYLINDER([1.3*footRadius/2.,dx - 2*footRadius])(100)
	otherSideSupport = MAP([S1,S3,S2])(otherSideSupport)
	otherSideSupport = R([1,2])(-PI/2.)(otherSideSupport)
	otherSideSupport = T([1,2,3])([footRadius,footRadius,7*dz/20.])(otherSideSupport)
	otherSideSupports = [otherSideSupport, T([2])([dy-2*footRadius])(otherSideSupport)]
	support = S(1)(.75)(support)
	support = T([1,2,3])([footRadius,footRadius,dz/2. - footRadius/2.])(support)
	supports = [support, T([1])([dx - 2*footRadius])(support)]

	seat = CUBOID([dx - 2*footRadius, dy - 2*footRadius, seatHeight])
	seat = T([1,2,3])([footRadius, footRadius, dz/2.-footRadius/2.])(seat)

	seatBack = CUBOID([dx - 2*footRadius, seatBackThickness, seatBackHeight])
	seatBack = T([1,2,3])([footRadius, footRadius, dz - 2*footRadius - seatBackHeight])(seatBack)

	for foot in feet:
		if(foot[1] != footRadius):
			solidFoot = CYLINDER([footRadius, dz/2.])(100)
			footSphere = T([1,2,3])([foot[0],foot[1],dz/2.])(sphere)
		else:
			solidFoot = CYLINDER([footRadius, dz - footRadius])(100)
			footSphere = T([1,2,3])([foot[0],foot[1],dz - footRadius])(sphere)
		solidFoot = T([1,2])([foot[0],foot[1]])(solidFoot)
		chair.append(solidFoot)
		chair.append(footSphere)

	box = SKEL_1(CUBOID([dx,dy,dz]))

	chair.append(box)
	chair.append(seat)
	chair.append(seatBack)
	chair = chair + supports + sideSupports + otherSideSupports

	return COLOR(Color4f([193/255., 154/255., 107/255., 1]))(STRUCT(chair))


def ggpl_professor_desk(dx, dy, dz):
	desk = []
	footRadius = .05
	deskThickness = .03
	border = dx/30
	knobRadius = .02

	feet = [[0 + footRadius + border,0 + footRadius + border],[dx - footRadius - border,0 + footRadius + border], [dx - footRadius - border, dy - footRadius -border], [0 + footRadius + border, dy - footRadius - border]]

	for foot in feet:
		solidFoot = CYLINDER([footRadius, dz - deskThickness])(100)
		solidFoot = T([1,2])([foot[0],foot[1]])(solidFoot)
		desk.append(solidFoot)

	deskPlane = CUBOID([dx, dy, deskThickness])
	deskPlane = T([3])(dz- deskThickness)(deskPlane)
	deskPlane = COLOR(Color4f([139/255., 232/255., 184/255., 1]))(deskPlane)
	desk.append(deskPlane)

	deskSupport = CUBOID([dx - 2*border - 2* footRadius, footRadius, 2*deskThickness])
	deskSupportFirst = T([1,2,3])([border+footRadius/2., border + footRadius/2., dz - 3*deskThickness])(deskSupport)
	deskSupports = [deskSupportFirst, T([1,2,3])([border+footRadius/2., dy-SIZE([2])(deskSupport)[0]-border-footRadius/2, dz - 3*deskThickness])(deskSupport)]

	anotherDeskSupport =  CUBOID([footRadius, dy - 2*border - 2*footRadius, 2*deskThickness])
	anotherDeskSupportFirst = T([1,2,3])([border + footRadius/2, border + footRadius/2, dz - 3*deskThickness])(anotherDeskSupport)
	anotherDeskSupports = [anotherDeskSupportFirst, T([1,2,3])([dx - SIZE([1])(anotherDeskSupport)[0]-border-footRadius/2 ,border + footRadius/2, dz - 3*deskThickness])(anotherDeskSupport)]

	drawer = CUBOID([dx/3-border-2*footRadius, dy/2., dz/10 + footRadius])
	drawer = T([1,2,3])([border + 2*footRadius, border + 2*footRadius, dz - deskThickness - 2*deskThickness - dz/10])(drawer)
	drawerWall = CUBOID([dx/3-border-2*footRadius, footRadius, dz/10])
	drawerWall = T([1,2,3])([border + 2*footRadius, 2*border, dz - deskThickness - 2*deskThickness - dz/10])(drawerWall)
	knob = SPHERE(knobRadius)([40,40])
	knob = JOIN(SKEL_1(knob))
	knob = T([1,2,3])([border + 2*footRadius + SIZE([1])(drawerWall)[0]/2, border + footRadius*.65, dz - deskThickness - 2*deskThickness - SIZE([3])(drawerWall)[0]/2])(knob)
	drawers = [drawer, drawerWall, knob, T([1])([dx - 2*border - 4*footRadius - SIZE([1])(drawer)[0]]), drawer, drawerWall, knob]

	box = SKEL_1(CUBOID([dx,dy,dz]))

	desk.append(box)
	desk = desk + deskSupports + anotherDeskSupports + drawers
	return COLOR(Color4f([193/255., 154/255., 107/255., 1]))(STRUCT(desk))

def ggpl_closet(dx, dy, dz):
	brown = Color4f([129/255., 65/255., 13/255., 1])
	waterGreen = Color4f([139/255., 232/255., 184/255., 1])
	closet = []
	dividerWidth = dx*.05
	mainStructureWidth = dx*.95

	mainStructure = CUBOID([mainStructureWidth,dy*.95, dz*.97])
	mainStructure = T([1])([dx*.025])(mainStructure)
	mainStructure = COLOR(brown)(mainStructure)

	divider = CUBOID([dividerWidth/2., dy, dz])
	divider = COLOR(brown)(divider)
	dividers = [divider, T([1])([dx*.975])(divider)]

	door = CUBOID([mainStructureWidth/2, dy*.025, dz*.9])
	door = COLOR(waterGreen)(door)
	door = T([1,2,3])([dividerWidth/2., dy*.95, dz*.06])(door)
	doors = [door, T([1])([dividerWidth/2. + SIZE([1])(door)[0] - dx*.02]), door]

	knob = SPHERE(.02)([30,30])
	knob = JOIN(SKEL_1(knob))
	knob = COLOR(brown)(knob)
	knob = T([1,2,3])([dx*.45, dy*.99, dz*.5])(knob)

	box = SKEL_1(CUBOID([dx,dy,dz]))

	closet.append(mainStructure)
	closet.append(box)
	closet.append(knob)
	closet = closet + dividers + doors

	return STRUCT(closet)

def ggpl_main():
	table = ggpl_table(2,2,1)
	tables = [table, T([1])(3)(ggpl_table(2,2,1)), T([2])([3])(ggpl_table(2,2,1)), T([1,2])([3,3])(ggpl_table(2,2,1))]

	desk = ggpl_professor_desk(1.5,1.,1.25)

	chair = ggpl_chair(.8, .7, 1.5)

	closet = ggpl_closet(2,.8,2.5)
	closet = R([1,2])(-PI/2)(closet)
	closet = T([1])(-2.5)(closet)

	chair = T([1,2])([.40,-.6])(chair)

	professorDesk = STRUCT([chair, desk])
	professorDesk = T([1,2])([.8,-2.5])(professorDesk)

	classroom = []
	classroom.append(closet)
	classroom = classroom + tables
	classroom = STRUCT(classroom)
	completeClassroom = STRUCT([classroom, professorDesk])

	floor = SIZE([1,2])(completeClassroom)
	floor[0] = floor[0] + .3 * floor[0]
	floor[1] = floor[1] + .3 * floor[1]
	floor = INSR(PROD)([Q(floor[0]), Q(floor[1]), Q(-.01)])
	floor = COLOR(Color4f([100/255., 100/255., 100/255., .2]))(floor)
	floor = T([1,2])([-SIZE([1])(floor)[0]/2. + .5, -SIZE([2])(floor)[0]/2. + .5])(floor)
	
	VIEW(STRUCT([classroom, professorDesk, floor]))

ggpl_main()

