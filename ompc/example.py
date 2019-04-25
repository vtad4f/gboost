end# Example training and testing a 2-class graph boosting classifier

disp(mcat([mstring('Loading example graphs...')]))
load(mstring('example_graphs'))

disp(mcat([mstring('   '), num2str(length(train_G)), mstring(' training samples')]))
disp(mcat([mstring('   '), num2str(length(test_G)), mstring(' test samples')]))
disp(mstring(' '))

disp(mcat([mstring('We train a 2-class graph boosting classifier.')]))
disp(mcat([mstring('the settings are:')]))
disp(mcat([mstring('   nu = 0.2, the LPBoost nu-parameter controlling training accuracy')]))
disp(mcat([mstring('   conv_epsilon = 0.05, the LPBoost convergence tolerance parameter')]))
disp(mcat([mstring('   max_col = 25, generate 25 hypotheses in each iteration (multiple pricing)')]))
disp(mstring(' '))
disp(mcat([mstring('Please press return to start training...')]))
pause()

[cl, cfun] = gboost2(train_G, train_Y, 0.2, 0.05)
disp(mcat([mstring('The classifier has been trained successfully.')]))
disp(mcat([mstring('There are '), num2str(length(find(cl.alpha > 1e-5))), mstring(' active subgraph stumps.')]))
disp(mcat([mstring('Please press return to test the classifier...')]))
pause()

[Yout, Yreal, GY] = cfun(test_G)
accuracy = length(find(Yout == test_Y)) / length(test_Y)
disp(mcat([mstring('   test accuracy = '), num2str(accuracy)]))
[auc, eer, curve] = rocscore(Yreal, test_Y)
disp(mcat([mstring('   test ROC AUC = '), num2str(auc)]))
disp(mcat([mstring('   test ROC EER = '), num2str(eer)]))



