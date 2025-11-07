import pandas as pd
import numpy as np
print("Basic imports successful")

# Generate simple data
data = {'Student_ID': [1, 2, 3], 'Score': [80, 70, 60]}
df = pd.DataFrame(data)
print("DataFrame created:", df)

# Save simple Excel file
df.to_excel('test.xlsx', index=False)
print("Excel file created successfully")