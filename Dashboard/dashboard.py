import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

# Helper function yang dibutuhkan untuk menyiapkan berbagai dataframe


def create_average_order_value_by_location_df(df):
    average_order_value_by_location = df.groupby(['customer_zip_code_prefix', 'customer_city', 'customer_state'])['price'].mean().reset_index()
    average_order_value_by_location.sort_values(by='price', ascending=False, inplace=True)
    return average_order_value_by_location

def create_delivery_satisfaction_analysis_df(df):
    delivery_satisfaction_analysis = df.groupby('order_status').agg(
    mean_delivery_time=('delivery_time', 'mean'),
    mean_review_score=('review_score', 'mean')
    
    ).reset_index()
    
    return delivery_satisfaction_analysis

def create_sales_distribution_df(df):
    sales_distribution = df.groupby(['product_category_name', 'customer_state'])['price'].sum().reset_index()   
   
    return sales_distribution

def create_monthly_sales_trend_df(df):
    df['order_month'] = df['order_purchase_timestamp'].dt.to_period('M')
    monthly_sales_trend = df.groupby(['order_month', 'product_category_name'])['price'].sum().reset_index()
    monthly_sales_trend.sort_values(by='price', ascending=False, inplace=True)
    return monthly_sales_trend

def create_average_category_sales_df(df):
    average_sales = df.groupby('product_category_name')['price'].mean().reset_index()
    category_sales = average_sales.sort_values(by='price', ascending=False)   
    return category_sales

def create_rfm_df(df):
    rfm_df = all_df.groupby(by="customer_id", as_index=False).agg({
    "order_purchase_timestamp": "max", # mengambil tanggal order terakhir
    "order_id": "nunique", # menghitung jumlah order
    "price": "sum" # menghitung jumlah revenue yang dihasilkan
    })
    rfm_df.columns = ["customer_id", "max_order_timestamp", "frequency", "monetary"]
    
    rfm_df["max_order_timestamp"] = rfm_df["max_order_timestamp"].dt.date
    recent_date = df["order_purchase_timestamp"].dt.date.max()
    rfm_df["recency"] = rfm_df["max_order_timestamp"].apply(lambda x: (recent_date - x).days)
    rfm_df.drop("max_order_timestamp", axis=1, inplace=True)
    
    return rfm_df

# Load cleaned data
all_df = pd.read_csv("all_data.csv")

datetime_columns = ["order_purchase_timestamp", "order_delivered_customer_date"]
all_df.sort_values(by="order_purchase_timestamp", inplace=True)
all_df.reset_index(inplace=True)

for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])

# Filter data
min_date = all_df["order_purchase_timestamp"].min()
max_date = all_df["order_purchase_timestamp"].max()

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = all_df[(all_df["order_purchase_timestamp"] >= str(start_date)) & 
                (all_df["order_purchase_timestamp"] <= str(end_date))]

# st.dataframe(main_df)

# # Menyiapkan berbagai dataframe
average_order_value_by_location_df = create_average_order_value_by_location_df(main_df)
delivery_satisfaction_analysis_df = create_delivery_satisfaction_analysis_df(main_df)
sales_distribution_df = create_sales_distribution_df(main_df)
monthly_sales_trend_df = create_monthly_sales_trend_df(main_df)
average_category_sales_df = create_average_category_sales_df(main_df)
rfm_df = create_rfm_df(main_df)


# plot number of sales distribution
st.subheader("Sales Distribution")

fig = plt.figure(figsize=(14, 7))
sns.barplot(
    data=sales_distribution_df.sort_values(by="price", ascending=False), 
    x='customer_state', 
    y='price', 
    palette='viridis',
    
    )
plt.title('Average Sales by Product Category', fontsize=24)
plt.xlabel('Customer State', fontsize=22)
plt.ylabel('Average Sales (in currency)', fontsize=22)
plt.xticks( rotation=45, ha='right', fontsize=20)
plt.yticks(fontsize=20)
plt.tight_layout()
st.pyplot(fig)


# monthly sales trend
st.subheader("Monthly Sales Trend")

fig= plt.figure(figsize=(24, 20))


monthly_sales_trend_df['order_month'] = monthly_sales_trend_df['order_month'].dt.to_timestamp()

monthly_sales_trend = monthly_sales_trend_df.sort_values('order_month')

for category in monthly_sales_trend['product_category_name'].unique():
    category_data = monthly_sales_trend[monthly_sales_trend['product_category_name'] == category]
    plt.plot(category_data['order_month'], category_data['price'], label=category, marker='o', markersize=3)

plt.title('Monthly Sales Trend by Product Category', fontsize=24)
plt.xlabel('Order Month', fontsize=22)
plt.ylabel('Total Sales (in currency)', fontsize=22)



plt.xticks(rotation=45, ha='right', fontsize=20)
plt.yticks(fontsize=20)


plt.grid(True, linestyle='--', alpha=0.7, axis='both')


plt.legend(title='Product Category', loc='center left', bbox_to_anchor=(1, 0.5), ncol=1)

st.pyplot(fig)

# average sales
st.subheader("Average Sales Per Product")

fig= plt.figure(figsize=(40, 28))
sns.barplot(data=average_category_sales_df, x='product_category_name', y='price', palette='viridis')
plt.title('Average Sales by Product Category', fontsize=32)
plt.xlabel('Product Category', fontsize=28)
plt.ylabel('Average Sales (in currency)', fontsize=28)
plt.xticks(rotation=45, ha='right', fontsize=24)
plt.yticks(fontsize=24)
plt.tight_layout()
st.pyplot(fig)


# Best Customer Based on RFM Parameters
st.subheader("Best Customer Based on RFM Parameters")

col1, col2, col3 = st.columns(3)

with col1:
    avg_recency = round(rfm_df.recency.mean(), 1)
    st.metric("Average Recency (days)", value=avg_recency)

with col2:
    avg_frequency = round(rfm_df.frequency.mean(), 2)
    st.metric("Average Frequency", value=avg_frequency)

with col3:
    avg_frequency = format_currency(rfm_df.monetary.mean(), "AUD", locale='es_CO') 
    st.metric("Average Monetary", value=avg_frequency)

fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(35, 15))
colors = ["#FF6F61", "#6B5B95", "#88B04B", "#F7CAC9", "#92A8D1"]

sns.barplot(y="recency", x="customer_id", data=rfm_df.sort_values(by="recency", ascending=True).head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("customer_id", fontsize=30)
ax[0].set_title("By Recency (days)", loc="center", fontsize=50)
ax[0].tick_params(axis='y', labelsize=30)
ax[0].tick_params(axis='x', labelsize=35, labelrotation=45)



sns.barplot(y="frequency", x="customer_id", data=rfm_df.sort_values(by="frequency", ascending=False).head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("customer_id", fontsize=30)
ax[1].set_title("By Frequency", loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=30)
ax[1].tick_params(axis='x', labelsize=35, labelrotation=45)


sns.barplot(y="monetary", x="customer_id", data=rfm_df.sort_values(by="monetary", ascending=False).head(5), palette=colors, ax=ax[2])
ax[2].set_ylabel(None)
ax[2].set_xlabel("customer_id", fontsize=30)
ax[2].set_title("By Monetary", loc="center", fontsize=50)
ax[2].tick_params(axis='y', labelsize=30)
ax[2].tick_params(axis='x', labelsize=35, labelrotation=45)

st.pyplot(fig)
