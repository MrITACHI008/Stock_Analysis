#import libraries and install libraries
# yahoo finance for data
# dash and ploty

import yfinance as yf
import dash
from dash.dependencies import Input, Output
from dash import dcc, html
import plotly.graph_objects as go


## Load stock price data from Yahoo Finance

def load_data(ticker, interval='1m'):
    try:
        stock_data = yf.download(ticker, interval=interval)
        return stock_data
    except Exception as e:
        print(f"Failed to download data for {ticker}: {e}")
        return None

# Create the initial figure
fig = go.Figure()

# Set up the Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div([
    dcc.Graph(id='candlestick-chart'),
    dcc.Interval(
        id='interval-component',
        interval=60*1000,  # in milliseconds, update every 1 minute
        n_intervals=0
    )
])



# Define the callback to update the chart
@app.callback(Output('candlestick-chart', 'figure'),
              Input('interval-component', 'n_intervals'))

def update_chart(n_intervals):
    # Load real-time data from Yahoo Finance at 1-minute intervals
    stock_data = load_data('^NSEI')

    # Create or update the candlestick chart
    fig = go.Figure(data=[go.Candlestick(x=stock_data.index,
                                         open=stock_data['Open'],
                                         high=stock_data['High'],
                                         low=stock_data['Low'],
                                         close=stock_data['Close']
                                         )])
    fig.update_layout(title='Real-Time Candlestick Chart - NIFTY50',
                      xaxis_title='Date',
                      yaxis_title='Stock Price',
                      xaxis_rangeslider_visible=False)
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
