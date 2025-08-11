import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime

# Load the processed data
df = pd.read_csv('soul_foods_pink_morsels_sales.csv')

# Convert date column to datetime
df['date'] = pd.to_datetime(df['date'])

# Sort by date
df = df.sort_values('date')

# Create the Dash app
app = dash.Dash(__name__)

# Define the layout
app.layout = html.Div([
    # Header
    html.H1("Soul Foods - Pink Morsels Sales Analysis Dashboard", 
             style={'textAlign': 'center', 'color': '#2E86AB', 'marginBottom': 30}),
    
    # Subtitle explaining the business question
    html.H3("Business Question: Were sales higher before or after the Pink Morsel price increase on January 15, 2021?",
             style={'textAlign': 'center', 'color': '#A23B72', 'marginBottom': 20}),
    
    # Date range selector
    html.Div([
        html.Label("Select Date Range:"),
        dcc.DatePickerRange(
            id='date-picker',
            start_date=df['date'].min(),
            end_date=df['date'].max(),
            display_format='YYYY-MM-DD'
        )
    ], style={'margin': '20px', 'textAlign': 'center'}),
    
    # Region filter
    html.Div([
        html.Label("Filter by Region:"),
        dcc.Dropdown(
            id='region-filter',
            options=[
                {'label': 'All Regions', 'value': 'all'},
                {'label': 'North', 'value': 'north'},
                {'label': 'South', 'value': 'south'},
                {'label': 'East', 'value': 'east'},
                {'label': 'West', 'value': 'west'}
            ],
            value='all',
            style={'width': '200px', 'margin': '0 auto'}
        )
    ], style={'margin': '20px', 'textAlign': 'center'}),
    
    # Main line chart
    dcc.Graph(
        id='sales-chart',
        style={'height': '600px'}
    ),
    
    # Summary statistics
    html.Div([
        html.H4("Summary Statistics", style={'textAlign': 'center', 'color': '#F18F01'}),
        html.Div(id='summary-stats', style={'textAlign': 'center', 'margin': '20px'})
    ]),
    
    # Business insight
    html.Div([
        html.H4("Business Insight", style={'textAlign': 'center', 'color': '#C73E1D'}),
        html.Div(id='business-insight', style={'textAlign': 'center', 'margin': '20px', 'fontSize': '18px'})
    ]),
    
    # Footer
    html.Footer([
        html.P("Soul Foods Sales Analysis Dashboard - Created with Dash",
               style={'textAlign': 'center', 'color': '#666', 'marginTop': '40px'})
    ])
])

@app.callback(
    [Output('sales-chart', 'figure'),
     Output('summary-stats', 'children'),
     Output('business-insight', 'children')],
    [Input('date-picker', 'start_date'),
     Input('date-picker', 'end_date'),
     Input('region-filter', 'value')]
)
def update_chart(start_date, end_date, region_filter):
    # Filter data based on selected date range and region
    filtered_df = df.copy()
    
    if start_date and end_date:
        filtered_df = filtered_df[
            (filtered_df['date'] >= start_date) & 
            (filtered_df['date'] <= end_date)
        ]
    
    if region_filter != 'all':
        filtered_df = filtered_df[filtered_df['region'] == region_filter]
    
    # Create the line chart
    fig = go.Figure()
    
    # Add line for each region
    for region in filtered_df['region'].unique():
        region_data = filtered_df[filtered_df['region'] == region]
        fig.add_trace(go.Scatter(
            x=region_data['date'],
            y=region_data['sales'],
            mode='lines+markers',
            name=region.title(),
            line=dict(width=2),
            marker=dict(size=6)
        ))
    
    # Add vertical line for January 15, 2021 (price increase date)
    price_increase_date = '2021-01-15'
    if pd.to_datetime(price_increase_date) >= filtered_df['date'].min() and pd.to_datetime(price_increase_date) <= filtered_df['date'].max():
        fig.add_vline(
            x=price_increase_date,
            line_dash="dash",
            line_color="red",
            annotation_text="Price Increase: Jan 15, 2021",
            annotation_position="top right"
        )
    
    # Update layout
    fig.update_layout(
        title="Pink Morsels Sales Over Time by Region",
        xaxis_title="Date",
        yaxis_title="Sales ($)",
        hovermode='x unified',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    
    # Update x-axis to show dates nicely
    fig.update_xaxes(
        gridcolor='lightgray',
        showgrid=True
    )
    
    # Update y-axis
    fig.update_yaxes(
        gridcolor='lightgray',
        showgrid=True
    )
    
    # Calculate summary statistics
    total_sales = filtered_df['sales'].sum()
    avg_sales = filtered_df['sales'].mean()
    total_records = len(filtered_df)
    
    # Calculate sales before and after price increase if the date is in range
    price_increase_date = pd.to_datetime('2021-01-15')
    if price_increase_date >= filtered_df['date'].min() and price_increase_date <= filtered_df['date'].max():
        before_increase = filtered_df[filtered_df['date'] < price_increase_date]['sales'].sum()
        after_increase = filtered_df[filtered_df['date'] >= price_increase_date]['sales'].sum()
        
        summary_stats = html.Div([
            html.P(f"Total Sales: ${total_sales:,.2f}"),
            html.P(f"Average Daily Sales: ${avg_sales:.2f}"),
            html.P(f"Total Records: {total_records:,}"),
            html.P(f"Sales Before Price Increase (Jan 15, 2021): ${before_increase:,.2f}"),
            html.P(f"Sales After Price Increase (Jan 15, 2021): ${after_increase:,.2f}")
        ])
        
        # Determine business insight
        if after_increase > before_increase:
            insight = f"📈 Sales were HIGHER after the price increase! Sales increased by ${after_increase - before_increase:,.2f} after January 15, 2021."
        else:
            insight = f"📉 Sales were LOWER after the price increase. Sales decreased by ${before_increase - after_increase:,.2f} after January 15, 2021."
    else:
        summary_stats = html.Div([
            html.P(f"Total Sales: ${total_sales:,.2f}"),
            html.P(f"Average Daily Sales: ${avg_sales:.2f}"),
            html.P(f"Total Records: {total_records:,}"),
            html.P("Note: Price increase date (Jan 15, 2021) not in selected date range")
        ])
        insight = "Select a date range that includes January 15, 2021 to see the impact of the price increase."
    
    return fig, summary_stats, insight

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050) 