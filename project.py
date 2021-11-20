import numpy
import gambit
from decimal import *
import sys

#AGT TERM PROJECT CODE#
#Mayank Raj 18CS30028#
#Yarlagadda Srihas 18CS10057#
#Himanshu Choudhary 18CS10023#

#constant definitions
QUARANTINE = -2
HAPPINESS_1 = 5
HAPPINESS_2 = 10
C = 1

#creating the game and the solver instances
g = gambit.Game.new_table([3,3,3,3,3,3,3,3,3,3])
solver = gambit.nash.ExternalEnumPureSolver()


def utility(player, indexes, theta_profile):
    infectedcount = 0
    utility = float(0)
    #find number of infected people playing the same strategy
    for i in range(5):
        if(theta_profile[i]==1 and indexes[player]==indexes[2*i+1]):
            infectedcount+=1
    
    #calculate utility
    if(indexes[player]==1):
        utility = HAPPINESS_1 - C*infectedcount
    elif(indexes[player]==2):
        utility = HAPPINESS_2 - C*infectedcount
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
    pindexes=[]
    for i in range(5):
        pindexes.append(0)
    prob = float(0)
    i=0
    ptheta = float(0)
    #calculate the probability of other players types given type of player
    while (True):
        if (pindexes[player]==theta_profile[player]):
            #all cases where 'player' has given type
            prob+=P[i]
            for j in range(5):
                if not pindexes[j]==theta_profile[j]:
                    #mismatch at some type
                    break
                elif j==4:
                    #probability of type profile = theta_profile
                    ptheta = P[i]
        if not increment(pindexes, 5, 2):
            break
        i+=1
    #return the marginal probability
    if(ptheta==float(0)):
        return 0
    else:
        return (ptheta/prob)

#calculate the prior probability distribution
P=[]
pindexes=[]
pinf=[0.1, 0.1, 0.1, 0.1, 0.1]
for i in range(5):
    pindexes.append(0)
while (True):
    prob=float(1)
    #find the joint probability of each player having the given type
    for i in range(5):
        if(pindexes[i]==1):
            prob *= pinf[i]
        else:
            prob *= 1-pinf[i]
    P.append(prob)
    if not increment(pindexes, 5, 2):
        break

#update the utilities for each player and strategy
for profile in g.contingencies:
    for i in range(10):
        payoff = Decimal(0)
        g[profile][i] = Decimal(0)
        #payoff of quarantine
        if profile[i]==0:
            g[profile][i] = QUARANTINE
        else:
            theta_prof = []
            for i in range(5):
                theta_prof.append(0)
            while (True):
                #add a term to the selten game utility
                if(theta_prof[i/2]==(i%2)):
                    u = marginal(i/2, theta_prof, P)*utility(i, profile, theta_prof)
                    payoff = payoff + Decimal(u)
                if not increment(theta_prof, 5, 2):
                    break
        g[profile][i] = payoff

print(solver.solve(g))
