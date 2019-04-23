@mfunction("classifier, cfun")
def gboost1d5(G=None, Y=None, nu=None, conv_epsilon=None):
    
    # 1.5-class graph based LPBoosting
    
    disp(mcat([mstring('=== GLPBOOST = BEGIN = 1.5-class graph based LPBoosting ===')]))
    # FIXME: make convergence threshold (0.1) configurable
    [classifier, cfun] = lpboost(G, Y, conv_epsilon, nu, lambda X, Y, u, beta, max_col: findhypothesis_graph(X, Y, u, beta, max_col, 1), 1)
    disp(mcat([mstring('=== END ===')]))
    
    

