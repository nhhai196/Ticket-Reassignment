from openpyxl import *
import copy
from numpy import * 
import datastructure as ds


# 
def statistics(filename, A, x, b,  numf, numg, fb2col, FP, famsize):
	print("+++++++++++++++++++++++++++++++++++ Statistics +++++++++++++++++++++++++++++++++++++")
	
	
	nmf, nmp, bysize, fbyng, pbyng, fbypref, pbypref = stathelper(x, numf, numg, fb2col, FP, famsize)
	
	print("nmf = " + str(nmf))
	print("nmp = " + str(nmp))
	print(bysize)
	print(fbyng)
	print(pbyng)
	print(fbypref)	
	print(pbypref)
	
	avgnmf = mean(nmf)
	avgnmp = mean(nmp)
	avgbysize = [0] * 5
	
	# Violations
	V, P = violations(A,x,b)
	
	maxv = max(P)
	print('V = ' + str(V))
	print('P = ' + str(P))
	print('max violation =' + str(maxv))
	
	#
	for i in range(5):
		avgbysize[i] = mean(bysize[i])
		
	
	# Save to a file 
	wb=load_workbook(filename)
	ws=wb["Sheet3"]
	
	for i in range(numg):
		wcell = ws.cell(3, 35+i)
		wcell.value = nmf[i]
		
	for i in range(numg):
		wcell = ws.cell(4, 35+i)
		wcell.value = nmp[i]
		
	for i in range(5):
		for j in range(numg):
			wcell = ws.cell(6+i, 35+j)
			wcell.value = bysize[i][j]
	
	
	wcell = ws.cell(13, 10)
	wcell.value = 'Scarf'
	wcell = ws.cell(14, 10)
	wcell.value = avgnmf
	wcell = ws.cell(15, 10)
	wcell.value = avgnmp
	for i in range(5):
		wcell = ws.cell(16+i, 10)
		wcell.value = avgbysize[i]
		
	for i in range(numg):
		wcell = ws.cell(23+i, 10)
		wcell.value = fbyng[i]
	
	for i in range(numg):
		wcell = ws.cell(32+i, 10)
		wcell.value = pbyng[i]
		
	ws=wb["Sheet4"]
	for i in range(numg):
		wcell = ws.cell(19+i, 10)
		wcell.value = fbypref[i]
		
	for i in range(numg):
		wcell = ws.cell(28+i, 10)
		wcell.value = pbypref[i]
		
	wb.save(filename)
		
	
	return 

	
# Helper function 
def stathelper(x, numf, numg, fb2col, FP, famsize):
	# Intialize
	nmf = [0] * numg
	nmp = [0] * numg
	fbyng = [0] * numg
	pbyng = [0] * numg
	fbypref = [0] * numg
	pbypref = [0] * numg
	
	bysize = zeros((5,numg), dtype=int32)
	
	# Compute
	for i in range(len(x)):
		if x[i] >= 1: 
			(f, b) = ind2fb(i, fb2col, numf + numg)
			size = getbundlesize(b)
			fbyng[size-1] += x[i]
			pbyng[size-1] += x[i] * famsize[f]
			
			#print(b)
			#print(bysize)
			for j in range(numg):
				if b[j] >= 1:
					nmf[j] += x[i]
					nmp[j] += x[i] * famsize[f]
					
					bysize[famsize[f]-1][j] += x[i] 
					#print('here')
					##print(j)
					#print(bysize)
					
					fbypref[FP[f][j] - 1] += x[i]
					pbypref[FP[f][j] - 1] += x[i] * famsize[f]
					
	return nmf, nmp, bysize, fbyng, pbyng, fbypref, pbypref
	
# Compute violations
def violations(A, x, b):
	realb = mul(A,x)
	V = [0] * len(b)
	P = [0] * len(b)
	
	for i in range(len(realb)):
		if (realb[i] > b[i]):
			V[i] = realb[i] - b[i]
			P[i] = round(V[i]/b[i] * 100, 1)
	
	print(realb)
	return V, P
	
			
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
	
def mean(x):
	return round(sum(x)/len(x))

	
# Multiply a matrix with a vector
def mul(A, x):
	return [ds.dotproduct(a,x) for a in A]