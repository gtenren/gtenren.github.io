import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, auc, roc_auc_score


def extract_match(data, profile, interest, obs):
    ''' 
    map the profiles from data and construct a new data frame
    determine the match between the person and the partner
    find the age and income difference
    find number of shared interest
    return a row of data frome
    '''

    match = data['match'].iloc[obs]
    
    #extract iid and pid for mapping
    iid = data['iid'].iloc[obs]
    pid = data['pid'].iloc[obs]

    #map the data from profile
    person = profile[profile['iid']==iid]
    partner = profile[profile['iid']==pid]

    age = person['age'].values-partner['age'].values
    income = person['income'].values-partner['income'].values

    if str(person['field_cd']) == str(partner['field_cd']):
        field = 1
    else:
        field = 0

    if str(person['race']) == str(partner['race']):
        race = 1
    else:
        race = 0

    if str(person['from']) == str(partner['from']):
        origin = 1
    else:
        origin = 0
    
    if str(person['go_out']) == str(partner['go_out']):
        go_out = 1
    else:
        go_out = 0

    count = 0
    for i in interest: 
        if int(person[i]) == 1 and int(partner[i]) == 1:
            count = count+1

    df = pd.DataFrame({'match':match,'age':age,'income':income,'origin':origin,
                       'race':race,'go_out':go_out,'interest':count,'field_cd':field})

    return df




def model_evaluation_score(model, X_train,X_valid,X_test,y_train,y_valid,y_test):
    '''return a dictionary of acc and auc for training,validating and testing dataset for binary classification model'''

    #create the list of probability of positive predicted by the model
    y_probas_train = model.predict_proba(X_train)
    y_probas_valid = model.predict_proba(X_valid)
    y_probas_test = model.predict_proba(X_test)
    y_score_train = model.predict_proba(X_train)[:,1]
    y_score_valid = model.predict_proba(X_valid)[:,1]
    y_score_test = model.predict_proba(X_test)[:,1]
    
    
    #predicted class
    predicted_train = model.predict(X_train)
    predicted_valid = model.predict(X_valid)
    predicted_test = model.predict(X_test)
    
    #calculate result
    train_acc = accuracy_score(y_train,predicted_train)
    train_auc = roc_auc_score(y_train,y_score_train)
    valid_acc = accuracy_score(y_valid,predicted_valid)
    valid_auc = roc_auc_score(y_valid,y_score_valid)
    test_acc = accuracy_score(y_test,predicted_test)
    test_auc = roc_auc_score(y_test,y_score_test)
    
    return {'train_acc':train_acc, 'train_auc':train_auc,
            'valid_acc':valid_acc, 'valid_auc':valid_auc, 'test_acc':test_acc, 'test_auc':test_auc }