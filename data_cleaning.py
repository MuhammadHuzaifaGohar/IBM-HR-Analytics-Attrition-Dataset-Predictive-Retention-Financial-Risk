import pandas as pd
from sklearn.preprocessing import LabelEncoder

def load_and_clean_data(url):
    df = pd.read_csv(url)
    
    # Drop zero-variance columns and non-useful identifiers
    cols_to_drop = ['EmployeeCount', 'EmployeeNumber', 'Over18', 'StandardHours']
    df = df.drop(cols_to_drop, axis=1)
    
    # Encode categorical variables
    le = LabelEncoder()
    categorical_cols = df.select_dtypes(include=['object']).columns
    
    # Store mapping if needed, but for now, we transform
    for col in categorical_cols:
        df[col] = le.fit_transform(df[col])
        
    return df
