######################## Ordinal Pivot ############################
import datastructure as ds

# @clist	: an ordinal basis
# @c		: a column that will be added to the basis
# @fp		: famimy preferences
# @rmins	: row min of the basis 

def ordinalpivot(clist, c, rmins, numf, fp):
	numrows = len(clist)
	
	# Remove column c from the basis
	clist.remove(c)
	
	# Find row minimizers after removing
	newrmins, row = getnewrowmins(clist, c, rmins, numf, fp)
	
	# Find the column with 2 row minimizers, 
	# and the row containing the old minimizer
	col2mins, jstar = getcoltwomins(rmins, newrmins)
	
	# Find the column k that maximizes c_{jstar, k}
	newc = findcolmax()
	
	# Update the basis
	clist.add(newc)
	
	# Update row mins of the new basis 
	newrmins[jstar] = newc
	
	# Return
	return clist, newc, newrmins
#	
def	getrowmin(clist, row, numf, fp):
	rm = clist[0]
	for i in range(1, len(clist)):
		if ds.strictlyprefer(rm, clist[i], row, numf, fp)
			rm = clist[i]
			
	return rm

# When removing one col from the basis, only one row minimizer is changed
def getnewrowmins(clist, c, rmins, numf, fp):
	for i in range(len(rmins)):
		if (c == rmins[i]):
			row = i
			break
			
	# Update the min of the row just found above, all others stay the same 
	rmins(row) = getrowmin(clist, row, numf, fp)
	
	return rmins, row
		
# 
def getcoltwomins(rmins, newrmins):
	for i in range(len(rmins)):
		if (rmins[i] !=  newmins[i]):
			return newmins[i], i
		
	# If not found raise some error
	print("getcoltwomins: Something went wrong !!!!")

# This is the most challenging function to write	
def findcolmax():
	# TODO 
	return 
	
# takes a column, a row, and numf
# returns the type of the column with respect to the row
# 1:non-active slack variable, 2: non-slack with zero coefficient, 
# 3: non-slack with non-zero coefficient, 4: active slack variable 
def getcoltype(c, row, numf):
	if isslack(c):	# slack variable
		if (c[0] == -row):
			return 4
		else:
			return 1
	else:			# non-slack variable
		if iszerocoff(c, row, numf):	# zero 
			return 2
		else:							# non-zero
			return 3

# 
def getfeasiblecols(row, rmins, ordlist, numf, minprice, mtmoney, fclist):
	# Update for the row only, others stay the same 
	fclist[row], minprice, mtmoney = getfeasiblecolsone(row, rmins[row], ordlist[row], numf, minprice, mtmoney, fclist[row])
	
	# Get the list of  feasible columns by intersecting all the list in fclist
	#TODO
	
	return 
	

#
def getfeasiblecolsone(row, rmin, order, numf, minprice, mtmoney):
	# Ignore the price of rmin
	rm = (rmin[0], rmin[1])
	
	# Find the index of rm in the order
	ind = order.index(rm)
	
	type = getcoltype(rmin, row, numf)
	if (type == 1):			# rmin can't be a non-active slack variable
		print("++++++ Something wrong +++++++++")
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
		fc = order		# any col, any price is Ok
	
	return fc, minprice, mtmoney

#  list intersection
def intersection(x, y):
	x = set(x)
	return [a for a in y if a in x ]

