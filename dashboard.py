import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Read data
orders_df = pd.read_csv('./data/orders.csv')
lineitem_df = pd.read_csv('./data/lineitem.csv')
supplier_df = pd.read_csv('./data/supplier.csv')
partsupp_df = pd.read_csv('./data/partsupp.csv')
customer_df = pd.read_csv('./data/customer.csv')
nation_df = pd.read_csv('./data/nation.csv')
region_df = pd.read_csv('./data/region.csv')

# Merge orders and lineitem dataframes to get sales information
merged_df = pd.merge(orders_df, lineitem_df, on='order_key')
merged_df['total_sales'] = merged_df['quantity'] * merged_df['extended_price']

# Convert order date to datetime format
merged_df['order_date'] = pd.to_datetime(merged_df['order_date'])

# Merge with Nation dataframe to get nation/region information
merged_df = pd.merge(merged_df, customer_df, on='customer_key')
merged_df = pd.merge(merged_df, nation_df, on='nation_key', suffixes=('_order', '_nation'))
merged_df = pd.merge(merged_df, region_df, on='region_key', suffixes=('_nation', '_region'))

# Create a Streamlit instance
# Create a Streamlit instance
st.set_page_config(page_title="Claudy Consulting", page_icon=":cloud:",layout="wide")
with open('style.css') as reader:
    st.markdown(f'<style>{reader.read()}</style>', unsafe_allow_html=True)


# Sidebar
st.sidebar.header('Welcome to Claudy Consulting :cloud: Official Dashboard')
st.sidebar.image("./images/embedded_analytics.PNG", use_column_width=True)
st.sidebar.subheader('Unlocking Revenue with Embedded Analytics')
st.sidebar.write('We are pioneering the realization of embedded analytics solutions for software companies. Let us be your travel guide on the journey to transforming how your customers and partners experience data.')
st.sidebar.subheader('More about us:')
st.sidebar.link_button("Our company", "https://www.claudyconsulting.com/")
st.sidebar.link_button("Our team", "https://www.linkedin.com/in/marcel-kintscher/")

# Group sales data by date
sales_over_time = merged_df.groupby('order_date')['total_sales'].sum().reset_index()

startDate = pd.to_datetime(sales_over_time['order_date']).min()
endDate = pd.to_datetime(sales_over_time['order_date']).max()

col1, col2 = st.columns(2)

with col1:
    col3, col4 = st.columns(2)
    with col3:
        date1 = pd.to_datetime(st.date_input("Start Date", startDate))
    with col4:
        date2 = pd.to_datetime(st.date_input("End Date", endDate))

    sales_over_time = sales_over_time[(sales_over_time["order_date"] >= date1) & (sales_over_time["order_date"] <= date2)].copy()

    # Plot sales over time
    fig = px.line(sales_over_time, x='order_date', y='total_sales', labels={"order_date": "Date", "total_sales": "Total Sales (USD)"}, title='Sales Over Time')
    fig.update_layout(title_x=0.5, margin=dict(l=20, r=20, t=120, b=20), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',  font=dict(color='rgb(20, 20, 20)'), showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # Sales and Profits by Nation/Region
    sales_profit_by_nation = merged_df.groupby(['nation_name', 'region_name']).agg({'total_sales':'sum', 'total_price':'sum'}).reset_index()
    sales_profit_by_nation = sales_profit_by_nation.sort_values(by=['total_price'])

    fig3 = go.Figure(data=[
        go.Bar(name='Sales', x=sales_profit_by_nation['nation_name'], y=sales_profit_by_nation['total_sales'], marker_color='darkblue'),
        go.Bar(name='Profits', x=sales_profit_by_nation['nation_name'], y=sales_profit_by_nation['total_price'], marker_color='lightcoral')
    ])
    fig3.update_layout(barmode='group', margin=dict(l=50, r=50, t=50, b=10), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',  
    font=dict(color='rgb(20, 20, 20)'), showlegend=True)
    st.subheader('Sales and profits by Nation')
    st.plotly_chart(fig3, use_container_width=True)

# Top 10 Customers by Sales
top_customers_sales = customer_df.merge(merged_df.groupby('customer_key')['total_sales'].sum().nlargest(10).reset_index(), on='customer_key')
top_customers_sales_sorted = pd.merge(top_customers_sales, nation_df, left_on='nation_key', right_on='nation_key', how='left')

# Top 10 Customers by Profit
top_customers_profit = customer_df.merge(merged_df.groupby('customer_key')['total_price'].sum().nlargest(10).reset_index(), on='customer_key')
top_customers_profit_sorted = pd.merge(top_customers_profit, nation_df, left_on='nation_key', right_on='nation_key', how='left')

# Top 10 Suppliers by Sales
top_suppliers_sales = supplier_df.merge(partsupp_df.groupby('supplier_key')['supply_cost'].sum().nlargest(10).reset_index(), on='supplier_key')
top_suppliers_sales_sorted = pd.merge(top_suppliers_sales, nation_df, left_on='nation_key', right_on='nation_key', how='left')

col1, col2 = st.columns(2)

with col1:
    # Add a dropdown to select the table to display
    option = st.selectbox('Select a table', ('Top 10 Customers by Sales', 'Top 10 Customers by Profit', 'Top 10 Suppliers by Sales'))

    if option == 'Top 10 Customers by Sales':
        # Display Top 10 Customers by Sales
        fig = px.bar(top_customers_sales_sorted, x='nation_name', y='total_sales', color='customer_name', labels={"customer_name": "Customer Name", "total_sales": "Total Sales (USD)", "nation_name": "Nation"}, title='Top 10 Customers by Sales')
        fig.update_layout(title_x=0.5, margin=dict(l=20, r=20, t=50, b=20), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',  font=dict(color='rgb(20, 20, 20)'), showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    elif option == 'Top 10 Customers by Profit':
        # Display Top 10 Customers by Profit
        fig = px.bar(top_customers_profit_sorted, x='nation_name', y='total_price', color='customer_name', labels={"customer_name": "Customer Name", "total_price": "Total Profit (USD)", "nation_name": "Nation"}, title='Top 10 Customers by Profit')
        fig.update_layout(title_x=0.5, margin=dict(l=20, r=20, t=50, b=20), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',  font=dict(color='rgb(20, 20, 20)'), showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    elif option == 'Top 10 Suppliers by Sales':
        # Display Top 10 Suppliers by Cost
        fig = px.bar(top_suppliers_sales_sorted, x='nation_name', y='supply_cost', color='supplier_name', labels={"supplier_name": "Supplier Name", "supply_cost": "Total Cost (USD)", "nation_name": "Nation"}, title='Top 10 Suppliers by Sales')
        fig.update_layout(title_x=0.5, margin=dict(l=20, r=20, t=50, b=20), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', showlegend=False,  font=dict(color='rgb(20, 20, 20)'))
        st.plotly_chart(fig, use_container_width=True)

with col2:
    # Impact of Returns on Sales and Discount vs. Sales
    merged_df['returns'] = merged_df['return_flag'].apply(lambda x: 1 if x == 'R' else 0)

    color_map = {'R': 'lightblue', 'N': 'lightcoral'}
    merged_df = merged_df.sort_values(by=['total_sales'])
    merged_df['discount'] = merged_df['discount'] * 100

    # Plot scatter plot with customized colors
    fig_scatter = px.scatter(merged_df, x='discount', y='total_sales', 
                            color_discrete_map=color_map, 
                            labels={'discount': 'Discount (%)', 'total_sales': 'Total Sales'}, 
                            title='Impact of Discounts', 
                            hover_name='order_date', hover_data=['customer_name'])

    # Update layout of the scatter plot
    fig_scatter.update_layout(
        margin=dict(l=20, r=20, t=50, b=20), 
        paper_bgcolor='rgba(0,0,0,0)', 
        plot_bgcolor='rgba(0,0,0,0)',  
        font=dict(color='rgb(20, 20, 20)'), 
        showlegend=False)

    # Add a slider to filter data based on discount
    discount_range = st.slider('Select discount range', min_value=0, max_value=0, value=(0, 100))

    # Filter data based on selected discount range
    filtered_df = merged_df[(merged_df['discount'] >= discount_range[0]) & (merged_df['discount'] <= discount_range[1])]

    # Plot filtered data
    fig_scatter_filtered = px.scatter(filtered_df, x='discount', y='total_sales', 
                                    color_discrete_map=color_map, 
                                    labels={'discount': 'Discount (%)', 'total_sales': 'Total Sales'}, 
                                    title='Impact of Discounts (Filtered)', 
                                    hover_name='order_date', hover_data=['customer_name'])

    # Update layout of the filtered scatter plot
    fig_scatter_filtered.update_layout(
        margin=dict(l=40, r=20, t=50, b=20), 
        paper_bgcolor='rgba(0,0,0,0)', 
        plot_bgcolor='rgba(0,0,0,0)',  
        font=dict(color='rgb(20, 20, 20)'), 
        showlegend=False)

    # Display the filtered scatter plot
    st.plotly_chart(fig_scatter_filtered, use_container_width=True)
