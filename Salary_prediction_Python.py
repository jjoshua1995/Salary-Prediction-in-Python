#!/usr/bin/env python
# coding: utf-8

# # Salary Predictions Based on Job Descriptions

# The goal of the project is to predict salaries based on job descriptions.There are different factors affecting the salary of job like degree, job type, designation,educations and years of experience.
# We will build a model that will consider all the factors availabe in the data and predict salaries accordingly and thereby
# help companies in deciding the salaries of new hires.

# ### Importing necessary package libraries

# In[49]:


# Import the required libraries

import pandas as pd
import numpy as np

# Import libraries for visualization
import matplotlib.pyplot as plt
import seaborn as sns

# import libraries for preprocessing data
from sklearn.preprocessing import LabelEncoder

#Import libraries for data Modelling
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import ExtraTreesRegressor
import lightgbm
from lightgbm import LGBMRegressor
from sklearn.model_selection import RandomizedSearchCV
from sklearn.metrics import mean_squared_error
import lightgbm

# Ignore deprecation warnings in sklearn
import warnings
warnings.filterwarnings('ignore')
import pickle


# ### Define class for initial data loading and exploratory data analysis

# In[50]:


class Data:

    def __init__(self, train_features, train_target, test_features, target_col):
        ''' The class is used to for  processes  like data load, merge and expolartory data analysis.
        This class accepts following 4 input:-

        train_features - path of file which contains features of training data
        train_target   - path of file which contains target of training data
        test_features  - path of which file contains features of test data
        target         - name of target column'''

        self.train_features= train_features
        self.train_target  = train_target
        self.test_features = test_features
        self.target_col       = target_col
        self.process_data()
        
    def process_data(self):
        self._create_train_df()
        self._create_test_df()
        self._find_column_stat()
        self._print_train_stats()
        self._verify_invalid_data(self.train_df, self.target_col)
        self._verify_duplicate_data()
        
    def _create_train_df(self):
        ''' The function loads Train data'''
        train_features_df = self._load_csv(train_features)
        train_target_df = self._load_csv(train_target)
        self.train_df = self._merge_df(train_features_df, train_target_df)
        
    def _create_test_df(self):
        ''' The function loads Test data'''
        self.test_df = self._load_csv(test_features)
        
    def _load_csv(self, file):
        ''' The function will load the csv file into a dataframe'''
        return pd.read_csv(file)
    
        
    def _find_column_stat(self):
        self.cat_cols = self._find_cat_cols(self.train_df)
        self.num_cols = self._find_num_cols(self.train_df)

    def _print_train_stats(self):
        print(' \n --------------- Train Data Statistics --------------------')
        self.print_stats(self.train_df)
        self._verify_nan(self.train_df)

    def _print_test_stats(self):
        print('\n --------------- Test Data Statistics --------------------')
        self.print_stats(self.test_df)

    
    def _merge_df(self, df1, df2):
        ''' This method will merge 2 dataframes '''
        return pd.merge(df1, df2)

    def print_stats(self, df):
        print('-------------------------------------------------')
        print('Number of rows and columns of the Dataframe - {}'.format(df.shape))
        print('-------------------------------------------------')
        print('\n Dataframe information:- \n')
        print('\n{}'.format(df.info()))
        print('-------------------------------------------------')
        print(' Statistical summary  of Numerical data variables :- \n \n{}'.format(df.describe()))
        print('-------------------------------------------------')
        print(' Statistical summary of Categorical data variables :- \n \n{}'.format(df.describe(include='O')))

    def _verify_nan(self, df):
        '''The  functions checks the presence of any null values in a dataframe'''
        nan = np.sum(df.isna().sum())
        if nan == 0:
            print('\n\n --> There are no Null values in the dataframe')
        else:
            print('Following columns have null values in dataframe\n\n{}'
                  .format(df.isnull().sum()))
            
    def _find_cat_cols(self, df):
        '''The function extracts  the categorical columns in a dataset'''
        self.cat_cols = df.select_dtypes(include=['O']).columns.tolist()
        print('-----------------------------------------')
        print('List of all Categorical variables  in the  data:- {}'
              .format(self.cat_cols))
        print('-----------------------------------------')
        return self.cat_cols

    def _find_num_cols(self, df):
        '''The function extracts the numerical columns in a dataset'''
        num_cols = df.select_dtypes(exclude=['O']).columns.tolist()
        print('List of all Numerical variables in the  data:- {}'
              .format(num_cols))
        print('-----------------------------------------')
        return num_cols
    
    
    def _verify_invalid_data(self, df, cols):
        ''' This function is used to find outlier  values in various columns of dataframe'''
        for col in [cols]:
            val_cnt = np.sum(df[col] <= 0)
            if val_cnt > 0:
                self.invalid_flag = True
                print('\n ---> There are {} invalid values are present in {} column'.format(val_cnt, col))

    def _verify_duplicate_data(self):
        '''The functions checks for any duplicate values in the dataset '''
        print('\n ---> There are {} duplicate values are present in  the Training data'
              .format(self.train_df.duplicated().sum()))
        


# ### Define class to conduct exploratory data analysis and plot variables

# In[51]:


class DrawPlot:

    sns.set(style="whitegrid")

    def __init__(self, data):
        self.data = data
        self.train_df = data.train_df
        self.target_col = data.target_col
        self.cat_cols = data.cat_cols
        self.num_cols = data.num_cols
        self.cor_cols = ['jobType_mean', 'degree_mean', 'major_mean', 'industry_mean',
                         'companyId_mean', 'yearsExperience', 'milesFromMetropolis', 'salary']
        self.target_col = data.target_col
        self.process_eda()

    def process_eda(self):
        self._DistPlot()
        self._BoxPlot()
        self._Heatmap()

    def _DistPlot(self):
        '''The function  plots the histogram of all numeric variables in dataframe'''
        fig = plt.figure(figsize=(14, 14))
        for idx, col in enumerate(self.num_cols):
            fig.add_subplot(len(self.num_cols), len(self.num_cols), idx+1)
            sns.distplot(self.train_df[col], bins=10)
            plt.tight_layout()

    def _BoxPlot(self):
        '''The function  plot the Box plots of all Categorical variables in dataframe'''
        df = self.train_df.copy()
        fig = plt.figure(figsize=(14, 18))
        for idx, col in enumerate(self.cat_cols):
            if len(self.train_df[col].unique()) < 10:
                df[col +
                    '_mean'] = df.groupby(col)[self.target_col].transform('mean')
                fig.add_subplot(3, 2, idx+1)
                sns.boxenplot(x=col, y=self.target_col,
                              data=df.sort_values(col + '_mean'))
                plt.title('Comparison of salaries as per {}'.format(
                    col), fontsize=14)
                plt.tight_layout()
                plt.xticks(rotation=45)

    def _Heatmap(self):
        '''The function  plots the correlation between all numeric variables in dataframe'''
        df = self.train_df.copy()
        for col in self.cat_cols:
            if len(self.train_df[col].unique()) < 100:
                df[col +
                    '_mean'] = df.groupby(col)[self.target_col].transform('mean')
        fig = plt.figure(figsize=(12,8))
        sns.heatmap(df[self.cor_cols].corr(), annot=True)
        plt.tight_layout()
        plt.title('Correlation Matrix', fontsize=16)
        plt.xticks(rotation=45)


# In[52]:





# # Feature engineering and Data preprocessing 

# In[53]:


class FeatureEngg:
    '''The class will perform Feature Engineering such as Label Encoding, data cleaning, Impute missing  values etc.'''

    def __init__(self, data):
        self.data = data
        self.target = data.target_col
        self.invalid_flag = data.invalid_flag
        self.function = {'group_mean': 'mean', 'group_median': 'median',
                         'group_max': 'max', 'group_min': 'min', 'group_mad': 'mad'}
        self.cat_cols = ['jobType', 'degree', 'major', 'industry', 'companyId']
        self.impute_cols = ['jobType', 'industry', 'degree', 'major']
        self.id_col = 'jobId'
        self.labels = {}
        self._process_feature_engg()

    def _process_feature_engg(self):
        self._Feature_engg_train_df()
        self._Feature_engg_test_df()

    def _Feature_engg_train_df(self):
        if self.invalid_flag:
            self._clean_df()
        train_df = self._Label_Encoder(data.train_df, self.cat_cols)
        self.train_df = self.drop_cols(train_df, self.id_col)
        groupby_df = self._create_groupby(self.train_df, self.cat_cols)
        self.group_df = self._calc_group_stats(groupby_df, data.target_col)
        self.data.train_df = self._merge_groupby(
            self.train_df, self.group_df, self.cat_cols)

    def _Feature_engg_test_df(self):
        test_df = self._Label_Encoder(
            data.test_df, self.cat_cols, test_data=True)
        self.test_df = self.drop_cols(test_df, self.id_col)
        self.test_df = self._merge_groupby(
            self.test_df, self.group_df, self.cat_cols)
        self.data.test_df = self._impute_nan(self.test_df, self.function)

    def _Label_Encoder(self, df, cols, test_data=False):
        ''' This method creates label encoding for categorical data'''
        if not test_data:
            for col in cols:
                le = LabelEncoder()
                le.fit(df[col])
                self.labels[col] = le
                df[col] = le.transform(df[col])
        else:
            for col, le in self.labels.items():
                df[col] = le.transform(df[col])
        return df

    def drop_cols(self, df, cols):
        df = df.drop(columns=cols, axis=1)
        return df

    def _clean_df(self):
        print('In this dataframe some invalid values are present in salary column. we need to drop those  values \n')
        print('Shape of Dataframe before change:- {}'.format(data.train_df.shape))
        data.train_df = data.train_df[data.train_df['salary'] > 0]
        data.train_df.reset_index()
        print('Shape of Dataframe after dropping invalid rows:- {}'.format(
            data.train_df.shape, data.train_df.shape[0]))

    def _create_groupby(self, df, cols):
        df = df.groupby(cols)
        return df

    def _merge_groupby(self, df1, df2, keys):
        return pd.merge(df1, df2, on=keys, how='left')

    # Calculate group statistics of groups
    def _calc_group_stats(self, df, target):
        group_df = pd.DataFrame({'group_mean': df[target].mean()})
        group_df['group_median'] = df[target].median()
        group_df['group_max'] = df[target].max()
        group_df['group_min'] = df[target].min()
        group_df['group_mad'] = df[target].mad()
        group_df.reset_index(inplace=True)
        return group_df

    def _impute_nan(self, df, function):
        ''' There are some missing values present in test data in newly created features. From the 
        correlation plot,we knew that, correaltion of company id & salary is very minimum. So, we 
        have filled that missing values by taking group of other 4 columns. This imputer function 
        is specifc to this project'''
        for col, func in function.items():
            df[col] = df[col].fillna(df.groupby(
                self.impute_cols)[col].transform(func))
        return df


# # Build  models and evaluate models to predict output responses

# In[54]:


class Eval_Model:
    '''This class will perform model evaluation based on Mean Square Error. 
    MSE -  It is the average squared difference between the estimated values and the actual value.
    In this class we have defined a baseline model, which considers group_mean as predicted value and we 
    are using the cross validation technique to calculate the MSE of 3 different models and then using 
    best model to calculate the Best model out of 3 (Linear Regreesion, Extra Tree Regression & 
    Light GBM Regression).'''

    def __init__(self, data, models):
        self.data = data
        self.models = models
        self.mean_mse = {}
        self.best_model = None
        self.prediction = None
        self.target_col = data.target_col
        self.base_target_df = data.train_df.group_mean
        self.target_df = data.train_df[data.target_col]
        self.feature_df = data.train_df.drop(data.target_col, axis=1)
        self.test_df = data.test_df
        self._process_models()

    def _process_models(self):
        self._baseline_model()
        self._cross_validate_model()
        self._best_model_process()

    def _baseline_model(self):
        '''For any baseline model, We can calculate the Mean of target, which is a good estimate.
        In this project, we had alreay calculated 'group_mean' of target, so, We have used the same for 
        baseline model'''
        self.mean_mse['Baseline_model'] = mean_squared_error(
            self.target_df, self.base_target_df)

    def _cross_validate_model(self, cv=3):
        print('\nCross Validation in progress.......')
        for model in self.models:
            scores = cross_val_score(
                model, self.feature_df, self.target_df, cv=cv, scoring='neg_mean_squared_error')
            self.mean_mse[model] = -1.0*np.mean(scores)

    def _best_model_process(self):
        '''This method will select the best model and perform fit on train data'''
        self.best_model = min(self.mean_mse, key=self.mean_mse.get)
        self._print_model_stats()
        print('\nFitting the Best Model.....')
        self.best_model.fit(self.feature_df, self.target_df)
        self._plot_feature_importance()
        print('\nPredicting on test data using the Best Model')
        self.test_df[self.target_col] = self.best_model.predict(self.test_df)

    def _print_model_stats(self):
        'This method will print the statistics of model'
        print('Models Statistics.......')
        for key, item in self.mean_mse.items():
            print('    \n Score of model {} :-'.format(key))
            print('\n          MSE - {}'.format(item))
        print('\n Best model is --------->\n\n {} :-'.format(self.best_model))
        print('\n          MSE - {}'.format(self.mean_mse[self.best_model]))

    def _plot_feature_importance(self):
        '''This method prints the feature importance used to train model'''
        print('\nPredicting Feature Importances')
        features = self.feature_df.columns.to_list()
        importances = self.best_model.feature_importances_
        indices = np.argsort(importances)
        plt.figure(figsize=(6, 6))
        plt.title('Feature Importances')
        plt.barh(range(len(indices)),
                 importances[indices], color='b', align='center')
        plt.yticks(range(len(indices)), [features[i] for i in indices])
        plt.xlabel('Relative Importance')
        plt.show()

    @staticmethod
    def save_results(sub_file, df):
        print('\nSaving the predictions to a CSV file')
        df.to_csv(sub_file, index=False)

    @staticmethod
    def save_best_model(model_file, model):
        '''This model save the best model to a file'''
        print('\nSaving the Best Model to a file')
        pickle.dump(model, open(model_file, 'wb'))

    @staticmethod
    def tune_hyperparameter(estimator, param_grid, n_iter=5, scoring='neg_mean_absolute_error', cv=5, n_jobs=-2, refit=False):
        ''' This method is used to find the hyperparameters used in models'''
        rs_cv = RandomizedSearchCV(estimator=estimator, param_distribution=param_grid,
                                   n_iter=n_iter,
                                   cv=cv,
                                   n_jobs=n_jobs,
                                   refit=refit)
        rs_cv.fit(feature_df, target_df)
        return rs_cv.best_params_


# ### Define parameters to initiate class

# In[55]:


# Defining parameters to instantiate and load Data
train_features = 'C:/Users/jjosh/Desktop/Salary prediction R/Input files/train_features.csv'
train_target = 'C:/Users/jjosh/Desktop/Salary prediction R/Input files/train_salaries.csv'
test_features = 'C:/Users/jjosh/Desktop/Salary prediction R/Input files/test_features.csv'
target_col = 'salary'


# ### Basic statisitcs of the data

# In[56]:


# create an instance of data object
data = Data(train_features, train_target, test_features, target_col)


# ### Create plots and instantiate it to visualize insight of data

# In[57]:


plot = DrawPlot(data)    


# ### Instantiate Feature engineering class and preprocessing data

# In[58]:


Feature_engineering = FeatureEngg(data)


# ### Evaluation of Models and selecting best model

# In[59]:


# Here we have defined 3 different algorithms i.e Linear Regression, ExtraTreeRegressor and LightGBMregressor
# ExtraTreeRegressor and LightGBMRegressor are Ensemble methods and we have tuned their hyperparameters.
lr = LinearRegression()
etr = ExtraTreesRegressor(n_estimators=40, max_depth=12,
                          min_samples_split=2,  min_samples_leaf=2, random_state=42)
lgbm = LGBMRegressor(colsample_bytree=0.8, max_depth=-1,
                     n_estimators=2000, num_leaves=15, subsample=1.0)

models = [lr, etr, lgbm]

model = Eval_Model(data, models)


# ### Saving submission output results
# 

# In[61]:


sub_file = 'C:/Users/jjosh/Desktop//Salary_Prediction_Submission.csv'
model.save_results(sub_file,model.test_df)


# In[ ]:




