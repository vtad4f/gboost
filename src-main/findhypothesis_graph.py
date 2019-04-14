def findhypothesis_graph (X, Y, u, beta, max_col, htype):
   """
      Graph boosting stump generator
      
      This function is the gateway between the LPBoost algorithm and gSpan.  It
      generates the decision stumps that correspond to the most violated
      constraints of the LP.  It does it by using the weighted gSpan subgraph
      mining.
      
      Author: Sebastian Nowozin <sebastian.nowozin@tuebingen.mpg.de>
      Date: 8th December 2006
      
      Input
         X: (1,n) cellarray of n graph structures.
         Y: (n,1) sample labels (1 or -1).
         u: (n,1) sample weights (>= 0).
         beta: Minimum required gain.
         max_col: Maximum number of constraint violating columns/stumps to produce.
         htype: 1 or 2, 1: 1.5-class, outputs {0, 1}, 2: 2-class, outputs {-1, 1}
      
      Output
         h: (1,p), p <= max_col, cellarray of structures with elements
            .h: classifier function.
            .hi: additional information.
            .GY: classifier response, one (n,1) column.
   """
   # The maximum number of subgraph patterns to return.
   boostN = 1
   if max_col > 0:
      boostN = max_col

   # subg: (1,p) cellarray of graphs
   # ybase: (1,p) basic response value (normally constant)
   # GY: (n,p) response on the n training patterns
   subg, ybase, GY = gspan (X, 2, [0 16], Y, u, beta, boostN, 1e6, htype)
   print(' '.join(['gSpan returned ', str(len(subg)), ' subgraphs']))

   if len(subg) == 0:
      h=[]
   else:
      h=[]
      for i in range(1, len(subg) + 1):
         h[i]=[] # TODO - set to struct?
         h[i].h = lambda G: graph_stump_classifier (G, subg[i], ybase[i], htype) # TODO - does i change?
         h[i].hi = subg[i]
         h[i].GY = GY(:,i)	# subgraph response on training data # TODO - slicing?
         h[i].GY(find(h[i].GY))=1
         if htype == 2:
            h[i].GY(find(h[i].GY == 0))=-1
            h[i].GY = ybase[i]*h[i].GY
         #h[i].GY(find(h[i].GY)) = count[i]	# Convert counts to flags
   return h
   
   
   
def graph_stump_classifier (G, subg, ybase, htype):
   """
   """
   y=zeros(len(G),1)
   for i in range(1, len(G) + 1):
      count = graphmatch (subg, G[i], 1, 0)

      # Singular classifier with positive outputs, for 1.5-class LPBoosting
      if htype == 1:
         if count > 0:
            y[i] = ybase
         else:
            y[i] = 0	# Output zero in case pattern wasn't found
      # Complementary-closed classifier that can return negative outputs for
      # 2-class LPBoosting.
      elif htype == 2:
         if count > 0:
            y[i] = ybase
         else:
            y[i] = -ybase
   return y
   
   
   