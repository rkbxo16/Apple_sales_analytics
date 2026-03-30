import os
import pandas as pd

# 1. Get the folder
script_dir = os.path.dirname(os.path.abspath(__file__))

# 2. Get the parent folder
parent_dir = os.path.dirname(script_dir)

# 3. Join it with the data path
file_path = os.path.join(parent_dir, 'data', 'processed', 'Apple_sales_clean.csv')

df = pd.read_csv(file_path)

print("Total Revenue:", df["Total_sale"].sum())

print("Total Orders:", df["Order ID"].nunique())

aov = df["Total_sale"].sum() / df["Order ID"].nunique()
print("Average Order Value:", round(aov, 2))

# Insights
product_perf = df.groupby("Product")["Total_sale"].sum().sort_values(ascending=False)
print(product_perf)

region_perf = df.groupby("Region")["Total_sale"].sum().sort_values(ascending=False)
print(region_perf)

segment_perf = df.groupby("Customer_Type")["Total_sale"].sum()
print(segment_perf)

# Monthly Trends
monthly = df.groupby("Month")["Total_sale"].sum()
print(monthly)

# Top Customers
top_customers = df.groupby("Customer_Name")["Total_sale"].sum().nlargest(5)
print(top_customers)

