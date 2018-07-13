"""
Implementing a Random Tree (RT) learner

@Name : Nidhi Nirmal Menon
@UserID : nmenon34
"""

import pandas as pd
import numpy as np

class RTLearner(object):
    def __init__(self,leaf_size,verbose=False):
        self.leaf_size=leaf_size
        self.verbose=verbose
        self.learner=[]

    def author(self):
        """
        @summary Returning the author user ID
        """
        return 'nmenon34'

    def build_tree(self, data):
        tree=np.array([])
        flag=0
        if(data.shape[0]<=self.leaf_size):
            tree = np.array([['leaf', data[0][-1],'-1','-1']])
            return tree

        X_attr = int(np.random.randint(data.shape[1]-1))

        #if values of Xattribute are the same
        if(np.all(data[:,X_attr] == data[0][X_attr])):
            return np.array([['leaf', np.mean(data[:, -1]), '-1', '-1']])


        data = data[np.argsort(data[:, X_attr])]
        splitVal = np.median(data[0:, X_attr])
        if max(data[:,X_attr])==splitVal:
            return np.array([['leaf', np.mean(data[:, -1]), '-1', '-1']])


	#building left and right sub-trees
        leftTree=self.build_tree(data[data[:,X_attr]<=splitVal])
        rightTree=self.build_tree(data[data[:,X_attr]>splitVal])
        root=[X_attr,splitVal, 1, leftTree.shape[0]+1]
        tree= np.vstack((root,leftTree,rightTree))
        return tree


    def addEvidence(self, Xtrain, Ytrain):
        data=[]
        tree=[]
        data=np.concatenate(([Xtrain,Ytrain[:,None]]),axis=1)
        tree=self.build_tree(data)
        self.learner = np.array(tree)


    def query(self, trainX):
        row=0
        predY=np.array([])
        for data in trainX:
            while(self.learner[row][0]!='leaf'):
                X_attr=self.learner[row][0]
                X_attr = int(float(X_attr))
                if(float(data[X_attr]) <= float(self.learner[row][1])):
                    row=row+int(float(self.learner[row][2]))
                else:
                    row=row+int(float(self.learner[row][3]))
                row=int(float(row))
            if(self.learner[row][0]=='leaf'):
                predY=np.append(predY, float(self.learner[row][1]))
                row=0
        return predY
