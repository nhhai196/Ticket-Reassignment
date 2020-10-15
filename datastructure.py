
import collections

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