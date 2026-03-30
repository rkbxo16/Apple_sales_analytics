import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
# To locate the csv file to load
script_dir = os.path.dirname(os.path.abspath(__file__))

parent_dir = os.path.dirname(script_dir)

file_path = os.path.join(parent_dir, 'data', 'processed', 'Apple_sales_clean.csv')

df = pd.read_csv(file_path)
# Sales by Products
ax = df.groupby("Product")["Total_sale"].sum().plot(kind="bar")

ax.yaxis.set_major_formatter(mtick.StrMethodFormatter('£{x:,.0f}'))

plt.xticks(rotation=45,)
plt.title("Revenue by Product")
plt.ylabel("Revenue (£)")
plt.tight_layout()
plt.show()
# Monthly Trend
ay=df.groupby("Month")["Total_sale"].sum().plot(kind="line")
plt.title("Monthly Revenue Trend")
ay.yaxis.set_major_formatter(mtick.StrMethodFormatter('£{x:,.0f}'))
plt.ylabel("Revenue (£)")
plt.tight_layout()
plt.show()

# Customer Segment
df.groupby("Customer_Type")["Total_sale"].sum().plot(kind="pie", autopct="%1.1f%%")
plt.title("Customer Contribution")
plt.ylabel("")
plt.show()