import numpy as np
import DTLearner as dt
import RTLearner as rt
import BagLearner as bg
import LinRegLearner as lrl

class InsaneLearner(object):

    def __init__(self,verbose = False):
        
        self.learner_list=[]
        for i in range(0,20):
            self.learner_list.append(bg.BagLearner(lrl.LinRegLearner,kwargs={},bags=20))
        #pass # move along, these aren't the drones you're looking for

    def author(self):
        return 'nmenon34' # replace tb34 with your Georgia Tech username

    def addEvidence(self,dataX,dataY):
        """
        @summary: Add training data to learner
        @param dataX: X values of data to add
        @param dataY: the Y training values
        """
        for learner in self.learner_list:
            learner.addEvidence(dataX,dataY)
        
    def query(self,points):
        """
        @summary: Estimate a set of test points given the model we built.
        @param points: should be a numpy array with each row corresponding to a specific query.
        @returns the estimated values according to the saved model.
        """
        q=[]
        for lr in self.learner_list:
            q.append(lr.query(points))
        q_array = np.array(q)
        ans = np.mean(q_array,axis=0)

        return ans.tolist()

if __name__=="__main__":
    print "the secret clue is 'zzyzx'"

