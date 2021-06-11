def predict(x, w):
    dot = 0
    for i in range(len(w)):
        dot += x[i] * w[i]
    if dot < 0:
        return 0
    else:
        return 1

def learn(features, labels, epochs, J, eta):
    '''
    Inputs: 

        J (int): the number of features per instance
        features (list): a list of N instances, each with J features: 
                         * e.g. features might be [[1,0,1,0], [0,1,1,1]] 
                                which represents N=2 instances
                                with J=4 instances per point
        labels (list): a list of N labels: 
                            * 1 represents positive instances 
                            * -1 represents negative instances
        epochs (int): an integer, equal to number of passes through the training data
        eta (float): a learning rate

    Outputs: 
        w (list): a list of learned weights
    '''
    w = [] # initialize w, the weights
    for j in range(J): 
        w.append(0)

    for epoch in range(epochs):
        for index, feature_list in enumerate(features):
            yhat = predict(x=feature_list, w=w)
            y = labels[index]
            if y == yhat:
                pass # do nothing
            else:
                for j in range(J):
                    w[j] += eta * ((y - yhat) * feature_list[j])
    return w

if __name__ == "__main__":
    features = [[0, 1], [1, 0], [1, 1], [1, 0]]
    labels = [1,-1, 1, -1]
    w = learn(features, labels, epochs=10, J=2, eta=.1)
    
    for i, f in enumerate(features):
        print(predict(f, w) == labels[i])

