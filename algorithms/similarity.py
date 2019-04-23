# Authors: Kyungchan "Will" Koh & Spencer Chang
# Rice University COMP 580
# Final Project
#
# This file contains similarity functions that could be
# used for ACE.

import math
import numpy as np
import pandas as pd

class HashFunc():
  def SRP(x, y):
    '''
    Given two vectors, computes the SRP using cosine similarity.

    The equation is (in latex): $1 - \\frac{\\theta}{\\pi}$, where
    $\\theta = cos^{-1}\\left(\\frac{x^Ty}{||x||_2||y||_2}\\right)$

      @param x  First vector of numbers.
      @param y  Second vector of numbers.
      @returns  The SRP of x and y.
    '''
    numerator = np.dot(x, y)
    denominator = np.linalg.norm(x) * np.linalg.norm(y)
    return 1 - math.acos(numerator / denominator) / math.pi

  def some_hash_func(key, j):
    '''
    Temporary placeholder for a hash function.

    @param key  A row in a pandas dataframe.
    @param j    The jth hash function to be used.
    '''
    pass