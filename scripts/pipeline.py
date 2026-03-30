import datetime

import pandas as pd
import numpy as np

def load_data(path):
    return pd.read_csv(path)

def clean_data(df):
    # Clean column names
    df.columns = df.columns.str.strip()

    # Remove duplicates
    df = df.drop_duplicates()
    return df

def transform_data(df):
    # Rename columns
    df = df.rename(columns={
        "Order Date": "PURCHASE_DATE",
        "Sales": "UNIT_PRICE",
        "Product Name": "PRODUCT",
        "Customer Name": "CUSTOMER_NAME",
        "Customer ID": "CUSTOMER_ID",
        "Postal Code": "POSTAL_CODE",
        "Region": "REGION",
        "City": "CITY",
        "Country": "COUNTRY",
        "Quantity": "QUANTITY",
        "Category": "PRODUCT_CATEGORY",
        "Order ID": "ORDER_ID",
        "Sub-Category": "SUB_CATEGORY",
    })
    # Convert date
    df["PURCHASE_DATE"] = pd.to_datetime(df["PURCHASE_DATE"], dayfirst=True)
    # Map to Apple-style products
    product_map = {
        "Technology": "iPhone",
        "Furniture": "MacBook",
        "Office Supplies": "iPad"
    }

    df["PRODUCT"] = df["PRODUCT_CATEGORY"].map(product_map)

    # Add extra Apple products
    extra_products = ["AirPods", "Apple Watch"]
    sampled_rows = df.sample(frac=0.3).index

    df.loc[sampled_rows, "PRODUCT"] = np.random.choice(
        extra_products,
        size=len(sampled_rows)
    )
    # Price Map
    price_map = {
        "iPhone": 999,
        "MacBook": 1999,
        "iPad": 799,
        "AirPods": 199,
        "Apple Watch": 399
    }
    df["UNIT_PRICE"] = df["PRODUCT"].map(price_map)

    # Add new fields
    df["QUANTITY"] = np.random.randint(1, 5, size=len(df))

    # Business metrics
    df["TOTAL_SALE"] = df["UNIT_PRICE"] * df["QUANTITY"]
    df["PURCHASE_MONTH"] = df["PURCHASE_DATE"].dt.to_period("M")
    df["PURCHASE_MONTH"] = df["PURCHASE_DATE"].dt.month


    # Fix categories based on product
    category_map = {
        "iPhone": ("Devices", "Smartphones"),
        "MacBook": ("Devices", "Laptops"),
        "iPad": ("Devices", "Tablets"),
        "AirPods": ("Accessories", "Audio"),
        "Apple Watch": ("Accessories", "Wearables")
    }
    df["PRODUCT_CATEGORY"] = df["PRODUCT"].apply(lambda x: category_map[x][0])
    df["SUB_CATEGORY"] = df["PRODUCT"].apply(lambda x: category_map[x][1])
    # Handle missing dates
    df = df.dropna(subset=["PURCHASE_DATE"])
    # Round values
    df["TOTAL_SALE"] = df["TOTAL_SALE"].astype(float).round(2)

    #some cleaning for the required report
    df=df.drop(columns={"Ship Mode","Product ID","Ship Date","Segment"})

    # Fix postal codes
    df["POSTAL_CODE"] = df["POSTAL_CODE"].astype(str).str.replace(".0", "", regex=False)
    # Make the dataset more consistent

    df["CUSTOMER_AGE"] = np.random.randint(18, 65, size=len(df))
    customer_age_map = df.groupby("CUSTOMER_ID")["CUSTOMER_AGE"].mean().round().astype(int)
    df["CUSTOMER_AGE"] = df["CUSTOMER_ID"].map(customer_age_map)
    # New fields
    # Customer segmentation
    def segment(CUSTOMER_AGE):
        if CUSTOMER_AGE<25:
            return "Student"
        elif CUSTOMER_AGE<40:
            return "Young Professional"
        else:
            return "Senior"
    df["CUSTOMER_SEGMENT"] = df["CUSTOMER_AGE"].apply(segment)

    df = df.groupby(
        ["ORDER_ID", "CUSTOMER_NAME", "PRODUCT"],
        as_index=False
    ).agg({
        "QUANTITY": "sum",
        "TOTAL_SALE": "sum",
        "UNIT_PRICE": "mean",
        "PRODUCT_CATEGORY": "first",
        "SUB_CATEGORY": "first",
        "REGION": "first",
        "PURCHASE_DATE": "first",
        "CUSTOMER_ID": "first",
        "PRODUCT": "first",
        "COUNTRY": "first",
        "CITY": "first",
        "POSTAL_CODE": "first",
        "PURCHASE_MONTH": "first",
        "CUSTOMER_AGE": "first",
        "CUSTOMER_SEGMENT": "first",
    })


    column_order = [
        # Order Details
        "ORDER_ID",
        "PURCHASE_DATE",
        "PURCHASE_MONTH",
        #Customer Details
        "CUSTOMER_ID",
        "CUSTOMER_NAME",
        "CUSTOMER_AGE",
        "CUSTOMER_SEGMENT",
        "COUNTRY",
        "REGION",
        "CITY",
        "POSTAL_CODE",
        #Product Details
        "PRODUCT_CATEGORY",
        "SUB_CATEGORY",
        "PRODUCT",
        #Sales
        "UNIT_PRICE",
        "QUANTITY",
        "TOTAL_SALE",

    ]

    df = df[column_order]
    return df

def save_data(df, path):
    df.to_csv(path, index=False)