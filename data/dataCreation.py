import pandas as pd
import random
from faker import Faker

# Initialize Faker, I will use it to 
faker = Faker()

# Function to generate random phone number
def generate_random_phone():
    return faker.phone_number()

# Generate random data for Region
num_regions = 10
region_data = {
    'region_key': [i+1 for i in range(num_regions)],
    'region_name': [faker.country() for _ in range(num_regions)],
    'comments': [faker.sentence() for _ in range(num_regions)]
}
region_df = pd.DataFrame(region_data)

# Generate random data for Nation
num_nations = 20
nation_data = {
    'nation_key': [i+1 for i in range(num_nations)],
    'nation_name': [faker.country() for _ in range(num_nations)],
    'region_key': [random.randint(1, num_regions) for _ in range(num_nations)],
    'comments': [faker.sentence() for _ in range(num_nations)]
}
nation_df = pd.DataFrame(nation_data)

# Generate random data for Part
num_parts = 100
part_data = {
    'part_key': [i+1 for i in range(num_parts)],
    'part_name': [faker.word() for _ in range(num_parts)],
    'manufacturer': [faker.company() for _ in range(num_parts)],
    'brand': [faker.word() for _ in range(num_parts)],
    'type': [faker.word() for _ in range(num_parts)],
    'size': [random.randint(1, 100) for _ in range(num_parts)],
    'container': [faker.word() for _ in range(num_parts)],
    'retail_price': [round(random.uniform(1, 1000), 2) for _ in range(num_parts)],
    'comments': [faker.sentence() for _ in range(num_parts)]
}
part_df = pd.DataFrame(part_data)

# Generate random data for Customer
num_customers = 500
customer_data = {
    'customer_key': [i+1 for i in range(num_customers)],
    'customer_name': [faker.name() for _ in range(num_customers)],
    'customer_address': [faker.address() for _ in range(num_customers)],
    'nation_key': [random.randint(1, num_nations) for _ in range(num_customers)],
    'phone_number': [generate_random_phone() for _ in range(num_customers)],
    'account_balance': [round(random.uniform(0, 10000), 2) for _ in range(num_customers)],
    'market_segment': [random.choice(['Segment_A', 'Segment_B', 'Segment_C']) for _ in range(num_customers)],
    'comments': [faker.sentence() for _ in range(num_customers)]
}
customer_df = pd.DataFrame(customer_data)

# Generate random data for Supplier
num_suppliers = 50
supplier_data = {
    'supplier_key': [i+1 for i in range(num_suppliers)],
    'supplier_name': [faker.company() for _ in range(num_suppliers)],
    'supplier_address': [faker.address() for _ in range(num_suppliers)],
    'nation_key': [random.randint(1, num_nations) for _ in range(num_suppliers)],
    'phone_number': [generate_random_phone() for _ in range(num_suppliers)],
    'account_balance': [round(random.uniform(0, 10000), 2) for _ in range(num_suppliers)],
    'comments': [faker.sentence() for _ in range(num_suppliers)]
}
supplier_df = pd.DataFrame(supplier_data)

# Random data for Orders
num_orders = 1000
order_data = {
    'order_key': [i+1 for i in range(num_orders)],
    'customer_key': [random.randint(1, num_customers) for _ in range(num_orders)],
    'order_status': [random.choice(['Pending', 'Processing', 'Shipped']) for _ in range(num_orders)],
    'total_price': [round(random.uniform(10, 1000), 2) for _ in range(num_orders)],
    'order_date': [faker.date_this_year() for _ in range(num_orders)],
    'order_priority': [random.choice(['Low', 'Medium', 'High']) for _ in range(num_orders)],
    'clerk': [faker.name() for _ in range(num_orders)],
    'ship_priority': [random.randint(1, 5) for _ in range(num_orders)],
    'comments': [faker.sentence() for _ in range(num_orders)]
}
orders_df = pd.DataFrame(order_data)

# Generate random data for Partsupp
num_partsupps = 200
partsupp_data = {
    'ID': [i+1 for i in range(num_partsupps)],
    'part_key': [random.randint(1, num_parts) for _ in range(num_partsupps)],
    'supplier_key': [random.randint(1, num_suppliers) for _ in range(num_partsupps)],
    'available_quantity': [random.randint(1, 100) for _ in range(num_partsupps)],
    'supply_cost': [round(random.uniform(1, 100), 2) for _ in range(num_partsupps)],
    'comments': [faker.sentence() for _ in range(num_partsupps)]
}
partsupp_df = pd.DataFrame(partsupp_data)

# Generate random data for Lineitem
num_lineitems = 2000
lineitem_data = {
    'ID': [i+1 for i in range(num_lineitems)],
    'order_key': [random.randint(1, num_orders) for _ in range(num_lineitems)],
    'part_supply_ID': [random.randint(1, num_partsupps) for _ in range(num_lineitems)],
    'line_number': [random.randint(1, 5) for _ in range(num_lineitems)],
    'quantity': [random.randint(1, 10) for _ in range(num_lineitems)],
    'extended_price': [round(random.uniform(10, 100), 2) for _ in range(num_lineitems)],
    'discount': [round(random.uniform(0, 0.5), 2) for _ in range(num_lineitems)],
    'tax': [round(random.uniform(1, 10), 2) for _ in range(num_lineitems)],
    'return_flag': [random.choice(['Y', 'N']) for _ in range(num_lineitems)],
    'line_status': [random.choice(['Pending', 'Shipped']) for _ in range(num_lineitems)],
    'ship_date': [faker.date_between(start_date='-1y', end_date='today') for _ in range(num_lineitems)],
    'commitment_date': [faker.date_between(start_date='-1y', end_date='today') for _ in range(num_lineitems)],
    'receipt_date': [faker.date_between(start_date='-1y', end_date='today') for _ in range(num_lineitems)],
    'ship_instructions': [faker.sentence() for _ in range(num_lineitems)],
    'ship_mode': [random.choice(['Air', 'Sea', 'Land']) for _ in range(num_lineitems)],
    'comments': [faker.sentence() for _ in range(num_lineitems)]
}
lineitem_df = pd.DataFrame(lineitem_data)

# Save data to CSV files
region_df.to_csv('Region.csv',sep=',', index=False)
nation_df.to_csv('Nation.csv',sep=',', index=False)
part_df.to_csv('Part.csv',sep=',', index=False)
customer_df.to_csv('Customer.csv',sep=',', index=False)
supplier_df.to_csv('Supplier.csv',sep=',', index=False)
orders_df.to_csv('Orders.csv',sep=',', index=False)
partsupp_df.to_csv('Partsupp.csv',sep=',', index=False)
lineitem_df.to_csv('Lineitem.csv',sep=',', index=False)

print("Generated data saved to CSV files.")