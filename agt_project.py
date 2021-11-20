import numpy
import gambit
from decimal import *
import sys

#AGT TERM PROJECT CODE#
#Mayank Raj 18CS30028#
#Yarlagadda Srihas 18CS10057#
#Himanshu Choudhary 18CS10023#

#constant definitions
QUARANTINE = -1
HAPPINESS_1 = 1
HAPPINESS_2 = 2
C = 1

#array of p_i values
pinf=[]

n = int(input("Enter the number of players (students): "))

print("Enter the value of p_i (probability of being infected) for each player, separated by newline:")
for reader in range(n):
    v = input()
    pinf.append(v)
    
print(pinf)
tab = []
for tabcreate in range(2*n):
    tab.append(3)
#creating the game and the solver instances
g = gambit.Game.new_table(tab)


def utility(player, indexes, theta_profile):
    infectedcount = 0
    utility = float(0)
    #find number of infected people playing the same strategy
    for i in range(n):
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
    for i in range(n):
        pindexes.append(0)
    prob = float(0)
    i=0
    ptheta = float(0)
    #calculate the probability of other players types given type of player
    while (True):
        if (pindexes[player]==theta_profile[player]):
            #all cases where 'player' has given type
            prob+=P[i]
            for j in range(n):
                if not pindexes[j]==theta_profile[j]:
                    #mismatch at some type
                    break
                elif j==n-1:
                    #probability of type profile = theta_profile
                    ptheta = P[i]
        if not increment(pindexes, n, 2):
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
for pos in range(n):
    pindexes.append(0)
while (True):
    prob=float(1)
    #find the joint probability of each player having the given type
    for i in range(n):
        if(pindexes[i]==1):
            prob *= pinf[i]
        else:
            prob *= 1-pinf[i]
    P.append(prob)
    if not increment(pindexes, n, 2):
        break

#update the utilities for each player and strategy
for profile in g.contingencies:
    for i in range(2*n):
        payoff = Decimal(0)
        g[profile][i] = Decimal(0)
        #payoff of quarantine
        if profile[i]==0:
            g[profile][i] = QUARANTINE
        else:
            theta_prof = []
            for tet in range(n):
                theta_prof.append(0)
            while (True):
                #add a term to the selten game utility
                if(theta_prof[i/2]==(i%2)):
                    u = marginal(i/2, theta_prof, P)*utility(i, profile, theta_prof)
                    payoff = payoff + Decimal(u)
                if not increment(theta_prof, n, 2):
                    break
            g[profile][i] = payoff

solver = gambit.nash.ExternalEnumPureSolver()
original_stdout = sys.stdout
with open('psnes.txt', 'w') as f:
    sys.stdout = f # Change the standard output to the output file.
    #solve for PSNEs
    print(solver.solve(g))    
    sys.stdout = original_stdout # Reset the standard output to its original value