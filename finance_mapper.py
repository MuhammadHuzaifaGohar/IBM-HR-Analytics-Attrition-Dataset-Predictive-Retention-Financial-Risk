def calculate_attrition_costs(df, multiplier=1.5):
    """
    Industry standard: Replacing an employee costs ~1.5x their annual salary.
    """
    df['Annual_Salary'] = df['MonthlyIncome'] * 12
    df['Replacement_Cost'] = df['Annual_Salary'] * multiplier
    return df

def get_revenue_at_risk(results_df):
    # Filter for employees the model thinks will leave (Prob > 60%) but haven't yet
    high_risk = results_df[(results_df['Actual'] == 0) & (results_df['Prob'] > 0.6)]
    return high_risk['Replacement_Cost'].sum(), len(high_risk)
