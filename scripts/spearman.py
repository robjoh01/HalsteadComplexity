import pandas as pd
from scipy.stats import spearmanr

output = 'plotly/js/spearman.csv'

# Sample data (you would paste your actual data here)
data = {
    'Version': ['2.0.0', '3.0.0', '4.0.0', '5.0.0', '6.0.0'],
    'Total Days': [525, 377, 705, 1317, 83],
    'Total Stars': [5520, 4470, 29190, 77760, 33891],
    'Total Volume': [1053757, 16323691, 26782155, 29665249, 39208526],
    'Total Effort': [38971215, 946063935, 7342057384, 2595233141, 3470759718],
    'Total Difficulty': [1270, 16670, 14769, 30361, 38714],
    'Total Delivered Bugs': [351, 5441, 8927, 9888, 13070],
    'Total Reported Bugs': [13, 73, 115, 305, 43],
    'Total LOC': [15356, 250582, 371192, 466213, 621067],
    'Total Files': [68, 829, 438, 1393, 1680],
    'Total __init__ Files': [14, 204, 309, 348, 429],
    'Total Changes': [1368827, 4652102, 6145908, 6824210, 2559428],
    'Avg Volume': [15496, 19691, 61146, 21296, 23338],
    'Avg Effort': [573106, 1141211, 16762688, 1863053, 2065928],
    'Avg Difficulty': [19, 20, 34, 22, 23],
    'Avg Delivered Bugs': [5, 7, 20, 7, 8],
    'Avg LOC': [226, 302, 847, 335, 370],
    'Avg Changes': [1651, 16556, 3725, 2930, 7251]
}

# Create DataFrame
df = pd.DataFrame(data)

# Drop the 'Version' column for correlation
numeric_df = df.drop(columns='Version')

# Run Spearman correlation
corr, p_value = spearmanr(numeric_df)

# Convert the correlation matrix to a DataFrame
corr_df = pd.DataFrame(corr, index=numeric_df.columns, columns=numeric_df.columns).round(2)

# Save to CSV
corr_df.to_csv(output)

print(f"Spearman exported to {output}")