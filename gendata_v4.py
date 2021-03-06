import random
from scipy import stats
import numpy as np
import copy

import xlsxwriter


def gendata(filename, numg, numf, fdist, numscore, minsize, numswaps, seatoffset, maxbsize, prunetype, prunenum):
#prunetype: 1: top, 2: random
#prunenum: number of bundles pruned

	numscore, scorelist = genscorelist(numscore, numg, numswaps)
	prefcdf = genprefcdf(numscore)
#	print(scorelist)
#	print(prefcdf)

	famdict, tupletoID, IDtobundle = genfam(numf, fdist, minsize, scorelist, prefcdf, maxbsize, prunetype, prunenum, seatoffset)
#	famdict[family][0]=size, famdict[family][1]=#seniors, famdict[family][2]=bundle preference
#	tupletoID[tuple([family][i])]= family's ID
	group = groupfamily(famdict)

#	print(group)

	workbook = xlsxwriter.Workbook(filename)
	wb = workbook.add_worksheet()


	wb.write(0, 0, 'Family Preference')
	wb.write(0, numg + 1, 'Family Size')
	wb.write(0, numg+ 3, 'Num Seniors')
	wb.write(0, numg + 5, 'Group ID')
	wb.write(0, numg + 7, 'Family Bundle Preference')

	row = 1
	for value in famdict.values():
#		print(value)
		temp = value[2]
#		print(temp)
		for col in range(numg):
			#print(temp[col])
			wb.write(row, col, temp[col])

		wb.write(row, numg + 1, value[0])
		wb.write(row, numg + 3, value[1])
		wb.write(row, numg + 5, tupletoID[tuple(value)])

		for i in range(len(IDtobundle[tupletoID[tuple(value)]])):
			sblist = IDtobundle[tupletoID[tuple(value)]][i]
			wb.write(row, numg + 7 + i, ",".join(map(str, sblist[1])))

		row += 1

	wb = workbook.add_worksheet()

	wb.write(0, 0, 'Family Preference')
	wb.write(0, numg + 1, 'Family Size')
	wb.write(0, numg + 3, 'Num Seniors')
	wb.write(0, numg + 5, 'Group Size')
	wb.write(0, numg + 7, 'Family Bundle Preference')

	row = 1
	for key, value in group.items():

		wb.write_row(row, 0, key[2])
		wb.write(row, numg + 1, key[0])
		wb.write(row, numg + 3, key[1])
		wb.write(row, numg + 5, len(value))
		for i in range(len(IDtobundle[row])):
			sblist = IDtobundle[row][i]
			wb.write(row, numg + 7 + i, ",".join(map(str, sblist[1])))
		row += 1

	wb = workbook.add_worksheet()
	wb.write(0, 0, 'Capacity')
	wb.write(0, 1, 'Alpha')
	wb.write(1, 0, round(numf * 2.65))	# Hardcode here for capacity
	for i in range(len(fdist)):
		wb.write(1, i+1, 2*(i+1)+seatoffset)

#	wb = workbook.add_worksheet()
#	wb.write(0, 0, 'Family Preference')

#	row = 1
#	for value in famdict.values():
#		sblist = genblist(value, maxbsize, seatoffset)
#		for i in range(len(sblist)):
#			wb.write(row, i, ",".join(map(str, sblist[i][1])))
#		row += 1

	workbook.close()

	#print(np.random.permutation([i for i in range(1,6)]))




	return famdict, group

def genblist(value, ub, extra):
	n = len(value[2])
	sblist = []
	for i in range(2**n-1, 0, -1):
		score = 0
		bundle = [0]*n
		bilist = [int(j) for j in list('{0:0b}'.format(i))]
		if sum(bilist) <= ub:
			bisize = len(bilist)
			for j in range(0,n-bisize):
				bilist.insert(0,0)
			for j in range(0,n):
				if bilist[j]==1:
					bundle[j] = value[0] + extra
					score = score + value[2][j]
			sblist.append([score, bundle])
	sblist.sort(key = lambda x: x[0], reverse=True)
	return sblist

def genblist_v2(value, ub, extra, prunetype, prunenum, seatoffset):
	n = len(value[2])
	sblist = []
	for i in range(2**n-1, 0, -1):
		score = 0
		bundle = [0]*n
		bilist = [int(j) for j in list('{0:0b}'.format(i))]
		if sum(bilist) <= ub:
			bisize = len(bilist)
			for j in range(0,n-bisize):
				bilist.insert(0,0)
			for j in range(0,n):
				if bilist[j]==1:
					bundle[j] = 2* value[0] + extra
					score = score + value[2][j]
			sblist.append([score, bundle])
	sblist.sort(key = lambda x: x[0], reverse=True)
	if prunetype==1:
		bundle = 0
		numpruned = 0
		while numpruned < prunenum:
			numpos = 0
			for item in range(len(sblist[bundle][1])):
				if sblist[bundle][1][item] > 0:
					numpos += 1
			if numpos == ub:
				del sblist[bundle]
				numpruned += 1
				continue
			bundle += 1
	if prunetype==2:
		bundle = 0
		numpruned = 0
		maxblist = []
		for bundle in range(len(sblist)):
			numpos = 0
			for item in range(len(sblist[bundle][1])):
				if sblist[bundle][1][item] > 0:
					numpos += 1
			if numpos == ub:
				maxblist.append(bundle)
		maxblist = np.random.permutation(maxblist)
		maxblist = sorted(maxblist[0:prunenum])
		for bundle in maxblist:
			del sblist[bundle-numpruned]
			numpruned += 1
	
	#print(sblist)
	return sblist

def groupfamily(famdict):
	group = {}

	for key, value in famdict.items():
		value = tuple(value)
		if value not in group:
			group[value] = [key]
		else:
			group[value].append(key)

	return group

def genbundle(tupletoID, maxbsize, prunetype, prunenum, seatoffset):
	IDtobundle = {}
	for key, value in tupletoID.items():
		sblist = genblist_v2(key, maxbsize, seatoffset, prunetype, prunenum, seatoffset)
		IDtobundle[value] = sblist
	return IDtobundle

def genfam(numf, dist, minsize, preflist, prefcdf, maxbsize, prunetype, prunenum, seatoffset):
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
	tupletoID = genID(famdict)

	IDtobundle = genbundle(tupletoID, maxbsize, prunetype, prunenum, seatoffset)

	return famdict, tupletoID, IDtobundle

def genID(famdict):
	numf = len(famdict)
	tupletoID = {}
	ID = 1
	for i in range(1, numf+1):
		if tuple(famdict[i]) not in tupletoID:
			tupletoID[tuple(famdict[i])] = ID
			ID += 1
	return tupletoID

def gensenior(famdict):
	numf = len(famdict)
	for i in range(1, numf+1):
		famdict[i][1] = randomsenior(famdict[i][0])

	return famdict

# random score over games
def randomscore(numg):
	score = [0] * numg
	for i in range(numg):
		score[i] = round(random.uniform(0.2, 1), 4)

	return score

def genscorelist(numscore, numg, numswaps):
	fewscore = 5

	smallslist = [randomscore(numg) for i in range(fewscore)]
	scorelist = []
	for i in range(numscore):
		temp = copy.copy(smallslist[random.randint(0,fewscore-1)])
		for j in range(numswaps):
			pos1 = random.randint(0, numg-1)
			pos2 = random.randint(0, numg-1)
			temp[pos1], temp[pos2] = temp[pos2], temp[pos1]

		scorelist.append(tuple(temp))

	scorelist = list(set(scorelist))

	return len(scorelist), scorelist

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




# gen a random pref based in preference cdf
def randompref(pcdf):
	rnum = random.uniform(0,1)

	for ind in range(len(pcdf)-1):
		if (pcdf[ind]<= rnum) and (rnum < pcdf[ind+1]):
			return ind




def randomsenior(anum):
	count = 0
	for i in range(anum):
		t = random.randint(2,4)
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

version = 1
numg = 6
numf = 1000
fdist = [0.15, 0.35, 0.3, 0.1, 0.1]
numscore = 40
minsize = 1
numswaps = 2
seatoffset = 4
maxbsize = 3
prunetype = 1
prunenum = 15
filename = 'data-' + str(numf) +'-prune-top-' + str(prunenum) + '-swap-' + str(numswaps) + '-offset-' + str(seatoffset) +'-score-' + str(numscore) + '-v-' + str(version) + '.xlsx'
gendata(filename, numg, numf, fdist, numscore, minsize, numswaps, seatoffset, maxbsize, prunetype, prunenum)
