from __future__ import division
from pylab import * # https://stsievert.com/blog/2015/09/01/matlab-to-python/
from gboost2 import gboost2
from my_src import *
# Example training and testing a 2-class graph boosting classifier

disp(['Loading example graphs '])
my_load('example-graphs.mat', globals())

disp(['   ', str(len(train_G)), ' training samples'])
disp(['   ', str(len(test_G)), ' test samples'])
disp(' ')

disp(['We train a 2-class graph boosting classifier.'])
disp(['the settings are:'])
disp(['   nu = 0.2, the LPBoost nu-parameter controlling training accuracy'])
disp(['   conv_epsilon = 0.05, the LPBoost convergence tolerance parameter'])
disp(['   max_col = 25, generate 25 hypotheses in each iteration (multiple pricing)'])
disp(' ')
disp(['Please press return to start training '])
my_pause()

cl, cfun = gboost2 (train_G, train_Y, 0.2, 0.05, nargout=2)
disp(['The classifier has been trained successfully.'])
disp(['There are ', str(len(find(cl.alpha > 1e-5))), ' active subgraph stumps.'])
disp(['Please press return to test the classifier '])
my_pause()

Yout, Yreal, GY = cfun (test_G, nargout=3)
accuracy = len(find(Yout == test_Y))/len(test_Y)
disp(['   test accuracy = ', str(accuracy)])
auc, eer, curve = rocscore (Yreal, test_Y, nargout=3)
disp(['   test ROC AUC = ', str(auc)])
disp(['   test ROC EER = ', str(eer)])

