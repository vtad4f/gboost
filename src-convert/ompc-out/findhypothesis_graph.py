@mfunction("h")
def findhypothesis_graph(X=None, Y=None, u=None, beta=None, max_col=None, htype=None):
    
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
    #    htype: 1 or 2, 1: 1.5-class, outputs {0, 1}, 2: 2-class, outputs {-1, 1}
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
        end    
        
        # subg: (1,p) cellarray of graphs
        # ybase: (1,p) basic response value (normally constant)
        # GY: (n,p) response on the n training patterns
        [subg, ybase, GY] = gspan(X, 2, mcat([0, 16]), Y, u, beta, boostN, 1e6, htype)    
        disp(mcat([mstring('gSpan returned '), num2str(length(subg)), mstring(' subgraphs')]))    
        
        if length(subg) == 0:        
            h = mcellarray([])        
        else:        
            h = mcellarray([])        
            for i in mslice[1:length(subg)]:            
                h(i).lvalue = mcat([])            
                h(i).h.lvalue = lambda G: graph_stump_classifier(G, subg(i), ybase(i), htype)            
                h(i).hi.lvalue = subg(i)            
                h(i).GY.lvalue = GY(mslice[:], i)            # subgraph response on training data
                h(i).GY(find(h(i).GY)).lvalue = 1            
                if htype == 2:                
                    h(i).GY(find(h(i).GY == 0)).lvalue = -1                
                    h(i).GY.lvalue = ybase(i) * h(i).GY                
                    end                
                    #h{i}.GY(find(h{i}.GY)) = count(i);   % Convert counts to flags
                    end                
                    end                
                    
                    

