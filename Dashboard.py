import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Product Category and City Sales Dashboard")

file = 'products_dataset.csv'
df_product = pd.read_csv(file)
file2 = 'product_category_name_translation.csv'
df_translation = pd.read_csv(file2)
merged_df = pd.merge(df_product, df_translation, on='product_category_name', how='inner')
df = merged_df
df.drop('product_category_name', axis='columns', inplace=True)
file3 = 'order_items_dataset.csv'
df_orderitem = pd.read_csv(file3)
file4 = 'orders_dataset.csv'
df_order = pd.read_csv(file4)
file5 = 'customers_dataset.csv'
df_customer = pd.read_csv(file5)

df = pd.merge(df, df_orderitem, on='product_id', how='inner')
df = pd.merge(df, df_order[['order_status', 'order_purchase_timestamp', 'order_id', 'customer_id']], on='order_id', how='inner')
df = pd.merge(df, df_customer, on='customer_id', how='inner')

st.sidebar.header("Filter by Category")
all_categories = df['product_category_name_english'].unique()

selected_categories = st.sidebar.multiselect('Select Categories', all_categories)
if selected_categories:
    filtered_df = df[df['product_category_name_english'].isin(selected_categories)]
else:
    filtered_df = df 

category_sales = filtered_df.groupby('product_category_name_english')['price'].sum()

top10_sales = category_sales.sort_values(ascending=False).head(10)

fig, ax = plt.subplots()
top10_sales.sort_values(ascending=True).plot(kind='barh', ax=ax)
ax.set_title("Top 10 Categories by Sales")
ax.set_ylabel("Product Category")
ax.set_xlabel("Total Sales (Price)")

st.pyplot(fig)

city_sales = df.groupby('customer_city')['price'].sum()
city_sales_with_total = [f"{city} (Total: ${sales:,.2f})" for city, sales in city_sales.items()]

st.sidebar.header("Top 5 City Sales Filter")
selected_cities_with_total = st.sidebar.multiselect('Select Cities (max 5)', city_sales_with_total, max_selections=5)
selected_cities = [city.split(" (")[0] for city in selected_cities_with_total]

explode_selection_with_total = st.sidebar.multiselect('Select Cities to Explode', selected_cities_with_total)
explode_selection = [city.split(" (")[0] for city in explode_selection_with_total]

if selected_cities:
    filtered_city_sales = city_sales[selected_cities].sort_values(ascending=False)
else:
    filtered_city_sales = city_sales.sort_values(ascending=False).head(5)  # Default to top 5 cities by sales

explode = [0.1 if city in explode_selection else 0 for city in filtered_city_sales.index]

fig2, ax2 = plt.subplots()
ax2.pie(filtered_city_sales, labels=filtered_city_sales.index, explode=explode, autopct='%1.1f%%', startangle=90)
ax2.set_title("Top 5 City Sales")

st.pyplot(fig2)

#Run dengan syntax pipenv run streamlit run Dashboard.py


