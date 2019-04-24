from sklearn.metrics import accuracy_score, auc, roc_auc_score
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scikitplot as skplt

def model_evaluation_score(model, X_train,X_test,y_train,y_test):
    '''return a dictionary of acc and auc for training and testing dataset for binary classification model'''

    #create the list of probability of positive predicted by the model
    y_probas_train = model.predict_proba(X_train)
    y_probas_test = model.predict_proba(X_test)
    y_score_train = model.predict_proba(X_train)[:,1]
    y_score_test = model.predict_proba(X_test)[:,1]
    
    
    #predicted class
    predicted_train = model.predict(X_train)
    predicted_test = model.predict(X_test)
    
    #calculate result
    train_acc = accuracy_score(y_train,predicted_train)
    train_auc = roc_auc_score(y_train,y_score_train)
    test_acc = accuracy_score(y_test,predicted_test)
    test_auc = roc_auc_score(y_test,y_score_test)
    
    return {'train_acc':train_acc, 'train_auc':train_auc,'test_acc':test_acc, 'test_auc':test_auc }
    
    
    
def model_evaluation_plot(model, X_train,X_test,y_train,y_test):
    '''return visualisation that display the classification evaulation of a model'''
    
    #create the list of probability of positive predicted by the model
    y_probas_train = model.predict_proba(X_train)
    y_probas_test = model.predict_proba(X_test)
    y_score_train = model.predict_proba(X_train)[:,1]
    y_score_test = model.predict_proba(X_test)[:,1]
    
    #predicted class
    predicted_train = model.predict(X_train)
    predicted_test = model.predict(X_test)
    
    #create plots for confusion matrix and roc curve
    skplt.metrics.plot_confusion_matrix(y_test, predicted_test) #create confusion matrix on test to review
    skplt.metrics.plot_roc(y_test, y_probas_test, plot_micro=False,plot_macro=False) #create a ROC
    plt.show()
    
    
def random_seed_check(model, data, target, random_seed, train_size=0.7, test_size =0.3):
    '''iteration through a list of different random seed and generate a data frame of results'''
    
    #initial list to store the evaluation results
    train_acc = []
    train_auc = []
    test_acc = []
    test_auc = []

    #iteration for list of random seed
    for r in random_seed:
        #generate different train test splits for different random seed 
        X_train, X_test, y_train, y_test = train_test_split(data, target, random_state=r, train_size=train_size, test_size =test_size)
        
        #fit the model
        model.fit(X_train,y_train)
        
        #generate a dictionary of result (see function def in Porfoio 3)
        evaluation = model_evaluation_score(model, X_train, X_test, y_train, y_test)
        
        #store result
        train_acc.append(evaluation['train_acc'])
        train_auc.append(evaluation['train_auc'])
        test_acc.append(evaluation['test_acc'])
        test_auc.append(evaluation['test_auc'])


    #create data frame
    result = pd.DataFrame({'train_acc':train_acc,
             'train_auc': train_auc,'test_acc':test_acc, 'test_auc':test_auc},index=random_seed)
    
    return result


def evaluate_score_plot(random_seed, result, compare = None):
    '''create plot for random_seed_check and provide comparison if necessary'''
    plt.figure(1, figsize=(9, 9))
    plt.subplot(221)
    plt.ylim(0.4)
    plt.plot(random_seed, result['train_acc'])
    if compare is not None:
        plt.plot(random_seed, compare['train_acc'])
        
    plt.title('training accuracy')
    
    plt.subplot(222)
    plt.ylim(0.4)
    plt.plot(random_seed, result['train_auc'])
    if compare is not None:
        plt.plot(random_seed, compare['train_auc'])
    
    plt.title('training auc')
    
    
    plt.subplot(223)
    plt.ylim(0.4)
    plt.plot(random_seed, result['test_acc'])
    if compare is not None:
        plt.plot(random_seed, compare['test_acc'])
    
    plt.title('test accuracy')
    
    plt.subplot(224)
    plt.ylim(0.4)
    plt.plot(random_seed, result['test_auc'])
    if compare is not None:
        plt.plot(random_seed, compare['test_auc'])
    plt.title('test auc')

    plt.show()
    
    
    
