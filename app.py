import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

df=pd.read_csv("cleaned_eda_sales3.csv")
df["order_date"] = pd.to_datetime(df["order_date"])

# page configuration

st.set_page_config(
    page_title="Sales Dashboard",
    layout="wide"
)
# title
st.title("SALES DASHBOARD")

# side bar 
# city
city=st.sidebar.selectbox(
    "city",
    ["all"] + df["city"].unique().tolist()
)

category=st.sidebar.selectbox(
    "category",
    ["all"] + df["category"].unique().tolist()
)

customer=st.sidebar.selectbox(
    "customer_type",
    ["all"] + df["customer_type"].unique().tolist()
)

month_order = [
    "January", "February", "March", "April",
    "May", "June", "July", "August",
    "September", "October", "November", "December"
]

month = st.sidebar.selectbox(
    "Month",
    ["all"] +[i for i in month_order if i in df["order_date"].dt.month_name().unique().tolist()]
)

date=st.sidebar.slider("date",min_value=0,max_value=31)

year=st.sidebar.selectbox(
    "year",
    ["all"] + df["order_date"].dt.year.unique().tolist()
)



filtered_by = df.copy()

if city != "all":
    filtered_by = filtered_by[filtered_by["city"] == city]

if category != "all":
    filtered_by = filtered_by[filtered_by["category"] == category]

if customer !="all":
    filtered_by=filtered_by[filtered_by["customer_type"]==customer]

if month != "all":
    filtered_by = filtered_by[
        filtered_by["order_date"].dt.month_name() == month
    ]

if year != "all":
    filtered_by = filtered_by[
        filtered_by["order_date"].dt.year == year
    ]
if date !=0 :
    filtered_by=filtered_by[filtered_by["order_date"].dt.day==date]



col1,col2,col3,col4=st.columns(4)
with col1:
    total_revenu=filtered_by["sales"].sum()

    st.metric(f"total revenue" ,f"{round(total_revenu/1000000,2)} M " )
with col2:

    Total_Orders=filtered_by["order_id"].count()

    st.metric("total orders",f"{Total_Orders}")
with col3:
    Average_Order_Value=filtered_by["sales"].mean()
    st.metric("avg order value ",f"{round(Average_Order_Value,2)}")
with col4:
    Total_Quantity=filtered_by["quantity"].sum()
    st.metric("total quantity" ,f"{Total_Quantity}")



Sales_by_City = filtered_by.groupby("city")["sales"].sum()
st.container()

st.subheader("SALES GRAPHS")
col1,col2=st.columns(2)
with col1:
    Sales_by_City = filtered_by.groupby("city")["sales"].sum()

    st.write("Sales by City")
    st.bar_chart(
            Sales_by_City,
        )
with col2:
    Sales_by_Category=filtered_by.groupby("category")["sales"].sum()

    st.write("sales by category")
    st.bar_chart(
        Sales_by_Category,
        )

st.container()
col1,col2=st.columns(2)
with col1:

    top5_products=filtered_by.groupby("product")["sales"].sum().sort_values(ascending=False).head(5)
    st.write("top 5 products")
    st.bar_chart(top5_products)
with col2:

    filtered_by["month"] = pd.Categorical(
    filtered_by["order_date"].dt.month_name(),
    categories=month_order,
    ordered=True
)

    monthly_sales = (
    filtered_by
    .groupby("month", observed=True)["sales"]
    .sum()
    )
    st.write("sales trend")
    st.line_chart(monthly_sales)

st.container()
col1,col2=st.columns(2)
with col1:
    Sales_by_Payment_Method=filtered_by.groupby("payment_method")["sales"].value_counts().reset_index()

    fig = px.pie(
    Sales_by_Payment_Method,
    names="payment_method",
    values="sales",
    title="Sales by payment_method"
)
    st.plotly_chart(fig, use_container_width=True)
