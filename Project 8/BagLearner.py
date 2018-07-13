"""
Implementing a Bag learner

@Name : Nidhi Nirmal Menon
@UserID : nmenon34
"""

import numpy as np
from random import randint
from scipy import stats

class BagLearner(object):

    def __init__(self, learner, kwargs = {"leaf_size":1}, bags = 20, boost = False, verbose = False):

        self.learner = learner
        self.learner_list = []
        for i in range(0,bags):
            self.learner_list.append(learner(**kwargs))
        self.bags = bags
        pass

    def author(self):
        """
        @summary Returning the author user ID
        """
        return 'nmenon34'


    def addEvidence(self, dataX, dataY):
        """
        @summary Adding the training data
        """
        train_rows = int(0.6* dataX.shape[0])
        for learner in self.learner_list:
            newX =[]
            newY =[]
            for i in range(0,train_rows):
                index = randint(0,dataX.shape[0]-1)
                tempX = dataX[index,:]
                tempY = dataY[index]
                newX.append(tempX)
                newY.append(tempY)

            learner.addEvidence(np.array(newX),np.array(newY))


    def query(self, points):
        """
        @summary: Estimate a set of test points given the model we built
        """
        temp=[]

        for learner in self.learner_list:
            temp.append(learner.query(points))

        temp_array = np.array(temp)
        res = stats.mode(temp_array)		#changing from regression to classification!
        #res = np.mean(temp_array,axis=0)
        #return res.tolist()
        return res[0][0]


if __name__ == "__main__":
    print "Bag learner"
