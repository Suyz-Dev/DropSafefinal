import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import joblib

print("Creating sample data and training model...")

# Create sample data for 100 students
np.random.seed(42)
num_students = 100

# Generate attendance data (40-100%)
attendance_data = {
    'Student_ID': range(1, num_students + 1),
    'Attendance': np.random.randint(40, 101, num_students)
}
attendance_df = pd.DataFrame(attendance_data)

# Generate test scores (20-100%)
scores_data = {
    'Student_ID': range(1, num_students + 1),
    'Test_Score': np.random.randint(20, 101, num_students)
}
scores_df = pd.DataFrame(scores_data)

# Generate fee status
fee_statuses = ['Paid', 'Pending', 'Overdue']
fees_data = {
    'Student_ID': range(1, num_students + 1),
    'Fee_Status': np.random.choice(fee_statuses, num_students, p=[0.7, 0.2, 0.1])
}
fees_df = pd.DataFrame(fees_data)

# Save Excel files
attendance_df.to_excel('sample_attendance.xlsx', index=False)
scores_df.to_excel('sample_scores.xlsx', index=False)
fees_df.to_excel('sample_fees.xlsx', index=False)

print("Sample Excel files created:")
print("- sample_attendance.xlsx")
print("- sample_scores.xlsx") 
print("- sample_fees.xlsx")

# Create and train a simple model
# Merge all data
merged_data = attendance_df.merge(scores_df, on='Student_ID').merge(fees_df, on='Student_ID')

# Create risk labels based on rules
merged_data['Dropped_Out'] = 0
merged_data.loc[
    (merged_data['Attendance'] < 60) | 
    (merged_data['Test_Score'] < 40) | 
    (merged_data['Fee_Status'] == 'Overdue'), 
    'Dropped_Out'
] = 1

# Prepare features
merged_data['Fee_Status_Code'] = merged_data['Fee_Status'].map({'Paid': 0, 'Pending': 1, 'Overdue': 2})
X = merged_data[['Attendance', 'Test_Score', 'Fee_Status_Code']]
y = merged_data['Dropped_Out']

# Train model
model = RandomForestClassifier(n_estimators=50, random_state=42)
model.fit(X, y)

# Save model
joblib.dump(model, 'dropout_model.joblib')
print("Model trained and saved as 'dropout_model.joblib'")
print("Setup complete!")