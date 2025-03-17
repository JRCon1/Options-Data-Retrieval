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

# Define colors
COLORS = {
    'primary': '#1a3d5c',
    'secondary': '#2c5282',
    'accent': '#3182ce',
    'background': '#f7fafc',
    'text': '#2d3748',
    'white': '#ffffff'
}

# Initialize the Dash app with external stylesheets
app = dash.Dash(__name__, 
    external_stylesheets=[
        'https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;600&display=swap',
        'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css'
    ],
    suppress_callback_exceptions=True
)

# Create the navigation bar layout
nav_bar = html.Div([
    dcc.Link('Stock Prices', href='/stock-prices', className='nav-link',
        style={
            'color': COLORS['white'],
            'padding': '1rem', 
            'textDecoration': 'none',
            'fontWeight': '600'
        }
    ),
    dcc.Link('Options Chain', href='/options-chain', className='nav-link',
        style={
            'color': COLORS['white'],
            'padding': '1rem',
            'textDecoration': 'none',
            'fontWeight': '600'
        }
    ),
    dcc.Link('Futures', href='/futures', className='nav-link',
        style={
            'color': COLORS['white'],
            'padding': '1rem',
            'textDecoration': 'none',
            'fontWeight': '600'
        }
    )
], style={
    'backgroundColor': COLORS['secondary'],
    'padding': '0.5rem',
    'display': 'flex',
    'justifyContent': 'center',
    'gap': '2rem'
})

# Create the stock prices page layout
stock_prices_layout = html.Div([
    nav_bar,
    # Hero section with background image
    html.Div([
        html.Div([
            html.H1('Stock Price Analytics',
                style={
                    'color': COLORS['white'],
                    'fontSize': '2.5rem', 
                    'fontWeight': '600',
                    'marginBottom': '1rem'
                }
            ),
            html.P('Download and analyze historical stock price data.',
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
    
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    dcc.Input(
                        id='stock-ticker',
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
                    
                    dcc.Dropdown(
                        id='timeframe',
                        options=[
                            {'label': '1 Month', 'value': 30},
                            {'label': '3 Months', 'value': 90},
                            {'label': '6 Months', 'value': 180},
                            {'label': '1 Year', 'value': 365},
                            {'label': '2 Years', 'value': 730},
                            {'label': '5 Years', 'value': 1825}
                        ],
                        value=365,
                        style={
                            'marginBottom': '1.5rem'
                        }
                    ),
                    
                    html.Button(
                        [
                            html.I(className="fas fa-download", style={'marginRight': '0.5rem'}),
                            'Download Stock Data'
                        ],
                        id='download-stock-button',
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
                    
                    dcc.Download(id='download-stock-data'),
                    
                    html.Div(
                        id='stock-output-message',
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

# Create the options chain page layout
options_chain_layout = html.Div([
    nav_bar,
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

# Create the futures page layout
futures_layout = html.Div([
    nav_bar,
    html.Div([
        html.Div([
            html.H1('Futures Market Analytics',
                style={
                    'color': COLORS['white'],
                    'fontSize': '2.5rem', 
                    'fontWeight': '600',
                    'marginBottom': '1rem'
                }
            ),
            html.P('Download and analyze futures market data.',
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
    
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    html.Label('Futures Symbol', style={'fontWeight': '600', 'color': COLORS['text'], 'marginBottom': '0.5rem'}),
                    dcc.Input(
                        id='futures-symbol',
                        type='text',
                        placeholder='Enter futures symbol (e.g., ES=F for E-mini S&P 500)',
                        style={
                            'width': '100%',
                            'padding': '0.75rem',
                            'borderRadius': '0.375rem',
                            'border': f'1px solid {COLORS["accent"]}',
                            'marginBottom': '1.5rem'
                        }
                    ),
                    
                    html.Label('Time Period', style={'fontWeight': '600', 'color': COLORS['text'], 'marginBottom': '0.5rem'}),
                    dcc.Dropdown(
                        id='futures-timeframe',
                        options=[
                            {'label': '1 Month', 'value': 30},
                            {'label': '3 Months', 'value': 90},
                            {'label': '6 Months', 'value': 180},
                            {'label': '1 Year', 'value': 365},
                            {'label': '2 Years', 'value': 730},
                            {'label': '5 Years', 'value': 1825}
                        ],
                        value=365,
                        style={
                            'marginBottom': '1.5rem'
                        }
                    ),
                    
                    html.Button(
                        [
                            html.I(className="fas fa-download", style={'marginRight': '0.5rem'}),
                            'Download Futures Data'
                        ],
                        id='download-futures-button',
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
                    
                    dcc.Download(id='download-futures-data'),
                    
                    html.Div(
                        id='futures-output-message',
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
    }),

    # Reference Section
    html.Div([
        html.Div([
            html.H2('Futures Symbol Reference',
                style={
                    'color': COLORS['text'],
                    'fontSize': '1.5rem',
                    'fontWeight': '600',
                    'marginBottom': '1.5rem',
                    'textAlign': 'center'
                }
            ),
            
            # Energy Futures
            html.Div([
                html.Button(
                    'Energy Futures',
                    id='energy-futures-button',
                    style={
                        'width': '100%',
                        'padding': '1rem',
                        'backgroundColor': COLORS['accent'],
                        'color': COLORS['white'],
                        'border': 'none',
                        'borderRadius': '0.375rem',
                        'textAlign': 'left',
                        'fontWeight': '600',
                        'marginBottom': '0.5rem'
                    }
                ),
                html.Div([
                    html.P('Crude Oil (WTI): CL=F', style={'margin': '0.5rem 0'}),
                    html.P('Brent Crude Oil: BZ=F', style={'margin': '0.5rem 0'}),
                    html.P('Natural Gas: NG=F', style={'margin': '0.5rem 0'}),
                    html.P('Heating Oil: HO=F', style={'margin': '0.5rem 0'}),
                    html.P('Gasoline (RBOB): RB=F', style={'margin': '0.5rem 0'})
                ], id='energy-futures-content', style={'display': 'none', 'padding': '1rem', 'backgroundColor': '#f8fafc'})
            ], style={'marginBottom': '1rem'}),

            # Metal Futures
            html.Div([
                html.Button(
                    'Metal Futures',
                    id='metal-futures-button',
                    style={
                        'width': '100%',
                        'padding': '1rem',
                        'backgroundColor': COLORS['accent'],
                        'color': COLORS['white'],
                        'border': 'none',
                        'borderRadius': '0.375rem',
                        'textAlign': 'left',
                        'fontWeight': '600',
                        'marginBottom': '0.5rem'
                    }
                ),
                html.Div([
                    html.P('Gold: GC=F', style={'margin': '0.5rem 0'}),
                    html.P('Silver: SI=F', style={'margin': '0.5rem 0'}),
                    html.P('Copper: HG=F', style={'margin': '0.5rem 0'}),
                    html.P('Platinum: PL=F', style={'margin': '0.5rem 0'}),
                    html.P('Palladium: PA=F', style={'margin': '0.5rem 0'})
                ], id='metal-futures-content', style={'display': 'none', 'padding': '1rem', 'backgroundColor': '#f8fafc'})
            ], style={'marginBottom': '1rem'}),

            # Agricultural Futures
            html.Div([
                html.Button(
                    'Agricultural Futures',
                    id='ag-futures-button',
                    style={
                        'width': '100%',
                        'padding': '1rem',
                        'backgroundColor': COLORS['accent'],
                        'color': COLORS['white'],
                        'border': 'none',
                        'borderRadius': '0.375rem',
                        'textAlign': 'left',
                        'fontWeight': '600',
                        'marginBottom': '0.5rem'
                    }
                ),
                html.Div([
                    html.P('Corn: ZC=F', style={'margin': '0.5rem 0'}),
                    html.P('Wheat: ZW=F', style={'margin': '0.5rem 0'}),
                    html.P('Soybeans: ZS=F', style={'margin': '0.5rem 0'}),
                    html.P('Soybean Oil: ZL=F', style={'margin': '0.5rem 0'}),
                    html.P('Cotton: CT=F', style={'margin': '0.5rem 0'}),
                    html.P('Sugar #11: SB=F', style={'margin': '0.5rem 0'}),
                    html.P('Coffee: KC=F', style={'margin': '0.5rem 0'}),
                    html.P('Cocoa: CC=F', style={'margin': '0.5rem 0'}),
                    html.P('Live Cattle: LE=F', style={'margin': '0.5rem 0'}),
                    html.P('Lean Hogs: HE=F', style={'margin': '0.5rem 0'})
                ], id='ag-futures-content', style={'display': 'none', 'padding': '1rem', 'backgroundColor': '#f8fafc'})
            ], style={'marginBottom': '1rem'}),

            # Index Futures
            html.Div([
                html.Button(
                    'Index Futures',
                    id='index-futures-button',
                    style={
                        'width': '100%',
                        'padding': '1rem',
                        'backgroundColor': COLORS['accent'],
                        'color': COLORS['white'],
                        'border': 'none',
                        'borderRadius': '0.375rem',
                        'textAlign': 'left',
                        'fontWeight': '600',
                        'marginBottom': '0.5rem'
                    }
                ),
                html.Div([
                    html.P('S&P 500 E-mini: ES=F', style={'margin': '0.5rem 0'}),
                    html.P('Nasdaq 100 E-mini: NQ=F', style={'margin': '0.5rem 0'}),
                    html.P('Dow Jones E-mini: YM=F', style={'margin': '0.5rem 0'}),
                    html.P('Russell 2000 E-mini: RTY=F', style={'margin': '0.5rem 0'})
                ], id='index-futures-content', style={'display': 'none', 'padding': '1rem', 'backgroundColor': '#f8fafc'})
            ], style={'marginBottom': '1rem'}),

            # Currency Futures
            html.Div([
                html.Button(
                    'Currency Futures',
                    id='currency-futures-button',
                    style={
                        'width': '100%',
                        'padding': '1rem',
                        'backgroundColor': COLORS['accent'],
                        'color': COLORS['white'],
                        'border': 'none',
                        'borderRadius': '0.375rem',
                        'textAlign': 'left',
                        'fontWeight': '600',
                        'marginBottom': '0.5rem'
                    }
                ),
                html.Div([
                    html.P('Euro FX: 6E=F', style={'margin': '0.5rem 0'}),
                    html.P('Japanese Yen: 6J=F', style={'margin': '0.5rem 0'}),
                    html.P('British Pound: 6B=F', style={'margin': '0.5rem 0'}),
                    html.P('Australian Dollar: 6A=F', style={'margin': '0.5rem 0'}),
                    html.P('Canadian Dollar: 6C=F', style={'margin': '0.5rem 0'}),
                    html.P('Swiss Franc: 6S=F', style={'margin': '0.5rem 0'})
                ], id='currency-futures-content', style={'display': 'none', 'padding': '1rem', 'backgroundColor': '#f8fafc'})
            ], style={'marginBottom': '1rem'}),

            # Interest Rate Futures
            html.Div([
                html.Button(
                    'Interest Rate Futures',
                    id='interest-futures-button',
                    style={
                        'width': '100%',
                        'padding': '1rem',
                        'backgroundColor': COLORS['accent'],
                        'color': COLORS['white'],
                        'border': 'none',
                        'borderRadius': '0.375rem',
                        'textAlign': 'left',
                        'fontWeight': '600',
                        'marginBottom': '0.5rem'
                    }
                ),
                html.Div([
                    html.P('10-Year T-Note: ZN=F', style={'margin': '0.5rem 0'}),
                    html.P('5-Year T-Note: ZF=F', style={'margin': '0.5rem 0'}),
                    html.P('2-Year T-Note: ZT=F', style={'margin': '0.5rem 0'}),
                    html.P('30-Year T-Bond: ZB=F', style={'margin': '0.5rem 0'}),
                    html.P('Eurodollar: GE=F', style={'margin': '0.5rem 0'})
                ], id='interest-futures-content', style={'display': 'none', 'padding': '1rem', 'backgroundColor': '#f8fafc'})
            ], style={'marginBottom': '1rem'})
        ], style={
            'padding': '2rem',
            'backgroundColor': COLORS['white'],
            'borderRadius': '0.5rem',
            'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1)',
            'maxWidth': '800px',
            'margin': '2rem auto'
        })
    ], style={
        'padding': '0 2rem',
        'maxWidth': '1200px',
        'margin': 'auto'
    })
], style={'backgroundColor': COLORS['background'], 'minHeight': '100vh'})

# Define the main app layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

# Create the URL routing callback
@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)
def display_page(pathname):
    if pathname == '/stock-prices' or pathname == '/':
        return stock_prices_layout
    elif pathname == '/options-chain':
        return options_chain_layout
    elif pathname == '/futures':
        return futures_layout
    else:
        return stock_prices_layout  # Default to stock prices page

# Create the stock data download callback
@app.callback(
    Output('download-stock-data', 'data'),
    Output('stock-output-message', 'children'),
    Output('stock-output-message', 'style'),
    Input('download-stock-button', 'n_clicks'),
    State('stock-ticker', 'value'),
    State('timeframe', 'value')
)
def download_stock_data(n_clicks, ticker, timeframe):
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
        start_date = end_date - dt.timedelta(days=timeframe)
        
        # Get historical data
        df = stock.history(start=start_date, end=end_date)
        
        if df.empty:
            return None, "No stock data found for this ticker", {
                'marginTop': '1rem',
                'padding': '1rem',
                'borderRadius': '0.375rem',
                'backgroundColor': '#fed7d7',
                'color': '#c53030',
                'display': 'block'
            }
        
        # Prepare for download
        return (
            dcc.send_data_frame(df.to_csv, f"{ticker}_stock_prices.csv"),
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

# Create the futures data download callback
@app.callback(
    Output('download-futures-data', 'data'),
    Output('futures-output-message', 'children'),
    Output('futures-output-message', 'style'),
    Input('download-futures-button', 'n_clicks'),
    State('futures-symbol', 'value'),
    State('futures-timeframe', 'value')
)
def download_futures_data(n_clicks, symbol, timeframe):
    if n_clicks is None:
        raise dash.exceptions.PreventUpdate
    
    if not symbol:
        return None, "Please enter a futures symbol", {
            'marginTop': '1rem',
            'padding': '1rem',
            'borderRadius': '0.375rem',
            'backgroundColor': '#fed7d7',
            'color': '#c53030',
            'display': 'block'
        }
    
    try:
        # Get futures data
        futures = yf.Ticker(symbol)
        
        # Calculate date range
        end_date = dt.datetime.now()
        start_date = end_date - dt.timedelta(days=timeframe)
        
        # Get historical data
        df = futures.history(start=start_date, end=end_date)
        
        if df.empty:
            return None, "No futures data found for this symbol", {
                'marginTop': '1rem',
                'padding': '1rem',
                'borderRadius': '0.375rem',
                'backgroundColor': '#fed7d7',
                'color': '#c53030',
                'display': 'block'
            }
        
        # Prepare for download
        return (
            dcc.send_data_frame(df.to_csv, f"{symbol}_futures_data.csv"),
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

# Add callbacks for collapsible sections
@app.callback(
    [Output('energy-futures-content', 'style'),
     Output('metal-futures-content', 'style'),
     Output('ag-futures-content', 'style'),
     Output('index-futures-content', 'style'),
     Output('currency-futures-content', 'style'),
     Output('interest-futures-content', 'style')],
    [Input('energy-futures-button', 'n_clicks'),
     Input('metal-futures-button', 'n_clicks'),
     Input('ag-futures-button', 'n_clicks'),
     Input('index-futures-button', 'n_clicks'),
     Input('currency-futures-button', 'n_clicks'),
     Input('interest-futures-button', 'n_clicks')]
)
def toggle_sections(energy_clicks, metal_clicks, ag_clicks, index_clicks, currency_clicks, interest_clicks):
    ctx = dash.callback_context
    if not ctx.triggered:
        return [{'display': 'none'}] * 6
    
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    styles = [{'display': 'none'}] * 6
    
    if button_id == 'energy-futures-button':
        styles[0] = {'display': 'block', 'padding': '1rem', 'backgroundColor': '#f8fafc'}
    elif button_id == 'metal-futures-button':
        styles[1] = {'display': 'block', 'padding': '1rem', 'backgroundColor': '#f8fafc'}
    elif button_id == 'ag-futures-button':
        styles[2] = {'display': 'block', 'padding': '1rem', 'backgroundColor': '#f8fafc'}
    elif button_id == 'index-futures-button':
        styles[3] = {'display': 'block', 'padding': '1rem', 'backgroundColor': '#f8fafc'}
    elif button_id == 'currency-futures-button':
        styles[4] = {'display': 'block', 'padding': '1rem', 'backgroundColor': '#f8fafc'}
    elif button_id == 'interest-futures-button':
        styles[5] = {'display': 'block', 'padding': '1rem', 'backgroundColor': '#f8fafc'}
    
    return styles

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, port=8050)