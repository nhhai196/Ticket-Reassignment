import csv
import sys
import random

#argv[1]: filename
#argv[2]: #families
#argv[3]: #games
#argv[4]: lower bound for family size/budget
#argv[5]: upper bound for family size/budget
#argv[6]: lower bound length of each family's preference list
#argv[7]: upper bound length of each family's preference list
#argv[8]: increase for the alpha function, for example, if it is 2,
#then each entry of each bundle will assign 2 extra seats
#argv[9]: capacity

flb = int(float(sys.argv[4]))
fub = int(float(sys.argv[5]))
llb = int(float(sys.argv[6]))
lub = int(float(sys.argv[7]))

with open(sys.argv[1], 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    numf = int(float(sys.argv[2]))
    numg = int(float(sys.argv[3]))
    inc = int(float(sys.argv[8]))
    csvwriter.writerow([numf,numg])
    for f in range(numf):
        fsize = random.randint(flb,fub)
        n = random.randint(llb,lub)
        row = [fsize]
        i = 0
        #n = min(m,pow(2,fsize)-1)
        while i < n:
            bundle = []
            next = 0
            for j in range(numg):
                numseats = random.randint(0,fsize)
                if numseats>0:
                    numseats = numseats+inc
                bundle.append(numseats)
            for item in row:
                if item==",".join(map(str, bundle)) or all([v==0 for v in bundle]):
                    next=1
                    break
            if next==1:
                continue
            i = i+1
            row.append(",".join(map(str, bundle)))
        csvwriter.writerow(row)
    cap = [int(float(sys.argv[9]))] * numg
    csvwriter.writerow(cap)
