from pyplasm import *
import csv
from ast import literal_eval as make_tuple

 
def intersperse(seq, value):
    """
    intersperse is a function that, given a list and a value, intersperse the list with the value.
    If the resultant list has an odd number of elements,
    a value is appended to the end of it.
 
    @param seq: the list to intersperse
    @param value: the value to insert into the new list
    @return res: a new list interspersed
    """
    res = [value] * (2 * len(seq) - 1)
    res[::2] = seq
    if (len(res)%2 != 0):
        res.append(value)
    return res
 
def drawStructure(beamDimensions, pillarDimensions, pillarDistances, interstoryHeights):
    """
    drawStructure is a function that, given beam's dimensions, pillars's dimensions, distances between the pillars (y-axis),
    interstory's heights (z-axis), return an HPC model of a space frame of reinforced concrete.
 
    @param beamDimensions: tuple, representing the dimensions of a beam (x,z)
    @param pillarDimensions: tuple, representing the dimensions of a pillar (x,y)
    @param pillarDistances: list representing the distances between pillars [dy1, dy2, ...]
    @param interstoryHeights: list representing the heights of every interstory [dz1, dz2, dz3, ...]
    @return model: HPC model of the space frame
    """
 	
    #generating values for the pillars Y-axis
    pillarDistances = [0] + pillarDistances
    linearPillars = intersperse(pillarDistances, pillarDimensions[1])
   
    #generating pillars HPC model
    pillars3D = INSR(PROD)([QUOTE([pillarDimensions[0], -3]),QUOTE(linearPillars), QUOTE(intersperse([-interstory for interstory in interstoryHeights], -beamDimensions[1]))])
           
    #generating values for horizontal beams perpendicular to the Y-axis
    horizontalBeamXYAxis = [pillarDimensions[0],-3]
    horizontalBeamYYAxis = intersperse([-beam for beam in pillarDistances], pillarDimensions[1])
    horizontalBeamYYAxis[0] = -horizontalBeamYYAxis[0]
   
    #generating HPC model of the beams perpendicular to the Y-axis
    beamsY3D = INSR(PROD)([QUOTE(horizontalBeamXYAxis), QUOTE(horizontalBeamYYAxis), QUOTE(intersperse(interstoryHeights,beamDimensions[1]))])
   
    #assembling the HPC model
    model = STRUCT([pillars3D, beamsY3D])
    return model

def generate_beams(file_name):
	"""
	generateBeams is a function that, given a csv file name generate the 3D HPC model of the beams. Actually the function uses ";"
	as default delimiter instead of the classic ",", that's useful in order to correctly parse lists and their elements.
	@param file_name: the csv file name 
	@return: the 3D HPC model of the beams
	"""
	#generating 1D beams list X-axis 
	with open(file_name, 'rb') as file:
		reader = csv.reader(file, delimiter=';')
		beamlengthX = []
		beamlengthZ = []
		data = []
		accumulator = 0
		for row in reader:
			accumulator = accumulator + 1
			data.append(row)
			if(accumulator == 2):
				if(float(data[0][0]) == 0):
					beamlengthX.append(-(make_tuple(data[1][1])[0]))
				else:
					beamlengthX.append(float(data[0][0])-make_tuple(data[1][1])[0])
					beamlengthX.append(-(make_tuple(data[1][1])[0]))
				accumulator = 0
				data = []
	#generating 1D beams list Y-axis 
	with open(file_name, 'rb') as file:
		reader = csv.reader(file, delimiter=';')
		data = []
		beamlengthY = []
		accumulator = 0
		for row in reader:
			beamlengthY = []
			accumulator = accumulator + 1
			data.append(row)
			if(accumulator == 2):
				beamlengthY.append(make_tuple(data[1][1])[1])
				for element in make_tuple(data[1][2]):
					beamlengthY.append(element)
					beamlengthY.append(make_tuple(data[1][1])[1])
				accumulator = 0
				data = []
	#generating 1D beams list Z-axis 
	with open(file_name, 'rb') as file:
		reader = csv.reader(file, delimiter=';')
		beamlengthZ = []
		accumulator = 0
		for row in reader:
			accumulator += 1
			if(accumulator == 2):
				beamlengthZ = intersperse(make_tuple(row[3]), make_tuple(row[0])[1])
				break
	#returning the 3D HPC model of the beams
	return INSR(PROD)([QUOTE(beamlengthX), QUOTE(beamlengthY), QUOTE(beamlengthZ)])

 
def ggpl_bone_structure(file_name):
	"""
	ggpl_bone_structure is a function that, given a file name create an entire 3D parametric (spatial) 
	building frame in reinforced concrete. The parametrization is given by the csv file named "file_name".
	@param file_name: the file name of the csv file containing the dataset
	@return : the 3D HPC model of the parametric (spatial) building frame in reinforced concrete
	"""

	with open(file_name, 'rb') as file:
		reader = csv.reader(file, delimiter=';')

		#used to store partial csv lines, usually 2
		data = []

		#list of 3D models
		frameList = []

		#distances used to calculate the starting point of every frame
		xdist = 0
		ydist = 0 
		zdist = 0

		#value used to control the iteration through the csv dataset
		accumulator = 0

		for row in reader:
			accumulator = accumulator + 1
			data.append(row)

			#if we had read 2 lines
			if(accumulator == 2):

				#variable rename and casting
				xPillar = float(data[0][0])
				yPillar = float(data[0][1])
				zPillar = float(data[0][2])
				beamDimensions = make_tuple(data[1][0])
				pillarDimensions = make_tuple(data[1][1])
				pillarDistances = make_tuple(data[1][2])
				interstoryHeights = make_tuple(data[1][3])

				xdist = xdist + xPillar
				ydist = ydist + yPillar
				zdist = zdist + zPillar

				#generating the frame
				model = drawStructure(beamDimensions, pillarDimensions, pillarDistances, interstoryHeights)

				#translating the frame according to the dataset
				frameElement = STRUCT([T(1)(xdist), T(2)(ydist), T(3)(zdist), model])

				#saving the new frame
				frameList.append(STRUCT([frameElement]))

				#restart iteration 
				accumulator = 0
				data = []

		frameList.append(generate_beams(file_name))
		return STRUCT(frameList)

 
VIEW(ggpl_bone_structure("frame_data_461400.csv"))