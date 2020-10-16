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
	rmins[row] = newrmins[row]
	rmins[jstar] = newc
	
	# Return
	return clist, newc, rmins
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
	
def findcolmax():
	# TODO 
	return 
	

