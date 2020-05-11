# Salary Prediction in Python
 Prediction of salary by Job description using Python
 
 # Summary 

The goal of the project is to predict salaries based on job descriptions. There are certain factors affecting  the prediction of salary like Education, degree ,Major , years of experience ,distance from metro city and  designation in the company.The project will help candidates to estimate their current salary and to predict their new salary if they wanted to change job .Moreover ,the project will help the companies to predcit the salaries of new hires.

# About the data

There are three files of input data : train_features, test_features, train_salaries.
The training data is split into two files namely train_features and train_salaries. Following are the features and their descriptions:

* JobId: The Id of job. It is unique for every employee.
*	companyid: The Id of company.
* JobType: The designation in the company.
* degree: Highest degree of a Employee.
* major: The field or subject on which, employee had completed his/her degree from university.
* industry: The field of company like Health, Finance, Oil etc.
* YearsofExperience: Years of Experiene of an Employee in the job.
* milesFromMetropolis: The distance in miles, the employee lives away from his/her office.
* salary: This is the target variable. It is the amount each employee receives.

# Descriptive statistics
![alt text](https://github.com/jjoshua1995/Salary-Prediction-in-R/blob/master/Figures/Descriptive%20stats.PNG)


# Exploratory data analysis

The target variable is distributed normally.The value ranges from 0 to 300k.

There are two variable which are continous variables.Below are the boxplots of milesFromMetropolis and yearsOfExperience 
showing there are not outliers in these variables.

![alt text](https://github.com/jjoshua1995/Salary-Prediction-in-Python/blob/master/Figures/Histogram.png)

Similarly , the exploratory data analysis has been conducted for all the categorical variables similar to the numerical variables.
Below plot shows the frequency analysis of jobs by degree wise.

![alt text](https://github.com/jjoshua1995/Salary-Prediction-in-Python/blob/master/Figures/boxplot_Jobtype.png)

![alt text](https://github.com/jjoshua1995/Salary-Prediction-in-Python/blob/master/Figures/boxplot_degree.png)


# Correlation analysis

Correlation analysis test are conducted to see any underlying relation exists between the variables in the data.
For numeric variables, normal correlation test is done and for categorical variables , analysis of variance tests are done.

Below plot is  the correlation matrix  for the numeric variables, where salary and years of experience are positive  correlated
and miles from metroplois and salary are negatively correlated.

![alt text](https://github.com/jjoshua1995/Salary-Prediction-in-Python/blob/master/Figures/Correlation%20Matrix.png)

For the categorical variables , correlation test cannot be conducted since they are not numeric variables.Hence ANOVA test is conducted
to see if the categories show any realtion to the target variable.

Below are the plots of various categories and the relation with the target variable.
Intrestingly ,all category variable thorugh ANOVA test show significant results to the target variable.

![alt text](https://github.com/jjoshua1995/Salary-Prediction-in-Python/blob/master/Figures/boxplot_industry.png)

![alt text](https://github.com/jjoshua1995/Salary-Prediction-in-Python/blob/master/Figures/boxplot_major.png)

Major - Engineering degree candiadtes gets highest salary and NONE category has lowest salary.

Degree- Doctoral degree candidates gets higher salaries and NONE category gets lowest salary.

Jobtype- CEO position has highest salary, whereas Janitor has lowest. The salary increase rapidly according to level of jobType.

Industry- The Finance & Oil are highest paying industries. 


# Data Preprocessing

There are some outliers in the target variable (Salary) since 0 cannot be a value in the target variable.So, outliers are removed from the training data.
Also , the features are converted to their respective data types.ie) category type variables are converted from character type to factor 
type variables.


# Feature Engineering 

Label encoding is applied to transform categorical features into numeric features. To enhance the performance of the models, following new features have been created by grouping Jobtype, degree, major, industry and companyId columns:

* group_mean :- Average salary of the group.
* group_median :- Median salary of the group.
* group_max :- Maximum salary of the group.
* group_min :- Minimum salary of the group.

# Model development

### Evaluation metric

To measure the effectiveness of the models that we are going to develop, we have used mean squared error (MSE) as evaluation metric.

### Baseline model

For any baseline model, We can calculate the average of target variable, which is a good estimate. In this project, we had already calculated 'group_mean' of target variable. So, we have used the same for our baseline model.

The mean MSE error obtained is :- 644.256325

### Best model selection

For this regression task, 3 different machine learning algorithms were selected, one linear and two ensembles, to see which performs better for the problem:

* Linear Regressor.
* Extra Tree Regressor.
* LightGBM Regressor.

We have tuned both ensemble models and following results have been achieved:

| Model                | MSE |
|----------------------|-----|
| Linear Regression    | 384 |
| ExtraTree Regression | 316 |
| LightGBM Regression  | 307 |


The lowest MSE error was returned by LightGBM Regressor. Once the best model was fitted with the train data, the feature importance generated by the model are following:

![alt text](https://github.com/jjoshua1995/Salary-Prediction-in-Python/blob/master/Figures/Feature_Importances.png)

# Conclusion

We can conclude that we have developed a model with MSE of 307.094494, to predict the salary based on the features given and newly generated features.

Salary varies according to the following:

* Salary decreases linearly with miles away from city
* Salary increases linearly with years of experience
* Job position: CEO > CTO, CFO > VP > Manager > Senior > Junior > Janitor
* Oil and finance industries are the highest paying sectors, while service and education are the lowest paying.

We can further try to improve the model by generating new features from 'yearsofExperience' and 'Milesfrom Metropolis' columns.



