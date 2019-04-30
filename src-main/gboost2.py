from __future__ import division
from pylab import * # https://stsievert.com/blog/2015/09/01/matlab-to-python/
from lpboost import lpboost
from findhypothesis_graph import findhypothesis_graph
from my_src import *
def gboost2(G=None, Y=None, nu=None, conv_epsilon=None, **kwargs):
   nargin, nargout = my_arg_reader(G, Y, nu, conv_epsilon, **kwargs)
   classifier, cfun = None, None
   
   
   # 2-class graph based LPBoosting
   
   disp(['=== GLPBOOST = BEGIN = 2-class graph based LPBoosting ==='])
   # FIXME: make convergence threshold (0.1) configurable
   classifier, cfun = lpboost (G, Y, conv_epsilon, nu, lambda X, Y, u, beta, max_col, **kwargs: findhypothesis_graph (X, Y, u, beta, max_col, 2, **kwargs), 2, nargout=2)
   disp(['=== END ==='])
   return [classifier, cfun][:nargout]
   
   