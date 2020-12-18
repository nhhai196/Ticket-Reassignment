import random
from scipy import stats
import numpy as np
import copy

import xlsxwriter


def gendata(filename, numg, numf, fdist, numpref, minsize, numswaps):

	numpref, preflist = genpreflistv2(numpref, numg, numswaps)
	prefcdf = genprefcdf(numpref)
	print(preflist)
	print(prefcdf)


	famdict = genfam(numf, fdist, minsize, preflist, prefcdf)
	group = groupfamily(famdict)

	print(group)

	workbook = xlsxwriter.Workbook(filename)
	wb = workbook.add_worksheet()


	wb.write(0, 0, 'Family Preference')
	wb.write(0, numg + 1, 'Family Size')
	wb.write(0, numg+ 3, 'Num Seniors')

	row = 1
	for value in famdict.values():
		print(value)
		temp = value[2]
		print(temp)
		for col in range(numg):
			#print(temp[col])
			wb.write(row, col, temp[col])

		wb.write(row, numg + 1, value[0])
		wb.write(row, numg + 3, value[1])
		row += 1

	wb = workbook.add_worksheet()

	wb.write(0, 0, 'Family Preference')
	wb.write(0, numg + 1, 'Family Size')
	wb.write(0, numg + 3, 'Num Seniors')
	wb.write(0, numg + 5, 'Group Size')

	row = 1
	for key, value in group.items():

		wb.write_row(row, 0, key[2])
		wb.write(row, numg + 1, key[0])
		wb.write(row, numg + 3, key[1])
		wb.write(row, numg + 5, len(value))
		row += 1
	workbook.close()

	#print(np.random.permutation([i for i in range(1,6)]))




	return famdict, group



def groupfamily(famdict):
	group = {}

	for key, value in famdict.items():
		value = tuple(value)
		if value not in group:
			group[value] = [key]
		else:
			group[value].append(key)

	return group

def genfam(numf, dist, minsize, preflist, prefcdf):
	famdict = {}
	fdist = distmul(dist, numf)

	f = 0;
	#print(fdist)
	for i in range(len(fdist)):
		#print('i =' + str(i))
		for j in range(1, fdist[i]+1):
			#print('j =' + str(j))
			f = f+1
			#print('f =' + str(f))
			famdict[f] = [i+minsize, (), ()]

	#print ("famdict first = " + str(famdict))
	famdict = gensenior(famdict)
	#print ("famdict second = " + str(famdict))
	famdict = genpref(famdict, preflist, prefcdf)
	#print ("famdict third = " + str(famdict))

	return famdict


def gensenior(famdict):
	numf = len(famdict)
	for i in range(1, numf+1):
		famdict[i][1] = randomsenior(famdict[i][0])

	return famdict


def genpreflist(numpref, numg):
	temp = [i for i in range(1, numg+1)]
	preflist = list(set([tuple(np.random.permutation(temp)) for i in range(numpref)]))

	return len(preflist), preflist

def genpreflistv2(numpref, numg, numswaps):
	fixpref = np.random.permutation([i for i in range(1, numg+1)])
	preflist = []
	for i in range(numpref):
		temp = copy.copy(fixpref)
		for j in range(numswaps):
			pos1 = random.randint(0, numg-1)
			pos2 = random.randint(0, numg-1)
			temp[pos1], temp[pos2] = temp[pos2], temp[pos1]

		preflist.append(tuple(temp))

	preflist = list(set(preflist))
	return len(preflist), preflist

def swapPositions(list, pos1, pos2):

    list[pos1], list[pos2] = list[pos2], list[pos1]
    return list

# Uniform distribution
def genprefcdf(numpref):
	temp = [i for i in range(numpref+1)]
	return stats.uniform.cdf(temp, loc = 0, scale = numpref)



def genpref(famdict, plist, prefcdf):
	numf = len(famdict)

	for i in range(numf):
		index = randompref(prefcdf)
		famdict[i+1][2] = plist[index]

	return famdict





def randompref(pcdf):
	rnum = random.uniform(0,1)

	for ind in range(len(pcdf)-1):
		if (pcdf[ind]<= rnum) and (rnum < pcdf[ind+1]):
			return ind




def randomsenior(anum):
	count = 0
	for i in range(anum):
		t = random.randint(1,4)
		if t == 1:
			count += 1

	return count




def distmul(dist, num):
	n = len(dist)
	ans = [round(num * x) for x in dist]
	s = sum(ans)
	if s > num:
		ans[0] = ans[0] + num - s
	elif s < num:
		ans[0] = ans[0] - num + s

	return ans

#filename = 'data-swap-1.xlsx'
#numg = 3
#numf = 3
#fdist = [0.5, 0.5]
#numpref = 1000
#minsize = 2
#numswaps = 1
################# Testing
filename = 'data4-swap.xlsx'
numg = 6
numf = 1000
fdist = [0.15, 0.35, 0.3, 0.15, 0.05]
numpref = 10
minsize = 1
numswaps = 1
gendata(filename, numg, numf, fdist, numpref, minsize, numswaps)
