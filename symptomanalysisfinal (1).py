# -*- coding: utf-8 -*-
"""symptomanalysisfinal.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1EMMP3l8A2CPxmnBpCOs3nZHKHoop3dmX
"""

# Import necessary libraries
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import chi2, mutual_info_classif
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
import seaborn as sns
import matplotlib.pyplot as plt

# Load the dataset
pcos_data = pd.read_csv('/content/PCOS_data.csv')

# Step 1: Correlation Analysis (for numerical features)
# Dropping irrelevant columns and target column (PCOS)
numeric_features = pcos_data.select_dtypes(include=[np.number]).drop(columns=['PCOS (Y/N)', 'Sl. No', 'Patient File No.'], errors='ignore')
correlation_matrix = numeric_features.corrwith(pcos_data['PCOS (Y/N)'])

# Plotting correlation for a quick visualization
plt.figure(figsize=(10, 8))
sns.barplot(x=correlation_matrix.values, y=correlation_matrix.index)
plt.title('Correlation with Target (PCOS)')
plt.xlabel('Correlation Coefficient')
plt.ylabel('Features')
plt.show()

# Step 2: Chi-Square Test (for categorical features)
# Encoding categorical features for Chi-square
categorical_features = ['Weight gain(Y/N)', 'hair growth(Y/N)', 'Skin darkening (Y/N)',
                        'Hair loss(Y/N)', 'Pimples(Y/N)', 'Fast food (Y/N)', 'Reg.Exercise(Y/N)']

# Convert categorical data into integers
for feature in categorical_features:
    pcos_data[feature] = pcos_data[feature].fillna(0).astype(int)

X_cat = pcos_data[categorical_features]
y = pcos_data['PCOS (Y/N)']

chi2_scores, p_values = chi2(X_cat, y)
chi2_results = pd.DataFrame({'Feature': categorical_features, 'Chi2 Score': chi2_scores, 'p-value': p_values})
chi2_results = chi2_results.sort_values(by='Chi2 Score', ascending=False)

print("Chi-Square Test Results:\n", chi2_results)

# Step 3: Feature Importance with Random Forest
# Fill missing values if any, encode categorical variables, and split data
pcos_data.fillna(0, inplace=True)
X = pcos_data.drop(columns=['PCOS (Y/N)', 'Sl. No', 'Patient File No.'], errors='ignore')
y = pcos_data['PCOS (Y/N)']

# Encoding non-numeric columns for Random Forest
X = pd.get_dummies(X, drop_first=True)

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Train Random Forest
rf_model = RandomForestClassifier(random_state=42)
rf_model.fit(X_train, y_train)

# Feature importance from Random Forest
feature_importances = pd.DataFrame({'Feature': X.columns, 'Importance': rf_model.feature_importances_})
feature_importances = feature_importances.sort_values(by='Importance', ascending=False)

print("\nFeature Importances from Random Forest:\n", feature_importances.head(10))

# Step 4: Mutual Information
# Calculate mutual information scores
mutual_info_scores = mutual_info_classif(X, y)
mutual_info_results = pd.DataFrame({'Feature': X.columns, 'Mutual Information': mutual_info_scores})
mutual_info_results = mutual_info_results.sort_values(by='Mutual Information', ascending=False)

print("\nMutual Information Scores:\n", mutual_info_results.head(10))

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split

# Step 1: Select the Top 15 Features based on Random Forest importance
top_15_features = feature_importances.head(15)['Feature'].values
X_top15 = X[top_15_features]  # Selecting only the top 15 features

# Step 2: Split Data into Training and Testing Sets
X_train, X_test, y_train, y_test = train_test_split(X_top15, y, test_size=0.3, random_state=42)

# Step 3: Train a Model (Random Forest Classifier as an example)
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# Step 4: Make Predictions
y_pred = model.predict(X_test)

# Step 5: Evaluate the Model
accuracy = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred)
conf_matrix = confusion_matrix(y_test, y_pred)

print("Accuracy of the model:", accuracy)
print("\nClassification Report:\n", report)
print("\nConfusion Matrix:\n", conf_matrix)

from sklearn.ensemble import GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Step 1: Gradient Boosting Classifier
gb_model = GradientBoostingClassifier(random_state=42)
gb_model.fit(X_train, y_train)
y_pred_gb = gb_model.predict(X_test)

# Evaluate Gradient Boosting Classifier
accuracy_gb = accuracy_score(y_test, y_pred_gb)
report_gb = classification_report(y_test, y_pred_gb)
conf_matrix_gb = confusion_matrix(y_test, y_pred_gb)

print("Gradient Boosting Classifier Accuracy:", accuracy_gb)
print("\nGradient Boosting Classification Report:\n", report_gb)
print("\nGradient Boosting Confusion Matrix:\n", conf_matrix_gb)

# Step 2: Support Vector Machine (SVM)
# Standardize the features for SVM (required for best performance with SVM)
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

svm_model = SVC(kernel='rbf', random_state=42)
svm_model.fit(X_train_scaled, y_train)
y_pred_svm = svm_model.predict(X_test_scaled)

# Evaluate SVM
accuracy_svm = accuracy_score(y_test, y_pred_svm)
report_svm = classification_report(y_test, y_pred_svm)
conf_matrix_svm = confusion_matrix(y_test, y_pred_svm)

print("SVM Classifier Accuracy:", accuracy_svm)
print("\nSVM Classification Report:\n", report_svm)
print("\nSVM Confusion Matrix:\n", conf_matrix_svm)



import shap

# Train a model (e.g., Gradient Boosting Classifier)
model = GradientBoostingClassifier(random_state=42)
model.fit(X_train, y_train)

# Use SHAP to explain model predictions
explainer = shap.TreeExplainer(model)  # for tree-based models like Gradient Boosting
shap_values = explainer.shap_values(X_test)

# Check the shape of shap_values
print(f"Shape of shap_values: {len(shap_values)}")

# Visualize SHAP summary plot for binary classification
# If it's binary classification, shap_values will have two arrays, one for each class
if len(shap_values) == 2:  # For binary classification
    shap.summary_plot(shap_values[1], X_test)  # Use [1] for the positive class
else:
    shap.summary_plot(shap_values, X_test)  # For multi-class classification or single class output

from sklearn.ensemble import VotingClassifier, StackingClassifier
from sklearn.svm import SVC
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Step 1: Define Base Models for Voting and Stacking
gb_model = GradientBoostingClassifier(random_state=42)
svm_model = SVC(kernel='rbf', random_state=42)

# Step 2: Voting Classifier (Majority Vote or Average)
voting_clf = VotingClassifier(estimators=[('gb', gb_model), ('svm', svm_model)], voting='hard')
voting_clf.fit(X_train, y_train)

# Evaluate Voting Classifier
y_pred_voting = voting_clf.predict(X_test)
accuracy_voting = accuracy_score(y_test, y_pred_voting)
report_voting = classification_report(y_test, y_pred_voting)
conf_matrix_voting = confusion_matrix(y_test, y_pred_voting)

print("Voting Classifier Performance:")
print("Accuracy:", accuracy_voting)
print("\nClassification Report:\n", report_voting)
print("\nConfusion Matrix:\n", conf_matrix_voting)

# Step 3: Stacking Classifier (Using Logistic Regression as Meta-model)
# StackingClassifier requires a meta-model, we use LogisticRegression as the meta-model
meta_model = LogisticRegression(random_state=42)

stacking_clf = StackingClassifier(
    estimators=[('gb', gb_model), ('svm', svm_model)],
    final_estimator=meta_model
)

stacking_clf.fit(X_train, y_train)

# Evaluate Stacking Classifier
y_pred_stacking = stacking_clf.predict(X_test)
accuracy_stacking = accuracy_score(y_test, y_pred_stacking)
report_stacking = classification_report(y_test, y_pred_stacking)
conf_matrix_stacking = confusion_matrix(y_test, y_pred_stacking)

print("\nStacking Classifier Performance:")
print("Accuracy:", accuracy_stacking)
print("\nClassification Report:\n", report_stacking)
print("\nConfusion Matrix:\n", conf_matrix_stacking)



from sklearn.ensemble import GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler

# Step 1: Gradient Boosting Classifier
gb_model = GradientBoostingClassifier(random_state=42)
gb_model.fit(X_train, y_train)

# Predict on test set
y_pred_gb = gb_model.predict(X_test)

# Training accuracy
accuracy_train_gb = accuracy_score(y_train, gb_model.predict(X_train))

# Evaluate Gradient Boosting Classifier
accuracy_gb = accuracy_score(y_test, y_pred_gb)
report_gb = classification_report(y_test, y_pred_gb)
conf_matrix_gb = confusion_matrix(y_test, y_pred_gb)

print("Gradient Boosting Classifier Training Accuracy:", accuracy_train_gb)
print("Gradient Boosting Classifier Test Accuracy:", accuracy_gb)
print("\nGradient Boosting Classification Report:\n", report_gb)
print("\nGradient Boosting Confusion Matrix:\n", conf_matrix_gb)

# Step 2: Support Vector Machine (SVM)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

svm_model = SVC(kernel='rbf', random_state=42)
svm_model.fit(X_train_scaled, y_train)

# Predict on test set
y_pred_svm = svm_model.predict(X_test_scaled)

# Training accuracy
accuracy_train_svm = accuracy_score(y_train, svm_model.predict(X_train_scaled))

# Evaluate SVM
accuracy_svm = accuracy_score(y_test, y_pred_svm)
report_svm = classification_report(y_test, y_pred_svm)
conf_matrix_svm = confusion_matrix(y_test, y_pred_svm)

print("\nSVM Training Accuracy:", accuracy_train_svm)
print("SVM Test Accuracy:", accuracy_svm)
print("\nSVM Classification Report:\n", report_svm)
print("\nSVM Confusion Matrix:\n", conf_matrix_svm)

from sklearn.ensemble import GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler

# Step 1: Gradient Boosting Classifier
from sklearn.ensemble import GradientBoostingClassifier

gb_model = GradientBoostingClassifier(random_state=42,
                                       n_estimators=50,  # Reduced from default 100
                                       max_depth=3,      # Reduced from default 3
                                       learning_rate=0.1,
                                       subsample=0.8)     # Added subsampling
gb_model.fit(X_train, y_train)

# Predict on test set
y_pred_gb = gb_model.predict(X_test)

# Training accuracy
accuracy_train_gb = accuracy_score(y_train, gb_model.predict(X_train))

# Evaluate Gradient Boosting Classifier
accuracy_gb = accuracy_score(y_test, y_pred_gb)
report_gb = classification_report(y_test, y_pred_gb)
conf_matrix_gb = confusion_matrix(y_test, y_pred_gb)

print("Gradient Boosting Classifier Training Accuracy:", accuracy_train_gb)
print("Gradient Boosting Classifier Test Accuracy:", accuracy_gb)
print("\nGradient Boosting Classification Report:\n", report_gb)
print("\nGradient Boosting Confusion Matrix:\n", conf_matrix_gb)

# Step 2: Support Vector Machine (SVM)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

svm_model = SVC(kernel='rbf', random_state=42)
svm_model.fit(X_train_scaled, y_train)

# Predict on test set
y_pred_svm = svm_model.predict(X_test_scaled)

# Training accuracy
accuracy_train_svm = accuracy_score(y_train, svm_model.predict(X_train_scaled))

# Evaluate SVM
accuracy_svm = accuracy_score(y_test, y_pred_svm)
report_svm = classification_report(y_test, y_pred_svm)
conf_matrix_svm = confusion_matrix(y_test, y_pred_svm)

print("\nSVM Training Accuracy:", accuracy_train_svm)
print("SVM Test Accuracy:", accuracy_svm)
print("\nSVM Classification Report:\n", report_svm)
print("\nSVM Confusion Matrix:\n", conf_matrix_svm)