import collections
import csv
import numpy
import sys

#################### MAIN ###########################


#numF = 2;

#s1 = list(1, 2, 4)
#s2 = list(3, 5, 6)
#p1 = list(1, 1, 1)
#p2 = list(0, 0, 0)

#c111 = tuple(1, s1, p1)
#c211 = tuple(2, s1, p1)
#c121 = tuple(1, s2, p1)
#c221 = tuple(2, s2, p1)





#####################################################

# @row: a row that can be either a family or a game
# @a: the first contract
# @b: the second contract
# returns YES if the first is more preferred than the second
# Otherwise returns NO

def strictlyprefer(a, b, row, numf, fp):
	if (row < numf):
		return fstrictlyprefer(a, b, row, numf, fp)
	else:
		return gstrictlyprefer(a, b, row, numf)
	
# for game row
# g is offset by  + numF
def gstrictlyprefer(a, b, g, numf):
	sa = isslack(a)
	sb = isslack(b)
	
	# Check if they are equal
	if (a == b):
		return False
	if (a[0] == -g):		# a is an active slack variable
		return False
		
	elif (b[0] == -g):		# b is an active slack variable
		return True
	# both are not active 
	if (sa and sb):
		return (a[0] > b[0])
	elif (sa and (not sb)):
		return True
	elif ((not sa) and sb):
		return False
	else:					# both are non-slack variable
		za = iszerocoff(a, row)
		zb = iszerocoff(b, row)
		
		if (za and zb):
			breaktie(a,b)
		elif (za and (not zb)):
			return True
		elif ((not za) and zb):
			return False
		else:				# both are non-zeros
			if (a[2][g-1] > b[2][g-1]):	# compare price
				return True
			elif (a[2][g-1] < b[2][g-1]):
				return False
			else: 		# break tie
				return breaktie(a,b)

# for a family row				
def fstrictlyprefer(a, b, f, numf, fp):
	sa = isslack(a)
	sb = isslack(b)
	
	# Check if they are equal
	if (a == b):
		return False
	if (a[0] == -g):		# a is an active slack variable
		return False
		
	elif (b[0] == -g):		# b is an active slack variable
		return True
	# both are not active 
	if (sa and sb):
		return (a[0] > b[0])
	elif (sa and (not sb)):
		return True
	elif ((not sa) and sb):
		return False
	else:					# both are non-slack variable
		za = iszerocoeff(a, row, numf)
		zb = iszerocoeff(b, row, numf)
		
		if (za and zb):
			breaktie(a,b)
		elif (za and (not zb)):
			return True
		elif ((not za) and zb):
			return False
		else:				# both are non-zeros
			if (fp[a[0]] < fp[b[0]]):
				return True
			elif (fp[a[0]] > fp[b[0]]):
				return False
			else:
				msa = dotproduct(a[1], a[2])	# money spent 
				msb = dotproduct(b[1], b[1])
				if (msa > msb):
					return True
				elif (msa < msb):
					return False
				else:
					breaktie(a,b)

# dot product of two vectors with the same length
def dotproduct(x, y):
	sum = 0
	for i in range(len(x)):
		sum = sum + x[i] * y[i]
		
	return sum
	
# Break tie two contracts a and b
def breaktie(a,b):
	if (a[0] < b[0]):
		return True
	elif (a[0] > b[0]):
		return False
	else:
		if (a[1] == b[1]):
			return breaktievector(a[2], b[2])
		else:
			return breaktievector(a[1], b[1])
 
# @a: the first bundle
# @b: the second bundle
def breaktievector(a, b):
    n = len(a)
    for i in range(n):
        if (a[i] < b[i]):
            return True
        elif (a[i] > b[i]):
            return False

    print("+++++++ Break tie: ERROR ++++++")

#
def isslack(c):
	return (c[0] < 0)

# for non-slack only
def iszerocoeff(a, row, numf):
	if (row < numf):
		return not(a[0] == row)
	else:
		return a[1][row - numf] == 0
	
#
def init(str):

    bundle2rank = [] #bundle maps to the rank, each family has one dictionary
    bundlelist = [] #preference list over bundles, each family has one list
    fb2col = {} #map (family,bundle) to the column index of matrix A
    numcol = 0

    #initialization and create slack contracts
    with open(sys.argv[1]) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                item_count = 0
                for item in row:
                    if item_count == 0:
                        numF = int(float(item)) #get number of families
                        budget = [0]*numF #create budget list
                        item_count = 1
                    elif item_count == 1:
                        numG = int(float(item)) #get number of games
                        break
                line_count += 1
            elif line_count < numF+1:
                item_count = 0
                for item in row:
                    if item_count == 0:
                        budget[line_count-1] = int(float(item)) #budget[f-1] denotes the budget of family f
                        item_count = 1
                        bundle2rank.append({})
                        bundlelist.append([])
                    elif item_count > 0:
                        if item.strip(): #filter empty string
                            intlist = [int(float(i)) for i in item.split(',')] #convert string to int
                            inttuple = tuple(intlist)
                            bundle2rank[line_count-1][inttuple] = item_count #bundle2rank[f-1] maps from a tuple bundle to rank for family f
                            bundlelist[line_count-1].append(inttuple) #bundle2rank[f-1] is the bundle ranking for family f
                            fb2col[(line_count-1,inttuple)] = numF + numG + numcol # (f-1, bundle) maps to the column index of A
                            item_count += 1
                            numcol += 1
            #print(bundle2rank[line_count-1])
            #print(bundlelist[line_count-1])
                line_count += 1
            else:
                capacity = [int(float(i)) for i in row if i.strip()] #capacity[g-1] is the capacity of game g
                #print(capacity)

#now we have bundle2rank, bundlerank, fb2col, capacity, and budget
#print(fb2col)

    A = numpy.zeros((numF+numG,numF+numG+numcol))

#create slack columns/Contracts
#in fb2col, negative family/game id only has the id as the key, no bundle needed
#clist = [] #contract list
    for i in range(numF):
#    clist.append((-1*(i+1),[],[]))
        fb2col[-1*(i+1)] = i
        A[i,i] = 1

    for i in range(numG):
#    clist.append((-1*(i+1+numF),[],[]))
        fb2col[-1*(i+1+numF)] = i+numF
        A[i+numF,i+numF] = 1

    col_count = numF + numG
    for i in range(numF):
        for j in bundlelist[i]:
            A[i, col_count] = 1
            game_count = 0
            for k in j:
                A[numF + game_count, col_count] = k
                game_count += 1
            col_count += 1

    return numF, numG, bundle2rank, bundlelist, fb2col, budget, capacity, numcol, A
#print(A)
