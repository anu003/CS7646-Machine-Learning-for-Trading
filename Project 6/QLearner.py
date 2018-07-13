"""
Template for implementing QLearner  (c) 2015 Tucker Balch
"""

import numpy as np
import random as rand

class QLearner(object):

    def author(self):
	return 'nmenon34'

    def __init__(self, \
        num_states=100, \
        num_actions = 4, \
        alpha = 0.2, \
        gamma = 0.9, \
        rar = 0.5, \
        radr = 0.99, \
        dyna = 0, \
        verbose = False):

        self.num_states = num_states
        self.num_actions = num_actions
        self.alpha = alpha
        self.gamma = gamma
        self.rar = rar
        self.radr = radr
        self.dyna = dyna
        self.verbose = verbose
        self.s = 0
        self.a = 0
        self.exp_tuple = []
        self.Q = np.random.uniform(-1.0, 1.0, [num_states,num_actions])

    def querysetstate(self, s):
        """
        @summary: Update the state without updating the Q-table
        @param s: The new state
        @returns: The selected action
        """
        self.s = s
        self.a = action = np.argmax(self.Q[s])
        if self.verbose: print "s =", s,"a =",action
        return action

    def query(self,s_prime,r):
        """
        @summary: Update the Q table and return an action
        @param s_prime: The new state
        @param r: The new reward
        @returns: The selected action
        """
        
        #update Q-table
        self.update_Q(self.s, self.a, s_prime, r)

        #update experience tuple
        self.exp_tuple.append((self.s, self.a, s_prime, r))

        #dyna
	if self.dyna>0:
            self.execute_dyna()

	prob = rand.uniform(0.0, 1.0)
        if prob < self.rar:
            action = rand.randint(0, self.num_actions - 1)
        else:
            action = np.argmax(self.Q[s_prime])
        self.rar *= self.radr
        if self.verbose: print "s =", s_prime,"a =", action,"r =",r
        self.s = s_prime
        self.a = action
        return action

    def update_Q(self, s, a, s_prime, r):
        self.Q[s, a] = (1-self.alpha)*self.Q[s,a]+self.alpha*(r+self.gamma*self.Q[s_prime, np.argmax(self.Q[s_prime])])

    def execute_dyna(self):
        exp_tuple_len = len(self.exp_tuple)
        random_tuple = np.random.randint(exp_tuple_len, size=self.dyna)
        for i in range(0, self.dyna):
            temp_tuple = self.exp_tuple[random_tuple[i]]
            rand_s = temp_tuple[0]
            rand_a = temp_tuple[1]
            rand_s_prime = temp_tuple[2]
            r = temp_tuple[3]
            self.update_Q(rand_s, rand_a, rand_s_prime, r)

if __name__=="__main__":
    print "Remember Q from Star Trek? Well, this isn't him"

