######################## Cardinal Pivot ############################
import numpy
import datastructure as ds

# @clist	: a list of contracts that is a cardinal basis. Note that 
#				the order of contracts is important. 
# @c		: a new column to add to the basis 
# @A 		: the constraint matrix. Note that this matrix will be updated
#     			after each cardinal basis step
# @b 		: the right hand side
# @fb2col	: (family, bundle) to column index (of the constraint matrix)

def cardinalpivot(clist, c, A, b, fb2col):
	#print("++++++++ Cardinal pivot:")
	#ds.printbasis(clist, fb2col)
	#print("----- Push in : " +str(c))
	numf = len(clist)
	# First check that if the contract (ignore the price vector) to add 
	# already in the basis. If Yes, just add the new contract and remove 
	# the old one.
	for i in range(len(clist)):
		tempc = clist[i]
		if (tempc[0] == c[0] and tempc[1] == c[1]):
			clist[i] = c
			#print("----- Kick out: " + str(tempc))
			#print(roundmatrix(A))
			#print(roundvector(b))
			return clist, tempc, A, b
	
	numrows = len(A)
	numcols = len(A[0])
	#print(numrows)
	#print(numcols)
	#print(b)
	
	# Index of the entering basic variable (added column)
	# TODO: need a mapping from (family, bundle) to index
	fbc = (c[0], c[1])
	cindex = fb2col[fbc]
	#print(cindex)
	
	# Perform ratio test to find the leaving basic variable (revomed column)
	minval = 10**10		# some large value
	pivotrow = -1 		# this will be the index of the leaving basic variable
	for row in range(numrows):
		if (A[row, cindex] > 0.00001):
			temp = b[row]/ A[row, cindex]
			if (temp < minval):
				minval = temp
				pivotrow = row
				
	### Update variables
	oldc = clist[pivotrow]
	clist[pivotrow] = c
	
	# Initialize to appropriate size
	newb = [0] * len(b)
	newA = numpy.zeros([numrows, numcols])
	
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
			newA[k, :] = A[k,:] - A[k,cindex] * newA[pivotrow, :]
			newb[k] = b[k] - A[k,cindex] * newb[pivotrow]
	
	#print("----- Kick out: " + str(oldc))
	#print(roundmatrix(newA))
	#print("newb = " + str(roundvector(newb)))
	return clist, oldc, newA, newb

	
def roundmatrix(A):
	m = len(A)
	n = len(A[0,:])
	B = numpy.zeros([m, n])
	for i in range(m):
		for j in range(n):
			B[i][j] = round(A[i][j], 2)
			
	return B
	
def roundvector(b):
	m = len(list(b))
	newb = numpy.zeros(m)
	for i in range(m):
		newb[i] = round(b[i], 2)
		
	return newb