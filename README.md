# Soul Foods Sales Analysis Dashboard

This repository contains a comprehensive analysis of Soul Foods' Pink Morsels sales data, including data processing scripts and an interactive dashboard.

## Project Overview

The project addresses the business question: **"Were sales higher before or after the Pink Morsel price increase on January 15, 2021?"**

## Files Description

- **`process_soul_foods_data.py`**: Python script that processes three CSV files containing transaction data for Soul Foods' morsel line
- **`soul_foods_pink_morsels_sales.csv`**: Processed output file containing Sales, Date, and Region data for Pink Morsels only
- **`soul_foods_dashboard.py`**: Interactive Dash application for visualizing sales data and answering the business question
- **`requirements.txt`**: Python dependencies required to run the dashboard

## Data Processing

The data processing script:
1. Filters for only "pink morsel" products from three input CSV files
2. Calculates sales by multiplying price × quantity
3. Combines data from all files into a single output with three columns: Sales, Date, Region

## Dashboard Features

The interactive dashboard includes:
- **Header**: Clear title and business question statement
- **Line Chart**: Sales data visualization over time, sorted by date with appropriate axis labels
- **Interactive Filters**: Date range selector and region filter
- **Summary Statistics**: Key metrics including total sales, averages, and before/after price increase analysis
- **Business Insight**: Clear answer to the business question with supporting data
- **Visual Indicators**: Red dashed line marking the January 15, 2021 price increase date

## Installation and Usage

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the dashboard:
   ```bash
   python soul_foods_dashboard.py
   ```

3. Open your browser and navigate to `http://localhost:8050`

## Business Answer

The dashboard will clearly show whether sales were higher before or after the Pink Morsel price increase on January 15, 2021, providing Soul Foods with actionable insights for their pricing strategy.
