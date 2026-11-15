import pandas as pd
import numpy as np
import sklearn as skl


import xgboost as xgb

import pickle

def To_DM_with_cat(dt: pd.DataFrame,y: pd.Series, cat_feat: list) -> xgb.DMatrix:
    dt[cat_feat] = dt[cat_feat].astype('str').astype('category')
    DM = xgb.DMatrix(dt, label = y, enable_categorical=True)
    return DM

def Training_XGB(parameters: list , Train_set: xgb.DMatrix, watch_list: list):
        training_track = {}
        tree_model = xgb.train(parameters, Train_set, num_boost_round=75,evals=watch_list, verbose_eval=False, evals_result=training_track)
        return tree_model, training_track


data_train  = pd.read_json('ECOMMERCE/train_data.json')
data_val = pd.read_json('ECOMMERCE/val_data.json')
data_test = pd.read_json('ECOMMERCE/test_data.json')


data_full_train = pd.concat([data_train, data_val], axis=0, ignore_index=True)

data_full_train.shape

X_train = data_full_train.iloc[:,:-1]
y_train = data_full_train['Churned']
X_test = data_test.iloc[:,:-1]
y_test = data_test['Churned']

CAT_FEATURES = ['Gender', 'Country', 'City', 'Payment_Method_Diversity', 'Signup_Quarter']


DM_train = To_DM_with_cat(X_train, y_train,CAT_FEATURES) 
DM_test = To_DM_with_cat(X_test, y_test, CAT_FEATURES)

watchlist = [(DM_train, 'train'), (DM_test, 'test')] 

xgb_final_params = par_max_depth = {
        'objective': 'binary:logistic',
        'tree_method': 'hist',

        'max_depth': 2,
        'gamma': 0.0,
        'min_child_weight':1,
        'subsample':1,

        'n_jobs': 8,
        'eta': 0.3,
        'eval_metric': 'auc',
        'verbosity': 1,
        'seed':1
        }

model, track = Training_XGB(xgb_final_params, DM_test, watchlist)

file_name = 'final_model.bin'

with open(file_name, 'wb') as f_out:
    pickle.dump(model, f_out)





