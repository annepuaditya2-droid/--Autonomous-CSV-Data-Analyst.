import pandas as pd
import random
from datetime import datetime, timedelta

print("Generating 1,000 rows of e-commerce data...")

# Setup realistic categories and pricing
categories = {
    'Electronics': (200, 1500),
    'Clothing': (15, 120),
    'Home & Garden': (30, 400),
    'Sports': (25, 250),
    'Books': (10, 45)
}
regions = ['North', 'South', 'East', 'West']
payment_methods = ['Credit Card', 'PayPal', 'Debit Card', 'Apple Pay']

data = []
start_date = datetime(2025, 1, 1)

for i in range(1000):
    category = random.choice(list(categories.keys()))
    unit_price = round(random.uniform(*categories[category]), 2)
    units_sold = random.randint(1, 8)
    discount = round(random.choice([0.0, 0.05, 0.10, 0.15, 0.20]), 2)
    
    # Calculate final revenue after discount
    revenue = round((unit_price * units_sold) * (1 - discount), 2)
    
    # Random date within the year 2025
    random_days = random.randint(0, 364)
    txn_date = (start_date + timedelta(days=random_days)).strftime('%Y-%m-%d')

    data.append([
        f"TXN-{1000 + i}", txn_date, category, random.choice(regions), 
        random.choice(payment_methods), units_sold, unit_price, discount, revenue
    ])

# Save to CSV
df = pd.DataFrame(data, columns=[
    'Transaction_ID', 'Date', 'Category', 'Region', 
    'Payment_Method', 'Units_Sold', 'Unit_Price', 'Discount', 'Total_Revenue'
])
df.to_csv('ecommerce_sales.csv', index=False)

print("✅ Success! 'ecommerce_sales.csv' has been created in your folder.")