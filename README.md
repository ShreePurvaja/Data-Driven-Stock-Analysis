# Stock Market Analysis Project

## Overview
This project performs an in-depth analysis of stock market data over the past year using Python, TIDB SQL, Streamlit, Seaborn, and Power BI. It focuses on extracting, transforming, analyzing, and visualizing stock performance to provide meaningful business insights and decision support for investors.

## Business Use Cases
- **Stock Performance Ranking**: Identify the top 10 best-performing (green) and worst-performing (red) stocks.
- **Market Overview**: Visualize overall market trends including average performance and green/red stock ratios.
- **Investment Insights**: Highlight consistently growing stocks and those with significant declines.
- **Decision Support**: Offer insights on average prices, volatility, and stock behavior for informed decision-making.

## Tools Used
- Python
- TIDB SQL
- Streamlit
- Seaborn
- Power BI

---

## Project Steps

### Step 1: Data Extraction and Transformation
- **Input Format**: YAML files organized by months and dates.
- **Goal**: Convert all data into CSV format.
- **Process**:
  1. Loop through each month's directory.
  2. For each date-wise YAML file, extract relevant fields (e.g., symbol, close price, volume).
  3. Organize data by symbols.
  4. Save each symbol’s data into a separate CSV file.
- **Output**: 50+ CSV files, one per stock symbol.

### Step 2: Data Preprocessing and Loading
- **Tools Used**: Pandas, NumPy
- **Actions**:
  - Load all CSVs into a combined DataFrame.
  - Parse date columns and ensure correct data types.
  - Handle missing values and outliers.
  - Calculate daily returns.

---

## Data Analysis & Visualization

### 1. Stock Performance Ranking
- **Objective**: Identify top 10 green and bottom 10 red stocks based on yearly returns.
- **Method**:
  - Compute annual return for each stock.
  - Sort and select top/bottom 10.
- **Visualization**: Bar chart showing the performance.

### 2. Market Overview
- **Metrics**:
  - Average stock price
  - Average volume
  - Count of green vs. red stocks
- **Visualization**: Summary dashboard with KPIs and pie/bar charts.

### 3. Volatility Analysis
- **Objective**: Measure stock risk via standard deviation of daily returns.
- **Steps**:
  - Calculate daily return: `(Close - Prev Close) / Prev Close`
  - Compute standard deviation for each stock.
  - Select top 10 most volatile stocks.
- **Visualization**: Bar chart of volatility by stock.

### 4. Cumulative Return Over Time
- **Objective**: Show cumulative return trends for top stocks.
- **Steps**:
  - Compute cumulative return by summing daily returns.
  - Select top 5 performers.
- **Visualization**: Line chart of cumulative returns.

### 5. Sector-wise Performance
- **Objective**: Analyze performance by industry sector.
- **Steps**:
  - Merge sector classification CSV with stock data.
  - Compute average yearly return per sector.
- **Visualization**: Bar chart with sector names on x-axis and return on y-axis.

### 6. Stock Price Correlation
- **Objective**: Understand relationships between different stocks.
- **Steps**:
  - Create a pivot table with stocks and their daily returns.
  - Calculate correlation matrix using `.corr()`.
- **Visualization**: Heatmap showing correlation coefficients.

### 7. Monthly Gainers and Losers
- **Objective**: Highlight top 5 gainers and losers for each month.
- **Steps**:
  - Group by month.
  - Compute monthly return for each stock.
  - Extract top and bottom 5 for each month.
- **Visualization**: 12 sets of dual bar charts (one for each month).

---

## Dashboards
- **Streamlit App**: Interactive web dashboard for all visualizations and KPIs.
- **Power BI**: Professional business dashboard with slicers and detailed insights.

---

## How to Run
1. **Install Requirements**
```bash
pip install -r requirements.txt
```

2. **Extract YAML to CSV**
```bash
python scripts/extract_yaml_to_csv.py
```

3. **Launch Streamlit Dashboard**
```bash
streamlit run app.py
```

---

## License
This project is open-source and available under the MIT License.

---

## Acknowledgements
- [Pandas](https://pandas.pydata.org/)
- [Seaborn](https://seaborn.pydata.org/)
- [Streamlit](https://streamlit.io/)
- [Power BI](https://powerbi.microsoft.com/)
- [TIDB](https://www.pingcap.com/en/products/tidb/)

---

> Feel free to fork this repo, raise issues, or suggest improvements!
