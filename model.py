import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# %matplotlib inline

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer,make_column_transformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler,OrdinalEncoder,FunctionTransformer
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.preprocessing import StandardScaler,RobustScaler, QuantileTransformer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.feature_selection import SelectKBest, mutual_info_regression

import pickle

# load the data
df = pd.read_csv("Student_dataset_3.csv")

# rename the columns
df.columns=['RollNo','Gender','Age','Location','Famsize','Pstatus','Medu','Fedu','Mjob','Fjob','reason','traveltime','studytime','Failures','Famsup','Paid','Activities','HigherEdu','Internet','Famrel','Freetime','GoOut','Health','10th%','12thordiploma%','EAMCETorECETrank','Internal','Prev cgpa','sgpa']

# remove duplicates 
df = df.drop_duplicates()


df['Eamcet Rank'] = 0
df['Ecet Rank'] = 0

df.loc[~df['RollNo'].str.contains('L'), 'Eamcet Rank'] = df.loc[~df['RollNo'].str.contains('L'), 'EAMCETorECETrank']
df.loc[df['RollNo'].str.contains('L'), 'Ecet Rank'] = df.loc[df['RollNo'].str.contains('L'), 'EAMCETorECETrank']
df.drop('EAMCETorECETrank', axis=1, inplace=True)

df['Prev cgpa'] = df['Prev cgpa'].replace(0, 5.5)
df['sgpa'] = df['sgpa'].replace(0, 5.5)
df['Total_eamcet/ecet_grade'] = 0
df['Fedu'] = df['Fedu'].replace('primary education (4th grade)', 'primary education( 4th grade )')

df['traveltime'] = df['traveltime'].replace('<1hr', '>1hr')


X = df.drop('sgpa', axis=1)
y = df['sgpa']

X_train,X_test,y_train,y_test=train_test_split(df.drop(columns=['sgpa']),df['sgpa'],test_size=0.2,random_state=42)


def get_eamcet_grade(rank):
    rank = rank
    conditions = [
        rank == 0,
        rank < 7000,
        rank < 8500,
        rank < 10000,
        rank < 25000
    ]
    choices = [0, 4, 3, 2, 1]
    return np.select(conditions, choices, default=0)

def get_ecet_grade(rank):
    
    conditions = [
        rank == 0,
        rank < 250,
        rank < 350,
        rank < 580,
        rank < 1000
    ]
    choices = [0, 4, 3, 2, 1]
    return np.select(conditions, choices, default=0)

ctf1 = ColumnTransformer([
        ('imputer1', SimpleImputer(strategy='mean'), [28]),  #Eamcet Rank
         ('Eamcet_transformer', FunctionTransformer(get_eamcet_grade), [28]),
        ('imputer2', SimpleImputer(strategy='mean'), [29]),  #Ecet Rank
        ('Ecet_transformer', FunctionTransformer(get_ecet_grade), [29]),
    ],
    remainder='passthrough'
)

def add_cols(X):
    # Add values at indices 1 and 3
    X[:, 1] = X[:, 1] + X[:, 3]

    # Replace the value at the last index with the sum of values at indices 1 and 3
    X[:, -1] = X[:, 1] + X[:, 3]

    return X

ctf2 = FunctionTransformer(add_cols)


categories_medu = ['None', 'primary education( 4th grade )', '5th to 9th grade', 'secondary education', 'higher education']
categories_fedu = ['None', 'primary education( 4th grade )', '5th to 9th grade', 'secondary education', 'higher education']
categories_travel=[ '<15 min','15 - 30 min','30min - 1hr','>1hr']
categories_study=[ '1- <2 hr', '2 to 5 hr','5 to 10 hr', '>10 hr']
categories_famrel=[ 'Bad','Good','Very good','excellent']
categories_freetime=['very low', 'low', 'high','very high']
categories_goout=[ '1 - very low', '2 - low', '3 - medium','4 - high','5 - very high']
categories_health=[ '1 - very bad', '2- bad', '3 - average','4 - good','5 - very good']

# Define the column transformer with ordinal encoding for Medu and Fedu
ctf3 = ColumnTransformer(transformers=[('ordinal', OrdinalEncoder(categories=[categories_medu,
                            categories_fedu,categories_travel,categories_study,categories_famrel,
                            categories_freetime,categories_goout,categories_health],dtype=np.int32),
                                        [10,11,15,16,23,24,25,26])], remainder='passthrough')

# define column transformer for one_hot encoding
ctf4 = ColumnTransformer(
    transformers=[
        ('one_hot_encode', OneHotEncoder(drop='first', sparse_output=False, dtype=np.int32), [13, 15, 17, 18, 19, 20, 22, 23, 24, 25, 26])
    ],
    remainder='passthrough'
)


# define the column transformer to apply scaling and capping
ctf5 = ColumnTransformer(transformers=[
    ('scaling', RobustScaler(), [31,32,33,34]),
    ('capping', QuantileTransformer(output_distribution='uniform', n_quantiles=60, random_state=42),[31,32,33,34])
], remainder='passthrough')

cols_to_drop=[0,1,2,3,31,32,33,34,35]

# define the transformer to drop the specified columns
ctf6 = ColumnTransformer(transformers=[
    ('drop_cols', 'drop', cols_to_drop)
], remainder='passthrough')

ctf7 = SelectKBest(score_func=mutual_info_regression, k=5)

ctf8=RandomForestRegressor()

pipe=Pipeline(
   [
       ('ctf1',ctf1),
       ('ctf2',ctf2),
       ('ctf3',ctf3),
       ('ctf4',ctf4),
       ('ctf5',ctf5),
       ('ctf6',ctf6),
       ('ctf7',ctf7),
       ('ctf8',ctf8)
   ])

pipe.fit(X_train,y_train)


pickle.dump(pipe,open('sapp_final_algo.pkl','wb'))

model=pickle.load(open('sapp_final_algo.pkl','rb'))


# result = pipe.predict(pd.DataFrame([['319126510001','FEMALE',  21  ,  'Urban'   ,     4    ,    'T'   ,"higher education",'higher education','Homemaker','civil services: administrative or police', 'Other'  , '30min - 1hr', '1- <2 hr' ,     0     , 'Yes'  ,  'No' ,    'Yes'    ,     'No'   ,    'Yes'  ,'excellent',   'high'  ,'3 - medium','5 - very good',  93.1   ,       96.3      ,   90.23   ,    9.4    ,    18238.0    ,      0     ,                        0]],
#                     columns=['RollNo'      ,'Gender', 'Age', 'Location', 'Famsize', 'Pstatus',      'Medu'      ,       'Fedu'     ,   'Mjob'  ,                  'Fjob'                  ,          'reason' ,  'traveltime', 'studytime', 'Failures','Famsup', 'Paid', 'Activities', 'HigherEdu', 'Internet', 'Famrel'  , 'Freetime',   'GoOut'  ,   'Health'    , '10th%' , '12thordiploma%', 'Internal','Prev cgpa',  'Eamcet Rank', 'Ecet Rank','Total_eamcet/ecet_grade']))

# print(result)