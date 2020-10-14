import sys
import datastructure

#argv[1]: number of families
#argv[2]: number of games
#argv[3]: row f denotes the preference list of family f (to be done)

numG = int(float(sys.argv[2]))
numF = int(float(sys.argv[1]))

#create slack columns/Contracts
clist = [] #contract list
for i in range(numF):
    clist.append((-1*(i+1),[],[]))

for i in range(numG):
    clist.append((-1*(i+1+numF),[],[]))

print(clist)
