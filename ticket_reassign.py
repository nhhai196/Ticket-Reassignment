import sys
import datastructure
import csv

#argv[1]: csv file name in the following format
#row 1: number of families, number of games
#row f+1: budget, then decreasing preference order over bundles, of family f
#row #family + 2: capacity of each game
#TODO: the bundles will be stored in a dictionary: bundle -> rank
#the quantity in the bundle is the alpha (unscaled)
#argv[2]: epsilon for price

bundle2rank = [] #bundle maps to the rank, each family has one dictionary

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
                elif item_count > 0:
                    if item.strip(): #filter empty string
                        intlist = [int(float(i)) for i in item.split(',')] #convert string to int
                        bundle2rank[line_count-1][tuple(intlist)] = item_count #bundle2rank[f-1] maps from a tuple bundle to rank for family f
                        item_count += 1
            print(bundle2rank[line_count-1])
            line_count += 1
        else:
            capacity = [int(float(i)) for i in row if i.strip()] #capacity[g-1] is the capacity of game g
            print(capacity)

#now we have bundle2rank, capacity, and budget

#create slack columns/Contracts
clist = [] #contract list
for i in range(numF):
    clist.append((-1*(i+1),[],[]))

for i in range(numG):
    clist.append((-1*(i+1+numF),[],[]))

print(clist)
