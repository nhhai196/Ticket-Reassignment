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

#def compare(row, a, b):


# for game row
def comparegame(g, a, b):
    sa = isslack(a)
    sb = isslack(b)

    if (sa and sb):
        return (a[0] >= b[0])
    elif (sa and (not sb)):
        return False
    elif ((not sa) and sb):
        return True
    else:
        if (a[2][g-1] > b[2][g-1]):
            return True
        elif (a[2][g-1] < b[2][g-1]):
            return False
        else: # break tie
            breaktie(a,b)


def breaktie(a,b):
    if (a[0] < b[0]):
        return True
    elif (a[0] > b[0]):
        return False
    else:
        return breaktiebundle(a[1], b[1])

# @a: the first bundle
# @b: the second bundle
def breaktiebundle(a, b):
    n = len(a)
    for i in range(n):
        if (a[i] < b[i]):
            return True
        elif (a[i] > b[i]):
            return False

    print("+++++++ Break tie bundle: ERROR++++++")

# for family row
def comparefamily(g, a, b):
    sa = isslack(a)
    sb = isslack(b)

    if (sa and sb):
        return (a[0] >= b[0])
    elif (sa and (not sb)):
        return False
    elif ((not sa) and sb):
        return True
    else:
        return True

        # TODO

# for family row

#def comparefamily(g, a, b):


#
def isslack(c):
	return (c[0] < 0)

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
