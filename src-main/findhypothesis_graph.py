from __future__ import division
from pylab import * # https://stsievert.com/blog/2015/09/01/matlab-to-python/
from gspan import gspan
from my_src import *
def findhypothesis_graph(X=None, Y=None, u=None, beta=None, max_col=None, htype=None, **kwargs):
   nargin, nargout = my_arg_reader(X, Y, u, beta, max_col, htype, **kwargs)
   
   
   # Graph boosting stump generator
   #
   # This function is the gateway between the LPBoost algorithm and gSpan.  It
   # generates the decision stumps that correspond to the most violated
   # constraints of the LP.  It does it by using the weighted gSpan subgraph
   # mining.
   #
   # Author: Sebastian Nowozin <sebastian.nowozin@tuebingen.mpg.de>
   # Date: 8th December 2006
   #
   # Input
   #    X: (1,n) cellarray of n graph structures.
   #    Y: (n,1) sample labels (1 or -1).
   #    u: (n,1) sample weights (>= 0).
   #    beta: Minimum required gain.
   #    max_col: Maximum number of constraint violating columns/stumps to produce.
   #    htype: 1 or 2, 1: 1.5-class, outputs [0, 1], 2: 2-class, outputs [-1, 1]
   #
   # Output
   #    h: (1,p), p <= max_col, cellarray of structures with elements
   #       .h: classifier function.
   #       .hi: additional information.
   #       .GY: classifier response, one (n,1) column.
   
   # The maximum number of subgraph patterns to return.
   boostN = 1
   if max_col > 0:
      boostN = max_col
   #end
   
   # subg: (1,p) cellarray of graphs
   # ybase: (1,p) basic response value (normally constant)
   # GY: (n,p) response on the n training patterns
   subg, ybase, GY = gspan (X, 2, array([ 0, 16 ]), Y, u, beta, boostN, 1e6, htype, nargout=3)
   disp(['gSpan returned ', str(len(subg)), ' subgraphs'])
   
   if len(subg) == 0:
      h={}
   else:
      h={}
      for i in range(1, len(subg)+1):
         h[i-1]=matrix([])
         h[i-1].h = lambda G, **kwargs: graph_stump_classifier (G, subg[i-1], ybase[i-1], htype)
         h[i-1].hi = subg[i-1]
         h[i-1].GY = GY[:,i-1]   # subgraph response on training data
         h[i-1].GY[find(h[i-1].GY)]=1
         if htype == 2:
            h[i-1].GY[find(h[i-1].GY == 0)]=-1
            h[i-1].GY = ybase[i-1] @ h[i-1].GY
         #end
         #h[i-1].GY[find(h[i-1].GY)] = count[i-1]   # Convert counts to flags
      #end
   #end
   return h
   
def graph_stump_classifier(G=None, subg=None, ybase=None, htype=None, **kwargs):
   nargin, nargout = my_arg_reader(G, subg, ybase, htype, **kwargs)
   
   
   y=zeros(len(G),1)
   for i in range(1, len(G)+1):
      count = graphmatch (subg, G[i-1], 1, 0)
   
      # Singular classifier with positive outputs, for 1.5-class LPBoosting
      if htype == 1:
         if count > 0:
            y[i-1] = ybase
         else:
            y[i-1] = 0   # Output zero in case pattern wasn't found
         #end
      # Complementary-closed classifier that can return negative outputs for
      # 2-class LPBoosting.
      elif htype == 2:
         if count > 0:
            y[i-1] = ybase
         else:
            y[i-1] = -ybase
         #end
      #end
   #end
   return y
   
   