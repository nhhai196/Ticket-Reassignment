import sys
import datastructure
import csv
import numpy

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
