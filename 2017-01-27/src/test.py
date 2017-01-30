from pyplasm import *
import random

def log():
	D = PROD([PROD([INTERVALS(1)(5), INTERVALS(2*PI)(10)]), Q(1)])
	bezCurve = BEZIERCURVE([[1.5,0,0],[0.5,0,0],[0.5,0,5],[0.5,0,7]])
	
	def log0(point):
		x,y,z = point
		radius,zero,quote = bezCurve([x])
		mapx = COS(y) * radius
		mapy = SIN(y) * radius
		return mapx * z,mapy * z,quote

	return MAP(log0)(D)

def leaves():
	D = T(1)(-PI/2)(PROD([INTERVALS(PI)(7), INTERVALS(2*PI)(7)]))
	D = PROD([D, Q(PI)])
	radius = 4
	bezCurve = BEZIERCURVE([[1.5,0,0],[0.5,0,0],[0.5,0,5],[0.5,0,7]])

	def leaves0(point):
		x,y,z = point
		mapx = -radius * COS(x) * COS(y)
		mapy = radius * COS(x) * SIN(y)
		mapz = radius * SIN(x + z)
		return mapx,mapy,mapz

	bezCurve = MAP(leaves0)(D)

	return R([2,3])(PI/2.)(bezCurve)

def render_tree():
	zscale = random.uniform(.5, 1.)
	xscale = random.uniform(0.45, .75)
	yscale = xscale
	randg = random.uniform(.1,.5)
	rot = random.uniform(0., 2*PI)
	logModel = MATERIAL([0.2,.15,0,.1,  0,0,0,1,  0,0,0,.1, 0,0,0,1, 1])(log())
	leavesModel = MATERIAL([.1,randg,0,.7,  0,0,0,1,  0,.1,0,1, 0,0,0,1, 10])(leaves())
	tree = S([1,2,3])([xscale,yscale,zscale])(R([1,2])(rot)(STRUCT([logModel, T(3)(10)(leavesModel)])))
	return tree

VIEW(render_tree())