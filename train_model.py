import pandas as pd
import numpy as np
import pickle

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler

from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report

# ==================================================
# STEP 1 : LOAD DATASET
# ==================================================

df = pd.read_csv("ats_resume_dataset_elite_v3.csv")
print(df["shortlisted"].value_counts())

print("Dataset Shape:")
print(df.shape)

print("\nColumns:")
print(df.columns)

print("Education Levels:")
print(df["education_level"].unique())

print("\nShortlisted Values:")
print(df["shortlisted"].unique())
# ==================================================
# STEP 2 : DATA CLEANING
# ==================================================

print("\nMissing Values:")
print(df.isnull().sum())

# ==================================================
# STEP 3 : HANDLE MISSING VALUES
# ==================================================

text_columns = [
    "resume_text",
    "resume_skills",
    "projects",
    "certifications",
    "job_role",
    "required_skills",
    "job_description"
]

for col in text_columns:
    if col in df.columns:
        df[col] = df[col].fillna("")

numeric_columns = [
    "experience_years",
    "job_experience_required",
    "skill_match_score",
    "experience_match",
    "education_match",
    "final_score",
    "similarity_score"
]

for col in numeric_columns:
    if col in df.columns:
        df[col] = df[col].fillna(df[col].mean())

# ==================================================
# STEP 4 : REMOVE DUPLICATES
# ==================================================

df.drop_duplicates(inplace=True)

print("\nShape After Cleaning:")
print(df.shape)

# ==================================================
# STEP 5 : ENCODE EDUCATION LEVEL
# ==================================================

encoder = LabelEncoder()

df["education_level"] = encoder.fit_transform(
    df["education_level"]
)

# ==================================================
# STEP 6 : FEATURE SELECTION
# ==================================================

X = df[
    [
        "experience_years",
        "education_level",
        "skill_match_score",
        "experience_match",
        "education_match",
        "final_score",
        "similarity_score"
    ]
]

y = df["shortlisted"]

# ==================================================
# STEP 7 : TRAIN TEST SPLIT
# ==================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)

# ==================================================
# STEP 8 : FEATURE SCALING
# ==================================================

scaler = StandardScaler()

X_train = scaler.fit_transform(X_train)

X_test = scaler.transform(X_test)

# ==================================================
# STEP 9 : TRAIN MODEL
# ==================================================

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)

# ==================================================
# STEP 10 : PREDICTION
# ==================================================

y_pred = model.predict(X_test)

# ==================================================
# STEP 11 : ACCURACY
# ==================================================

accuracy = accuracy_score(
    y_test,
    y_pred
)

print("\nAccuracy:")
print(accuracy)

# ==================================================
# STEP 12 : CONFUSION MATRIX
# ==================================================

print("\nConfusion Matrix:")

print(
    confusion_matrix(
        y_test,
        y_pred
    )
)

# ==================================================
# STEP 13 : CLASSIFICATION REPORT
# ==================================================

print("\nClassification Report:")

print(
    classification_report(
        y_test,
        y_pred
    )
)

# ==================================================
# STEP 14 : SAVE MODEL
# ==================================================

pickle.dump(
    model,
    open("model.pkl", "wb")
)

pickle.dump(
    scaler,
    open("scaler.pkl", "wb")
)

print("\nModel Saved Successfully")