from __future__ import division
from pylab import * # https://stsievert.com/blog/2015/09/01/matlab-to-python/
#import cvxpy as cvx # TODO - https://stackoverflow.com/questions/36755392/convert-a-semidefinite-program-from-cvx-to-cvxpy
from my_src import *
def lpboost(X=None, Y=None, conv_epsilon=None, nu=None, findhypothesis_1=None, boosting_type=None, max_col=None, **kwargs):
   nargin, nargout = my_arg_reader(X, Y, conv_epsilon, nu, findhypothesis_1, boosting_type, max_col, **kwargs)
   
   
   # 1.5/2-class LP Boosting,
   #
   # Author: Sebastian Nowozin <sebastian.nowozin@tuebingen.mpg.de>
   # Date: 8th December 2006
   #
   # Input
   #    X: The (l,p) (cell-) array containing l samples.  The entire row is
   #       passed to the findhypothesis function.
   #
   #    Y: The (l,1) array of training sample labels with elements in [ -1, 1 ].
   #       Must be ordered such that first all +1 samples come, then all -1
   #       samples.
   #
   #    conv_epsilon: An additional relaxation of the convergence condition,
   #        where 0 <= convergence_theta <= 1.  Usual choices are 0.01, 0.05 and
   #        0.1.  The check is (violation <= -theta + conv_epsilon)
   #
   #    nu: The real 0 < nu < 1 parameter (eg. somewhere between 0.02 and 0.1).
   #        For 2-class LPBoost nu is an upper bound on the misclassified samples
   #        of the training set.  (See Demiriz2002 LPBoost paper.)
   #
   #    findhypothesis_1: function f with signature [h]=f(X,Y,u,beta,max_col),
   #       where u are weights for the training samples and beta is the
   #       restricted master problem solution (see [Demiriz2002]).  The returned
   #       hypotheses h is a cellarray of structures with elements .h, .hi and
   #       .GY.  Each .h should be of the form Y=h[X], where each row of X is
   #       considered one sample.  The function has to solve the maximization
   #       problem (10) in [Demiriz2002], which is given by
   #
   #          h^ = arg max_[h \in H] \sum_[i=1-1]^l u_i y_i h(x_i),
   #
   #       that is, h^ is the function that maximized the margin of the weighted
   #       training samples.  u is a (l,1) real array.
   #
   #       For 1.5-class boosting, the hypothesis function is constrained to the
   #       range 0 <= y <= 1.
   #       For 2-class boosting, the hypothesis may return any real y.
   #
   #       'hi' is the "hypothesis information" which can be used to pass some
   #       data about it back to the caller of lpboost1d5.
   #
   #       max_col is the maximum number of columns to add in one iteration.
   #
   #    (optional) boosting_type: 1 for 1.5-class LPBoosting, 2 for standard
   #       2-class LPBoosting.  Note that you can also do 1-class LPBoosting by
   #       having no negative Y label and using boosting_type=1.
   #
   #    (optional) max_col: Maximum number of columns to add at each iteration.
   #       (default: 25).
   #
   # Output
   #    classifier: Structure with elements
   #       .alpha: The individual hypotheses.T weights as (1,n) real array.
   #       .H: The (1,n) cellarray of hypotheses.  The final classification function
   #          is then given by  f[x-1] = \sum_i alpha_i H_i[x-1].
   #       .Ytrain: The outputs for the training samples.
   #       .rho: array([ rho1, rho2 ])
   #       .class_thresh: For 1.5-class boosting it is the classification
   #          treshold, sum(classifier.rho)/2
   #
   #    (optional) cfunout: A combined classification function with signature
   #       [Y, Yreal] = cfun (X), Yreal is optional.
   #
   #    (optional) GY: The (my_size(X,1),n) array of classifier responses, where the
   #       (i,j)'th element encodes the response of subclassifier j on sample i.
   
   # Set default maximum number of columns to add in one iteration
   if nargin < 7 or my_isempty(max_col):
      max_col=25
   #end
   
   # Check and sort if Y is not sorted (the output Y will be in the original:
   # input order, though)
   Ysorted,I=my_sort(Y,1,'descend', nargout=2)
   if norm(Y-Ysorted,1) > 0:
      Y=Ysorted
      if my_size(X,1) == 1:
         X=X[I]
      else:
         X=X[I,:]
      #end
   else:
      I=range(1-1, my_size(Y,1))
   #end
   
   l1 = len(find(Y >= 0))
   l2 = len(find(Y < 0))
   l = l1 + l2
   m = 0
   
   theta = 0
   if l2 > 0:
      u = array([[ (1/l1) * 0.5 * ones((l1,1)) ],[ (1/l2) * 0.5 * ones((l2,1)) ]])
   else:
      u = array([ (1/l1) * 0.5 * ones((l1,1)) ])
   #end
   
   alpha=matrix([])   # The classifier weights
   H=matrix([])      # The hypothesis functions
   HI=matrix([])      # The hypothesis information
   Ytrain=zeros((l,1))
   rho=array([ 0, 0 ])
   
   iter = 1
   HM = zeros((l,0))
   while True:
      disp(['LPBoost iter ', str(iter)])
      m = m + 1
   
      # Select best new hypothesis for weighted training samples
      h = findhypothesis_1 (X, Y, u, theta, max_col, nargout=1)
      if len(h) > 0:
         # Find the maximum gain hypothesis, as h is possibly unordered, we
         # first search for the  maximum gain hypothesis.
         #
         # If the maximum gain is below theta, then no further improvement can
         # be made and we have converged to the global optimal solution (for
         # 2-class LPBoosting) or to a local optimal solution (1.5-class
         # LPBoosting).
         oval = -Inf
         for i in range(1, len(h)+1):
            oval_cur = (u * Y).T @ h[i-1].GY[:,1-1]
            #disp(['   hypothesis ', str(i), ': ', str(oval_cur)])
            if oval_cur > oval:
               oval = oval_cur
            #end
         #end
         #oval = (u * Y).T @ h[1-1].h[X]
         disp(['   optimality: ', str(oval), ' <= ', str(theta), ' + ', str(conv_epsilon), ' ?'])
      #end
   
      # Stopping condition: either no hypotheses are there anymore or best
      # hypothesis gain is too small.
      if len(h) == 0 or oval <= (theta + conv_epsilon):
         disp(['LPBoost optimality reached after ', str(iter), ' iterations.'])
   
         if len(h) == 0:
            disp(['   (no hypotheses left)'])
         else:
            disp(['   (no improvements left)'])
         #end
         m = m - 1
         break
      #end
   
      # Update combined hypothesis and restricted master problem
      for i in range(1, len(h)+1):
         H[m+i-1-1] = h[i-1].h
         HI[m+i-1-1] = h[i-1].hi
         #HM[:,m+i-1-1] = h[i-1].h[X]
         HM[:,m+i-1-1] = h[i-1].GY[:,1-1]
      #end
      m = m + len(h) - 1
   
      #disp(['   output: ', str(HM[:,m-1]')])
   
      # Solve the LPBoosting formulation (see [Demiriz2002] for the 2-class
      # formulation).
      if boosting_type == 1 and l2 > 0:
         # 1.5 class LPBoosting, see my short report about this formulation.
         # In essence, we restrict the weak learners to positive outputs and
         # thus only the presence of features can be used as indication for a
         # class decision, not their absence.
         disp(['1.5-class LPBoosting'])
         
         raise Exception('TODO - this was a matlab cvx code block')
   
         rho1 = opt_rho1
         rho2 = opt_rho2
         rho = array([ rho1, rho2 ])
      elif boosting_type == 1 and l2 == 0:
         # 1-class LPBoosting
         disp(['1-class LPBoosting'])
         
         raise Exception('TODO - this was a matlab cvx code block')
   
         rho1 = opt_rho1
         rho = array([ rho1 ])
      elif boosting_type == 2:
         # 2-class LPBoosting
         disp(['2-class LPBoosting'])
         D = 1/((l1+l2) @ nu)
         if D < (1/(l1+l2)) or D >= 1:
            error (['D (', str(D), ') outside dual feasibility boundary.'])
         #end
   
         raise Exception('TODO - this was a matlab cvx code block')
   
         rho = opt_rho
      #end
   
      alpha = opt_alpha
      theta = -cvx_optval   # primal: min, dual: max, gamma = - (dual result)
   
      u = zeros((l,1))
      for k in range(1, l1+1):
         u[k-1] = d_u1[k-1]
      #end
      for k in range(1, l2+1):
         u[l1+k-1] = d_u2[k-1]
      #end
   
      disp(['alpha: ', str(alpha.T)])
      if boosting_type == 1 and l2 > 0:
         disp(['rho1/2: ', str(rho1), ', ', str(rho2)])
      elif boosting_type == 1 and l2 == 0:
         disp(['rho: ', str(rho1)])
      elif boosting_type == 2:
         disp(['rho: ', str(rho)])
      #end
   
      iter = iter + 1
   #end
   
   Ytrain = zeros((l,1))
   for j in range(1, m+1):
      Ytrain = Ytrain + alpha[j-1] @ HM[:,j-1]
   #end
   
   # Output classifier structure
   classifier=matrix([])
   classifier.alpha = alpha
   #classifier.H = H # TODO - can't set attribute
   classifier.HI = HI
   classifier.Ytrain = Ytrain
   classifier.Ytrain[I] = Ytrain
   classifier.rho = rho
   classifier.HM = HM
   if boosting_type == 1:
      classifier.class_thresh = sum(classifier.rho)/2
   elif boosting_type == 2:
      classifier.class_thresh = 0
   #end
   
   # Output the combined, weighted hypothesis.
   if nargout >= 2:
      cfunout = lambda X, **kwargs: cfun (X, classifier)
   #end
   
   # If desired, output the classifier responses as well.
   if nargout >= 3:
      GY = HM
   #end
   return classifier, cfunout, GY
   
def cfun(X=None, classifier=None, **kwargs):
   nargin, nargout = my_arg_reader(X, classifier, **kwargs)
   
   
   # Combined boosting classifier
   #
   # Input
   #    X: Input data, in the form the individual classifiers take.
   #    classifier: The classifier structure.
   #       .alpha: (1,q) the weightings of subgraphs.
   #       .H: (1,q) cellarray of classifier functions.
   #       .HI: (1,q) cellarray of subgraphs.
   #       .Ytrain: (n,1) array of outputs on training set.
   #       .rho: (1,2) thresholds array([ high, low ]) for classification decision.
   #       .class_thresh: threshold for hard classification decision.
   #
   # Output
   #    Y: The (n,1) discrete outputs -1 (negative class) or 1 (positive class).
   #
   #    (optional) Yreal: The (n,1) real outputs >= 0.
   #
   #    (optional) GY: (n,q) classifier outputs.
   
   if my_size(X,1) == 1:
      X = X.T   # Bring X in column form
   #end
   n = my_size(X,1)
   
   # Compute the real classification outputs as weighted sum of the individual
   # classifiers.
   Yreal=matrix([])
   if nargout >= 3:
      GY = zeros(n,len(classifier.alpha))
   #end
   for j in range(1, len(classifier.alpha)+1):
      if classifier.alpha[j-1] >= 1e-5 or nargout >= 3:
         cout=classifier.H[j-1](X)
         if nargout >= 3:
            GY[:,j-1] = cout
         #end
   
         if my_isempty(Yreal):
            Yreal = classifier.alpha[j-1] @ cout
         else:
            Yreal = Yreal + classifier.alpha[j-1] @ cout
         #end
      #end
   #end
   
   Yout=-ones((n,1))
   Yout[find(Yreal >= classifier.class_thresh)]=1
   return Yout, Yreal, GY
   
   