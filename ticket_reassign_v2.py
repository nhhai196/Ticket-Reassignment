import sys
import datastructure
import csv
import numpy as np
import cardinalpivot as cp
import ordinalpivot as op
import scarfpivot as sp
import time
import numpy as np
import iterativerounding as ir
import random
import statistics as stat

#argv[1]: xlsx file name in the following format
#row 1: column labels: family preference / family size / num seniors / group size
#row f+1: info of family f
#argv[2]: budget of each senior, each non-senior has budget 1
#argv[3]: seat offset for alpha
#argv[4]: game capacity
#argv[5]: upper bound for bundle size
#argv[6]: epsilon for price

#ex: python ticket_reassign_v2.py data3-swap.xlsx 1.2 4 150 3 0.1 // with duplicates, 3X00 rounds?
#ex: python ticket_reassign_v2.py data3-swap.xlsx 1.2 2 150 3 0.05 // with duplicates, 5500 rounds
#ex: python ticket_reassign_v2.py data4-swap.xlsx 1.2 3 2000 3 0.1 // with duplicates, 8300 rounds

numF, numG, bundle2rank, bundlelist, fb2col, budget, numcol, A, b, plist, famsize = datastructure.init_v2(sys.argv[1],float(sys.argv[2]),int(float(sys.argv[3])),int(float(sys.argv[4])),int(float(sys.argv[5])))
#numF: number of family
#numG: number of games
#bundle2rank: bundle maps to the rank, each family has one dictionary
#bundlelist: preference list over bundles, each family has one list
#fb2col: map (family,bundle) to the column index of matrix A
#budget: budget[f-1] is the budget of family f
#numcol: number of columns for matrix A
#A: the Scarf matrix of size (numF+numG) x numcol, columns are in alphabetic order
#b: the capacity vector on RHS
#plist: plist[f][j] denotes family f's j-th most favorite game
#famsize: famsize[f] denotes the size of family f

print("++++++++++++++++++++++++++++++++++++++ Data +++++++++++++++++++++++++++++++++++++")

print('numF = ' + str(numF))
print('numG = ' + str(numG))
#print('bundle2rank:\n' + str(bundle2rank))
#print('bundlelist:\n' + str(bundlelist))
#print('fb2col:\n' + str(fb2col))
print('numcol = ' + str(numcol))
numrow = numF + numG
print('numrow = ' + str(numrow))

print('budget: ' + str(budget))
print('matrix A:\n' + str(A))
print('vector b:\n' + str(b))

clist = [] #contract list
for i in range(numF):
	clist.append((-1*(i+1),(),[]))

for i in range(numG):
	clist.append((-1*(i+1+numF),(),[]))

#print("clist = ")
#print(clist)


# Test cardinal pivot
#c = (1, bundlelist[1][1], [0,0])
#fbc = (c[0], c[1])
#print(fbc)

#b = [random.randint(1,3) for i in range(numF)]
#b = [1 for i in range(numF)]
#b = b + capacity
#print("b =" + str(b))

#newCB, oldc, newA, newb = cp.cardinalpivot(clist, c, A, b, fb2col)
#print(newCB)
#print(oldc)
#print(newA)
#print(newb)
#a = np.zeros([5 * 10**3, 10**6])

# Test ordinal pivot

print("Init ordinal basis:")
c, initOB = op.initordinalbasis(A, numF, numG, fb2col)
#print(initOB)

rmins = op.getallrowmins(initOB, numF, bundle2rank)
#for i in range(len(rmins)):
#	print(rmins[i])

ordlist = datastructure.genordlist(A, numF, bundle2rank, bundlelist, fb2col)

#print("matrix A:")
#print(A)
#print("ordlist:")
#print(ordlist)

# ordlist in the form (f,b)
col2fb = {value : key for (key, value) in fb2col.items()}
#print(col2fb)

newordlist = []
for l in ordlist:
	temp = list(map(lambda x: col2fb[x], l))
	newordlist.append(temp)

#print("new")
#print(newordlist)


#clist, newc, newrmins = op.ordinalpivot(initOB, oldc, rmins, numF, numG, bundle2rank, newordlist, fb2col)
#print(clist)
#print(datastructure.weaklyprefer((1,(2,0),[0,0]), (1,(2,0),[0.5,0]), 1, numF, bundle2rank))

start = time.time()
eps = float(sys.argv[6])

x = sp.scarfpivot(eps, clist, initOB, A, b, c, rmins, numF, numG, bundle2rank, newordlist, fb2col, budget, bundlelist)
end = time.time()
print('Scarf elapsed time =' + str(end - start))

## Iterative Rounding
# remove the slack variable
start = time.time()
A = A[:, numrow:]
#print("A= " + str(A))
#print("b = "+ str(b))
#realb = ir.mul(A, x)
#print(realb)

tol = 10**(-6)

xBar = ir.iterativerounding(A, x, b, tol, numF, numG)
print("xBar = " + str(xBar))

end = time.time()
print("Rounding elapsed time = " + str(end - start))


#print(len(xBar))
#print((plist))


## Statistics
filename = 'outputs-1000-families-6-games.xlsx'
print(b)
stat.statistics(filename, A, xBar, b, numF, numG, fb2col, plist, famsize)
