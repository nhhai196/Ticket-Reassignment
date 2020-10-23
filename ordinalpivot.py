######################## Ordinal Pivot ############################
import datastructure as ds
import copy
import functools as func
import math

# @clist	: an ordinal basis
# @c		: a column that will be added to the basis
# @fp		: famimy preferences
# @rmins	: row min of the basis

def ordinalpivot(clist, c, rmins, numf, numg, fp, ordlist, fb2col):
	eps = 0.1
	budget = 2
	numrows = len(clist)

	# Remove column c from the basis
	clist.remove(c)

	# Find row minimizers after removing
	newrmins, newrm = getnewrowmins(clist, c, rmins, numf, fp)
	print("New row mins:")
	for i in range(len(newrmins)):
		print(newrmins[i])
	print("The row that has new row min: " + str(newrm))

	# Find the column with 2 row minimizers,
	col2mins = getcoltwomins(rmins, newrmins)
	print("Col with two mins: " + str(col2mins))

	# Find the row containing the old minimizer
	istar = findoldminimizer(col2mins, rmins)
	print("Old minimizer istar = " + str(istar))

	# Find the column k that maximizes c_{istar, k}
	newc = []
	minprice = [0] * numg
	maxtms = [0] * numf
	fclist = [[]]* numrows
	newc = findcolmax(eps, newrm, istar, newrmins, ordlist, numf, minprice, maxtms, fclist, fb2col, budget)

	# Update the basis
	clist.append(newc)

	# Update row mins of the new basis
	newrmins[istar] = newc

	# Return
	print("newrmins=" + str(newrmins))
	return clist, newc, newrmins
#
def	getrowmin(clist, row, numf, fp):
	rm = clist[0]
	for i in range(1, len(clist)):
		if ds.strictlyprefer(rm, clist[i], row, numf, fp):
			rm = clist[i]

	return rm

# When removing one col from the basis, only one row minimizer is changed
def getnewrowmins(clist, c, rmins, numf, fp):
	row = None;
	newrmins = copy.deepcopy(rmins)
	for i in range(len(rmins)):
		if (c == rmins[i]):
			row = i
			#print("Found new row min" )
			break

	#print(row)
	# Update the min of the row just found above, all others stay the same
	newrmins[row] = getrowmin(clist, row, numf, fp)

	return newrmins, row

# This fucntion is called only once at the begin
def getallrowmins(clist, numf, fp):
	rmins = []
	for row in range(len(clist)):
		rmins.append(getrowmin(clist, row, numf, fp))

	return rmins
#
def getcoltwomins(rmins, newrmins):
	#print(rmins)
	#print(newrmins)
	for i in range(len(rmins)):
		if (rmins[i] !=  newrmins[i]):
			return newrmins[i]

	# If not found raise some error
	print("getcoltwomins: Something went wrong !!!!")

# Find old minimizer
def findoldminimizer(col2mins, rmins):
	for i in range(len(rmins)):
		if (col2mins == rmins[i]):
			return i

	print("find old min: Something went wrong!!!!!")
	
# This is the most challenging function to write	
def findcolmax(eps, newrm, istar, rmins, ordlist, numf, minprice, maxtms, fclist, fb2col, budget):
	# TODO 
	fc, minprice, maxtms = getfeasiblecols(newrm, istar, rmins, ordlist, numf, minprice, maxtms, fclist, fb2col)
	
	# sort feasible columns in deceasing order of preferences
	fc = sortorder(ordlist[istar], fc)
	
	print("feasible cols = " + str(list(map(lambda x: fb2col[x], fc))))
	print(minprice)
	print(maxtms)
	
	fbmins = list(map(lambda x: (x[0], x[1]), rmins))
	
	
	# Assuming fc is sorted in decreasing order
	# Linear search here, binary search might be better 
	for c in fc:		
		type = getcoltype(c, istar, numf)
		if ((type == 1)):
			return (c[0], c[1], [])
		elif (type == 2) or (type == 3):
			temp = findbestprice(eps, c, istar, rmins, numf, minprice, maxtms, budget, fbmins)
			print("temp = " + str(temp))
			if not not temp:
				return (c[0], c[1],temp)
		else:
			return (c[0], c[1], [])
	return 
	

	
def findbestprice(eps, c, istar, rmins, numf, minprice, maxtms, budget, fbmins):
	fbtprice = []						# family break tie price 
	gbtprice = []						# game break tie price 
	
	currminprice = copy.deepcopy(minprice)
	currmaxtms = copy.deepcopy(maxtms)
	
	cc = (c[0], c[1], minprice)
	
	if c not in fbmins:
		for row in range(len(rmins)):
			if (row < numf) and (row != istar):		# family case
				print("Do nothing 1")
					
			elif (row >= numf) and (row != istar):	# game case
				g = row - numf
				ctype = getcoltype(cc, row, numf)		
				mtype = getcoltype(rmins[row], row, numf)
				
				if (ctype == 3) and (mtype == 3):
					if not ds.breaktie(cc, rmins[row]):
						currminprice[g] = rmins[row][2][g] + eps	# must be eps higher
					else:
						currminprice[g] = rmins[row][2][g]
						
		return bestprice(istar, c[1], currminprice, [], budget+1, budget, numf)			
	# For a row that already have a contract without price (f,b) in the basis				
	else:
		index = fbmins.index(c)
		for row in range(len(rmins)):
			if (row < numf) and (row != istar) and (row != index):		# family case
				print("Do nothing 2")
					
			elif (row >= numf) and (row != istar) and (row != index):	# game case
				g = row - numf
				ctype = getcoltype(cc, row, numf)		
				mtype = getcoltype(rmins[row], row, numf)
				
				if (ctype == 3) and (mtype == 3):
					if not ds.breaktie(cc, rmins[row]):
						currminprice[g] = rmins[row][2][g] + eps	# must be eps higher
					else:
						currminprice[g] = rmins[row][2][g]
		# same family and same bundle, need to break tie carefuly here 
		ctype = getcoltype(cc, index, numf)		# verify cc
		mtype = getcoltype(rmins[index], index, numf)
		
		if (index < numf):						# family case
			fbtprice = rmins[2]
			if (ctype == 3) and (mtype == 3):	# non-zero coefficient	
				currmaxtms[row] =  rmins[index][2][index]
				
				temp = bestprice(istar, c[1], currminprice, fbtprice, currmaxtms[row], budget, numf)
				if not temp:
					currmaxtms[row] =  rmins[index][2][index] - eps
					fbtprice = []
					return bestprice(istar, c[1], currminprice, fbtprice, currmaxtms[row], budget, numf)
				else:
					return temp
				
		else:									# game case
			# break tie based on price
			g = index - numf
			if (istar >= numf):
				currminprice[g] = 0
				
			gbtprice = rmins[2]
			if (ctype == 3) and (mtype == 3):	# non-zero coefficient
				temp = bestprice(istar, c[1], currminprice, gbtprice, budget + 1, budget, numf)
				if not temp:
					gbtprice = []
					currminprice[g] = rmins[index][2][g] + eps
					return bestprice(istar, c[1], currminprice, gbtprice, budget + 1, budget, numf)
				else:
					return temp
					

		
	#btprice = fbtprice + gbtprice
	#if (len(btprice) > 1):
	#	print("findbestprice: Something wrong")
	#	return []
					
	#return currminprice, btprice currmaxtms

# 
def bestprice(istar, alpha, minprice, btprice, maxtot, budget, numf):
	if (istar < numf):	# family case
			return fbestprice(istar, alpha, minprice, btprice, maxtot, budget)
	else:				# game case
			return gbestprice(istar, alpha, minprice, btprice, maxtot, budget)
	
# Check if there exists a price that is coordinate-wise 
# greater than the minprice and is tie-break larger than btprice.

def fbestprice(istar, alpha, minprice, btprice, maxtot, budget):
	ms = ds.dotproduct(alpha, minprice)
	
	if isfeasibleprice(alpha, minprice, budget) and (ms <= maxtot):
		if not btprice:	# empty
			return minprice
		else:			# non-empty
			if ds.breaktievector(minprice, btprice):
				#jstar = breaktieindex(minprice, btprice)
				return minprice
			
			else:	# No
				return []
		
	else:		# No 
		return []

# Game		
def gbestprice(istar, alpha, minprice, btprice, maxtot, budget):
	ms = ds.dotproduct(alpha, minprice)
	
	if isfeasibleprice(alpha, minprice, budget) and (ms <= maxtot):
		if not btprice:	# empty
			return minprice
		else:			# non-empty
			if ds.breaktievector(minprice, btprice):
				jstar = breaktieindex(minprice, btprice)
				return minprice
			
			else:	# No
				return []
		
	else:		# No 
		return []

#g = istar - numf
#beta = math.floor(budget - ds.dotproduct(c[1], minprice))/(c[g] * eps)

#if beta < 0:
#	print("++++++++ No feasible price")
	
#newprice[g] = newprice[g] + beta * eps 	# TODO: check no rounding error 

# Takes two price vector x and y (of the same length), returns the smallest index s.t x[i] < y[i]
# If does not exist, returns -1.
def breaktieindex(x,y):
	for i in len(x):
		if (x[i] < y[i]):
			return i
			
	return -1

# Check if a price is feasible given the budget and alpha
def isfeasibleprice(alpha, price, budget):
	tol = 10**(-8)
	if (ds.dotproduct(alpha, price) <= budget + tol):
		return True
	else:
		return False

# takes a column, a row, and numf
# returns the type of the column with respect to the row
# 1:non-active slack variable, 2: non-slack with zero coefficient,
# 3: non-slack with non-zero coefficient, 4: active slack variable
def getcoltype(c, row, numf):
	if ds.isslack(c):	# slack variable
		if (c[0] == -row-1):
			return 4
		else:
			return 1
	else:			# non-slack variable
		if ds.iszerocoeff(c, row, numf):	# zero
			return 2
		else:							# non-zero
			return 3

#
def getfeasiblecols(newrm, istar, rmins, ordlist, numf, minprice, maxtms, fclist, fb2col):
	# TODO: Store values
	# Update for 2 rows only, that is the newrm and istar, others stay the same
	#fclist[newrm], minprice, maxtms = getfeasiblecolsone(newrm, rmins[newrm], ordlist[newrm], numf, minprice, maxtms, fclist[newrm])

	#fclist[istar], minprice, maxtms = getfeasiblecolsone(istar, rmins[istar], ordlist[istar], numf, minprice, maxtms, fclist[istar])

	for row in range(len(rmins)):
		if (row != istar):
			fclist[row], minprice, maxtms = getfeasiblecolsone(row, rmins[row], ordlist[row], numf, minprice, maxtms, fb2col)
			
	#print("List of feasible cols for each row = "+ str(fclist))
	fclist.remove(fclist[istar])
	#print("List of feasible cols for each row = "+ str(fclist))

	# Get the list of  feasible columns by intersecting all the list in fclist
	fcols = func.reduce(intersection, fclist)

	return fcols, minprice, maxtms


#
def getfeasiblecolsone(row, rmin, order, numf, minprice, maxtms, fb2col):
	# Ignore the price of rmin
	rm = (rmin[0], rmin[1])
	
	# Find the index of rm in the order
	index = order.index(rm)
	
	fc = []
	type = getcoltype(rmin, row, numf)
	if (type == 1):			# rmin can't be a non-active slack variable
		print("getfeasiblecolsone: Something wrong!!!!!")
	elif (type == 2):		# non-slack with zero coefficient
		# Remove everying after the index, any price is OK
		fc = order[0:index]
	elif (type == 3):		# non-slack with non-zero coefficient
		print("type 3")
		if (row < numf):	# family case
			# Remove all the cols that is less preferred than rmin
			fc = order[0:index]
			# the total money is at most ...
			maxtms[row] = ds.dotproduct(rmin[1], rmin[2])
		else:				# game case, price matters
			g = row - numf
			# The price of game g is at least as expensive as the price of game g at rmin
			minprice[g] = rmin[2][g]
	else:					# active slack variable
		print("type 4")
		fc = order[:len(order)-1]		# any col, any price except the last is Ok
	
	print("fc =" + str(list(map(lambda x: fb2col[x], fc))))
	return fc, minprice, maxtms

#  list intersection
def intersection(x, y):
	x = set(x)
	return [a for a in y if a in x ]
	
# sort a list
def sortorder(sortedlist, sublist):
	ssl = set(sublist)
	return [x for x in sortedlist if x in ssl]
	
	

