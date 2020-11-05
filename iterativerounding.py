# A : the constraint matrix
# v: the objective coefficients
# x : a dominating extreme point 
# tol: tolerance for double-floating error

def iterativerounding(A, x, b, tol):
	
	while True
		if isintsol(x, tol):	# integer solution
			return x
			
		


	
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