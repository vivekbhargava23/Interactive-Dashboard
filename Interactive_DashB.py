



import pandas as pd
import plotly.express as px
import streamlit as st



df = pd.read_excel(
    io = 'supermarkt_sales.xlsx',
    engine = 'openpyxl',
    skiprows = 3,
    usecols = 'B:R',
    nrows = 1000
    )

# Separating hourly data 
df.info()
# So "Time" column is an object type not a datetime type; so we convert it into datetime

df["hour"] = pd.to_datetime(df["Time"], format ="%H:%M:%S")  # this converts time coulumn into datatime format
df["hour"] = pd.to_datetime(df["Time"], format ="%H:%M:%S").dt.hour # Now we extract the hour information


# Setting Basci config of the web app

st.set_page_config(
    page_title= ('Sales Dashboard'),
    layout= 'wide'
    
    )


#st.dataframe(df)


# ---- Sidebar -----
st.sidebar.header("Please Filter here:")

city = st.sidebar.multiselect(
    "Select the City:", 
    options = df["City"].unique(),
    default = df["City"].unique()
    )


customer_type = st.sidebar.multiselect(
    "Select the Customer_type:", 
    options = df["Customer_type"].unique(),
    default = df["Customer_type"].unique()
    )


gender = st.sidebar.multiselect(
    "Select the Gender:", 
    options = df["Gender"].unique(),
    default = df["Gender"].unique()
    )

# Filter the Dataframe using query

df_selection = df.query(
    "City == @city & Customer_type == @customer_type & Gender ==@gender"
    
    )

#st.dataframe(df_selection)



# -------- Displaying KPIs -----------
st.title(":bar_chart: Sales Dashboard")

# Inserting paragraph using markdown field

st.markdown("##")

total_sales = int(df_selection["Total"].sum())
avg_rating = round(df_selection["Rating"].mean(),1)
star_rating = ":star:" *  int(round(avg_rating,0)) 
avg_sale_by_transaction = int(df_selection["Total"].mean())

left_col, mid_col, right_col = st.columns(3)

with left_col:
    st.subheader("Total Sales")
    st.subheader(f"US $ {total_sales:,}")
 
with mid_col:
    st.subheader("Average Rating")
    #st.markdown(f"{avg_rating:,} {star_rating}")
    st.subheader(f"{avg_rating:,} {star_rating}")

with right_col:
    st.subheader("Average Sales per Transaction")
    st.subheader(f"US $ {avg_sale_by_transaction}")
    
st.markdown("---")


# Understand groupby method
df1 = df.groupby(by="Product line")     # creates a group type of object, it doesnt have any integerish values here
df1 = df.groupby(by="Product line").sum()       #this gives the sum of all possible columns, which store numerical types of values, some columns may have string values those are not shown
df1 = df.groupby(by="Product line").sum()[["Total"]]    # filtering only TOTAL columns      # putting two [[]] makes it a dataframe
#df1 = df.groupby(by="Product line").sum()["Total"]   this is a series and not a dataframe


 
df_sales_by_prod_line = df_selection.groupby(by="Product line").sum()[["Total"]].sort_values(by = "Total")


fig1_product_sales = px.bar(
    df_sales_by_prod_line,
    x = "Total",
    y = df_sales_by_prod_line.index,
    orientation="h", # could use h here
    template= "plotly_white",
    title=("<b> Sales by product </b>"),
    
    )
st.plotly_chart(fig1_product_sales,use_container_width=True)




# ---------- Displaying sales by hours ----------

# Separating hourly data 

df_sales_by_hour = df_selection.groupby(by="hour").sum()[["Total"]]

fig2_hourly_sales = px.bar(
    df_sales_by_hour,
    x = df_sales_by_hour.index,
    y = "Total",
    title = "<b>Sales by hour</b>"
    )


st.plotly_chart(fig2_hourly_sales,use_container_width=True)



# ------ printing the two graphs together --------
left_col, right_col = st.columns(2)
left_col.plotly_chart(fig1_product_sales, use_container_width=True)
right_col.plotly_chart(fig2_hourly_sales, use_container_width=True)





































