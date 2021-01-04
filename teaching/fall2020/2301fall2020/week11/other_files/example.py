import matplotlib.pyplot as plt

acc_train = []
acc_test = []

alphas = [.0001, .001, .01, .1, 1., 10., 100.]
for a in alphas:

    classifier = SGDClassifier(loss='log', alpha=a, max_iter=1000, tol=1.0e-12, random_state=123)
    classifier.fit(X_train, Y_train)
    
    acc_train.append(accuracy_score(Y_train, classifier.predict(X_train)))
    acc_test.append(accuracy_score(Y_test, classifier.predict(X_test)))

# use the documentation to make a semilog plot 
# https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.pyplot.semilogx.html
plt.semilogx(alphas, acc_train, label='Training')
plt.semilogx(alphas, acc_test, label='Test')

plt.xlabel('Alpha')
plt.ylabel('Accuracy')
plt.legend(loc='upper right')

plt.show()