import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix

PREDICT_PATH = 'src/data/predictions.csv' # where we'll write our predictions in the end

# load training data into pandas df
X_train = pd.read_csv("src/data/train_created.csv")
X_test = pd.read_csv("src/data/nychanow_pass_two.csv")

# add features to data
X_test['no. buildings mentioned'] = X_test.apply(lambda row: len(row['buildings']),axis=1)


# feature extraction
X_train_processed = X_train.drop(columns=['url','class','buildings','start','end','all dates'])

# learn the model
Y_train = X_train['class']
model = LogisticRegression().fit(X_train_processed, Y_train)
# model = KNeighborsClassifier(n_neighbors=5).fit(X_train_processed,Y_train)
# model = DecisionTreeClassifier().fit(X_train_processed, Y_train)


# make predictions
X_test = X_test.drop(columns=['url','buildings','start','end','all dates','dates'])
Y_test_predictions = model.predict(X_test)

# write predictions to csv
X_test = pd.read_csv("src/data/nychanow_pass_two.csv")
# X_test['no. buildings mentioned'] = X_test.apply(lambda row: len(row['buildings']),axis=1)
X_test['predicted class'] = Y_test_predictions
X_test.to_csv(PREDICT_PATH)

