######################## Scarf Pivot ############################
import sys
import datastructure as ds
import csv
import numpy as np
import cardinalpivot as cp
import ordinalpivot as op
import time
import correctness as cor


def scarfpivot(eps, CB, OB, A, b, c, rmins, numf, numg, fp, ordlist, fb2col, budget):
	print("+++++++++++++++++++++++++++++++++ Scarf Pivoting ++++++++++++++++++++++++++++++++++")
	count = 0
	while True:
		print("============================= Round " + str(count +1) + " =============================")
		CB, newc, A, b = cp.cardinalpivot(CB, c, A, b, fb2col)
		count = count + 1
		
		if (fb2col[ds.contract2fb(newc)] == 0):
			#x = np.linalg.solve(A,b)
			#print("!!!!!!!! x = " + str(x))
			print(CB)
			print(b)
			print(OB)
			print(A)
			print("Card: done")
			
			if cor.isordbasis(eps, OB, numf, numg, fp, ordlist, fb2col, budget):
				print("@@@@@@@@@@@@@@@@@@@@ Sanity check passed")
			else:
				print("@@@@@@@@@@@@@@@@@@@@ Sanity check failed")
			break
		
		OB, c, rmins = op.ordinalpivot(eps, OB, newc, rmins, numf, numg, fp, ordlist, fb2col, budget)
		
		if (fb2col[ds.contract2fb(c)] == 0):
			#x = np.linalg.solve(A,b)
			#print("!!!!!!!! x = " + str(x))
			print("Ord: done")
			break
		
		#if count == 20:
		#	break
		
	#print("count = " + str(count))
	