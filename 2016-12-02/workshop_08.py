from pyplasm import *
from scipy.spatial import Delaunay
from larlib import *
import csv

with open("muriesterni.lines", "rb") as file:
	reader = csv.reader(file, delimiter=",")
	lista = []
	for row in reader:
		lista.append(POLYLINE([[float(row[0]), float(row[1])],[float(row[2]), float(row[3])]]))
muriesterni = STRUCT(lista)
pavimento = SOLIDIFY(muriesterni)
xfactor = 15/SIZE([1])(muriesterni)[0]
yfactor = 15.1/SIZE([2])(muriesterni)[0]
#muriesterni = S([1,2])([xfactor, yfactor])(muriesterni)
muretto = OFFSET([12,12])(muriesterni)
muretto = PROD([muretto, Q(3/xfactor)])

with open("muriinterni.lines", "rb") as file:
	reader = csv.reader(file, delimiter=",")
	lista = []
	for row in reader:
		lista.append(POLYLINE([[float(row[0]), float(row[1])],[float(row[2]), float(row[3])]]))
muriinterni = STRUCT(lista)
#muriinterni = S([1,2])([xfactor, yfactor])(muriinterni)
interni = OFFSET([7,7])(muriinterni)
test = DIFFERENCE([pavimento, interni])
print SPLITCELLS(test)
VIEW(STRUCT(SPLITCELLS(pavimento)))
print UKPOL(test)[1]
interni = PROD([interni, Q(3/xfactor)])

with open("porte.lines", "rb") as file:
	reader = csv.reader(file, delimiter=",")
	lista = []
	cuboid = []
	acc = 0
	for row in reader:
		acc = acc + 1
		cuboid.append([float(row[0]),float(row[1])])
		if(acc == 4):
			lista.append(MKPOL([cuboid,[[1,2,3,4]],None]))
			cuboid = []
			acc = 0
porte = STRUCT(lista)
listaporte = lista
#porte = S([1,2])([xfactor,yfactor])(porte)
porte = PROD([porte, Q(2.5/xfactor)])

with open("finestre.lines", "rb") as file:
	reader = csv.reader(file, delimiter=",")
	lista = []
	cuboid = []
	acc = 0
	for row in reader:
		acc = acc + 1
		cuboid.append([float(row[0]),float(row[1])])
		if(acc == 4):
			lista.append(MKPOL([cuboid,[[1,2,3,4]],None]))
			cuboid = []
			acc = 0
finestre = STRUCT(lista)
##VIEW(finestre)
listafinestre = lista
#finestre = S([1,2])([xfactor,yfactor])(finestre)
finestre = PROD([finestre, Q(SIZE([3])(muretto)[0]/2.)])
finestre = T(3)(SIZE([3])(muretto)[0]/4.)(finestre)

frame = STRUCT([muretto, interni])
#VIEW(porte)
#VIEW(finestre)
frame = DIFFERENCE([frame, porte, finestre])
#finiture = STRUCT([porte, finestre])
#VIEW(finiture)

#VIEW(S([1,2,3])([xfactor,yfactor, xfactor])(frame))