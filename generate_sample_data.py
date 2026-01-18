import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def generate_data(filename="customer_sales_data.csv"):
    # Set seed for reproducibility
    np.random.seed(42)
    random.seed(42)

    num_rows = 1000
    
    # Generate Customer IDs
    customer_ids = [f"CUST-{random.randint(1000, 1100)}" for _ in range(num_rows)]
    
    # Generate Products
    products = ["Laptop", "Smartphone", "Tablet", "Monitor", "Keyboard", "Mouse", "Headphones", "Webcam"]
    product_prices = {
        "Laptop": 1200, "Smartphone": 800, "Tablet": 450, "Monitor": 300,
        "Keyboard": 50, "Mouse": 30, "Headphones": 150, "Webcam": 80
    }
    
    row_products = [random.choice(products) for _ in range(num_rows)]
    quantities = [random.randint(1, 4) for _ in range(num_rows)]
    prices = [product_prices[p] for p in row_products]
    total_amounts = [q * p for q, p in zip(quantities, prices)]
    
    # Generate Dates
    start_date = datetime(2025, 1, 1)
    dates = [start_date + timedelta(days=random.randint(0, 364)) for _ in range(num_rows)]
    
    # Generate Regions
    regions = ["North", "South", "East", "West"]
    row_regions = [random.choice(regions) for _ in range(num_rows)]
    
    # Create Dataframe
    df = pd.DataFrame({
        "Transaction_ID": range(1, num_rows + 1),
        "Date": dates,
        "Customer_ID": customer_ids,
        "Product": row_products,
        "Quantity": quantities,
        "Unit_Price": prices,
        "Total_Amount": total_amounts,
        "Region": row_regions
    })
    
    # Add some missing values and duplicates for preprocessing testing
    df.loc[random.sample(range(num_rows), 20), "Region"] = np.nan
    df.loc[random.sample(range(num_rows), 10), "Unit_Price"] = np.nan
    
    # Add duplicates
    df = pd.concat([df, df.iloc[:15]], ignore_index=True)
    
    # Save to CSV
    df.to_csv(filename, index=False)
    print(f"Sample data generated: {filename}")

if __name__ == "__main__":
    generate_data()
