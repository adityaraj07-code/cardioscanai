# Major Project (Capstone Project)

# Heart Disease Prediction

import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.impute import SimpleImputer

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    confusion_matrix,
    roc_curve,
    roc_auc_score
)

import matplotlib.pyplot as plt
import seaborn as sns

# ==================================================
# LOAD DATASET
# ==================================================

df = pd.read_csv("heart_disease_uci.csv")

print("Dataset Shape:", df.shape)
print("\nColumns:")
print(df.columns)

# ==================================================
# CREATE BINARY TARGET
# ==================================================

df["target"] = (df["num"] > 0).astype(int)

# Drop original target
df.drop("num", axis=1, inplace=True)

# ==================================================
# REMOVE UNNECESSARY COLUMN
# ==================================================

if "id" in df.columns:
    df.drop("id", axis=1, inplace=True)

# ==================================================
# HANDLE MISSING VALUES
# ==================================================

# Numerical columns
num_cols = df.select_dtypes(include=np.number).columns

num_imputer = SimpleImputer(strategy="median")
df[num_cols] = num_imputer.fit_transform(df[num_cols])

# Categorical columns
cat_cols = df.select_dtypes(include="object").columns

cat_imputer = SimpleImputer(strategy="most_frequent")
df[cat_cols] = cat_imputer.fit_transform(df[cat_cols])

# ==================================================
# ENCODE CATEGORICAL FEATURES
# ==================================================

le = LabelEncoder()

for col in cat_cols:
    df[col] = le.fit_transform(df[col])

# ==================================================
# FEATURES AND TARGET
# ==================================================

X = df.drop("target", axis=1)
y = df["target"]

# ==================================================
# FEATURE SCALING
# ==================================================

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# ==================================================
# TRAIN TEST SPLIT
# ==================================================

X_train, X_test, y_train, y_test = train_test_split(
    X_scaled,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

# ==================================================
# LOGISTIC REGRESSION
# ==================================================

lr_model = LogisticRegression(max_iter=1000)

lr_model.fit(X_train, y_train)

lr_pred = lr_model.predict(X_test)

# ==================================================
# DECISION TREE
# ==================================================

dt_model = DecisionTreeClassifier(
    random_state=42,
    max_depth=5
)

dt_model.fit(X_train, y_train)

dt_pred = dt_model.predict(X_test)

# ==================================================
# EVALUATION FUNCTION
# ==================================================

def evaluate_model(name, y_true, y_pred):

    print("\n" + "="*50)
    print(name)
    print("="*50)

    print("Accuracy :", round(accuracy_score(y_true, y_pred),4))
    print("Precision:", round(precision_score(y_true, y_pred),4))
    print("Recall   :", round(recall_score(y_true, y_pred),4))

# ==================================================
# RESULTS
# ==================================================

evaluate_model(
    "Logistic Regression",
    y_test,
    lr_pred
)

evaluate_model(
    "Decision Tree",
    y_test,
    dt_pred
)

# ==================================================
# CONFUSION MATRIX
# ==================================================

cm = confusion_matrix(y_test, lr_pred)

plt.figure(figsize=(6,5))

sns.heatmap(
    cm,
    annot=True,
    fmt="d",
    cmap="Blues"
)

plt.title("Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")

plt.show()

# ==================================================
# ROC CURVE
# ==================================================

lr_prob = lr_model.predict_proba(X_test)[:,1]

fpr, tpr, thresholds = roc_curve(
    y_test,
    lr_prob
)

auc_score = roc_auc_score(
    y_test,
    lr_prob
)

plt.figure(figsize=(7,5))

plt.plot(
    fpr,
    tpr,
    label=f"AUC = {auc_score:.3f}"
)

plt.plot(
    [0,1],
    [0,1],
    linestyle="--"
)

plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Curve")

plt.legend()

plt.show()

# ==================================================
# SAMPLE PREDICTION
# ==================================================

sample = X.iloc[[0]]

prediction = lr_model.predict(sample)

print("\nSample Prediction:")

if prediction[0] == 1:
    print("Heart Disease Detected")
else:
    print("No Heart Disease")