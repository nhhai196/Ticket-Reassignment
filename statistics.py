


# 
def statistics(x, numf, numg, fb2col, FP, famsize):
	print("+++++++++++++++++++++++++++++++++++ Statistics +++++++++++++++++++++++++++++++++++++")
	nmf = matchedfam(x)
	print("nmf = " + str(nmf))
	
	nmp = matchedpeople(x, numf, numg, fb2col, famsize)
	print("nmp = " + str(nmp))
	
	fbyng = countfambynumgames(x, numf, numg, fb2col)
	print(fbyng)
	
	pbyng = countpeoplebynumgames(x, numf, numg, fb2col, famsize)
	print(pbyng)
	
	fbypref = countfambypref(x, numf, numg, fb2col, FP)
	print(fbypref)
	
	pbypref = countpeoplebypref(x, numf, numg, fb2col, FP, famsize)
	print(pbypref)
	
	return 
	
	
# count the number of matched families
def matchedfam(x):
	return sum(x)
	
# count the number of matched people
def matchedpeople(x, numf, numg, fb2col, famsize):
	count = 0
	for i in range(len(x)):
		if x[i]> 0: 
			(f, b) = ind2fb(i, fb2col, numf + numg)
			count += famsize[f]
	
	return count 
# count the number of families based on the number of games they get assigned
def countfambynumgames(x, numf, numg, fb2col):
	countlist = [0] * numg
	
	for i in range(len(x)):
		if x[i]> 0:
			f, b = ind2fb(i, fb2col, numf + numg)
			size = getbundlesize(b)
			countlist[size-1] += 1 
			
	return countlist
	
	
# count the number of families based on the number of games they get assigned
def countpeoplebynumgames(x, numf, numg, fb2col, famsize):
	countlist = [0] * numg
	
	for i in range(len(x)):
		if x[i]> 0:
			f, b = ind2fb(i, fb2col, numf + numg)
			size = getbundlesize(b)
			countlist[size-1] += famsize[f] 
			
	return countlist

# count the number of family based on preferences
def countfambypref(x, numf, numg, fb2col, FP):
	countlist = [0] * numg
	
	for i in range(len(x)):
		if x[i]> 0:
			f, b = ind2fb(i, fb2col, numf + numg)
			for j in range(len(b)):
				if b[j] > 0:
					countlist[FP[f][j] - 1] += 1
					
	return countlist
	
# count the number of family based on preferences
def countpeoplebypref(x, numf, numg, fb2col, FP, famsize):
	countlist = [0] * numg
	
	for i in range(len(x)):
		if x[i]> 0:
			f, b = ind2fb(i, fb2col, numf + numg)
			for j in range(len(b)):
				if b[j] > 0:
					countlist[FP[f][j] - 1] += famsize[f]
					
	return countlist
			
def ind2fb(ind, fb2col, numrows):
	#print('ind = ' + str(ind))
	# offset by the number of rows 
	for key, value in fb2col.items():
		if value == (ind + numrows):
			#print('key = '  + str(key))
			return key
			
			
def getbundlesize(bundle):
	size = 0
	for i in bundle:
		if i > 0:
			size += 1

	return size