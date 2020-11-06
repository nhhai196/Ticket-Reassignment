#from scipy.optimize import linprog
import datastructure as ds


# A : the constraint matrix
# v: the objective coefficients
# x : a dominating extreme point 
# tol: tolerance for double-floating error

def iterativerounding(A, x, b, tol, numf, numg):
	# Get the dimension
	numcol = len(x)
	
	# Initialize xBar
	xBar = [0] * numcol
	
	# Find family binding constraints 
	A_eq, A_ineq, numfeq, k, b_eq, b_ineq = fbindconstraints(A, x, b, tol, numf, numg)

	# Objective function: minimize
	v = [-1] * numcol
	
	# initialize a list for bookkeeping of x variables
    xremainind = [i for i in range(numcol)]
	
	while True:
		iind, xint, find, xfrac = seperateintfrac(x, tol)
		
		
		if not find:				# integer solution
			return x
				
		if 	len(x) == len(xfrac):	# no integral entry 
			print("No integral entry, eliminating a constraint")
			## looking for a game constraint to delete
			# igbind is the list of binding game constraints
			xup = roundup(x, tol)
			
			inds, A_eq_g = gbindconstraints(A_ineq[k:], x[k:], b_ineq[k:], tol)
			btemp = subtract(mul(A_eq_g, x), b_eq[numfeq:])
			
			# greedy choice
			elimind = btemp.index(min(btemp)) 
			
			# Delete the constraint 
			A_eq.remove(A_eq[elimind])
			b_eq.remove(b_eq[elimind])
			
		else:			# mixed integer and fractional sol
			print("mixed soltion, fixing integral entries")
			
			## Update the linear program
			# The objective coefficients
			vint, v = partitionmatrix([v], iind)
			
			#  For equality
			A_eq_int, A_eq = partitionmatrix(A_eq, iind)
			b_eq = subtract(b_eq, mul(A_eq_int, xint))
					
			# For inequality 
			A_ineq_int, A_ineq = partitionmatrix(A_ineq, iind)
			b_ineq = subtract(b_ineq, mul(A_ineq_int, xint))
			
			# Update remaining variables
			xremainind = [i if i not in iind]
			
			
		# Resolve the updated linear program	
		x = linprog(v, A_ub=A_ineq, b_ub=b_ineq, A_eq=A_eq, b_eq=b_eq, method='interior-point')	
		
		# Update the integral solution xBar
		xBar = 
		

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
			y[i] = 1
		
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
	temp = mul(A, x)
	inds = []
	A_eqg = []
	
	for i in range(len(b)):
		if abs(temp[i] - b[i]) <= tol:
			inds.append(i)
			A_eqg.append(A[i])
	
	return inds, A_eqg
	
	
	
print(subtract([1,2], [-1, -2]))		
#print(roundup([0.1, 0, 0.2], 10**(-6)))