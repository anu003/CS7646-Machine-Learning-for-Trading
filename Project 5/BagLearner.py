import numpy as np

class BagLearner(object):

    def __init__(self, learner, kwargs={"leaf_size":1},bags=20,boost=False, verbose = False):
        self.learner=learner
        self.learner_list = []
        
        for i in range(0,bags):
            self.learner_list.append(learner(**kwargs))
        self.bags = bags

        # pass # move along, these aren't the drones you're looking for

    def author(self):
        return 'nmenon34' # replace tb34 with your Georgia Tech username

    def addEvidence(self,dataX,dataY):
        """
        @summary: Add training data to learner
        @param dataX: X values of data to add
        @param dataY: the Y training values
        """
	index_list = np.linspace(0,dataX.shape[0]-1,dataX.shape[0])
	index_list = index_list.astype(int)

        for learner in self.learner_list:
		index = np.random.choice(index_list,index_list.size)
            	learner.addEvidence(dataX.take(index,axis=0),dataY.take(index,axis=0))
        
    def query(self,points):
        """
        @summary: Estimate a set of test points given the model we built.
        @param points: should be a numpy array with each row corresponding to a specific query.
        @returns the estimated values according to the saved model.
        """
        q=[]
        for learner in self.learner_list:
            q.append(learner.query(points))
        q_array = np.array(q)
        ans = np.mean(q_array,axis=0)

        return ans.tolist()

if __name__=="__main__":
    print "the secret clue is 'zzyzx'"

