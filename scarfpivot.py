######################## Scarf Pivot ############################
import sys
import datastructure as ds
import csv
import numpy as np
import cardinalpivot as cp
import ordinalpivot as op
import time
import correctness as cor


def scarfpivot(eps, CB, OB, A, b, c, rmins, numf, numg, fp, ordlist, fb2col, budget, budlist):
	print("+++++++++++++++++++++++++++++++++ Scarf Pivoting ++++++++++++++++++++++++++++++++++")
	count = 0
	fcount = 0
	while True:
		#if (count%50 == 0):
		#	print("============================= Round " + str(count +1) + " =============================")
		#start = time.time()
		CB, newc, A, b = cp.cardinalpivot(CB, c, A, b, fb2col)
		count = count + 1
		#end = time.time()
		#print("card time : " + str(end - start))
		if count % 100 ==99:
			print("round "+str(count+1))
		if (fb2col[ds.contract2fb(newc)] == 0):
			#x = np.linalg.solve(A,b)
			#print("!!!!!!!! x = " + str(x))
			#print(CB)
			#print(b)
			#print(OB)
			#print(A)
			#print("Card: done")

			#if cor.isordbasis(eps, OB, numf, numg, fp, ordlist, fb2col, budget):
			#	print("@@@@@@@@@@@@@@@@@@@@ Sanity check passed")
			#else:
			#	print("@@@@@@@@@@@@@@@@@@@@ Sanity check failed")
			break

		#start = time.time()
		OB, c, rmins, istar = op.ordinalpivot(eps, OB, newc, rmins, numf, numg, fp, ordlist, fb2col, budget)
		#end = time.time()
		#print("ord time: " + str(end - start))
		if (istar <numf):
			fcount += 1
		if (fb2col[ds.contract2fb(c)] == 0):
			#x = np.linalg.solve(A,b)
			#print("!!!!!!!! x = " + str(x))
			#print("Ord: done")
			break

		#if count == 5:
		#	break

	#print("count = " + str(count))
	#print("fcount = " + str(fcount))
	x = gotdomsol(CB, b, fb2col)
	#print(OB)
	CEprice = getCEprice(OB, numg)
	print("Found a dominating solution:")
	print(roundint(x))
	print("CE price = " + str(CEprice))

	# Sanity check
	#print(cor.ispseudoCE(x, CEprice, eps, fb2col, ordlist, budlist, numf, numg, budget))
	#print("Length of x = "  + str(len(x)))
	return x

# get the dominating solution from scarfpivot
def gotdomsol(basis, b, fb2col):
	n = len(basis)
	x = [0] * len(fb2col)

	for i in range(len(basis)):
		fb = ds.contract2fb(basis[i])
		ind = fb2col[fb]
		x[ind] = b[i]

	return x[n:]

# get the CE price
def getCEprice(OB, numg):
	price = [0] * numg
	for g in range(numg):
		temp = []
		for c in OB:
			if not ds.isslack(c):
				if c[1][g] > 0:	# positive coeff
					temp.append(c[2][g])

		if 	len(temp) > 0:
			price[g] = min(temp)

	return price

def roundint(x):
	ans = []
	for i in x:
		ans.append(round(i,2))
	return ans
