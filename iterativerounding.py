from scipy.optimize import linprog
import datastructure as ds



# A : the constraint matrix
# v: the objective coefficients
# x : a dominating extreme point 
# tol: tolerance for double-floating error

def iterativerounding(A, x, b, tol):
	# Get the dimension
	numcol = len(x)
	
	# Initialize xBar

	# Objective function
	f = [1] * numcol
	
	
	while True
		iind, xint, find, xfrac = seperateintfrac(x, tol)
		if not find:				# integer solution
			return x
			
			
		if 	len(x) == len(xfrac):	# no integral entry 
			print("No integral entry, eliminating a constraint")
			
			
			
			
			
		else:			# mixed integer and fractional sol
			print("mixed soltion, fixing integral entries")
			
		
			
		

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
	
print(roundup([0.1, 0, 0.2], 10**(-6)))