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
#row 1: column labels: family preference / family size / num seniors / group size /family bundle preference (with alpha and bundle size upper bound)
#row f+1: info of family f
#argv[2]: budget of each senior, each non-senior has budget 1
#argv[3]: game capacity
#argv[4]: epsilon for price

#below: seatoffset = 7 and numscore = 4
#ex: python ticket_reassign_v3.py data-cardinal1.xlsx 1.2 500 0.2 // 7300 rounds
#ex: python ticket_reassign_v3.py data-cardinal1.xlsx 1.2 500 0.05 // > 2M rounds!
#data-cardinal1.xlsx does not have sheet 3
#ex: python ticket_reassign_v3.py data-cardinal2.xlsx 1.2 125 0.2 // 800 rounds
#ex: python ticket_reassign_v3.py data-cardinal2.xlsx 1.2 125 0.15 // > 800K rounds!

#below: seatoffset = 6 and numscore = 3
#ex: python ticket_reassign_v3.py data-cardinal3.xlsx 1.2 500 0.1 // 1800 rounds
#ex: python ticket_reassign_v3.py data-cardinal3.xlsx 1.2 500 0.05 // > 200K rounds!

#below: seatoffset = 6, numscore = 5, fewscores = 4
#ex: python ticket_reassign_v3.py data-cardinal5.xlsx 1.2 500 0.05 // 3600 rounds
#ex: python ticket_reassign_v3.py data-cardinal6.xlsx 1.2 500 0.04 // 7200 rounds, this one has max violation 24.6%, may want to check

numF, numG, bundle2rank, bundlelist, fb2col, budget, numcol, A, b, plist, famsize, idtofam = datastructure.init_v3(sys.argv[1],float(sys.argv[2]),int(float(sys.argv[3])))
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
#id2fam: id2fam[i-1] returns a list of families with group id i

print("++++++++++++++++++++++++++++++++++++++ Data +++++++++++++++++++++++++++++++++++++")

print('numF = ' + str(numF))
print('numG = ' + str(numG))
print('bundle2rank:\n' + str(bundle2rank))
print(len(bundle2rank[1]))
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
eps = float(sys.argv[4])

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

numF2, numG2, bundle2rank2, bundlelist2, fb2col2, budget2, numcol2, A2, b2, plist2, famsize2, idtofam2 = datastructure.init_family(sys.argv[1],float(sys.argv[2]),int(float(sys.argv[3])))

print('fb2col2:\n' + str(fb2col2))
numrow2 = numF2 + numG2
print('numcol2 = ' + str(numcol2))
A2 = A2[:, numrow2:]

# Redistribute
x2 = ir.redistribute(x, numcol2, idtofam2, numF, numG, fb2col, fb2col2, numrow2)
print(x2)



tol = 10**(-6)

#xBar = ir.iterativerounding(A, x, b, tol, numF, numG)
xBar2 = ir.iterativerounding(A2, x2, b2, tol, numF2, numG2)
print("xBar2 = " + str(xBar2))

end = time.time()
print("Rounding elapsed time = " + str(end - start))


#print(len(xBar))
print((plist))


## Statistics
filename = 'outputs-card-' + '100' + '-families-' + str(numG) + '-games.xlsx'
print(b)
stat.statistics(filename, A2, xBar2, b2, numF2, numG2, fb2col2, plist2, famsize2, bundle2rank2)
