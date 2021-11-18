import numpy
import gambit
from fractions import Fraction

QUARANTINE = -2
HAPPINESS_1 = 5
HAPPINESS_2 = 10
C = 1

g = gambit.Game.new_table([3,3,3,3,3,3,3,3,3,3])

def utility(player, indexes, theta_profile):
    infectedcount = 0
    utility = float(0)
    for i in range(5):
        if(theta_profile[i]==1 and indexes[player]==indexes[2*i+1]):
            infectedcount+=1
    
    if(indexes[player]==1):
        utility = HAPPINESS_1 - C*infectedcount
    elif(indexes[player]==2):
        utility = HAPPINESS_2 - C*infectedcount
    else:
        print("issue")
        utility = -500
    
    return utility

def increment(indexes, size, actions):
    #reset all indices to zero until the first index that is not at its limit is found
    i = 0
    while (i < size and indexes[i] + 1 >= actions):
        indexes[i] = 0
        i = i+1

    if (i < size):
        indexes[i] = indexes[i]+1
        return True
    else:
        return False

def marginal(player,theta_profile,P):
    pindexes=[0,0,0,0,0]
    prob = float(0)
    i=0
    ptheta = float(0)
    while (True):
        if (pindexes[player]==theta_profile[player]):
            prob+=P[i]
            for j in range(5):
                if not pindexes[j]==theta_profile[j]:
                    break
                elif j==4:
                    ptheta = P[i]
        if not increment(pindexes, 5, 2):
            break
        i+=1
    if(ptheta==float(0)):
        return 0
    else:
        return (ptheta/prob)

m = numpy.array([ [ 0, 0 ], [ 0, 0 ] ], dtype=gambit.Rational)
g1 = gambit.Game.from_arrays(m, numpy.transpose(m))

P=[]
pindexes=[0,0,0,0,0]
while (True):
    prob=float(1)
    for i in range(5):
        if(pindexes[i]==1):
            prob *= 0.2
        else:
            prob *= 0.8
    P.append(prob)
    if not increment(pindexes, 5, 2):
        break

print(P)
indexes=[0,0,0,0,0,0,0,0,0,0]
for profile in g.contingencies:
    for i in range(10):
        if profile[i]==0:
            g[profile][i] = QUARANTINE
        else:
            theta_prof = [0,0,0,0,0]
            while (True):
                if(theta_prof[i/2]==(i%2)):
                    u = marginal(i/2, theta_prof, P)*utility(i, profile, theta_prof)
                    g[profile][i] += Fraction.from_float(u)
                if not increment(theta_prof, 5, 2):
                    break

solver = gambit.nash.ExternalEnumPureSolver()
print(solver.solve(g1))