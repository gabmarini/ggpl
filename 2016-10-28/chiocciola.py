from pyplasm import *
import math 

def circle(r):
	def circle0(p):
		alpha = p[0]
		return [r*COS(alpha), r*SIN(alpha)]
	return circle0

def make_step(step_length, step_width, riser):
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
	step_number = math.ceil(height/(inter_step+riser))
	step = TEXTURE("wood.jpg")(make_step(.8,[.03,.5],.04))
	handrail = make_handrail(.5,.8)
	ROT = R([1,2])(-2*PI/11)
	TR = T([3])([inter_step+riser])
	ladder = [step,handrail,ROT,TR]*int(step_number)
	pole = TEXTURE("copper.jpg")(CYLINDER([.03,step_number*(riser+inter_step)-inter_step])(20))
	ladder = [pole] + ladder
	return STRUCT(ladder)

def make_handrail(length, step_length):
	handrail = CYLINDER([0.04,length+length*0.075])(30)
	handrail = R([1,2])(PI/2)(handrail)
	handrail = R([2,3])(PI/2-SIN(length))(handrail)
	handrail = T([1,2,3])([step_length,length/2.,.7+.05])(handrail)
	handrail = TEXTURE("copper.jpg")(handrail)
	cyl1 = CYLINDER([0.02,.7+.05+TAN(SIN(length))*length/4.])(30)
	cyl1 = T([1,2,3])([step_length,length/2-length/4.,0.01])(cyl1)
	cyl1 = TEXTURE("steel.jpg")(cyl1)
	cyl2 = CYLINDER([0.02,.7+.05+TAN(SIN(length))*2*length/4.])(30)
	cyl2 = TEXTURE("steel.jpg")(cyl2)
	cyl2 = T([1,2,3])([step_length,length/2-2*length/4.,0.01])(cyl2)
	cyl3 = CYLINDER([0.02,.7+.05+TAN(SIN(length))*3*length/4.])(30)
	cyl3 = TEXTURE("steel.jpg")(cyl3)
	cyl3 = T([1,2,3])([step_length,length/2-3*length/4.,0.01])(cyl3)
	return STRUCT([handrail, cyl1, cyl2, cyl3])


VIEW((make_ladder(3,.20,.04)))
