# train_model.py
print("Starting DROPSAFE model training...")
import pandas as pd
import numpy as np
print("Basic imports successful")
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib
print("All imports successful")

# 1. Generate realistic synthetic data for 500 students
np.random.seed(42)  # Ensures we get the same results every time
num_students = 500

data = {
    'Student_ID': range(1, num_students + 1),
    'Attendance': np.clip(np.random.normal(80, 12, num_students), 40, 100).astype(int), # Normal distribution around 80%
    'Test_Score': np.clip(np.random.normal(65, 18, num_students), 15, 100).astype(int), # Normal distribution around 65%
    'Fee_Status': np.random.choice(['Paid', 'Pending', 'Overdue'], num_students, p=[0.7, 0.2, 0.1]), # 70% Paid, 20% Pending, 10% Overdue
}

df = pd.DataFrame(data)

# 2. Create the TARGET variable (Dropout Risk) based on logical rules
# This is how we "supervise" the machine learning
df['Dropped_Out'] = 0  # Initialize to 0 (Low Risk)

# Students are at high risk if they fail in multiple categories
df.loc[
    (df['Attendance'] < 75) &
    (df['Test_Score'] < 50) &
    (df['Fee_Status'] == 'Overdue'),
    'Dropped_Out'
] = 1  # High Risk

df.loc[
    (df['Attendance'] < 70) &
    (df['Test_Score'] < 40),
    'Dropped_Out'
] = 1  # High Risk

df.loc[
    (df['Test_Score'] < 35),
    'Dropped_Out'
] = 1  # High Risk

# 3. Prepare Features (X) and Target (y)
# Convert categorical 'Fee_Status' to numbers for the model to understand
df['Fee_Status_Code'] = df['Fee_Status'].map({'Paid': 0, 'Pending': 1, 'Overdue': 2})
feature_columns = ['Attendance', 'Test_Score', 'Fee_Status_Code']
X = df[feature_columns]
y = df['Dropped_Out']

# 4. Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 5. Create and train the Random Forest model
print("Training the Machine Learning Model...")
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 6. Check the model's accuracy
accuracy = model.score(X_test, y_test)
print(f"Model trained successfully! Accuracy: {accuracy:.2%}")

# 7. Save the model to a file for use in the main app
joblib.dump(model, 'dropout_model.joblib')
print("Model saved as 'dropout_model.joblib'")

# 8. (Optional) Save the synthetic data to Excel files to use for testing the dashboard
df[['Student_ID', 'Attendance']].to_excel('sample_attendance.xlsx', index=False)
df[['Student_ID', 'Test_Score']].to_excel('sample_scores.xlsx', index=False)
df[['Student_ID', 'Fee_Status']].to_excel('sample_fees.xlsx', index=False)
print("Sample data files created for testing.")