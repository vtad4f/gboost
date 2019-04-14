

def gboost2 (G, Y, nu, conv_epsilon):
   """
      2-class graph based LPBoosting
   """
   print(' '.join(['=== GLPBOOST = BEGIN = 2-class graph based LPBoosting ===']))
   # FIXME: make convergence threshold (0.1) configurable
   classifier, cfun = lpboost (G, Y, conv_epsilon, nu, lambda X, Y, u, beta, max_col: findhypothesis_graph (X, Y, u, beta, max_col, 2), 2)
   print(' '.join(['=== END ===']))
   
   return classifier, cfun
   
   