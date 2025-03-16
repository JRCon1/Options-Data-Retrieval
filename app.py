import numpy as np
import datetime as dt
import yfinance as yf
import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output, State
import pandas as pd
import io
import base64
from dash.dependencies import Input, Output

# Initialize the Dash app with external stylesheets
app = dash.Dash(__name__, 
    external_stylesheets=[
        'https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;600&display=swap',
        'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css'
    ]
)

# Define colors
COLORS = {
    'primary': '#1a3d5c',
    'secondary': '#2c5282',
    'accent': '#3182ce',
    'background': '#f7fafc',
    'text': '#2d3748',
    'white': '#ffffff'
}

# Define the layout
app.layout = html.Div([
    # Hero section with background image
    html.Div([
        html.Div([
            html.H1('Options Chain Analytics', 
                style={
                    'color': COLORS['white'],
                    'fontSize': '2.5rem',
                    'fontWeight': '600',
                    'marginBottom': '1rem'
                }
            ),
            html.P('Download and analyze comprehensive options data for any publicly traded company.',
                style={
                    'color': COLORS['white'],
                    'fontSize': '1.2rem',
                    'marginBottom': '2rem'
                }
            ),
        ], style={
            'maxWidth': '800px',
            'margin': 'auto',
            'padding': '4rem 2rem',
            'textAlign': 'center'
        })
    ], style={
        'backgroundColor': COLORS['primary'],
        'backgroundImage': 'linear-gradient(rgba(26, 61, 92, 0.9), rgba(26, 61, 92, 0.9))',
        'backgroundSize': 'cover',
        'backgroundPosition': 'center',
        'marginBottom': '2rem'
    }),
    
    # Main content
    html.Div([
        # Input Card
        html.Div([
            html.Div([
                html.I(className="fas fa-chart-line", style={'fontSize': '24px', 'color': COLORS['accent'], 'marginBottom': '1rem'}),
                html.H2('Options Data Parameters', 
                    style={
                        'color': COLORS['text'],
                        'fontSize': '1.5rem',
                        'fontWeight': '600',
                        'marginBottom': '2rem'
                    }
                ),
                
                # Input fields
                html.Div([
                    html.Label('Stock Ticker', style={'fontWeight': '600', 'color': COLORS['text'], 'marginBottom': '0.5rem'}),
                    dcc.Input(
                        id='ticker',
                        type='text',
                        placeholder='Enter stock ticker (e.g., AAPL)',
                        style={
                            'width': '100%',
                            'padding': '0.75rem',
                            'borderRadius': '0.375rem',
                            'border': f'1px solid {COLORS["accent"]}',
                            'marginBottom': '1.5rem'
                        }
                    ),
                    
                    html.Label('Option Type', style={'fontWeight': '600', 'color': COLORS['text'], 'marginBottom': '0.5rem'}),
                    dcc.Dropdown(
                        id='option-type',
                        options=[
                            {'label': 'Calls', 'value': 'CALL'},
                            {'label': 'Puts', 'value': 'PUT'},
                            {'label': 'Both', 'value': 'BOTH'}
                        ],
                        value='BOTH',
                        style={
                            'marginBottom': '1.5rem',
                            'borderRadius': '0.375rem'
                        }
                    ),
                    
                    html.Label('Lookback Days', style={'fontWeight': '600', 'color': COLORS['text'], 'marginBottom': '0.5rem'}),
                    dcc.Input(
                        id='lookback-days',
                        type='number',
                        value=60,
                        min=1,
                        style={
                            'width': '100%',
                            'padding': '0.75rem',
                            'borderRadius': '0.375rem',
                            'border': f'1px solid {COLORS["accent"]}',
                            'marginBottom': '1.5rem'
                        }
                    ),
                    
                    html.Button(
                        [
                            html.I(className="fas fa-download", style={'marginRight': '0.5rem'}),
                            'Download Options Data'
                        ],
                        id='download-button',
                        style={
                            'backgroundColor': COLORS['accent'],
                            'color': COLORS['white'],
                            'padding': '0.75rem 1.5rem',
                            'border': 'none',
                            'borderRadius': '0.375rem',
                            'cursor': 'pointer',
                            'width': '100%',
                            'fontSize': '1rem',
                            'fontWeight': '600',
                            'display': 'flex',
                            'alignItems': 'center',
                            'justifyContent': 'center',
                            'transition': 'background-color 0.2s'
                        }
                    ),
                    
                    dcc.Download(id='download-options-data'),
                    
                    html.Div(
                        id='output-message',
                        style={
                            'marginTop': '1rem',
                            'padding': '1rem',
                            'borderRadius': '0.375rem',
                            'backgroundColor': '#fed7d7',
                            'color': '#c53030',
                            'display': 'none'
                        }
                    )
                ])
            ], style={
                'padding': '2rem',
                'backgroundColor': COLORS['white'],
                'borderRadius': '0.5rem',
                'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1)',
                'maxWidth': '600px',
                'margin': 'auto'
            })
        ])
    ], style={
        'padding': '0 2rem',
        'maxWidth': '1200px',
        'margin': 'auto'
    })
], style={'backgroundColor': COLORS['background'], 'minHeight': '100vh'})

@app.callback(
    Output('download-options-data', 'data'),
    Output('output-message', 'children'),
    Output('output-message', 'style'),
    [Input('download-button', 'n_clicks')],
    [State('ticker', 'value'),
     State('option-type', 'value'),
     State('lookback-days', 'value')]
)
def download_options_data(n_clicks, ticker, option_type, lookback_days):
    if n_clicks is None:
        raise dash.exceptions.PreventUpdate
    
    if not ticker:
        return None, "Please enter a ticker symbol", {
            'marginTop': '1rem',
            'padding': '1rem',
            'borderRadius': '0.375rem',
            'backgroundColor': '#fed7d7',
            'color': '#c53030',
            'display': 'block'
        }
    
    try:
        # Get stock data
        stock = yf.Ticker(ticker)
        
        # Calculate date range
        end_date = dt.datetime.now()
        start_date = end_date - dt.timedelta(days=lookback_days)
        
        # Get options chain
        options_data = []
        
        # Get all available expiration dates
        expirations = stock.options
        
        for exp_date in expirations:
            opt_chain = stock.option_chain(exp_date)
            
            if option_type in ['CALL', 'BOTH']:
                calls = opt_chain.calls
                calls['Option_Type'] = 'CALL'
                options_data.append(calls)
                
            if option_type in ['PUT', 'BOTH']:
                puts = opt_chain.puts
                puts['Option_Type'] = 'PUT'
                options_data.append(puts)
        
        if not options_data:
            return None, "No options data found for this ticker", {
                'marginTop': '1rem',
                'padding': '1rem',
                'borderRadius': '0.375rem',
                'backgroundColor': '#fed7d7',
                'color': '#c53030',
                'display': 'block'
            }
            
        # Combine all data
        df = pd.concat(options_data, axis=0)
        
        # Prepare for download
        return (
            dcc.send_data_frame(df.to_csv, f"{ticker}_options_chain.csv"),
            "Download successful!",
            {
                'marginTop': '1rem',
                'padding': '1rem',
                'borderRadius': '0.375rem',
                'backgroundColor': '#c6f6d5',
                'color': '#2f855a',
                'display': 'block'
            }
        )
        
    except Exception as e:
        return None, f"Error: {str(e)}", {
            'marginTop': '1rem',
            'padding': '1rem',
            'borderRadius': '0.375rem',
            'backgroundColor': '#fed7d7',
            'color': '#c53030',
            'display': 'block'
        }

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, port=8050) 