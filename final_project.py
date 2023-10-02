# -*- coding: utf-8 -*-
"""Final_project.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ZNnE67GV03gHKOdpWLY0bKJijpCWdUSG

# **Health Insurance Cost Prediction**

Run all the cells using 'Run All' Options in the Runtime
"""

# Import necessary libraries and modules
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.subplots as sp
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import r2_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV
from xgboost import XGBRegressor

# Uncomment the following line to install the 'feature-engine' library
#!pip install feature-engine

# Import 'feature-engine' library for feature engineering tasks
import feature_engine
from feature_engine.outliers import ArbitraryOutlierCapper

# Suppress warnings
import warnings
warnings.filterwarnings('ignore')

# Load the dataset from a CSV file named 'health_insurance.csv'
data=pd.read_csv('health_insurance.csv') #I have changed the datset name, health insurance(indent) - with underscore to avoid mistakes
data

# Check the basic information about the dataset
data.info()

# Check the description of the dataset
data.describe()

# Check the missing values in the dataset
data.isnull().sum()

# features of the dataset
features = ['sex', 'smoker', 'region']

# Create a subplot grid with 'pie' subplot type
fig = sp.make_subplots(rows=1, cols=len(features), subplot_titles=features, specs=[[{'type':'pie'}]*len(features)])

for i, col in enumerate(features):
    x = data[col].value_counts()
    fig.add_trace(go.Pie(
        labels=x.index,
        values=x.values,
        textinfo='percent+label',
        hole=0.3,
    ), row=1, col=i+1)

# Update the layout to improve the appearance
fig.update_layout(
    title_text='Distribution of Categorical Features',
    showlegend=False,
    height=400,
    width=1200,
)

fig.show()

# features of the dataset
features = ['sex', 'children', 'smoker', 'region']

# Create subplots
fig = make_subplots(rows=2, cols=2, subplot_titles=features)

for i, col in enumerate(features):
    row = (i // 2) + 1
    col_num = (i % 2) + 1

    # Create a bar plot for mean 'charges' grouped by the current feature
    df = data.groupby(col).mean()['charges']
    bar_chart = go.Bar(x=data.index, y=data.values, name='Mean Charges')

    # Add the bar chart to the subplot
    fig.add_trace(bar_chart, row=row, col=col_num)

# Update the layout to improve the appearance
fig.update_layout(
    title_text='Mean Charges by Categorical Features',
    showlegend=False,
    height=600,
    width=1000,
)

# Show the interactive plot
fig.show()

# features of the dataset
features = ['age', 'bmi']

# Create an interactive scatter plot using Plotly Express
fig = px.scatter(data, x=features[0], y='charges', color='smoker', labels={'charges': 'Charges'}, title='Scatter Plot of Charges vs. Age and BMI')

# Add the second scatter plot
fig.add_scatter(x=data[features[1]], y=data['charges'], mode='markers', marker=dict(size=5, opacity=0.5), name='Non-smoker')

# Update the layout
fig.update_layout(
    showlegend=True,
    xaxis_title=features[0],
    yaxis_title='Charges',
    height=400,
    width=800,
)

# Show the interactive plot
fig.show()

# Create a box plot of the 'age' variable using Plotly Express
fig = px.box(data, y='age', title='Box Plot of Age', color_discrete_sequence=['#FF5733'])

# Customize the layout of the plot
fig.update_layout(
    xaxis_title='',
    yaxis_title='Age',
    height=400,
    width=600,
)

# Show the interactive plot
fig.show()

# Create a box plot of the 'bmi' variable using Plotly Express
fig = px.box(data, y='bmi', title='Box Plot of BMI', color_discrete_sequence=['#FF5733'])

# Customize the layout of the plot
fig.update_layout(
    xaxis_title='',
    yaxis_title='BMI',
    height=400,
    width=600,
)
# Show the interactive plot
fig.show()

# Calculate the first quartile (Q1), second quartile (Q2 or median), and third quartile (Q3)
Q1 = data['bmi'].quantile(0.25)
Q3 = data['bmi'].quantile(0.75)

# Calculate the interquartile range (IQR)
iqr = Q3 - Q1

# Calculate the lower limit for outliers
lowlim = Q1 - 1.5 * iqr

# Calculate the upper limit for outliers
upplim = Q3 + 1.5 * iqr

# Print the lower and upper limits for outliers
print("Lower Limit for Outliers:", lowlim)
print("Upper Limit for Outliers:", upplim)

# Initialize ArbitraryOutlierCapper with minimum and maximum capping values for 'bmi'
arb = ArbitraryOutlierCapper(min_capping_dict={'bmi': 13.6749}, max_capping_dict={'bmi': 47.315})

# Apply outlier capping to the 'bmi' variable in the DataFrame
data[['bmi']] = arb.fit_transform(data[['bmi']])

# Create a box plot to visualize the 'bmi' variable after outlier capping
fig = px.box(data, y='bmi', title='Box Plot of BMI (After Outlier Capping)', color_discrete_sequence=['#FF5733'])

# Customize the plot layout
fig.update_layout(
    xaxis_title='',          # Remove x-axis label
    yaxis_title='BMI',      # Set y-axis label to 'BMI'
    height=400,             # Set the plot height
    width=600               # Set the plot width
)

# Show the interactive box plot
fig.show()

# Calculate and print the skewness of the 'bmi' variable
a = data['bmi'].skew()
print("Skewness of BMI in the data:", a)

# Calculate and print the skewness of the 'age' variable
b = data['age'].skew()
print("Skewness of Age in the data:", b)

# Map 'sex' column to numerical values
data['sex'] = data['sex'].map({'male': 0, 'female': 1})

# Map 'smoker' column to numerical values
data['smoker'] = data['smoker'].map({'yes': 1, 'no': 0})

# Map 'region' column to numerical values
data['region'] = data['region'].map({'northwest': 0, 'northeast': 1, 'southeast': 2, 'southwest': 3})

# Calculate the correlation matrix
corr_matrix = data.corr()

# Create an interactive correlation plot using Plotly Graph Objects
fig = go.Figure(data=go.Heatmap(
    z=corr_matrix.values,
    x=list(corr_matrix.columns),
    y=list(corr_matrix.index),
    colorscale='Viridis',  # You can choose a different color scale
))

# Update the layout of the figure
fig.update_layout(
    title_text='Correlation Heatmap',  # Set the title of the plot
    xaxis_title='Features',  # Label for the x-axis
    yaxis_title='Features',  # Label for the y-axis
    height=500,  # Set the height of the plot
    width=700,  # Set the width of the plot
)

# Show the interactive plot
fig.show()

corr_matrix #observe the corr_matrix

# 'X' as features and 'Y' as the target variable
X=data.drop(['charges'],axis=1)
Y=data[['charges']]

# Initialize empty lists to store results
l1 = []  # List to store training accuracy
l2 = []  # List to store test accuracy
l3 = []  # List to store cross-validation scores

cvs = 0  # Initialize cross-validation score

# Loop through different random states (from 40 to 49)
for i in range(40, 50):
    # Split the data into training and testing sets
    xtrain, xtest, ytrain, ytest = train_test_split(X, Y, test_size=0.2, random_state=i)

    # Initialize and fit a Linear Regression model
    lrmodel = LinearRegression()
    lrmodel.fit(xtrain, ytrain)

    # Calculate and append the training accuracy
    l1.append(lrmodel.score(xtrain, ytrain))

    # Calculate and append the test accuracy
    l2.append(lrmodel.score(xtest, ytest))

    # Calculate cross-validation score using 5-fold cross-validation and update 'cvs'
    cvs = (cross_val_score(lrmodel, X, Y, cv=5)).mean()
    l3.append(cvs)

# Create a DataFrame to store and display the results
df1 = pd.DataFrame({'train acc': l1, 'test acc': l2, 'cvs': l3})

# Display the DataFrame with results
df1

# Split the data into training and testing sets with a fixed random state (42)
xtrain, xtest, ytrain, ytest = train_test_split(X, Y, test_size=0.2, random_state=42)

# Initialize a Linear Regression model
lrmodel = LinearRegression()

# Fit the Linear Regression model on the training data
lrmodel.fit(xtrain, ytrain)

# Print the R-squared (coefficient of determination) score for the training set
print("Training R-squared:", lrmodel.score(xtrain, ytrain))

# Print the R-squared (coefficient of determination) score for the test set
print("Test R-squared:", lrmodel.score(xtest, ytest))

# Calculate and print the mean cross-validation score using 5-fold cross-validation
cross_val_mean = cross_val_score(lrmodel, X, Y, cv=5).mean()
print("Cross-Validation Mean:", cross_val_mean)

# Initialize a Support Vector Regressor (SVR) model
svrmodel = SVR()

# Fit the SVR model on the training data
svrmodel.fit(xtrain, ytrain)

# Predict the target values for the training and test sets
ypredtrain1 = svrmodel.predict(xtrain)
ypredtest1 = svrmodel.predict(xtest)

# Calculate and print the R-squared (coefficient of determination) score for the training set
print("Training R-squared:", r2_score(ytrain, ypredtrain1))

# Calculate and print the R-squared score for the test set
print("Test R-squared:", r2_score(ytest, ypredtest1))

# Calculate and print the mean cross-validation score using 5-fold cross-validation
cross_val_mean = cross_val_score(svrmodel, X, Y, cv=5).mean()
print("Cross-Validation Mean:", cross_val_mean)

# Initialize a RandomForestRegressor model with a random state
rfmodel = RandomForestRegressor(random_state=42)

# Fit the RandomForestRegressor model on the training data
rfmodel.fit(xtrain, ytrain)

# Predict the target values for the training and test sets
ypredtrain2 = rfmodel.predict(xtrain)
ypredtest2 = rfmodel.predict(xtest)

# Calculate and print the R-squared score for the training set
print("Training R-squared:", r2_score(ytrain, ypredtrain2))

# Calculate and print the R-squared score for the test set
print("Test R-squared:", r2_score(ytest, ypredtest2))

# Calculate and print the mean cross-validation score using 5-fold cross-validation
cross_val_mean = cross_val_score(rfmodel, X, Y, cv=5).mean()
print("Cross-Validation Mean:", cross_val_mean)

# Define a grid of hyperparameters to search over
param_grid = {'n_estimators': [10, 40, 50, 98, 100, 120, 150]}

# Create a GridSearchCV object with the RandomForestRegressor model, hyperparameter grid, and scoring metric
grid = GridSearchCV(estimator=RandomForestRegressor(random_state=42), param_grid=param_grid, scoring="r2", cv=5)

# Fit the GridSearchCV object on the training data to find the best hyperparameters
grid.fit(xtrain, ytrain)

# Print the best hyperparameters found by the grid search
print("Best Hyperparameters:", grid.best_params_)

# Initialize a new RandomForestRegressor model with the best number of estimators
rfmodel = RandomForestRegressor(random_state=42, n_estimators=120)

# Fit the RandomForestRegressor model with the best hyperparameters on the training data
rfmodel.fit(xtrain, ytrain)

# Predict the target values for the training and test sets with the updated model
ypredtrain2 = rfmodel.predict(xtrain)
ypredtest2 = rfmodel.predict(xtest)

# Calculate and print the R-squared score for the training set with the updated model
print("Training R-squared (Updated Model):", r2_score(ytrain, ypredtrain2))

# Calculate and print the R-squared score for the test set with the updated model
print("Test R-squared (Updated Model):", r2_score(ytest, ypredtest2))

# Calculate and print the mean cross-validation score using 5-fold cross-validation with the updated model
cross_val_mean = cross_val_score(rfmodel, X, Y, cv=5).mean()
print("Cross-Validation Mean (Updated Model):", cross_val_mean)

# Import GradientBoostingRegressor and GridSearchCV from sklearn
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import GridSearchCV

# Initialize a GradientBoostingRegressor model
gbmodel = GradientBoostingRegressor()

# Fit the GradientBoostingRegressor model on the training data
gbmodel.fit(xtrain, ytrain)

# Predict the target values for the training and test sets
ypredtrain3 = gbmodel.predict(xtrain)
ypredtest3 = gbmodel.predict(xtest)

# Calculate and print the R-squared score for the training set
print("Training R-squared:", r2_score(ytrain, ypredtrain3))

# Calculate and print the R-squared score for the test set
print("Test R-squared:", r2_score(ytest, ypredtest3))

# Calculate and print the mean cross-validation score using 5-fold cross-validation
cross_val_mean = cross_val_score(gbmodel, X, Y, cv=5).mean()
print("Cross-Validation Mean:", cross_val_mean)

# Define a grid of hyperparameters to search over for GradientBoostingRegressor
param_grid = {'n_estimators': [10, 15, 19, 20, 21, 50], 'learning_rate': [0.1, 0.19, 0.2, 0.21, 0.8, 1]}

# Create a GridSearchCV object with the GradientBoostingRegressor model, hyperparameter grid, and scoring metric
grid = GridSearchCV(estimator=GradientBoostingRegressor(), param_grid=param_grid, scoring="r2", cv=5)

# Fit the GridSearchCV object on the training data to find the best hyperparameters
grid.fit(xtrain, ytrain)

# Print the best hyperparameters found by the grid search
print("Best Hyperparameters:", grid.best_params_)

# Initialize a new GradientBoostingRegressor model with the best hyperparameters
gbmodel = GradientBoostingRegressor(n_estimators=19, learning_rate=0.2)

# Fit the GradientBoostingRegressor model with the best hyperparameters on the training data
gbmodel.fit(xtrain, ytrain)

# Predict the target values for the training and test sets with the updated model
ypredtrain3 = gbmodel.predict(xtrain)
ypredtest3 = gbmodel.predict(xtest)

# Calculate and print the R-squared score for the training set with the updated model
print("Training R-squared (Updated Model):", r2_score(ytrain, ypredtrain3))

# Calculate and print the R-squared score for the test set with the updated model
print("Test R-squared (Updated Model):", r2_score(ytest, ypredtest3))

# Calculate and print the mean cross-validation score using 5-fold cross-validation with the updated model
cross_val_mean = cross_val_score(gbmodel, X, Y, cv=5).mean()
print("Cross-Validation Mean (Updated Model):", cross_val_mean)

# Initialize an XGBRegressor model
xgmodel = XGBRegressor()

# Fit the XGBRegressor model on the training data
xgmodel.fit(xtrain, ytrain)

# Predict the target values for the training and test sets
ypredtrain4 = xgmodel.predict(xtrain)
ypredtest4 = xgmodel.predict(xtest)

# Calculate and print the R-squared score for the training set
print("Training R-squared:", r2_score(ytrain, ypredtrain4))

# Calculate and print the R-squared score for the test set
print("Test R-squared:", r2_score(ytest, ypredtest4))

# Calculate and print the mean cross-validation score using 5-fold cross-validation
cross_val_mean = cross_val_score(xgmodel, X, Y, cv=5).mean()
print("Cross-Validation Mean:", cross_val_mean)

# Define a grid of hyperparameters to search over for XGBRegressor
param_grid = {'n_estimators': [10, 15, 20, 40, 50], 'max_depth': [3, 4, 5], 'gamma': [0, 0.15, 0.3, 0.5, 1]}

# Create a GridSearchCV object with the XGBRegressor model, hyperparameter grid, and scoring metric
grid = GridSearchCV(estimator=XGBRegressor(), param_grid=param_grid, scoring="r2", cv=5)

# Fit the GridSearchCV object on the training data to find the best hyperparameters
grid.fit(xtrain, ytrain)

# Print the best hyperparameters found by the grid search
print("Best Hyperparameters:", grid.best_params_)

# Initialize a new XGBRegressor model with the best hyperparameters
xgmodel = XGBRegressor(n_estimators=15, max_depth=3, gamma=0)

# Fit the XGBRegressor model with the best hyperparameters on the training data
xgmodel.fit(xtrain, ytrain)

# Predict the target values for the training and test sets with the updated model
ypredtrain4 = xgmodel.predict(xtrain)
ypredtest4 = xgmodel.predict(xtest)

# Calculate and print the R-squared score for the training set with the updated model
print("Training R-squared (Updated Model):", r2_score(ytrain, ypredtrain4))

# Calculate and print the R-squared score for the test set with the updated model
print("Test R-squared (Updated Model):", r2_score(ytest, ypredtest4))

# Calculate and print the mean cross-validation score using 5-fold cross-validation with the updated model
cross_val_mean = cross_val_score(xgmodel, X, Y, cv=5).mean()
print("Cross-Validation Mean (Updated Model):", cross_val_mean)

#comparing the performance of different regression models
# Initialize models
models = {
    'Linear Regression': LinearRegression(),
    'SVR': SVR(),
    'Random Forest': RandomForestRegressor(random_state=42, n_estimators=120),
    'Gradient Boosting': GradientBoostingRegressor(n_estimators=19, learning_rate=0.2),
    'XGBoost': XGBRegressor(n_estimators=15, max_depth=3, gamma=0)
}

results = []

# Train and evaluate each model
for model_name, model in models.items():
    xtrain, xtest, ytrain, ytest = train_test_split(X, Y, test_size=0.2, random_state=42)
    model.fit(xtrain, ytrain)
    ypred_train = model.predict(xtrain)
    ypred_test = model.predict(xtest)
    train_r2 = r2_score(ytrain, ypred_train)
    test_r2 = r2_score(ytest, ypred_test)
    cv_score = cross_val_score(model, X, Y, cv=5).mean()
    results.append({'Model': model_name, 'Train R-squared': train_r2, 'Test R-squared': test_r2, 'Cross-Validation R-squared': cv_score})

# Create a DataFrame from the results
df_results = pd.DataFrame(results)

# Create an interactive plot using Plotly Express
fig = px.bar(df_results, x='Model', y=['Train R-squared', 'Test R-squared', 'Cross-Validation R-squared'],
             title='Model Comparison',
             labels={'value': 'R-squared'},
             height=500)

# Customize the layout
fig.update_layout(barmode='group', xaxis_tickangle=-45)

# Show the interactive plot
fig.show()

feats = pd.DataFrame(data= grid.best_estimator_.feature_importances_, index=X.columns,columns=['Importance'])

# Create an interactive bar plot using Plotly Express with a vibrant color palette
fig = px.bar(feats, x=feats.index, y='Importance', title='Feature Importances',
             labels={'Importance': 'Importance Score'},
             color_discrete_sequence=px.colors.qualitative.Set1)  # You can choose a different color palette

# Customize the layout
fig.update_layout(xaxis_title='Features', yaxis_title='Importance Score', xaxis_tickangle=-45, height=400, width=800)

# Show the interactive plot
fig.show()

# Filter and select important features with importance score greater than 0.01
important_features = feats[feats['Importance'] > 0.01]

# Display the selected important features
important_features

# Drop 'sex' and 'region' columns from the dataset
data.drop(['sex', 'region'], axis=1, inplace=True)

# Create feature matrix (Xf) without the 'charges' column
Xf = data.drop(['charges'], axis=1)

# Create another feature matrix (X) without the 'charges' column
X = data.drop(['charges'], axis=1)

# Split the data into training and testing sets
xtrain, xtest, ytrain, ytest = train_test_split(Xf, Y, test_size=0.2, random_state=42)

# Initialize the final XGBoost regression model with specified hyperparameters
finalmodel = XGBRegressor(n_estimators=15, max_depth=3, gamma=0)

# Train the final model on the training data
finalmodel.fit(xtrain, ytrain)

# Make predictions on the training and testing data
ypredtrain4 = finalmodel.predict(xtrain)
ypredtest4 = finalmodel.predict(xtest)

# Calculate and print the model's performance metrics
print("Training Accuracy (R-squared): ", r2_score(ytrain, ypredtrain4))
print("Test Accuracy (R-squared): ", r2_score(ytest, ypredtest4))
print("Cross-Validation Score (R-squared): ", cross_val_score(finalmodel, X, Y, cv=5).mean())

# Import the 'dump' function from the 'pickle' library
from pickle import dump

# Serialize and save the final XGBoost regression model to a binary file
# The 'wb' mode is used to write in binary mode
dump(finalmodel, open('final_model.pkl', 'wb'))

# Create a new DataFrame with input data for prediction
new_data = pd.DataFrame({
    'age': 19,
    'sex': 'male',
    'bmi': 27.9,
    'children': 0,
    'smoker': 'yes',
    'region': 'northeast'
}, index=[0])

# Map the 'smoker' column to numerical values (1 for 'yes', 0 for 'no')
new_data['smoker'] = new_data['smoker'].map({'yes': 1, 'no': 0})

# Drop the 'sex' and 'region' columns as they were dropped during model training
new_data = new_data.drop(['sex', 'region'], axis=1)

# Use the trained 'finalmodel' to predict health insurance charges for the new data
finalmodel.predict(new_data)