from __future__ import division
from pylab import * # https://stsievert.com/blog/2015/09/01/matlab-to-python/
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../ompc/examples/mex'))
#import mex
#mexgspan = mex.mexFunc('gspan') # TODO - there seems to be a seg fault
from my_src import *
def gspan(G=None, minsup=None, size_req=None, boostY=None, boostWeights=None, boostTau=None, boostN=None, boostMax=None, boostType=None, **kwargs):
   nargin, nargout = my_arg_reader(G, minsup, size_req, boostY, boostWeights, boostTau, boostN, boostMax, boostType, **kwargs)
   subg, count, GY = None, None, None
   return array([]), array([]), array([]) # TODO - load mex gspan dll
   
   # gSpan frequent graph substructure algorithm.
   #   and
   # gSpan based graph boosting.
   #
   # (This is a Matlab wrapper around the modified gspan implementation of Taku
   #  Kudo.)
   #
   # Author: Sebastian Nowozin <sebastian.nowozin@tuebingen.mpg.de>
   # Date: 15th November 2006
   #
   # Find all subgraphs in the set of graphs G that appear at least minsup times.
   #
   # Note: For graph boosting, this function should normally not be used
   #    directly, but through the gboost1d5 or gboost2 functions.
   #
   ###
   # Input
   #   G: (1,n) cellarray of n graph structures with this layout
   #     g.nodelabels: (n,1) discrete integer labels [L_1  L_2   L_n]
   #     g.edges: (m,2) edges, array([ from, to ]) at each line:
   #       [e_1_[from-1] e_1_[to-1] edgelabel_1   e_m_[from-1] e_m_[to-1] edgelabel_m]
   #       The node indices go from 1 to n.  (They will be converted to 0-(n-1)
   #       internally and converted back.)
   #
   #   minsup: The minimum number of times a frequent pattern has to appear in G.
   #
   #   (optional) size_req: Either [] for no limit, or (1,2) real col-vector
   #      array([ min_node_count, max_node_count ]), which limits the returned graphs to
   #      have a number of nodes p, such that
   #         min_node_count <= p <= max_node_count.
   #      If max_node_count < min_node_count, only the lower bound is used.
   #      (default: array([ 0, 0 ]))
   #
   # For graph boosting:
   #   boostY: (n,1) array of labels in [-1, 1].
   #
   #   boostWeights: (n,1) array of reals in array([[ 0 ],[ 1 ]]).
   #
   #   boostTau: tau parameter (normally set to 0).  This is the start gain it
   #      has to beat.
   #
   #   boostN: integer > 0.  From the best patterns, only the best boostN patterns
   #      are returned.
   #
   #   boostMax: The maximum number of exploration steps to take or zero for
   #      infinity (1e6 is a good choice here).
   #
   #   boostType: 1 for 1.5-class weak learners with outputs [0, 1], 2 for
   #      2-class weak learners with outputs [-1, 1].
   #
   ###
   # Output
   #   subg: (1,p) cellarray of p graph structures that appear frequently in G.
   #
   #   (optional) count: (1,p) uint32 array giving at element i the number of times
   #     graphs[i-1] appears in G (duplicates within one graph only counted once).
   #
   #   (in case of graph boosting count is)
   #   count: (1,p) cellarray of [ -1, 1 ], giving the classifiers h_[<subg>,<subgY>].
   #
   #   (optional) GY: (n,p) double array giving individual counts for each
   #       subgraph/graph pair.  At (i,j) the number of counts of the j'th
   #       subgraph found in the i'th graph is recorded.  This takes no
   #       additional computation time to record.
   #
   
   if nargin < 2 or nargin > 10 or nargout > 3:
      raise Exception(['Invalid number of input or output parameters.'])
   #end
   
   d_size_req = array([ 0, 0 ])
   if nargin >= 3:
      if my_isempty(size_req):
         size_req = array([ 0, 0 ])
      #end
   
      if my_size(size_req,1) != 1 or my_size(size_req,2) != 2:
         raise Exception(['size_req parameter invalid.'])
      #end
      d_size_req = size_req
   #end
   
   for i in range(1, len(G)+1):
      v, r = verifygraph (G[i-1], nargout=2)
      if v != 1:
         raise Exception(['Graph ', str(i), ': ', r])
      #end
   #end
   if my_size(G,2) == 1:
      G=G.T   # put it as row.
   #end
   
   if nargin > 3:
      disp(['Starting gspan-boost run '])
      if boostTau < 0.0:
         boostTau = 0.0
      #end
   
      if nargout == 3:
         subg, count, GY = mexgspan (G, minsup, d_size_req, 0, boostY, boostWeights, boostTau, boostN, boostMax, boostType, nargout=3)
      elif nargout == 2:
         subg, count = mexgspan (G, minsup, d_size_req, 0, boostY, boostWeights, boostTau, boostN, boostMax, boostType, nargout=2)
      elif nargout == 1:
         subg = mexgspan (G, minsup, d_size_req, 0, boostY, boostWeights, boostTau, boostN, boostMax, boostType, nargout=1)
      #end
   else:
      disp(['Starting normal gspan run '])
      if nargout == 3:
         subg, count, GY = mexgspan (G, minsup, d_size_req, 0, nargout=3)
      elif nargout == 2:
         subg, count = mexgspan (G, minsup, d_size_req, 0, nargout=2)
      elif nargout == 1:
         subg = mexgspan (G, minsup, d_size_req, 0, nargout=1)
      #end
   #end
   
   # Filter out duplicates (this is due to undirected edges)
   for i in range(1, len(subg)+1):
      subg[i-1].edges = unique (subg[i-1].edges, 'rows')
   #end
   return [subg, count, GY][:nargout]
   
def verifygraph(G=None, **kwargs):
   nargin, nargout = my_arg_reader(G, **kwargs)
   valid, reason = None, None
   return True, 'Graph is ok.' # TODO - Python equivalent of nodelabels and edges?
   
   # Verify if the directed graph G is valid, that is::
   #
   # 1. Does not contain any self-referential or duplicate edges.
   # 2. Uses proper indices.
   
   nodes = my_size(G.nodelabels,1)
   
   # Check for indices
   if my_size(G.edges, 1) > 0:
      I = find (G.edges[:,1-1] <= 0 | G.edges[:,1-1] > nodes | G.edges[:,2-1] <= 0 | G.edges[:,2-1] > nodes)
      if len(I) != 0:
         valid = 0
         if nargout >= 2:
            reason = array([ 'Edge indices not within 1-', str(nodes), '.' ])
         #end
         return
      #end
   
      # Check for self referential edges (self-loops)
      I = find (G.edges[:,1-1] == G.edges[:,2-1])
      if len(I) != 0:
         valid = 0
         if nargout >= 2:
            reason = array([ 'Graph has ', str(len(I)), ' self-loops.' ])
         #end
         return
      #end
   #end
   
   # Check for duplicate edges
   # DISABLED as both our gspan modification as well as mexrelabel support
   #    multiple edge attributes
   # TODO
   if False:
      E = G.edges[:,(1-1):(2-1)]
      Eu = unique(E,'rows')
      if my_size(E,1) != my_size(Eu,1):
         valid = 0
         if nargout >= 2:
            reason = array([ 'There are ', str(my_size(E,1)-my_size(Eu,1)), ' duplicate edges.' ])
         #end
         return
      #end
   #end
   
   if nargout >= 2:
      reason = 'Graph is ok.'
   #end
   valid = 1
   return [valid, reason][:nargout]
   