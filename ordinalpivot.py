######################## Ordinal Pivot ############################
import datastructure as ds
import copy
import functools as func
import math
import correctness as cor

# @clist	: an ordinal basis
# @c		: a column that will be added to the basis
# @fp		: famimy preferences
# @rmins	: row min of the basis

def ordinalpivot(eps, clist, c, rmins, numf, numg, fp, ordlist, fb2col, budget):
	print("++++++++ Ordinal Pivot:")
	#eps = 0.1
	#budget = 3
	numrows = len(clist)
	
	#print("Row minimizers:")
	#ds.printbasis(rmins, fb2col)

	# Remove column c from the basis
	print("---- Kick out: " + str(c))
	#clist.remove(c)
	removecon(clist, c)
	
	# Find row minimizers after removing
	newrmins, newrm = getnewrowmins(clist, c, rmins, numf, fp)
	#print("Row mins after removing :" + str(c))
	#ds.printbasis(newrmins, fb2col)
	#print("The row that has new row min: " + str(newrm))

	# Find the column with 2 row minimizers,
	col2mins = getcoltwomins(rmins, newrmins)
	#print("Col with two mins: " + str(col2mins))

	# Find the row containing the old minimizer
	istar = findoldminimizer(col2mins, rmins)
	#print("------------ Old minimizer istar = " + str(istar))
	#if istar >= numf:
	#	print("***************************** Game case finally")
		#return None

	# Find the column k that maximizes c_{istar, k}
	newc = []
	minprice = [0] * numg
	maxtms = [0] * numf
	fclist = [[]]* numrows
	newc = findcolmax(eps, newrm, istar, newrmins, ordlist, numf, minprice, maxtms, fclist, fb2col, budget)

	# Update the basis
	clist.append(newc)
	print("---- Push in : " + str(newc) + " : " + str(fb2col[(newc[0], newc[1])]))

	# Update row mins of the new basis
	newrmins[istar] = newc

	# Sanity check
	#print("Sanity check:" + str(clist))
	#temp = getallrowmins(clist, numf, fp)
	#if (temp !=newrmins):
	#	print("---- ordinal pivot: Something wrong !!!!!!!")
	#	ds.printbasis(temp, fb2col)
	#	print(temp)
	#print("budget = " +str(budget))
	#if cor.isordbasis(eps, clist, numf, numg, fp, ordlist, fb2col, budget):
	#	print("@@@@@@@@@@@@@@@@@@@@ Sanity check passed")
	#else:
	#	print("@@@@@@@@@@@@@@@@@@@@ Sanity check failed")
	#	return

	#print("New row mins:")
	#ds.printbasis(newrmins, fb2col)
	# Return
	return clist, newc, newrmins, istar


def initordinalbasis(A, numf, numg, fb2col):

	initOB = []
	
	# Find the first zeros non-slack col with respect the first row
	numcol = len(A[0,:])

	for colindex in range(numf+numg, numcol):
		if A[0,colindex] == 0:
			break
	
	print(colindex)	
	for (f, b) in fb2col:
		#print("key = " + str(key))
		#print(value)
		if  fb2col[(f,b)] == colindex:
			break
	
	p = [0] * numg
	c = (f, b, p)
	
	initOB.append(c)
	for i in range(1, numf+numg):
		initOB.append((-1*(i+1),(),[]))
		
	return c, initOB
	
#
def removecon(clist, c):
	for x in clist:
		if ds.isequalcon(x, c):
			clist.remove(x)
			return clist
#
def	getrowmin(clist, row, numf, fp):
	rm = clist[0]

	#print("row = " +str(row))
	for i in range(1, len(clist)):
		#print(clist[i])
		#print(ds.strictlyprefer(rm, clist[i], row, numf, fp))
		if ds.strictlyprefer(rm, clist[i], row, numf, fp):
			rm = clist[i]
			#print("++++Swap")
	#print(rm)
	return rm

# When removing one col from the basis, only one row minimizer is changed
def getnewrowmins(clist, c, rmins, numf, fp):
	row = None;
	newrmins = copy.deepcopy(rmins)
	for i in range(len(rmins)):
		if ds.isequalcon(c, rmins[i]):
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
		temp = getrowmin(clist, row, numf, fp)
		#print("temp = " + str(temp))
		rmins.append(getrowmin(clist, row, numf, fp))

	return rmins
#
def getcoltwomins(rmins, newrmins):
	#print(rmins)
	#print(newrmins)
	for i in range(len(rmins)):
		if not ds.isequalcon(rmins[i], newrmins[i]):
			return newrmins[i]

	# If not found raise some error
	print("getcoltwomins: Something went wrong !!!!")

# Find old minimizer
def findoldminimizer(col2mins, rmins):
	for i in range(len(rmins)):
		if ds.isequalcon(col2mins, rmins[i]):
			return i

	print("find old min: Something went wrong!!!!!")
	
# This is the most challenging function to write	
def findcolmax(eps, newrm, istar, rmins, ordlist, numf, minprice, maxtms, fclist, fb2col, budget):
	# TODO 
	fc, minprice, maxtms = getfeasiblecols(newrm, istar, rmins, ordlist, numf, minprice, maxtms, fclist, fb2col)
	
	# sort feasible columns in deceasing order of preferences
	fc = sortorder(ordlist[istar], fc)
	
	#print("--- Feasible cols = " + str(list(map(lambda x: fb2col[x], fc))))
	#print(minprice)
	#print(maxtms)
	
	fbmins = list(map(lambda x: (x[0], x[1]), rmins))
	
	
	# Assuming fc is sorted in decreasing order
	# Linear search here, binary search might be better 
	mpvlist = []		# Store the highest price vectors of feasible cols of type 3
	mpglist =[]			# Store the highest price of the game of feasible cols of type 3
	t3clist = []		# Store all feasible cols of type 3
	
	# pop out the slack col of type 4 in the feasible cols list
	scol = fc.pop(len(fc)-1)
	
	for c in fc:		
		type = getcoltype(c, istar, numf)
		if ((type == 1)):
			return (c[0], c[1], [])
		elif (type == 2):
			temp = findbestprice(eps, c, istar, rmins, numf, minprice, maxtms, budget[c[0]], fbmins)
			#print("temp = " + str(temp))
			if not not temp:
				#temp = roundprice(temp)
				return (c[0], c[1],temp)
				
		if (type == 3):
			if istar < numf:	# family case
				temp = findbestprice(eps, c, istar, rmins, numf, minprice, maxtms, budget[c[0]], fbmins)
				if not not temp:
					#temp = roundprice(temp)
					return (c[0], c[1],temp)
			else:				# game case
				# In this case need to loop through all feasible cols of type 3
				# and find the col that can pay the highest price
				#print("@@@@@@ c = " +str(c))
				t3clist.append(c)
				temp = findbestprice(eps, c, istar, rmins, numf, minprice, maxtms, budget[c[0]], fbmins)
				
				#print(temp)
				mpvlist.append(temp)
				if temp == []:
					mpglist.append(-1)
					
				else:
					#temp = roundprice(temp)
					mpglist.append(round(temp[istar-numf], 3))

			
	# If not return yet, must be type 3 and istar >= numf
	if (istar >= numf):
		#print("@@@@ Game case: looking for the best price")
		maxval = max(mpglist)
		index = mpglist.index(maxval)
		fb = t3clist[index]
		price = mpvlist[index]
		#print(maxval)
		#print(mpglist)
		#print(mpvlist)
		
		if not not price:
			#price = roundprice(price)
			return (fb[0], fb[1], price)
		
	# If not return yet, the best col must the the type 4
	return (scol[0], scol[1], [])
	

# always returns the best price or []
	
def findbestprice(eps, c, istar, rmins, numf, minprice, maxtms, budget, fbmins):
	numg = len(rmins) - numf
	fbtprice = [0] * numg					# family break tie price 
	gbtprice = [0] * numg					# game break tie price
	diff = []								# the bestprice must be different from diff
	
	currminprice = [0] * (len(rmins) - numf) #copy.deepcopy(minprice)
	currmaxtms = [0] * numf #copy.deepcopy(maxtms)
	
	cc = (c[0], c[1], currminprice)
	
	if c not in fbmins:
		for row in range(len(rmins)):
			#if (row < numf) and (row != istar):		# family case
			#	print("Do nothing 1")
					
			if (row >= numf) and (row != istar):	# game case
				g = row - numf
				ctype = getcoltype(cc, row, numf)		
				mtype = getcoltype(rmins[row], row, numf)
				
				if (ctype == 3) and (mtype == 3):					
					if not ds.breaktie(cc, rmins[row]):
						currminprice[g] = rmins[row][2][g] + eps	# must be eps higher
						#print("---- TODO")
					else:
						currminprice[g] = rmins[row][2][g]
						
		return bestprice(eps, istar, c[1], currminprice, [], budget+1, budget, numf, diff)			
	# For a row that already have a contract without price (f,b) in the basis				
	else:
		#print("-------------------------- Interesting Case")
		index = fbmins.index(c)
		if (index == istar):
			for i in range(len(fbmins)):
				if (i != istar) and (fbmins[i] == c):
					index = i

		#print("###################index = " + str(index))
		#print("###################istar = " + str(istar))
		
		# best price must be differrent from the existing one
		diff = rmins[index][2]
		
		for row in range(len(rmins)):
			#if (row < numf) and (row != istar) and (row != index):		# family case
			#	print("---- Family case")
					
			if (row >= numf) and (row != istar) and (row != index):	# game case
				#print("---- Game case")
				g = row - numf
				ctype = getcoltype(cc, row, numf)		
				mtype = getcoltype(rmins[row], row, numf)
				
				if (ctype == 3) and (mtype == 3):
					#print("--- Check point")
					if not ds.breaktie(cc, rmins[row]):
						currminprice[g] = rmins[row][2][g] + eps	# must be eps higher
					else:
						currminprice[g] = rmins[row][2][g]
		# same family and same bundle, need to break tie carefuly here 
		ctype = getcoltype(cc, index, numf)		# verify cc
		mtype = getcoltype(rmins[index], index, numf)
		
		if (index < numf):						# family case
			#print("---------------- Family case")
			
			if (ctype == 3) and (mtype == 3):	# non-zero coefficient
				fbtprice = rmins[index][2]
				currmaxtms[index] =  ds.dotproduct(c[1], rmins[index][2])
				
				temp = bestprice(eps, istar, c[1], currminprice, fbtprice, currmaxtms[index], budget, numf, diff)
				if not temp:
					currmaxtms[index] =  ds.dotproduct(c[1], rmins[index][2]) - eps
					fbtprice = []
					return bestprice(eps, istar, c[1], currminprice, fbtprice, currmaxtms[index], budget, numf, diff)
				else:
					return temp
			elif (ctype == 2) and (mtype == 2):
				fbtprice = rmins[index][2]
				return bestprice(eps, istar, c[1], currminprice, fbtprice, budget+1, budget, numf, diff)
			else:
				return bestprice(eps, istar, c[1], currminprice, [], budget+1, budget, numf, diff)
				
		else:									# game case
			#print("---------------- Finally touched game case")
			# break tie based on price
			g = index - numf
			if (istar >= numf):
				currminprice[istar - numf] = 0
				
			
			if (ctype == 3) and (mtype == 3):	# non-zero coefficient
				#print("*********** Degbug Here")
				#print("price = " + str(currminprice))
				
				if (istar <numf):
					gbtprice = rmins[index][2]
					currminprice[g] = rmins[index][2][g] 	
					temp = bestprice(eps, istar, c[1], currminprice, gbtprice, budget + 1, budget, numf, diff)
					if not temp:
						gbtprice = []
						currminprice[g] = rmins[index][2][g] + eps
						return bestprice(eps, istar, c[1], currminprice, gbtprice, budget + 1, budget, numf, diff)
					else:
						return temp
				else:
					#print("&&&&&&&&&&&&&&&&&&&&&&&& Check")
					gbtprice = rmins[index][2]
					currminprice[g] = rmins[index][2][g] 	
					temp1 = bestprice(eps, istar, c[1], currminprice, gbtprice, budget + 1, budget, numf, diff)

					gbtprice = []
					currminprice[g] = rmins[index][2][g] + eps
					temp2 = bestprice(eps, istar, c[1], currminprice, gbtprice, budget + 1, budget, numf, diff)
					
					#print("temp1 =" + str(temp1))
					#print("temp2 =" +str(temp2))
					
					if (temp1 == []) and (temp2 == []):
						return []
					elif (temp1 == []) and (temp2 != []):
						return temp2
					elif (temp1 != []) and (temp2 == []):
						return temp1
					else:
						tol = 10**(-6)
						if not ds.isequalprice(temp1, temp2):
							if (temp1[istar - numf] + tol >= temp2[istar-numf]):
								return temp1
							else:
								return temp2
						else:
							return temp1
			elif (ctype == 2) and (mtype == 2):
				gbtprice = rmins[index][2]
				return bestprice(eps, istar, c[1], currminprice, gbtprice, budget+1, budget, numf, diff)
			else:
				return bestprice(eps, istar, c[1], currminprice, [], budget+1, budget, numf, diff)

# 
def bestprice(eps, istar, alpha, minprice, btprice, maxtot, budget, numf, diff):
	if (istar < numf):	# family case
			return fbestprice(istar, alpha, minprice, btprice, maxtot, budget)
	else:				# game case
			return gbestprice(eps, istar, alpha, numf, minprice, btprice, maxtot, budget, diff)
		
	
	
# Check if there exists a price that is coordinate-wise 
# greater than the minprice and is tie-break larger than btprice.

def fbestprice(istar, alpha, minprice, btprice, maxtot, budget):
	#print("Debug")
	#print(minprice)
	#print(btprice)
	#print(maxtot)
	
	ms = ds.dotproduct(alpha, minprice)
	tol = 10**(-6)
	
	if isfeasibleprice(alpha, minprice, budget) and (ms <= maxtot + tol):
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
def gbestprice(eps, istar, alpha, numf, minprice, btprice, maxtot, budget, diff):
	ms = ds.dotproduct(alpha, minprice)
	tol = 10**(-6)
	bestprice = copy.deepcopy(minprice)
	g = istar - numf
	
	#print("minprice =" + str(minprice))
	#print("btprice =" + str(btprice))
	#print(maxtot)
	
	
	if isfeasibleprice(alpha, minprice, budget) and (ms <= maxtot + tol):
		if not btprice:	# empty
			#print("++++++++++++ gbest price: TODO 1")
			bestprice[g] = gfindmaxprice(eps, g, alpha, minprice, maxtot, budget)
			
		else:			# non-empty
			#print("++++++++++++ gbest price: TODO 2")
			if ds.breaktievector(minprice, btprice):
				jstar = breaktieindex(minprice, btprice)
				#print("jstar = " + str(jstar))
				
				if (g < jstar):
					bestprice[g] = btprice[g]	# TODO
				elif (g == jstar):
					#print("THIS CASE")
					if (btprice[g] >= eps - 10**(-8)):
						bestprice[g] = btprice[g] - eps
					else:
						bestprice = []
				else:	# set the price as high as possible
					bestprice[g] = gfindmaxprice(eps, g, alpha, minprice, maxtot, budget)
			
			else:	# No
				bestprice = []
		
	else:		# No 
		bestprice = []
		
	if (bestprice == diff):
		bestprice = []
	
	#print("Set bestprice = " + str(bestprice))
	return bestprice
	
# 
def gfindmaxprice(eps, g, alpha, minprice, maxtot, budget):
	#bestprice = copy.deepcopy(minprice)
	tol = 10**(-6)
	#print(maxtot)
	#print(budget)
	#print(alpha)
	#print(min(maxtot, budget) - ds.dotproduct(alpha, minprice))
	#print(alpha[g] * eps)
	beta = math.floor((min(maxtot, budget) - ds.dotproduct(alpha, minprice) + tol)/(alpha[g] * eps))
	#print("beta = " + str(beta))

	if beta < 0:
		print("++++++++ gfindmaxprice: no feasible price")
	
	bestprice = minprice[g] + beta * eps 	# TODO: check no rounding error 
	
	return bestprice

# Takes two price vector x and y (of the same length), returns the smallest index s.t x[i] < y[i]
# If does not exist, returns -1.
def breaktieindex(x,y):
	tol = 10**(-6)
	for i in range(len(x)):
		if (x[i] < y[i] - tol): # TODO
			return i
			
	return -1

# Check if a price is feasible given the budget and alpha
def isfeasibleprice(alpha, price, budget):
	tol = 10**(-6)
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
	#print("order = " + str(list(map(lambda x: fb2col[x], order))))
	# Ignore the price of rmin
	rm = (rmin[0], rmin[1])
	#print(rm)
	# Find the index of rm in the order
	index = order.index(rm)
	
	fc = []
	type = getcoltype(rmin, row, numf)
	#print ("type = " + str(type) + " ", end ='')
	if (type == 1):			# rmin can't be a non-active slack variable
		print("getfeasiblecolsone: Something wrong!!!!!")
	elif (type == 2):		# non-slack with zero coefficient
		# Remove everying after the index, any price is OK
		fc = order[0:index+1]
	elif (type == 3):		# non-slack with non-zero coefficient
		#print("type 3")
		if (row < numf):	# family case
			#print("family case")
			# Remove all the cols that is less preferred than rmin
			fc = order[0:index+1]
			#print("index = " + str(index))
			#print(order)
			# the total money is at most ...
			maxtms[row] = ds.dotproduct(rmin[1], rmin[2])
		else:				# game case, price matters
			#print("game case")
			g = row - numf
			fc = order[:len(order) - 1]
			# The price of game g is at least as expensive as the price of game g at rmin
			minprice[g] = rmin[2][g]
	else:					# active slack variable
		#print("type 4")
		fc = order[:len(order)-1]		# any col, any price is OK
	
	#print("row = " + str(row) + ": " + "fc =" + str(list(map(lambda x: fb2col[x], fc))))
	return fc, minprice, maxtms

#  list intersection
def intersection(x, y):
	x = set(x)
	return [a for a in y if a in x ]
	
# sort a list
def sortorder(sortedlist, sublist):
	ssl = set(sublist)
	return [x for x in sortedlist if x in ssl]
	
# 
def roundprice(p):
	for i in range(len(p)):
		p[i] = round(p[i],3)
		
		
