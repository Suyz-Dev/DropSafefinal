from sklearn.ensemble import RandomForestClassifier
import joblib

# Create and train a simple model
model = RandomForestClassifier(n_estimators=10, random_state=42)
X = [[80,75,0],[60,50,1],[90,85,0]]  # [Attendance, Test_Score, Fee_Status_Code]
y = [0,1,0]  # [Low Risk, High Risk, Low Risk]
model.fit(X, y)

# Save the model
joblib.dump(model, 'dropout_model.joblib')
print("Model saved as dropout_model.joblib")