import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set file path
file_path = r'C:\Users\nisch\Downloads\New folder\Hackathon_Working_Data.csv'

# Check if file exists
if not os.path.exists(file_path):
    raise FileNotFoundError(f"The file at path {file_path} does not exist. Please check the file path.")
else:
    print(f"File found at {file_path}")

# Load the dataset
df = pd.read_csv(file_path)

# Print the first few rows to confirm successful loading
print(df.head())

# Drop unnecessary columns if they exist
columns_to_drop = ['File Name', 'Column Name', 'Column Description']
for column in columns_to_drop:
    if column in df.columns:
        df.drop(columns=[column], inplace=True)

# Define key columns
key_columns = ['QTY', 'VALUE', 'SGRP', 'SSGRP', 'CMP', 'MBRD', 'BRD', 'DAY', 'BILL_ID', 'BILL_AMT', 'PRICE']

# Check if key columns exist in the dataframe
missing_columns = [col for col in key_columns if col not in df.columns]
if missing_columns:
    print(f"Missing key columns: {missing_columns}")
else:
    # Drop rows with missing values in key columns
    df.dropna(subset=key_columns, inplace=True)

    # Check for missing values again
    print("Missing values after cleaning:")
    print(df.isnull().sum())

    # Feature Engineering: Calculate total purchase value if not already available
    if 'TOTALVALUE' not in df.columns or df['TOTALVALUE'].isnull().all():
        df['TOTALVALUE'] = df['QTY'] * df['PRICE']

    # Save the cleaned data
    cleaned_file_path = 'C:/Users/nisch/Desktop/cleaned_transaction_data.csv'
    df.to_csv(cleaned_file_path, index=False)
    print(f"Cleaned data saved to {cleaned_file_path}")

    # Distribution of Quantities and Values
    plt.figure(figsize=(14, 6))

    plt.subplot(1, 2, 1)
    sns.histplot(df['QTY'], bins=50, kde=True)
    plt.title('Distribution of Quantities')

    plt.subplot(1, 2, 2)
    sns.histplot(df['VALUE'], bins=50, kde=True)
    plt.title('Distribution of Values')

    plt.tight_layout()
    plt.show()

    # Top 10 Products by Total Quantity Sold
    top_products_qty = df.groupby('BRD')['QTY'].sum().sort_values(ascending=False).head(10)
    plt.figure(figsize=(10, 6))
    sns.barplot(x=top_products_qty.values, y=top_products_qty.index)
    plt.title('Top 10 Products by Quantity Sold')
    plt.xlabel('Total Quantity Sold')
    plt.ylabel('Product Brand')
    plt.show()

    # Top 10 Products by Total Value
    top_products_value = df.groupby('BRD')['TOTALVALUE'].sum().sort_values(ascending=False).head(10)
    plt.figure(figsize=(10, 6))
    sns.barplot(x=top_products_value.values, y=top_products_value.index)
    plt.title('Top 10 Products by Total Value')
    plt.xlabel('Total Value')
    plt.ylabel('Product Brand')
    plt.show()

    # Customer Purchase Patterns over Time
    if 'DAY' in df.columns and 'MONTH' in df.columns:
        df['DAY'] = df['DAY'].astype(int)
        df['MONTH'] = df['MONTH'].astype('category')
        purchase_patterns = df.groupby(['MONTH', 'DAY'])['TOTALVALUE'].sum().reset_index()
        plt.figure(figsize=(14, 6))
        sns.lineplot(x='DAY', y='TOTALVALUE', hue='MONTH', data=purchase_patterns)
        plt.title('Customer Purchase Patterns over Time')
        plt.xlabel('Day of the Month')
        plt.ylabel('Total Purchase Value')
        plt.show()