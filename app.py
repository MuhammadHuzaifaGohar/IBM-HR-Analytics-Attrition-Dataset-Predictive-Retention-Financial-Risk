import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix

# --- 1. DATA ACQUISITION ---
# Using the standard IBM HR Attrition dataset from a public GitHub mirror
url = "https://raw.githubusercontent.com/nelson-wu/employee-attrition-ml/master/WA_Fn-UseC_-HR-Employee-Attrition.csv"
df = pd.read_csv(url)

# --- 2. DATA ENGINEERING FOR CEO INSIGHTS ---
# Let's add a "Cost of Turnover" column. 
# Industry standard: Replacing a professional costs ~1.5x their annual salary.
df['Annual_Salary'] = df['MonthlyIncome'] * 12
df['Replacement_Cost'] = df['Annual_Salary'] * 1.5

# Convert Attrition to numeric for analysis
le = LabelEncoder()
df['Attrition_Num'] = le.fit_transform(df['Attrition']) # Yes=1, No=0

# --- 3. THE "HR PAIN POINT" ANALYSIS ---
def get_hr_insights(df):
    print("--- HR STRATEGIC SUMMARY ---")
    avg_tenure = df['YearsAtCompany'].mean()
    total_risk_exposure = df[df['Attrition'] == 'Yes']['Replacement_Cost'].sum()
    
    print(f"Average Employee Tenure: {avg_tenure:.1f} years")
    print(f"Current Financial Loss from Attrition: ${total_risk_exposure:,.2f}")
    print("-" * 30)

get_hr_insights(df)

# --- 4. PRE-PROCESSING FOR MACHINE LEARNING ---
# Dropping non-useful columns
df_ml = df.drop(['EmployeeCount', 'EmployeeNumber', 'Over18', 'StandardHours', 'Annual_Salary'], axis=1)

# Encoding categorical variables
cat_cols = df_ml.select_dtypes(include=['object']).columns
for col in cat_cols:
    df_ml[col] = le.fit_transform(df_ml[col])

# Splitting Data
X = df_ml.drop(['Attrition', 'Attrition_Num', 'Replacement_Cost'], axis=1)
y = df_ml['Attrition_Num']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# --- 5. PREDICTIVE MODELING (RANDOM FOREST) ---
model = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
model.fit(X_train, y_train)

# --- 6. QUANTIFYING FUTURE RISK (THE CEO REPORT) ---
# We predict on the test set and see which "Active" employees are high risk
test_preds = model.predict(X_test)
test_probs = model.predict_proba(X_test)[:, 1]

results = pd.DataFrame({
    'Actual_Attrition': y_test,
    'Predicted_Prob': test_probs,
    'Replacement_Cost': df.loc[X_test.index, 'Replacement_Cost']
})

# Identify "High Risk" (Probability > 70%) who haven't left yet
high_risk_stayers = results[(results['Actual_Attrition'] == 0) & (results['Predicted_Prob'] > 0.6)]
potential_saving = high_risk_stayers['Replacement_Cost'].sum()

print(f"\n--- CEO EXECUTIVE ALERT ---")
print(f"High-Risk Employees Identified: {len(high_risk_stayers)}")
print(f"Revenue at Risk (Next 6 Months): ${potential_saving:,.2f}")
print("Recommendation: Targeted retention bonuses for high-impact roles.")

# --- 7. VISUALIZATION FOR PRESENTATION ---
plt.figure(figsize=(12, 6))

# Plot 1: Feature Importance (What is driving people away?)
importances = pd.Series(model.feature_importances_, index=X.columns).sort_values(ascending=True).tail(10)
plt.subplot(1, 2, 1)
importances.plot(kind='barh', color='skyblue')
plt.title('Top 10 Drivers of Attrition')

# Plot 2: Attrition by Monthly Income
plt.subplot(1, 2, 2)
sns.boxplot(x='Attrition', y='MonthlyIncome', data=df, palette='Set2')
plt.title('Income Level vs. Attrition')

plt.tight_layout()
plt.show()
