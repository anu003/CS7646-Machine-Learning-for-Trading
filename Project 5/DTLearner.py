import numpy as np

class DTLearner(object):

    def __init__(self, leaf_size=1, verbose=False):
        #pass # move along, these aren't the drones you're looking for
	self.tree=None
	self.leaf_size=leaf_size

    def author(self):
        return 'nmenon34' # replace tb34 with your Georgia Tech username

    def addEvidence(self,dataX,dataY):
        """
        @summary: Add training data to learner
        @param dataX: X values of data to add
        @param dataY: the Y training values
        """
        ## slap on 1s column so linear regression finds a constant term
        #newdataX = np.ones([dataX.shape[0],dataX.shape[1]+1])
        #newdataX[:,0:dataX.shape[1]]=dataX

        ## build and save the model
        #self.model_coefs, residuals, rank, s = np.linalg.lstsq(newdataX, dataY)

	dataY=np.array([dataY])
	new_dataY=dataY.T	#transpose of dataY
	all_data=np.append(dataX,new_dataY,axis=1)
	self.tree=self.build_tree(all_data)

    def build_tree(self,data):
	if data.shape[0]<=self.leaf_size:	#if no.of nodes left < leaf-size, all are leaf nodes. hence, return mean
		return np.array([["Leaf",np.mean(data[:,-1]),-1,-1]])

	if np.all(data[0,-1]==data[:,-1],axis=0):	#if all values in dataY are same
		return np.array([["Leaf",data[0,-1],-1,-1]])
        else:
		feature=int(self.best_feature(data))
		Split_Val=np.median(data[:,feature])	#median of all values in column of best feature

		Max=max(data[:,feature])
		if Max==Split_Val:
			return np.array([['Leaf',np.mean(data[:,-1]),-1,-1]])	#empty right sub-tree. Only left sub-tree formed

		Left_Tree=self.build_tree(data[data[:,feature]<=Split_Val])	#lesser values form left sub-tree
            	Right_Tree=self.build_tree(data[data[:,feature]>Split_Val])	#larger values form right sub-tree

		root = np.array([[feature,Split_Val,1,Left_Tree.shape[0]+1]])
		temp = np.append(root,Left_Tree,axis=0)
		return np.append(temp,Right_Tree,axis=0)

    def best_feature(self,data):
	#returns index of selected feature column
	
	Max_val=0
        best_feature=0

	dataX=data.shape[1]-1	#extract dataX
        dataY=data[:,data.shape[1]-1]	#extract dataY

	temp=[]
        for feature in range(0,dataX):
            correlation_val = np.corrcoef(data[:,feature],dataY)
            correlation_val = abs(correlation_val[0,1])
            temp.append(correlation_val)
            
        for i in range(0,len(temp)):
            if temp[i]>Max_val:
                Max_val = temp[i]
                best_feature = i
        best_feature = int(best_feature)
       
        return int(best_feature)

    def query(self,points):
        """
        @summary: Estimate a set of test points given the model we built.
        @param points: should be a numpy array with each row corresponding to a specific query.
        @returns the estimated values according to the saved model.
        """
	#return (self.model_coefs[:-1] * points).sum(axis = 1) + self.model_coefs[-1]

	ans=[]
	row_count=points.shape[0]	#[0] returns rows, [1] returns columns
	for row in range(0,row_count):
		value=self.query_tree(points[row,:])	#pass the current row to query_tree() to determine corresponding value
		ans.append(float(value))
	return ans

    def query_tree(self, my_tuple):
	row=0

	#if not a leaf node
	while(self.tree[row,0]!='Leaf'):
		feature=self.tree[row,0]
		Split_Val=self.tree[row,1]
		
		if my_tuple[int(float(feature))]<=float(Split_Val):
			row=row+int(float(self.tree[row,2]))	#Left_Tree
		else:
			row=row+int(float(self.tree[row,3]))	#Right_Tree

	#if a leaf node
	return self.tree[row,1]

if __name__=="__main__":
    print "the secret clue is 'zzyzx'"

