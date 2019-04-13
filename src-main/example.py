# Example training and testing a 2-class graph boosting classifier

import scipy.io as sio


print(' '.join(['Loading example graphs...']))
mat = sio.loadmat('example-graphs.mat')
train_G = mat['train_G']
test_G = mat['test_G']

print(' '.join(['   ', str(len(train_G)), ' training samples']))
print(' '.join(['   ', str(len(test_G)), ' test samples']))
print(' ')

print(' '.join(['We train a 2-class graph boosting classifier.']))
print(' '.join(['the settings are:']))
print(' '.join(['   nu = 0.2, the LPBoost nu-parameter controlling training accuracy']))
print(' '.join(['   conv_epsilon = 0.05, the LPBoost convergence tolerance parameter']))
print(' '.join(['   max_col = 25, generate 25 hypotheses in each iteration (multiple pricing)']))
print(' ')
print(' '.join(['Please press return to start training...']))
input()

[cl, cfun] = gboost2 (train_G, train_Y, 0.2, 0.05)
print(' '.join(['The classifier has been trained successfully.']))
print(' '.join(['There are ', str(len(find(cl.alpha > 1e-5))), ' active subgraph stumps.']))
print(' '.join(['Please press return to test the classifier...']))
input()

[Yout, Yreal, GY] = cfun (test_G)
accuracy = len(find(Yout == test_Y))/len(test_Y)
print(' '.join(['   test accuracy = ', str(accuracy)]))
[auc, eer, curve] = rocscore (Yreal, test_Y)
print(' '.join(['   test ROC AUC = ', str(auc)]))
print(' '.join(['   test ROC EER = ', str(eer)]))

