import streamlit as st
import pandas as pd
import plotly.express as px
import mysql.connector
from mysql.connector import Error

# 🌍 App Settings
st.set_page_config(page_title="Nifty 50 Stock Dashboard", layout="wide")
st.title("📈 Nifty 50 Stock Analysis Dashboard")

# 🔌 TiDB DB connection
@st.cache_data
def load_data():
    try:
        connection = mysql.connector.connect(
            host="gateway01.ap-southeast-1.prod.aws.tidbcloud.com",
            port=4000,
            user="2yYzWuNLpsRGRUo.root",
            password="LziV3VzKcgY6K7lq",
            database="yearly_stocks",
        )
        query = "SELECT * FROM yearly_stocks.stock_data"
        df = pd.read_sql(query, connection)
        df['date'] = pd.to_datetime(df['date'])
        return df
    except Error as e:
        st.error(f"Failed to connect: {e}")
        return pd.DataFrame()

# Load data
df = load_data()

if df.empty:
    st.warning("No data available from TiDB.")
    st.stop()


# 📦 Sidebar Filters
st.sidebar.header("🔎 Filter Options")

# Year filter
df['year'] = df['date'].dt.year
years = sorted(df['year'].unique())
selected_years = st.sidebar.multiselect("Select Year(s)", years, default=years)

# Month filter
df['month'] = df['date'].dt.to_period('M').astype(str)
months = sorted(df['month'].unique())
selected_months = st.sidebar.multiselect("Select Month(s)", months, default=months)

# Date filter
min_date = df['date'].min()
max_date = df['date'].max()
selected_date_range = st.sidebar.date_input("Select Date Range", [min_date, max_date])

# Sector filter
all_sectors = df['sector'].dropna().unique().tolist()
selected_sectors = st.sidebar.multiselect("Select Sector(s)", all_sectors, default=all_sectors)

# Top N slider
top_n = st.sidebar.slider("Select Top N Stocks", min_value=5, max_value=15, value=10)

# ✅ Apply Filters
filtered_df = df[
    (df['year'].isin(selected_years)) &
    (df['month'].isin(selected_months)) &
    (df['sector'].isin(selected_sectors)) &
    (df['date'] >= pd.to_datetime(selected_date_range[0])) &
    (df['date'] <= pd.to_datetime(selected_date_range[1]))
].copy()

# ➕ Add daily return before it's needed
filtered_df['daily_return'] = filtered_df.groupby('ticker')['close'].pct_change()

# 📊 Market Summary
st.markdown(" ")
st.markdown("---")
st.markdown("### 📊 Market Summary")

summary_returns = filtered_df.sort_values('date').groupby('ticker')['close'].agg(['first', 'last']).reset_index()
summary_returns['status'] = summary_returns.apply(lambda row: 'Green' if row['last'] > row['first'] else 'Red', axis=1)

green_count = (summary_returns['status'] == 'Green').sum()
red_count = (summary_returns['status'] == 'Red').sum()

avg_price = filtered_df['close'].mean()
avg_volume = filtered_df['volume'].mean()

col_summary1, col_summary2, col_summary3 = st.columns(3)
with col_summary1:
    st.metric("🟢 Green Stocks", green_count)
    st.metric("🔴 Red Stocks", red_count)
with col_summary2:
    st.metric("📈 Average Close Price", f"{avg_price:.2f}")
with col_summary3:
    st.metric("📊 Average Volume", f"{avg_volume:,.0f}")

# 🏆 Yearly Top Gainers & Losers
st.markdown(" ")
st.markdown("---")
st.markdown("### 🏆 Yearly Top Gainers & Losers")

returns = filtered_df.sort_values('date').groupby('ticker')['close'].agg(['first', 'last'])
returns['return'] = (returns['last'] / returns['first']) - 1
returns = returns['return'].sort_values(ascending=False)

col1, col2 = st.columns(2)
with col1:
    st.write(f"Top {top_n} Gainers")
    st.dataframe(returns.head(top_n).round(4).reset_index())
with col2:
    st.write(f"Top {top_n} Losers")
    st.dataframe(returns.tail(top_n).round(4).reset_index())

# 💥 Volatility
st.markdown(" ")
st.markdown("---")
st.markdown(f"### 💥 Volatility - Top {top_n} Most Volatile Stocks")

volatility = filtered_df.groupby('ticker')['daily_return'].std().sort_values(ascending=False).head(top_n).reset_index()
fig_vol = px.bar(volatility, x='ticker', y='daily_return', title=f'Top {top_n} Most Volatile Stocks')
st.plotly_chart(fig_vol, use_container_width=True)

# 📈 Cumulative Return
st.markdown(" ")
st.markdown("---")
st.markdown(f"### 📈 Cumulative Return Over Time (Top {top_n})")

top_tickers = returns.head(top_n).index
cum_df = filtered_df[filtered_df['ticker'].isin(top_tickers)].copy()
cum_df['cumulative_return'] = cum_df.groupby('ticker')['daily_return'].cumsum()
fig_cum = px.line(cum_df, x='date', y='cumulative_return', color='ticker', title=f"Cumulative Return (Top {top_n} Stocks)")
st.plotly_chart(fig_cum, use_container_width=True)

# 🏭 Sector-wise Performance
st.markdown(" ")
st.markdown("---")
st.markdown("### 🏭 Sector-wise Performance")

sector_returns = filtered_df.sort_values('date').groupby('ticker')['close'].agg(['first', 'last']).reset_index()
sector_returns['yearly_return'] = (sector_returns['last'] / sector_returns['first']) - 1
ticker_sector_map = filtered_df[['ticker', 'sector']].drop_duplicates()
sector_returns = sector_returns.merge(ticker_sector_map, on='ticker', how='left')
sector_grouped = sector_returns.groupby('sector')['yearly_return'].mean().reset_index().sort_values(by='yearly_return', ascending=False)
fig_sector = px.bar(sector_grouped, x='sector', y='yearly_return', title='📊 Average Yearly Return by Sector', labels={'yearly_return': 'Avg Return'}, color='sector')
st.plotly_chart(fig_sector, use_container_width=True)

# 📊 Correlation Heatmap
st.markdown(" ")
st.markdown("---")
st.markdown("### 📊 Correlation Heatmap of Daily % Change in Closing Prices")

# Step 1: Pivot table for closing prices
pivot_table = filtered_df.pivot(index='date', columns='ticker', values='close')

# Step 2: Calculate % daily change
returns_pct = pivot_table.pct_change().dropna() * 100

# Step 3: Correlation matrix
corr_matrix = returns_pct.corr()

# Step 4: Plot correlation heatmap
fig_corr = px.imshow(
    corr_matrix,
    title="Stock Price Correlation Heatmap (Daily % Change)",
    color_continuous_scale='RdBu_r',
    text_auto=".2f",
    width=1200,
    height=700
)
st.plotly_chart(fig_corr, use_container_width=False)


# 🗓️ Monthly Gainers and Losers
st.markdown(" ")
st.markdown("---")
st.markdown("### 🗓️ Monthly Gainers and Losers")

monthly = filtered_df.groupby(['month', 'ticker'])['close'].agg(['first', 'last']).reset_index()
monthly['monthly_return'] = (monthly['last'] / monthly['first']) - 1

if selected_months:
    monthly_selected = monthly[monthly['month'].astype(str) == selected_months[0]]
    top_month = monthly_selected.sort_values('monthly_return', ascending=False).head(top_n)
    bottom_month = monthly_selected.sort_values('monthly_return').head(top_n)

    col3, col4 = st.columns(2)
    with col3:
        fig_top = px.bar(top_month, x='ticker', y='monthly_return', title=f"Top {top_n} Gainers - {selected_months[0]}")
        st.plotly_chart(fig_top, use_container_width=True)
    with col4:
        fig_bottom = px.bar(bottom_month, x='ticker', y='monthly_return', title=f"Top {top_n} Losers - {selected_months[0]}")
        st.plotly_chart(fig_bottom, use_container_width=True)

# 📌 Footer
st.markdown("---")
st.caption("Data-driven stock analysis using Streamlit & Plotly")
