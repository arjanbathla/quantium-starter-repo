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
    # Header with enhanced styling
    html.Div([
        html.H1("🍪 Soul Foods - Pink Morsels Sales Analysis Dashboard", 
                 style={'textAlign': 'center', 'color': '#2E86AB', 'marginBottom': 20, 'fontSize': '2.5em', 'fontWeight': 'bold', 'textShadow': '2px 2px 4px rgba(0,0,0,0.1)'}),
        html.Hr(style={'border': '2px solid #2E86AB', 'width': '80%', 'margin': '0 auto 30px auto'})
    ], style={'backgroundColor': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', 'padding': '30px', 'borderRadius': '15px', 'marginBottom': '30px', 'boxShadow': '0 8px 32px rgba(0,0,0,0.1)'}),
    
    # Subtitle explaining the business question
    html.Div([
        html.H3("🎯 Business Question: Were sales higher before or after the Pink Morsel price increase on January 15, 2021?",
                 style={'textAlign': 'center', 'color': '#A23B72', 'marginBottom': 20, 'fontSize': '1.4em', 'fontWeight': '600'}),
        html.P("Use the filters below to explore sales data by region and date range", 
               style={'textAlign': 'center', 'color': '#666', 'fontSize': '1.1em', 'fontStyle': 'italic'})
    ], style={'backgroundColor': '#fff3cd', 'padding': '20px', 'borderRadius': '10px', 'marginBottom': '30px', 'border': '2px solid #ffeaa7'}),
    
    # Date range selector with enhanced styling
    html.Div([
        html.Label("📅 Select Date Range:", style={'fontSize': '18px', 'fontWeight': 'bold', 'marginBottom': '15px', 'color': '#495057'}),
        dcc.DatePickerRange(
            id='date-picker',
            start_date=df['date'].min(),
            end_date=df['date'].max(),
            display_format='YYYY-MM-DD',
            style={'margin': '0 auto'}
        )
    ], style={'margin': '30px', 'textAlign': 'center', 'padding': '25px', 'backgroundColor': '#e3f2fd', 'borderRadius': '12px', 'boxShadow': '0 4px 8px rgba(0,0,0,0.1)', 'border': '2px solid #bbdefb'}),
    
    # Region filter with radio buttons
    html.Div([
        html.Label("🌍 Filter by Region:", style={'fontSize': '18px', 'fontWeight': 'bold', 'marginBottom': '10px', 'color': '#495057'}),
        dcc.RadioItems(
            id='region-filter',
            options=[
                {'label': '🌍 All Regions', 'value': 'all'},
                {'label': '🧭 North', 'value': 'north'},
                {'label': '🧭 South', 'value': 'south'},
                {'label': '🧭 East', 'value': 'east'},
                {'label': '🧭 West', 'value': 'west'}
            ],
            value='all',
            inline=True,
            style={'margin': '0 auto', 'textAlign': 'center'}
        )
    ], style={'margin': '30px', 'textAlign': 'center', 'padding': '20px', 'backgroundColor': '#f8f9fa', 'borderRadius': '10px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'}),
    
    # Main line chart with enhanced styling
    html.Div([
        html.H4("📊 Sales Performance Over Time", style={'textAlign': 'center', 'color': '#2E86AB', 'marginBottom': '20px', 'fontSize': '1.6em', 'fontWeight': 'bold'}),
        dcc.Graph(
            id='sales-chart',
            style={'height': '600px'}
        )
    ], style={'margin': '30px', 'padding': '25px', 'backgroundColor': 'white', 'borderRadius': '15px', 'boxShadow': '0 8px 25px rgba(0,0,0,0.15)', 'border': '2px solid #e9ecef'}),
    
    # Summary statistics with enhanced styling
    html.Div([
        html.H4("📈 Summary Statistics", style={'textAlign': 'center', 'color': '#F18F01', 'marginBottom': '25px', 'fontSize': '1.5em', 'fontWeight': 'bold'}),
        html.Div(id='summary-stats', style={'textAlign': 'center', 'margin': '20px', 'fontSize': '16px'})
    ], style={'margin': '30px', 'padding': '25px', 'backgroundColor': '#fff8e1', 'borderRadius': '12px', 'boxShadow': '0 4px 12px rgba(0,0,0,0.1)', 'border': '2px solid #ffcc02'}),
    
    # Business insight with enhanced styling
    html.Div([
        html.H4("💡 Business Insight", style={'textAlign': 'center', 'color': '#C73E1D', 'marginBottom': '25px', 'fontSize': '1.5em', 'fontWeight': 'bold'}),
        html.Div(id='business-insight', style={'textAlign': 'center', 'margin': '20px', 'fontSize': '18px', 'fontWeight': '500'})
    ], style={'margin': '30px', 'padding': '25px', 'backgroundColor': '#ffebee', 'borderRadius': '12px', 'boxShadow': '0 4px 12px rgba(0,0,0,0.1)', 'border': '2px solid #ef5350'}),
    
    # Footer with enhanced styling
    html.Footer([
        html.Hr(style={'border': '2px solid #2E86AB', 'width': '60%', 'margin': '40px auto 20px auto'}),
        html.P("🍪 Soul Foods Sales Analysis Dashboard - Created with Dash & Python", 
               style={'textAlign': 'center', 'color': '#666', 'marginTop': '20px', 'fontSize': '16px', 'fontStyle': 'italic'}),
        html.P("📊 Powered by Data-Driven Insights", 
               style={'textAlign': 'center', 'color': '#999', 'marginTop': '10px', 'fontSize': '14px'})
    ], style={'backgroundColor': '#f8f9fa', 'padding': '30px', 'borderRadius': '15px', 'marginTop': '40px'})
], style={'backgroundColor': '#f5f7fa', 'minHeight': '100vh', 'padding': '20px', 'fontFamily': "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif"})

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
    
    # Add line for each region with enhanced styling and colors
    colors = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D', '#6C5CE7']
    for i, region in enumerate(filtered_df['region'].unique()):
        region_data = filtered_df[filtered_df['region'] == region]
        color = colors[i % len(colors)]
        fig.add_trace(go.Scatter(
            x=region_data['date'],
            y=region_data['sales'],
            mode='lines+markers',
            name=region.title(),
            line=dict(width=3, color=color),
            marker=dict(size=8, color=color, line=dict(width=1, color='white')),
            hovertemplate=f'<b>{region.title()}</b><br>' +
                         'Date: %{x}<br>' +
                         'Sales: $%{y:,.2f}<br>' +
                         '<extra></extra>'
        ))
    
    # Add vertical line for January 15, 2021 (price increase date) with enhanced styling
    price_increase_date = '2021-01-15'
    if pd.to_datetime(price_increase_date) >= filtered_df['date'].min() and pd.to_datetime(price_increase_date) <= filtered_df['date'].max():
        fig.add_vline(
            x=price_increase_date,
            line_dash="dash",
            line_color="#FF6B6B",
            line_width=3,
            annotation=dict(
                text="🚨 Price Increase<br>Jan 15, 2021",
                textangle=0,
                font=dict(size=14, color="#FF6B6B"),
                bgcolor="rgba(255, 255, 255, 0.9)",
                bordercolor="#FF6B6B",
                borderwidth=2
            ),
            annotation_position="top right"
        )
    
    # Update layout with enhanced styling
    fig.update_layout(
        title={
            'text': "🍪 Pink Morsels Sales Performance Over Time by Region",
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20, 'color': '#2E86AB', 'family': 'Arial, sans-serif'}
        },
        xaxis_title="📅 Date",
        yaxis_title="💰 Sales ($)",
        hovermode='x unified',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            bgcolor='rgba(255,255,255,0.8)',
            bordercolor='#2E86AB',
            borderwidth=1
        ),
        plot_bgcolor='#f8f9fa',
        paper_bgcolor='white',
        font=dict(family="Arial, sans-serif", size=12),
        margin=dict(l=80, r=80, t=100, b=80)
    )
    
    # Update x-axis to show dates nicely with enhanced styling
    fig.update_xaxes(
        gridcolor='#e9ecef',
        showgrid=True,
        gridwidth=1,
        zeroline=False,
        linecolor='#2E86AB',
        linewidth=2,
        tickfont=dict(size=12, color='#495057')
    )
    
    # Update y-axis with enhanced styling
    fig.update_yaxes(
        gridcolor='#e9ecef',
        showgrid=True,
        gridwidth=1,
        zeroline=True,
        zerolinecolor='#2E86AB',
        zerolinewidth=2,
        linecolor='#2E86AB',
        linewidth=2,
        tickfont=dict(size=12, color='#495057')
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
            html.Div([
                html.Span("💰 ", style={'fontSize': '24px'}),
                html.Span(f"Total Sales: ${total_sales:,.2f}", style={'fontSize': '18px', 'fontWeight': 'bold', 'color': '#2E86AB'})
            ], style={'margin': '15px 0', 'padding': '10px', 'backgroundColor': 'white', 'borderRadius': '8px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'}),
            html.Div([
                html.Span("📊 ", style={'fontSize': '24px'}),
                html.Span(f"Average Daily Sales: ${avg_sales:.2f}", style={'fontSize': '18px', 'fontWeight': 'bold', 'color': '#A23B72'})
            ], style={'margin': '15px 0', 'padding': '10px', 'backgroundColor': 'white', 'borderRadius': '8px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'}),
            html.Div([
                html.Span("📝 ", style={'fontSize': '24px'}),
                html.Span(f"Total Records: {total_records:,}", style={'fontSize': '18px', 'fontWeight': 'bold', 'color': '#F18F01'})
            ], style={'margin': '15px 0', 'padding': '10px', 'backgroundColor': 'white', 'borderRadius': '8px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'}),
            html.Div([
                html.Span("⬇️ ", style={'fontSize': '24px'}),
                html.Span(f"Sales Before Price Increase (Jan 15, 2021): ${before_increase:,.2f}", style={'fontSize': '18px', 'fontWeight': 'bold', 'color': '#28a745'})
            ], style={'margin': '15px 0', 'padding': '10px', 'backgroundColor': 'white', 'borderRadius': '8px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'}),
            html.Div([
                html.Span("⬆️ ", style={'fontSize': '24px'}),
                html.Span(f"Sales After Price Increase (Jan 15, 2021): ${after_increase:,.2f}", style={'fontSize': '18px', 'fontWeight': 'bold', 'color': '#dc3545'})
            ], style={'margin': '15px 0', 'padding': '10px', 'backgroundColor': 'white', 'borderRadius': '8px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'})
        ])
        
        # Determine business insight with enhanced styling
        if after_increase > before_increase:
            insight = html.Div([
                html.Div([
                    html.Span("📈 ", style={'fontSize': '32px'}),
                    html.Span("Sales were HIGHER after the price increase!", style={'fontSize': '20px', 'fontWeight': 'bold', 'color': '#28a745'})
                ], style={'margin': '10px 0'}),
                html.Div([
                    html.Span(f"Sales increased by ${after_increase - before_increase:,.2f} after January 15, 2021", 
                             style={'fontSize': '18px', 'color': '#28a745'})
                ])
            ], style={'padding': '20px', 'backgroundColor': '#d4edda', 'borderRadius': '10px', 'border': '2px solid #c3e6cb'})
        else:
            insight = html.Div([
                html.Div([
                    html.Span("📉 ", style={'fontSize': '32px'}),
                    html.Span("Sales were LOWER after the price increase.", style={'fontSize': '20px', 'fontWeight': 'bold', 'color': '#dc3545'})
                ], style={'margin': '10px 0'}),
                html.Div([
                    html.Span(f"Sales decreased by ${before_increase - after_increase:,.2f} after January 15, 2021", 
                             style={'fontSize': '18px', 'color': '#dc3545'})
                ])
            ], style={'padding': '20px', 'backgroundColor': '#f8d7da', 'borderRadius': '10px', 'border': '2px solid #f5c6cb'})
    else:
        summary_stats = html.Div([
            html.Div([
                html.Span("💰 ", style={'fontSize': '24px'}),
                html.Span(f"Total Sales: ${total_sales:,.2f}", style={'fontSize': '18px', 'fontWeight': 'bold', 'color': '#2E86AB'})
            ], style={'margin': '15px 0', 'padding': '10px', 'backgroundColor': 'white', 'borderRadius': '8px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'}),
            html.Div([
                html.Span("📊 ", style={'fontSize': '24px'}),
                html.Span(f"Average Daily Sales: ${avg_sales:.2f}", style={'fontSize': '18px', 'fontWeight': 'bold', 'color': '#A23B72'})
            ], style={'margin': '15px 0', 'padding': '10px', 'backgroundColor': 'white', 'borderRadius': '8px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'}),
            html.Div([
                html.Span("📝 ", style={'fontSize': '24px'}),
                html.Span(f"Total Records: {total_records:,}", style={'fontSize': '18px', 'fontWeight': 'bold', 'color': '#F18F01'})
            ], style={'margin': '15px 0', 'padding': '10px', 'backgroundColor': 'white', 'borderRadius': '8px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'}),
            html.Div([
                html.Span("⚠️ ", style={'fontSize': '24px'}),
                html.Span("Note: Price increase date (Jan 15, 2021) not in selected date range", style={'fontSize': '16px', 'fontWeight': 'bold', 'color': '#6c757d'})
            ], style={'margin': '15px 0', 'padding': '10px', 'backgroundColor': 'white', 'borderRadius': '8px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'})
        ])
        insight = html.Div([
            html.Div([
                html.Span("ℹ️ ", style={'fontSize': '32px'}),
                html.Span("Select a date range that includes January 15, 2021 to see the impact of the price increase.", 
                         style={'fontSize': '18px', 'fontWeight': 'bold', 'color': '#17a2b8'})
            ], style={'margin': '10px 0'})
        ], style={'padding': '20px', 'backgroundColor': '#d1ecf1', 'borderRadius': '10px', 'border': '2px solid #bee5eb'})
    
    return fig, summary_stats, insight

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8050) 