from __future__ import division
from pylab import * # https://stsievert.com/blog/2015/09/01/matlab-to-python/
from my_src import *
def gboost1d5(G=None, Y=None, nu=None, conv_epsilon=None, **kwargs):
   nargin, nargout = my_arg_reader(G, Y, nu, conv_epsilon, **kwargs)
   classifier, cfun = None, None
   
   
   # 1.5-class graph based LPBoosting
   
   disp(['=== GLPBOOST = BEGIN = 1.5-class graph based LPBoosting ==='])
   # FIXME: make convergence threshold (0.1) configurable
   classifier, cfun = lpboost (G, Y, conv_epsilon, nu, lambda X, Y, u, beta, max_col, **kwargs: findhypothesis_graph (X, Y, u, beta, max_col, 1, **kwargs), 1, nargout=2)
   disp(['=== END ==='])
   return [classifier, cfun][:nargout]
   