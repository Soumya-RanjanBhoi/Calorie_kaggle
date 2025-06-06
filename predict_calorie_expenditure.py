# -*- coding: utf-8 -*-
"""Predict Calorie Expenditure.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1U6g9LcfSskbeS7rC09eQDgrCuuHBVqMJ
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

df_train=pd.read_csv("/content/calorie_exp kaggle train.csv")
df_test=pd.read_csv("/content/calorie_exp kaggle test.csv")

df_test.shape

df_train.shape

df_train.sample(10)

df_train.shape

df_train.info()

df_train.isnull().sum()

df_train["Calories"]=df_train["Calories"].fillna(df_train["Calories"].mean())

from ydata_profiling import ProfileReport
p=ProfileReport(df_train)
p.to_file(output_file="Data Analysis")

!pip install ydata-profiling

col=['Age', 'Height', 'Weight', 'Duration', 'Heart_Rate',
       'Body_Temp', 'Calories']

plt.figure(figsize=(14,7))
sns.boxplot(df_train[col])

for coln in col:
  Q1=df_train[coln].quantile(.25)
  Q3=df_train[coln].quantile(.75)

  IQR=Q3-Q1

  lower_bound= Q1 - IQR * 1.5
  upper_bound= Q3 + IQR *1.5

  df_train[coln] = np.where(
      df_train[coln]>upper_bound,
      upper_bound,
      np.where(
          df_train[coln]<lower_bound,
          lower_bound,
          df_train[coln]
      )
  )

plt.figure(figsize=(14,7))
sns.boxplot(df_train[col])

X=df_train.drop(["Calories"],axis=1)
y=df_train["Calories"]

from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import StandardScaler

col

coln_transformer=ColumnTransformer([
    ("tsf1",StandardScaler(),["id"]),
    ("tsf2",SimpleImputer(strategy="mean"),["Body_Temp"]),
    ("tsf3",OneHotEncoder(sparse_output=False,drop="first"),["Sex"])
],remainder="passthrough")

from sklearn.model_selection import train_test_split

x_train,x_test,y_train,y_test=train_test_split(X,y,test_size=0.4,random_state=42)

x_train=coln_transformer.fit_transform(x_train)
x_test=coln_transformer.transform(x_test)

X=coln_transformer.fit_transform(X)

from sklearn.model_selection import cross_val_score

!pip install optuna

from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor,AdaBoostRegressor
from sklearn.linear_model import LinearRegression

import optuna

def objective(trial):
    classifier_name = trial.suggest_categorical("classifier_name", [
        "RandomForestRegressor", "GradientBoostingRegressor"
    ])

    if classifier_name == "RandomForestRegressor":
        n_estimators = trial.suggest_int("n_estimators", 100, 500)
        criterion = trial.suggest_categorical("criterion", [
            "squared_error", "absolute_error", "friedman_mse", "poisson"
        ])
        bootstrap = trial.suggest_categorical("bootstrap", [True, False])
        max_samples = trial.suggest_float("max_samples", 0.2, 1.0) if bootstrap else None
        max_features = trial.suggest_float("max_features", 0.3, 1.0)

        model = RandomForestRegressor(
            n_estimators=n_estimators,
            criterion=criterion,
            bootstrap=bootstrap,
            max_samples=max_samples,
            max_features=max_features
        )

    elif classifier_name == "GradientBoostingRegressor":
        loss = trial.suggest_categorical("loss", [
            "squared_error", "absolute_error", "huber", "quantile"
        ])
        learning_rate = trial.suggest_float("learning_rate", 0.1, 1.0)
        n_estimators = trial.suggest_int("n_estimators", 100, 500)
        subsample = trial.suggest_float("subsample", 0.2, 1.0)
        max_features= trial.suggest_float("max_samples", 0.5, 1.0)

        model = GradientBoostingRegressor(
            loss=loss,
            learning_rate=learning_rate,
            n_estimators=n_estimators,
            subsample=subsample,
            max_features=max_features
        )

    score = cross_val_score(model, x_train,y_train, cv=2).mean()
    return score

study=optuna.create_study(direction="maximize",sampler=optuna.samplers.TPESampler())
study.optimize(objective,n_trials=50)



model2=GradientBoostingRegressor(
    loss="squared_error",
    n_estimators=500,
    subsample=0.8,
    max_features=0.7

)

model2.fit(x_train,y_train)

y_pred2=model2.predict(x_test)

r2_score(y_test,y_pred2)

model_=RandomForestRegressor(
    n_estimators=307,
    criterion="friedman_mse",
    bootstrap=True,
    max_samples=0.9,
    max_features=0.53
)

model_.fit(x_train,y_train)

from sklearn.metrics import r2_score

y_pred=model_.predict(x_test)

r2_score(y_test,y_pred)

df_test

id=df_test["id"].sort_values()

df_test.isnull().sum()

coln_transformer_1=ColumnTransformer([
    ("tsf1",StandardScaler(),["id"]),
    ("tsf2",SimpleImputer(strategy="mean"),["Body_Temp","Weight","Duration","Heart_Rate"]),
    ("tsf3",OneHotEncoder(sparse_output=False,drop="first"),["Sex"])
],remainder="passthrough")

df_test.columns

col1=['Age', 'Height', 'Weight', 'Duration', 'Heart_Rate',
       'Body_Temp']

plt.figure(figsize=(14,7))
sns.boxplot(df_test[col1])

for coln in col1:
  Q1=df_test[coln].quantile(.25)
  Q3=df_test[coln].quantile(.75)

  IQR=Q3-Q1

  lower_bound= Q1 - IQR * 1.5
  upper_bound= Q3 + IQR *1.5

  df_test[coln] = np.where(
      df_test[coln]>upper_bound,
      upper_bound,
      np.where(
          df_test[coln]<lower_bound,
          lower_bound,
          df_test[coln]
      )
  )

df_test=coln_transformer_1.fit_transform(df_test)

model_.predict(df_test)

predictions_df = pd.DataFrame({"id":id ,'Calories': model_.predict(df_test)})
predictions_df.head(5)

predictions_df.shape

predictions_df.to_csv('pred_kaggle_comp-2.csv', index=False)

predictions_df2 = pd.DataFrame({"id":id ,'Calories': model2.predict(df_test)})
predictions_df2.head(5)

predictions_df2.to_csv('model-2-pred.csv', index=False)

model3=GradientBoostingRegressor(
    loss='absolute_error',
    learning_rate= 0.16625122472816245,
    n_estimators= 263,
    subsample=0.8941961094380628,
    max_features= 0.7957330182374482
)

model3.fit(x_train,y_train)

y_pred3=model3.predict(x_test)
r2_score(y_test,y_pred3)

prediction3=pd.DataFrame({"id":id,"Calories":model3.predict(df_test)})
print(prediction3.head(5))

prediction3.to_csv("model-3.csv",index=False)

from sklearn.ensemble import VotingRegressor

from sklearn.tree import DecisionTreeRegressor

models=[
    ("models1",GradientBoostingRegressor(loss='absolute_error', learning_rate= 0.16625122472816245, n_estimators= 263,subsample=0.8941961094380628,
    max_features= 0.7957330182374482) ),

    ("models2",RandomForestRegressor(n_estimators=307,criterion="friedman_mse",bootstrap=True,max_samples=0.9,max_features=0.53)),

    ("models3",DecisionTreeRegressor())
]

model4=VotingRegressor(
    estimators=models

)

model4.fit(x_train,y_train)

y_pred4=model4.predict(x_test)

r2_score(y_test,y_pred4)

prediction3=pd.DataFrame({"id":id,"Calories":model4.predict(df_test)})
print(prediction3.head(5))

prediction3.to_csv("model-4.csv",index=False)

