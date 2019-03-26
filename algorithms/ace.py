# Authors: Kyungchan "Will" Koh & Spencer Chang
# Rice University COMP 580
# Final Project
#
# This file contains an implementation of Array of (Locally Sensitive)
# Count Estimations (ACE). 
#
# The data structure is described in: https://arxiv.org/pdf/1706.06664.pdf

import similarity

class ACE():
  # Class representation of ACE.

  def __init__(self, K, L):
    self.K = K
    self.L = L
    self.arrays = [[0 for i in range(2 ** K)] for i in range(L)]

  def preprocess(self, D):
    '''
    Preprocesses a dataset into ACE.

    @param D  The dataset.
    '''
    pass

  def query(self, q):
    '''
    Queries ACE for anomaly detection.

    @param q  The query.
    '''
    pass

  def insert(self, x):
    '''
    Inserts a new element into ACE.

    @param x  The new element.
    '''
