import sys
import datastructure
import csv
import numpy as np
import cardinalpivot as cp
import ordinalpivot as op

#argv[1]: csv file name in the following format
#row 1: number of families, number of games
#row f+1: budget, then decreasing preference order over bundles, of family f
#row #family + 2: capacity of each game
#the quantity in the bundle is the alpha (unscaled)
#argv[2]: epsilon for price

numF, numG, bundle2rank, bundlelist, fb2col, budget, capacity, numcol, A = datastructure.init(sys.argv[1])
#numF: number of family
#numG: number of games
#bundle2rank: bundle maps to the rank, each family has one dictionary
#bundlelist: preference list over bundles, each family has one list
#fb2col: map (family,bundle) to the column index of matrix A
#budget: budget[f-1] is the budget of family f
#capacity: capacity[g-1] is the capacity of game g
#numcol: number of columns for matrix A
#A: the Scarf matrix of size (numF+numG) x numcol

print('numF: ' + str(numF))
print('numG: ' + str(numG))
print('bundle2rank:\n' + str(bundle2rank))
print('bundlelist:\n' + str(bundlelist))
print('fb2col:\n' + str(fb2col))
print('budget: ' + str(budget))
print('capacity: ' + str(capacity))
print('numcol: ' + str(numcol))
print('matrix A:\n' + str(A))


clist = [] #contract list
for i in range(numF):
	clist.append((-1*(i+1),(),[]))

for i in range(numG):
	clist.append((-1*(i+1+numF),(),[]))

print("clist = ")
print(clist)


# Test cardinal pivot
c = (1, bundlelist[1][1], [0,0])
fbc = (c[0], c[1])
print(fbc)

b = [1 for i in range(3)]
b = b + capacity
print(b)


newCB, oldc, newA, newb = cp.cardinalpivot(clist, c, A, b, fb2col)
print(newCB)
print(oldc)
print(newA)
print(newb)
#a = np.zeros([5 * 10**3, 10**6])

# Test ordinal pivot
initOB = []
initOB.append(c)
for i in range(1, numF+numG):
	initOB.append((-1*(i+1),(),[]))


print("Init ordinal basis:")
print(initOB)

rmins = op.getallrowmins(initOB, numF, bundle2rank)
for i in range(len(rmins)):
	print(rmins[i])

ordlist = datastructure.genordlist(A, numF, bundle2rank, bundlelist, fb2col)

print("matrix A:")
print(A)
print("ordlist:")
print(ordlist)

# ordlist in the form (f,b)
col2fb = {value : key for (key, value) in fb2col.items()}
print(col2fb)

newordlist = []
for l in ordlist:
	temp = list(map(lambda x: col2fb[x], l))
	newordlist.append(temp)

#print(newordlist)


op.ordinalpivot(initOB, oldc, rmins, numF, numG, bundle2rank, newordlist, fb2col)
