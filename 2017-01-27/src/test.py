from pyplasm import *
import random

def bottom():
	c = BEZIERCURVE([[1.5,0,0],[0.5,0,0],[0.5,0,5],[0.5,0,7]])
	domain = PROD([INTERVALS(1)(2*7), INTERVALS(2*PI)(7)])
	domain = PROD([domain, Q(1)])
	def bottom0(point):
		x,y,z = point
		r,none,q = c([x])
	
		fx = COS(y) * r
		fy = SIN(y) * r
		return fx * z,fy * z,q
	return MAP(bottom0)(domain)

def top():
	dom = T(1)(-PI/2.0)(PROD([INTERVALS(PI)(7), INTERVALS(2*PI)(7)]))
	dom = PROD([dom, Q(PI)])

	r = 4
	def chioma0(point):
		x,y,z = point
		fx = -r * COS(x) * COS(y)
		fy = r * COS(x) * SIN(y)
		fz = r * SIN(x + z)
		return fx,fy,fz

	c = MAP(chioma0)(dom)
	return R([2,3])(PI/2.)(c)

def render_tree():
	zscale = random.uniform(.5, 1.)
	xscale = random.uniform(0.45, .75)
	yscale = xscale
	rg = random.uniform(.1,.5)
	rot = random.uniform(0., PI)
	bot = MATERIAL([0.2,.15,0,.1,  0,0,0,1,  0,0,0,.1, 0,0,0,1, 1])(bottom())
	topt = MATERIAL([.1,rg,0,.7,  0,0,0,1,  0,.1,0,1, 0,0,0,1, 10])(top())
	#topt = MATERIAL([0,0,0,1,  0,rg,0,1,  0,.1,0,1, 0,0,0,1, 10])(top())

	#topt = TEXTURE("texture/leaf.jpg")(topt)
	#bot = TEXTURE("texture/bot_wood.jpg")(bot)
	tree = S([1,2,3])([xscale,yscale,zscale])(R([1,2])(rot)(STRUCT([bot, T(3)(10)(topt)])))
	return tree

#VIEW(render_tree())