"""
template for generating data to fool learners (c) 2016 Tucker Balch
"""

import numpy as np
import math

# this function should return a dataset (X and Y) that will work
# better for linear regression than decision trees
def best4LinReg(seed=1489683273):
    np.random.seed(seed)
    #X = np.zeros((100,2))
    #Y = np.random.random(size = (100,))*200-100
    # Here's is an example of creating a Y from randomly generated
    # X with multiple columns
    #Y = X[:,0] + np.sin(X[:,1]) + X[:,2]**2 + X[:,3]**3
    #rows=np.random.randint(10,1001)
    #cols=np.random.randint(2,1001)
    rows=50
    cols=10
    X=np.zeros((rows,cols))
    X=np.random.random((rows, cols))
    #X[0,0]=np.random.randint(1,10)
    #for c in range(1,cols):
	#X[0,c]=X[0,c-1]+1
    #for r in range(1,rows):
	#X[r,0]=X[r-1,0]+1
    #for a in range(1,rows):
	#for b in range(1,cols):
	    #X[a,b]=X[a-1,b-1]+1
    Y=np.zeros(rows)
    for i in range(0,rows):
        Y[i]=X[i,:].sum()
    return X, Y

def best4DT(seed=1489683273):
    np.random.seed(seed)
    #X = np.zeros((100,2))
    #Y = np.random.random(size = (100,))*200-100
    #rows=np.random.randint(10,1001)
    #cols=np.random.randint(2,1001)
    rows=100
    cols=10
    #X=np.zeros((rows,cols))
    X=np.random.random_integers(0,1000000,(rows, cols))
    #X=np.random.random((rows, cols))
    
    #new=np.zeros(rows)
    #X[0,0]=np.random.randint(1,5)
    #for c in range(1,cols):
	#X[0,c]=X[0,c-1]+1
    #for r in range(1,rows):
	#X[r,0]=X[r-1,0]**2
    #for a in range(1,rows):
	#for b in range(1,cols):
	    #X[a,b]=X[a-1,b-1]**2
    Y=np.zeros(rows)
    #for i in range(0,rows):
        #new[i]=X[i,:].sum()
	#med=np.median(new)
	#if new[i]<med:
	    #Y[i]=1
	#else:
	    #Y[i]=100
    for i in range(0,rows):
	if X[i,1] < 1.5:
	    Y[i]=0
	else:
	    Y[i]=1
    return X, Y

def author():
    return 'nmenon34' #Change this to your user ID

if __name__=="__main__":
    print "they call me Tim."
