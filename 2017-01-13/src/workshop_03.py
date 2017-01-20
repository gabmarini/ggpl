from pyplasm import *
import math 

def circle(r):
	def circle0(p):
		alpha = p[0]
		return [r*COS(alpha), r*SIN(alpha)]
	return circle0

def make_step(step_length, step_width, riser):
	"""
	make_step is a function that given a step length, a step width and a riser generate a single step of a spiral
	stair, including a pole's part at the beginning of the step.
	@param step_length: the length of a single step
	@param step_width: the width of a single step
	@param riser: riser value of the step
	"""
	min,max = step_width
	diff = (max-min)/2.
	step_partial = POLYLINE([[0,0],[0,min],[step_length, min+diff],[step_length,-diff]])
	step_partial = JOIN(step_partial)
	refiner_big = JOIN(MAP(circle(max/2.))(INTERVALS(PI)(32)))
	refiner_big = R([1,2])(-PI/2)(refiner_big)
	refiner_big = S(1)(.3)(refiner_big)
	refiner_big = T([1,2])([step_length,min/2.])(refiner_big)
	refiner_small = JOIN(MAP(circle(min))(INTERVALS(PI)(32)))
	refiner_small = R([1,2])(-PI/2)(refiner_small)
	refiner_small = T([2])([min/2.])(refiner_small)
	step_partial = DIFFERENCE([step_partial, refiner_small])
	step = STRUCT([refiner_big, step_partial])
	step = PROD([step, Q(riser)])
	step = T([2])([-min/2.])(step)
	refiner_pole = CYLINDER([min+(min*0.2),riser])(20)
	return STRUCT([step,refiner_pole])


def make_ladder(height, inter_step, riser):
	"""
	make_ladder is a function that given an height, an inter step value and a riser return the model of a ladder.
	@param height: the desired height of the stair
	@param inter_step: the desired height between two steps
	@param riser: the desired riser value for a step
	@return ladder: the ladder model
	"""
	step_number = math.ceil(height/(inter_step+riser))
	step = TEXTURE("texture/wood.jpg")(make_step(.8,[.03,.5],.04))
	handrail = make_handrail(.5,.8)
	ROT = R([1,2])(-2*PI/11)
	TR = T([3])([inter_step+riser])
	ladder = [step,handrail,ROT,TR]*int(step_number)
	pole = TEXTURE("texture/copper.jpg")(CYLINDER([.03,step_number*(riser+inter_step)-inter_step])(20))
	ladder = [pole] + ladder
	return STRUCT(ladder)

def make_handrail(length, step_length):
	"""
	make_handrail is a function that given an handrail lenght and a step length generate the handrail model 
	of the corresponding step.
	@param length: the length of the handrail
	@param step_length: the lenght of the step
	@return handrail: handrail's model generated
	"""
	handrail = CYLINDER([0.04,length+length*0.075])(30)
	handrail = R([1,2])(PI/2)(handrail)
	handrail = R([2,3])(PI/2-SIN(length))(handrail)
	handrail = T([1,2,3])([step_length,length/2.,.7+.05])(handrail)
	handrail = TEXTURE("texture/copper.jpg")(handrail)
	cyl1 = CYLINDER([0.02,.7+.05+TAN(SIN(length))*length/4.])(30)
	cyl1 = T([1,2,3])([step_length,length/2-length/4.,0.01])(cyl1)
	cyl1 = TEXTURE("texture/steel.jpg")(cyl1)
	cyl2 = CYLINDER([0.02,.7+.05+TAN(SIN(length))*2*length/4.])(30)
	cyl2 = TEXTURE("texture/steel.jpg")(cyl2)
	cyl2 = T([1,2,3])([step_length,length/2-2*length/4.,0.01])(cyl2)
	cyl3 = CYLINDER([0.02,.7+.05+TAN(SIN(length))*3*length/4.])(30)
	cyl3 = TEXTURE("texture/steel.jpg")(cyl3)
	cyl3 = T([1,2,3])([step_length,length/2-3*length/4.,0.01])(cyl3)
	return STRUCT([handrail, cyl1, cyl2, cyl3])
