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
	mtmoney = [0] * numf
	fclist = [[]]* numrows
	newc = findcolmax(newrm, istar, rmins, ordlist, numf, minprice, mtmoney, fclist, fb2col)

	# Update the basis
	#clist.append(newc)

	# Update row mins of the new basis
	#newrmins[istar] = newc

	# Return
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
def findcolmax(newrm, istar, rmins, ordlist, numf, minprice, mtmoney, fclist, fb2col):
	# TODO 
	fc, minprice, mtmoney = getfeasiblecols(newrm, istar, rmins, ordlist, numf, minprice, mtmoney, fclist, fb2col)
	
	# sort feasible columns in deceasing order of preferences
	fc = sortorder(ordlist[istar], fc)
	
	print("feasible cols = " + str(list(map(lambda x: fb2col[x], fc))))
	print(minprice)
	print(mtmoney)
	
	# Assuming fc is sorted in decreasing order
	# Linear search here, binary search might be better 
	for c in fc:
		type = getcoltype(c, istar, numf)
		if ((type == 1)):
			return c
		elif (type == 2):
			return c # TODO: this is not correct
		elif (type == 3):
			bol = existfeasibleprice()
			if bol:
				return # TODO
		else:
			return c
	return 
	
	
#
def gbestprice(eps, c, istar, rmins, numf, minprice, mtmoney, budget):
	btlist = []			# break tie list 
	newprice = copy.deepcopy(minprice)
	newmtmoney = copy.deepcopy(mtmoney)
	
	cc = (c[0], c[1], minprice)
	
	# now need to check whether the price needs to be adjusted due to breaking tie
	for row in range(len(rmins)):
		if (row < numf) and (row != istar):		# family case
			ctype = getcoltype(cc, row, numf)		# verify cc
			mtype = getcoltype(rmins[row], row, numf)
			
			# if same family and same bundle, need to break tie carefuly here 
			if (c[0] == rmins[0]) and (c[1] == rmins[1]):
				if (ctype == 2) and (mtype == 2):	# zero coefficient
					# break tie based on price
					btlist.append(rmins[2])
					
				elif (ctype == 3) and (mtype == 3):	# non-zero coefficient	
					newmtmoney[row] =  newmtmoney[row] + eps
				
		elif (row >= numf) and (row != istar):	# game case
			ctype = getcoltype(cc, row, numf)		# verify cc
			mtype = getcoltype(rmins[row], row, numf)
			
			# if same family and same bundle, need to break tie carefuly here 
			if (c[0] == rmins[0]) and (c[1] == rmins[1]):
				# break tie based on price
				btlist.append(rmins[2])
			else:		# different 
				if (ctype == 3) and (mtype == 3):
					if not ds.breaktie(cc, rmins[row]):
						newprice[g] = eps + newprice[g]	# must be eps higher
	
	# Check if there exists a price that is coordinate-wise 
	# greater than the minprice and is tie-break larger than each price in btlist
	# set price of the game g as high as possible
	g = istar - numf
	beta = math.floor(budget - ds.dotproduct(c[1], minprice))/(c[g] * eps)
	
	if beta < 0:
		print("++++++++ No feasible price")
		
	newprice[g] = newprice[g] + beta * eps 	# TODO: check no rounding error 
	


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
def getfeasiblecols(newrm, istar, rmins, ordlist, numf, minprice, mtmoney, fclist, fb2col):
	# TODO: Store values
	# Update for 2 rows only, that is the newrm and istar, others stay the same
	#fclist[newrm], minprice, mtmoney = getfeasiblecolsone(newrm, rmins[newrm], ordlist[newrm], numf, minprice, mtmoney, fclist[newrm])

	#fclist[istar], minprice, mtmoney = getfeasiblecolsone(istar, rmins[istar], ordlist[istar], numf, minprice, mtmoney, fclist[istar])

	for row in range(len(rmins)):
		if (row != istar):
			fclist[row], minprice, mtmoney = getfeasiblecolsone(row, rmins[row], ordlist[row], numf, minprice, mtmoney, fb2col)
			
	#print("List of feasible cols for each row = "+ str(fclist))
	fclist.remove(fclist[istar])
	#print("List of feasible cols for each row = "+ str(fclist))

	# Get the list of  feasible columns by intersecting all the list in fclist
	fcols = func.reduce(intersection, fclist)

	return fcols, minprice, mtmoney


#
def getfeasiblecolsone(row, rmin, order, numf, minprice, mtmoney, fb2col):
	# Ignore the price of rmin
	rm = (rmin[0], rmin[1])
	
	# Find the index of rm in the order
	ind = order.index(rm)
	
	fc = []
	type = getcoltype(rmin, row, numf)
	if (type == 1):			# rmin can't be a non-active slack variable
		print("getfeasiblecolsone: Something wrong!!!!!")
	elif (type == 2):		# non-slack with zero coefficient
		# Remove everying after the index, any price is OK
		fc = order[0:index]
	elif (type == 3):		# non-slack with non-zero coefficient
		if (row < numf):	# family case
			# Remove all the cols that is less preferred than rmin
			fc = order[0:index]
			# the total money is at least ...
			mtmoney[row] = ds.dotproduct(rmin[1], rmin[2])
		else:				# game case, price matters
			g = row - numf
			# The price of game g is at least as expensive as the price of game g at rmin
			minprice[g] = rmin[2][g]
	else:					# active slack variable
		fc = order[:len(order)-1]		# any col, any price except the last is Ok

	return fc, minprice, mtmoney

#  list intersection
def intersection(x, y):
	x = set(x)
	return [a for a in y if a in x ]
	
# sort a list
def sortorder(sortedlist, sublist):
	ssl = set(sublist)
	return [x for x in sortedlist if x in ssl]
	
	

