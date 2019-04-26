# Authors: Kyungchan "Will" Koh & Spencer Chang
# Rice University COMP 580
# Final Project
#
# This file contains an implementation of Array of (Locally Sensitive)
# Count Estimations (ACE). 
#
# The data structure is described in: https://arxiv.org/pdf/1706.06664.pdf

from array import array
import pandas as pd
from .similarity import HashFunc

class ACE():
  # Class representation of ACE.

  def __init__(self, K, L, alpha):
    self.K = K
    self.L = L
    self.alpha = alpha
    self.arrays = [array('h') for j in range(self.L)]  # 'h' for signed shorts. 'H' for unsigned shorts.
    for j in range(self.L):
      for _ in range(2 ** K):
        self.arrays[j].append(0)
    self.mu = 0
    self.n = 0

  def preprocess(self, D):
    '''
    Preprocesses a dataset into ACE.

    @param D  The dataset represented using a pandas dataframe.
    '''
    for idx, row in D.iterrows():
      mu_incre = 0
      for j in range(self.L):
        hash_val = HashFunc.hash_tweet(row, j)
        self.arrays[j][hash_val] += 1
        mu_incre += ((2 * self.arrays[j][hash_val] + 1) / (self.L * 1.0))
      self.mu = ((self.n * self.mu) + mu_incre) / ((self.n + 1) * 1.0)
      self.n += 1

  def query(self, q):
    '''
    Queries ACE for anomaly detection.

    @param q  The query item represented as a row in the dataframe.
    @returns  True if q is an anomaly. False otherwise.
    '''
    score = 0
    for j in range(self.L):
      hash_val = HashFunc.hash_tweet(q, j)
      score += ((self.arrays[j][hash_val]) / (self.L * 1.0))

    return (score <= (self.mu - self.alpha))
