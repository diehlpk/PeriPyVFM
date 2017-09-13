import csv
import numpy as np
from peripydic import *
import random
from scipy.optimize import minimize, fmin_cobyla
import sys

def readVirtualField(filename):

    data = []
    with open(filename, 'rb') as csvfile:
            csvreader = csv.reader(csvfile, delimiter=',')
            next(csvreader, None)
            for row in csvreader:
                data.append(np.array(map(float, row)))

    u = np.zeros((len(data), 2))

    for i in range(0, len(data)):
        u[i][0] = data[i][4] 
        u[i][1] = data[i][5] 

    return u


def writeParaview(deck, problem):
    ccm = IO.ccm.CCM_calcul(deck,problem)
    deck.vtk_writer.write_data(deck, problem, ccm)


def res(Wint_vf1,Wint_vf2):
     Wext_vf1 = 3750.
     Wext_vf2 = -140625.
     Wint_vf1 += 323.58134265
     Wint_vf2 += -17720.35699
     return np.sqrt((Wint_vf1+Wext_vf1)**2 + (Wint_vf2+Wext_vf2)**2) / np.sqrt(Wext_vf1**2 + Wext_vf2**2)


def residual(P, deck):

    deck.bulk_modulus = P[0]
    deck.shear_modulus = P[1]

    problem = DIC_problem(deck)
    Wint_vf1 = 0.
    Wint_vf2 = 0.
 
    for i in range(0, len(deck.geometry.nodes)):
	
        # Internal virtual work from PD internal forces and virtual field #1
        Wint_vf1 += np.dot(problem.force_int[i,:,1] , u1[i]) * deck.geometry.volumes[i]  
        
        # Internal virtual work from PD internal forces and virtual field #2
        Wint_vf2 += np.dot(problem.force_int[i,:,1] , u2[i]) * deck.geometry.volumes[i] 

    if deck.vtk_writer.vtk_enabled == True:
        writeParaview(deck,problem)
    
    print "K =", deck.bulk_modulus, "G =", deck.shear_modulus
    print res(Wint_vf1,Wint_vf2)
    #sys.exit()
    return res(Wint_vf1,Wint_vf2)
    
    
    
## MINIMIZATION

# Virtual fields read in CSV files
u1 = readVirtualField("./csv/mesh_vf2.csv")
u2 = readVirtualField("./csv/mesh_vf3.csv")

# Deck to define PD parameters
deck = DIC_deck("./input_elas_2D.yaml")

# Domain of definition to look for the material properties
bnds=((0.1,10000),(0.1,10000))   

# Initial value for the minimization
#p = np.array((random.uniform(0.1, 10.) * 1000., random.uniform(0.1, 10.) * 1000.), dtype=float)
<<<<<<< HEAD
#p = np.array([3333.3333,1538.4615])
p = np.array([3500,2000])
=======
#p = np.array([3333.33333,1538.46154])
p = 1.05 * np.array([3333.33333,1538.46154])
>>>>>>> 428f30c595322d688d5e3ade7a7a2766f454cd38

# Minimization process
res = minimize(residual, p, args=(deck), method='COBYLA', tol=1e-8,
                   options={'rhobeg': 1.,'disp': True })
 
#res = minimize(residual, p, args=(deck), method='L-BFGS-B', bounds=bnds)

print res.x