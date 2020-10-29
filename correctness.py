######################## Tetsing #########################################
# This module contains all functions that are needed to test the correctness
# of ordinal pivot and cardinal pivot

import ordinalpivot as op
import math
import datastructure as ds

def isordbasis(eps, basis, numf, numg, fp, ordlist, fb2col, budget):
	# Get all the row mins
	rmins = op.getallrowmins(basis, numf, fp)
	flag = True
	for c in fb2col:
		if (c[0] >=0):
			prices = enumprice(eps, c[1], numg, budget[c[0]])
			for p in prices:
				contract = (c[0], c[1], p)
				if not dominated(contract, rmins, numf, fp):
					print("+++++++++++ ERROR: col below not dominated")
					print(contract)
					print(rmins)
					flag = False
					#return False
							
	return flag
				
# def 
def dominated(contract, rmins, numf, fp):
	for row in range(len(rmins)):
		if ds.weaklyprefer(rmins[row], contract, row, numf, fp):
			#print(contract, end ='')
			#print(" dominated by ", end ='')
			#print(rmins[row])
			return True
			
	return False
	

# enumerate all possible prices
def enumprice(eps, alpha, numg, budget):
	if numg == 0:
		return [[]]
	#if numg == 1:
	#	if (alpha[0] == 0):
	#		return [[0]]
	#	else:
	#		maxp = math.floor(budget/(eps * alpha[0])) + 1
	#		return [[i * eps] for i in range(maxp)]
	else:
		allprices = []
		if (alpha[0] == 0):
			temp = enumprice(eps, alpha[1:], numg-1, budget)
			prices = [[0] + x for x in temp]
					
			#print(prices)
			allprices = allprices + prices
		else:
			maxp = math.floor(budget/(eps*alpha[0])) + 1
			#print(maxp)
			
			for i in range(maxp):
				val = i * eps
				#print("val = " +str(val))
				temp = enumprice(eps, alpha[1:], numg-1, budget - i * eps * alpha[0])
				#print(temp)
				prices = [[val] + x for x in temp]
					
				#print(prices)
				allprices = allprices + prices
			
	return allprices
	
def enumpriceall(eps, alpha, numg, budget):
	allprices = []
	for i in range(len(budget)):
		allprices[i] = enumprice(eps, alpha[i], numg, budget[i])
		
	return allprices


