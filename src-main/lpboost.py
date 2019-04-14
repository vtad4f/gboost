

def lpboost (X, Y, conv_epsilon, nu, findhypothesis_1, boosting_type, max_col):
   """
      1.5/2-class LP Boosting,
      
      Author: Sebastian Nowozin <sebastian.nowozin@tuebingen.mpg.de>
      Date: 8th December 2006
      
      Input
         X: The (l,p) (cell-) array containing l samples.  The entire row is
            passed to the findhypothesis function.
      
         Y: The (l,1) array of training sample labels with elements in { -1, 1 }.
            Must be ordered such that first all +1 samples come, then all -1
            samples.
      
         conv_epsilon: An additional relaxation of the convergence condition,
            where 0 <= convergence_theta <= 1.  Usual choices are 0.01, 0.05 and
            0.1.  The check is (violation <= -theta + conv_epsilon)
      
         nu: The real 0 < nu < 1 parameter (eg. somewhere between 0.02 and 0.1).
            For 2-class LPBoost nu is an upper bound on the misclassified samples
            of the training set.  (See Demiriz2002 LPBoost paper.)
      
         findhypothesis_1: function f with signature [h]=f(X,Y,u,beta,max_col),
            where u are weights for the training samples and beta is the
            restricted master problem solution (see [Demiriz2002]).  The returned
            hypotheses h is a cellarray of structures with elements .h, .hi and
            .GY.  Each .h should be of the form Y=h(X), where each row of X is
            considered one sample.  The function has to solve the maximization
            problem (10) in [Demiriz2002], which is given by
      
               h^ = arg max_{h \in H} \sum_{i=1}^l u_i y_i h(x_i),
      
            that is, h^ is the function that maximized the margin of the weighted
            training samples.  u is a (l,1) real array.
      
            For 1.5-class boosting, the hypothesis function is constrained to the
            range 0 <= y <= 1.
            For 2-class boosting, the hypothesis may return any real y.
      
            'hi' is the "hypothesis information" which can be used to pass some
            data about it back to the caller of lpboost1d5.
      
            max_col is the maximum number of columns to add in one iteration.
      
         (optional) boosting_type: 1 for 1.5-class LPBoosting, 2 for standard
            2-class LPBoosting.  Note that you can also do 1-class LPBoosting by
            having no negative Y label and using boosting_type=1.
      
         (optional) max_col: Maximum number of columns to add at each iteration.
            (default: 25).
      
      Output
         classifier: Structure with elements
            .alpha: The individual hypotheses' weights as (1,n) real array.
            .H: The (1,n) cellarray of hypotheses.  The final classification function
               is then given by  f(x) = \sum_i alpha_i H_i(x).
            .Ytrain: The outputs for the training samples.
            .rho: [rho1 rho2]
            .class_thresh: For 1.5-class boosting it is the classification
               treshold, sum(classifier.rho)/2
      
         (optional) cfunout: A combined classification function with signature
            [Y, Yreal] = cfun (X), Yreal is optional.
      
         (optional) GY: The (size(X,1),n) array of classifier responses, where the
            (i,j)'th element encodes the response of subclassifier j on sample i.
   """
   # Set default maximum number of columns to add in one iteration
   if nargin < 7 or isempty(max_col):
      max_col=25

   # Check and sort if Y is not sorted (the output Y will be in the original
   # input order, though)
   Ysorted,I=sort(Y,1,'descend')
   if norm(Y-Ysorted,1) > 0:
      Y=Ysorted
      if size(X,1) == 1:
         X=X(I)
      else:
         X=X(I,:)
   else:
      I=1:size(Y,1)

   l1 = len(find(Y >= 0))
   l2 = len(find(Y < 0))
   l = l1 + l2
   m = 0

   theta = 0
   if l2 > 0:
      u = [(1/l1)*0.5*ones(l1,1)  (1/l2)*0.5*ones(l2,1)]
   else:
      u = [(1/l1)*0.5*ones(l1,1)]

   alpha=[]   # The classifier weights
   H=[]      # The hypothesis functions
   HI=[]      # The hypothesis information
   Ytrain=zeros(l,1)
   rho=[0 0]

   iter = 1
   HM = zeros(l,0)
   while true
      print(' '.join(['LPBoost iter ', str(iter)]))
      m = m + 1

      # Select best new hypothesis for weighted training samples
      [h] = findhypothesis_1 (X, Y, u, theta, max_col)
      if len(h) > 0:
         # Find the maximum gain hypothesis, as h is possibly unordered, we
         # first search for the  maximum gain hypothesis.
         #
         # if the maximum gain is below theta, then no further improvement can
         # be made and we have converged to the global optimal solution (for
         # 2-class LPBoosting) or to a local optimal solution (1.5-class
         # LPBoosting).
         oval = -Inf
         for i in range(1, len(h) + 1):
            oval_cur = (u.*Y)'*h{i}.GY(:,1)
            #print(' '.join(['   hypothesis ', str(i), ': ', str(oval_cur)]))
            if oval_cur > oval:
               oval = oval_cur
         #oval = (u.*Y)'*h{1}.h(X)
         print(' '.join(['   optimality: ', str(oval), ' <= ', str(theta), ' + ', ...
            str(conv_epsilon), ' ?']))

      # Stopping condition: either no hypotheses are there anymore or best
      # hypothesis gain is too small.
       if len(h) == 0 or oval <= (theta + conv_epsilon):
         print(' '.join(['LPBoost optimality reached after ', str(iter), ' iterations.']))

         if len(h) == 0:
            print(' '.join(['   (no hypotheses left)']))
         else:
            print(' '.join(['   (no improvements left)']))
           m = m - 1
           break

      # Update combined hypothesis and restricted master problem
      for i in range(1, len(h) + 1):
         H{m+i-1} = h{i}.h
         HI{m+i-1} = h{i}.hi
         #HM(:,m+i-1) = h{i}.h(X)
         HM(:,m+i-1) = h{i}.GY(:,1)
      m = m + len(h) - 1

      #print(' '.join(['   output: ', str(HM(:,m)')]))

      # Solve the LPBoosting formulation (see [Demiriz2002] for the 2-class
      # formulation).
      if boosting_type == 1 and l2 > 0:
         # 1.5 class LPBoosting, see my short report about this formulation.
         # In essence, we restrict the weak learners to positive outputs and
         # thus only the presence of features can be used as indication for a
         # class decision, not their absence.
         print(' '.join(['1.5-class LPBoosting']))
         cvx_begin
            variables opt_alpha(m) opt_rho1(1) opt_rho2(1) opt_xi1(l1) opt_xi2(l2)
            dual variables d_u1{l1} d_u2{l2}
            minimize (-opt_rho1 + opt_rho2 + sum(opt_xi1)/(l1*nu) + sum(opt_xi2)/(l2*nu))
               for k in range(1, l1 + 1):
                  HM(k,:)*opt_alpha - opt_rho1 + opt_xi1(k) >= 0 : d_u1{k}
               for k in range(1, l2 + 1):
                  HM(l1+k,:)*opt_alpha - opt_rho2 - opt_xi2(k) <= 0 : d_u2{k}
               sum(opt_alpha) == 1
               opt_alpha >= 0
               opt_xi1 >= 0
               opt_xi2 >= 0
               opt_rho1 >= 0
               opt_rho2 >= 0
         cvx_end

         rho1 = opt_rho1
         rho2 = opt_rho2
         rho = [rho1 rho2]
      elif boosting_type == 1 and l2 == 0:
         # 1-class LPBoosting
         print(' '.join(['1-class LPBoosting']))
         cvx_begin
            variables opt_alpha(m) opt_rho1(1) opt_xi1(l1)
            dual variables d_u1{l1}
            minimize (-opt_rho1 + sum(opt_xi1)/(l1*nu))
               for k in range(1, l1 + 1):
                  HM(k,:)*opt_alpha - opt_rho1 + opt_xi1(k) >= 0 : d_u1{k}
               sum(opt_alpha) == 1
               opt_alpha >= 0
               opt_xi1 >= 0
               opt_rho1 >= 0
         cvx_end

         rho1 = opt_rho1
         rho = [rho1]
      elif boosting_type == 2:
         # 2-class LPBoosting
         print(' '.join(['2-class LPBoosting']))
         D = 1/((l1+l2)*nu)
         if D < (1/(l1+l2)) or D >= 1:
            error (['D (', str(D), ') outside dual feasibility boundary.'])

         cvx_begin
            variables opt_alpha(m) opt_rho(1) opt_xi1(l1) opt_xi2(l2)
            dual variables d_u1{l1} d_u2{l2}
            minimize (-opt_rho + D*(sum(opt_xi1)+sum(opt_xi2)))
               for k in range(1, l1 + 1):
                  # Y is 1
                  #HM(k,:)*opt_alpha - opt_rho + opt_xi1(k) >= 0 : d_u1{k}
                  HM(k,:)*opt_alpha - opt_rho + opt_xi1(k) >= 0 : d_u1{k}
               for k in range(1, l2 + 1):
                  # Y is -1, hence <=
                  -HM(l1+k,:)*opt_alpha - opt_rho + opt_xi2(k) >= 0 : d_u2{k}
               sum(opt_alpha) == 1
               opt_alpha >= 0
               opt_xi1 >= 0
               opt_xi2 >= 0
         cvx_end
         
         
         rho = opt_rho

      alpha = opt_alpha
       theta = -cvx_optval   # primal: min, dual: max, gamma = - (dual result)

       u = zeros(l,1)
       for k in range(1, l1 + 1):
           u(k) = d_u1{k}
       for k in range(1, l2 + 1):
           u(l1+k) = d_u2{k}

      print(' '.join(['alpha: ', str(alpha')]))
      if boosting_type == 1 and l2 > 0:
         print(' '.join(['rho1/2: ', str(rho1), ', ', str(rho2)]))
      elif boosting_type == 1 and l2 == 0:
         print(' '.join(['rho: ', str(rho1)]))
      elif boosting_type == 2:
         print(' '.join(['rho: ', str(rho)]))

      iter = iter + 1

   Ytrain = zeros(l,1)
   for j in range(1, m + 1):
      Ytrain = Ytrain + alpha(j)*HM(:,j)

   # Output classifier structure
   classifier=[]
   classifier.alpha = alpha
   classifier.H = H
   classifier.HI = HI
   classifier.Ytrain = Ytrain
   classifier.Ytrain(I) = Ytrain
   classifier.rho = rho
   classifier.HM = HM
   if boosting_type == 1:
      classifier.class_thresh = sum(classifier.rho)/2
   elif boosting_type == 2:
      classifier.class_thresh = 0

   # Output the combined, weighted hypothesis.
   if nargout >= 2:
      cfunout = lambda X: cfun (X, classifier)

   # if desired, output the classifier responses as well.
   if nargout >= 3:
      GY = HM
      
   return classifier, cfunout, GY
   
   
def cfun (X, classifier):
   """
      Combined boosting classifier
      
      Input
         X: Input data, in the form the individual classifiers take.
         classifier: The classifier structure.
            .alpha: (1,q) the weightings of subgraphs.
            .H: (1,q) cellarray of classifier functions.
            .HI: (1,q) cellarray of subgraphs.
            .Ytrain: (n,1) array of outputs on training set.
            .rho: (1,2) thresholds [high low] for classification decision.
            .class_thresh: threshold for hard classification decision.
      
      Output
         Y: The (n,1) discrete outputs -1 (negative class) or 1 (positive class).
      
         (optional) Yreal: The (n,1) real outputs >= 0.
      
         (optional) GY: (n,q) classifier outputs.
   """
   if size(X,1) == 1:
      X = X'   # Bring X in column form
   n = size(X,1)

   # Compute the real classification outputs as weighted sum of the individual
   # classifiers.
   Yreal=[]
   if nargout >= 3:
      GY = zeros(n,len(classifier.alpha))
   for j in range(1, len(classifier.alpha) + 1):
      if classifier.alpha(j) >= 1e-5 or nargout >= 3:
         cout=classifier.H{j}(X)
         if nargout >= 3:
            GY(:,j) = cout

         if isempty(Yreal):
            Yreal = classifier.alpha(j)*cout
         else:
            Yreal = Yreal + classifier.alpha(j)*cout

   Yout=-ones(n,1)
   Yout(find(Yreal >= classifier.class_thresh))=1
   return Yout, Yreal, GY
   
   