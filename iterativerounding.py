from scipy.optimize import linprog
import datastructure as ds
import numpy as np
import math
import copy
import threading

# A : the constraint matrix
# v: the objective coefficients
# x : a dominating extreme point 
# tol: tolerance for double-floating error

def iterativerounding(A, x, b, tol, numf, numg):
	print("+++++++++++++++++++++++++++++++++ Iterative Rounding +++++++++++++++++++++++++++++++")
	A = list(map(list, A))
	# Get the dimension
	numcol = len(x)
	
	# Initialize xBar
	xBar = [0] * numcol
	
	# Find family binding constraints 
	A_eq, A_ineq, numfeq, k, b_eq, b_ineq = fbindconstraints(A, x, b, tol, numf, numg)
	#print(len(A_eq))
	#print(len(A_ineq))
	#print(b_eq)
	#print(b_ineq)
	#print(numfeq)
	#print("init k = " + str(k))

	# Objective function: minimize
	v = [-1] * numcol
	
	# initialize a list for bookkeeping of x variables
	xremainind = [i for i in range(numcol)]
	round = 1
	elim = 0;
	while True:
		print("++++++++++++ Round = " + str(round))
		#t = printint()
		
		round += 1
		
		iind, xint, find, xfrac = seperateintfrac(x, tol)
		
		
		if not find:				# integer solution
			#print("Integral sol")
			#stop_threads = True
			#t.cancel()
			break
				
		if 	len(x) == len(xfrac):	# no integral entry 
			#print("No integral entry, eliminating a constraint")
			## looking for a game constraint to delete
			xup = roundup(x, tol)
			
			#print("k=" + str(k))
			#inds, A_eq_g = gbindconstraints(A_ineq[k:], xfrac, b_ineq[k:], tol)
			#print(A_eq_g)
			#print(xup)
			#print(xup)
			#btemp = subtract(mul(A_eq_g, xup), b_ineq[k:])
			btemp = subtract(mul(A_ineq[k:], xup), b_ineq[k:])
			
			# greedy choice
			elimind = btemp.index(min(btemp))
			elimind += k
			
			elim += 1
			
			# Delete the constraint 
			A_ineq.remove(A_ineq[elimind])
			#print(b_ineq[elimind])
			b_ineq.remove(b_ineq[elimind])
			
		else:			# mixed integer and fractional sol
			#print("mixed soltion, fixing integral entries")
			
			## Update the linear program
			# The objective coefficients
			vint, [v] = partitionmatrix([v], iind)
			
			#  For equality
			A_eq_int, A_eq = partitionmatrix(A_eq, iind)
			b_eq = subtract(b_eq, mul(A_eq_int, xint))
					
			# For inequality 
			A_ineq_int, A_ineq = partitionmatrix(A_ineq, iind)
			b_ineq = subtract(b_ineq, mul(A_ineq_int, xint))
			
			# Update remaining variables
			for i in iind:
				xBar[xremainind[i]] = x[i]
				
			
			temp = []
			for i in find:
				temp.append(xremainind[i])
			
			xremainind = temp 
			#print("remain indices:" + str(xremainind))
			
			# Clean up useless constraints
			A_eq, b_eq = cleanupeq(A_eq, b_eq)
			A_ineq, b_ineq, k = cleanupineq(A_ineq, b_ineq, k)
			#print("Check k = " + str(k))
			
			
		#print(v)
		#print("A_eq = " + str(len(A_eq)))
		#print(b_eq)
		
		#print("A_ineq = " + str(len(A_ineq)))
		#print(b_ineq)

		# Resolve the updated linear program
		if not A_eq and not A_ineq:
			#print("This case")
			x = [0] * len(xremainind)
		elif not A_eq and not b_eq:
			res = linprog(v, A_ub=A_ineq, b_ub=b_ineq, A_eq=None, b_eq=None, method='simplex')
			x = res['x']
		elif not A_ineq and not b_ineq:
			res = linprog(v, A_ub=None, b_ub=None, A_eq=A_eq, b_eq=b_eq, method='simplex')
			x = res['x']
		else:
			res = linprog(v, A_ub=A_ineq, b_ub=b_ineq, A_eq=A_eq, b_eq=b_eq, method='simplex')
			x = res['x']
		
			
			
		
		
		#print("x = " + str(x))
		
	# Update the integral solution xBar
	for i in iind:
		xBar[xremainind[i]] = x[i]
	
	print("eliminated " + str(elim) + " constraints")
	return roundint(xBar)
	
# Print some statement
def printint():
	t = threading.Timer(5.0, printint).start()
	print('IR: running')
	return t

# Takes a solution x, and returns list of indicies i suct that x[i] is integal
def seperateintfrac(x, tol):
	iind = []
	find = []
	xint = []
	xfrac = []
	
	for i in range(len(x)):
		if abs(x[i] - round(x[i])) <= tol:
			iind.append(i)
			xint.append(x[i])
		else:
			find.append(i)
			xfrac.append(x[i])
			
	return iind, xint, find, xfrac


# Round up a vector x
def roundup(x, tol):
	y = [0] * len(x)
	for i in range(len(x)):
		if x[i] > tol:
			y[i] = math.ceil(x[i])
		
	return y
	
# Check if a solution is an integer solution	
def isintsol(x, tol):
	for i in range(len(x)):
		if abs(x[i] - round(x[i])) > tol:
			return False
			
	return True
	
# Multiply a matrix with a vector
def mul(A, x):
	return [ds.dotproduct(a,x) for a in A]

# 
def partitionmatrix(A, iind):
	if len(A) == 0:
		return [], []
	numrow = len(A)
	numcol = len(A[0])
	
	Aint = []
	Afrac = []
	for i in range(numrow):
		aint = []
		afrac =[]
		for j in range(numcol):
			if j in iind:
				aint.append(A[i][j])
			else:
				afrac.append(A[i][j])
				
		Aint.append(aint)
		Afrac.append(afrac)
		
	return Aint, Afrac
	
# subtract two vector coordinatewise 
def subtract(x, y):
	return [x[i]- y[i] for i in range(len(x))]
	
# find family binding constraints
def fbindconstraints(A, x, b, tol, numf, numg):
	val = mul(A, x)
	A_eq = []
	A_ineq = []
	b_eq = []
	b_ineq = []
	numfeq = 0
	numfineq = 0
	
	for i in range(len(b)):
		if ( abs(val[i] - b[i]) <= tol) and (i < numf):
			A_eq.append(A[i])
			b_eq.append(b[i])
			numfeq = numfeq + 1
				
		else:
			A_ineq.append(A[i])
			b_ineq.append(b[i])
			if i < numf:
				numfineq = numfineq + 1
			
	return A_eq, A_ineq, numfeq, numfineq, b_eq, b_ineq


# find game binding constraints	
def gbindconstraints(A, x, b, tol):
	#print(A)
	#print(x)
	temp = mul(A, x)
	inds = []
	A_eqg = []
	
	for i in range(len(b)):
		if abs(temp[i] - b[i]) <= tol:
			inds.append(i)
			A_eqg.append(A[i])
	
	return inds, A_eqg
	
# clean up useless constraints
def cleanupeq(A, b):
	#if (A == None) or (b == None):
	#	return None, None
	
	newA = []
	newb = []
	for row in range(len(A)):
		if not allzeros(A[row]):
			newA.append(A[row])
			newb.append(b[row])
			
	return newA, newb
	
def cleanupineq(A, b, k):
	#if (A == None) or (b == None):
	#	return None, None, 0
		
	newA = []
	newb = []
	newk = k
	for row in range(len(A)):
		if not allzeros(A[row]):
			newA.append(A[row])
			newb.append(b[row])
		elif row < k:
			newk = newk - 1
			
	return newA, newb, newk 
	
def allzeros(x):
	tol = 10**(-6)
	for i in x:
		if not (abs(i) <= tol):
			return False
			
	return True
	
def roundint(x):
	ans = []
	for i in x:
		ans.append(round(i))
	return ans
	
#print(subtract([1,2], [-1, -2]))		
#print(roundup([0.1, 0, 0.2], 10**(-6)))

### Redistribute evenly the group dominating solution to a family dominating solution 
def redistribute(x, numcol2, IDlist, numf, numg, fb2col, fb2col2, numrow2):
	newx = [0] * numcol2
	for i in range(len(x)):
		if x[i] > 0: 
			(gID, b) = ind2fb(i, fb2col, numf + numg)
			newx = redistributeone(x[i], gID, b, IDlist, newx, fb2col2, numrow2)

	return newx

def redistributeone(val, gID, b, IDlist, newx, fb2col2, numrow2):
	groupsize = len(IDlist[gID]) # Check offset by 1 or not 
	for f in IDlist[gID]:
		col = fb2col2[(f-1, b)] - numrow2
		#print(col)
		#print(len(newx))
		newx[col] = val/groupsize
		
	return newx
	
	
def ind2fb(ind, fb2col, numrows):
	#print('ind = ' + str(ind))
	# offset by the number of rows 
	for key, value in fb2col.items():
		if value == (ind + numrows):
			#print('key = '  + str(key))
			return key
			
		
		