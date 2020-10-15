######################## Cardinal Pivot ############################
from numpy import * 

# @clist: 	a list of contracts that is a cardinal basis. Note that 
#			the order of contracts is important. 
# @newc:	a new column to add to the basis 
# @A: 		the constraint matrix. Note that this matrix will be updated
#     		after each cardinal basis step
# @b: 		the right hand side

def cardinalpivot(clist, newc, A, b):
	# First check that if the contract (ignore the price vector) to add 
	# already in the basis. If Yes, just add the new contract and remove 
	# the old one.
	for i in range(len(clist)):
		c = clist[i]
		if (c[0] == newc[0] and c[1] == newc[1]):
			clist[i] = newc
			return (clist, c)
	
	numrows = len(A)
	numcols = len(A[0])
	
	# Index of the entering basic variable (added column)
	# TODO: need a mapping from (family, bundle) to index
	cindex = getindex(newc)
	
	# Perform ratio test to find the leaving basic variable (revomed column)
	minval = 10**10		# some large value
	pivotrow = -1 		# this will be the index of the leaving basic variable
	for row in range(numrows):
		if (A[row, cindex] > 0.00001):
			temp = A[row, cindex]/b[row]
			if (temp < minval):
				minval = temp
				pivotrow = row
				
	### Update variables
	oldc = clist[row]
	clist[row] = newc
	
	# Initialize to appropriate size
	newb = numpy.zeros([numrows, 1])
	newA = numpy.zeros([numrow, numcols])
	
	## Update the pivotrow
	# Copy pivotrow and normalizing to 1
	newA[pivotrow, :] = A[pivotrow, :] / A[pivotrow, cindex] 
	
	# Update pivotrow of right hand side
	newb[pivotrow] = b[pivotrow]/A[pivotrow, cindex]

	## Update all other rows
	for k in range(numrows):
		if (not (k == pivotrow)):
			# Set it equal to the original value minus a multiple 
			# of normalized pivotrow
			newA[k, :] = A[k,:] - A[k,:] * newA[pivotrow, :]
			newb[k] = b[k] - A[k,cindex] * B[pivotrow]
			
	return (clist, oldc, newA, newb)