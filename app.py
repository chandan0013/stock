import os
from   flask import Flask, render_template, request, redirect, Response
from   bokeh.embed import components

import pandas as pd
from   bokeh.plotting import figure, output_file, show
import quandl
quandl.ApiConfig.api_key = "miwt4s4UiJH7JgU1PA1p"


app = Flask(__name__)

def read_data(stock='AAPL', year='2017', month='01'):

    stock = stock.upper()
    
        
    mydata = pd.DataFrame()
    try:
      mydata = quandl.get('WIKI/'+stock, start_date=year+'-'+month+'-01', end_date=year+'-12-31')
    except:
      return f"COULDN'T FIND STOCK {stock}!"
    
    close_prices = pd.Series()
    try:
      if month=='12':
        close_prices = mydata['Close'].loc[(mydata.index >= year+'-'+month)]
      else:
        close_prices = mydata['Close'].loc[(mydata.index >= year+'-'+month) &
                                           (mydata.index <  year+'-'+str(int(month)+1))]
    except:
      return "COULDN'T FIND DATA IN THAT TIME PERIOD"
  
    fig1 = figure(title=stock + ' during requested period ', x_axis_label= year + '/' + month, y_axis_label='Reported Stock Price')
    
    fig1.line(pd.DatetimeIndex(close_prices.index.values).day,close_prices.values)
    ##error will also returned to main app.py
    return fig1

@app.route('/', methods=['GET'])
def index():
  return render_template('index.html')

@app.route('/make_plot', methods=['POST'])
def plot():
  plot = read_data(stock=request.form['stock'],
                                   year=request.form['year'],
                                   month=request.form['month'])
  if isinstance(plot, str):
    return plot
  else:
    script, div = components(plot)
    return render_template('stock_plot.html', script=script, div=div)

@app.route('/about')
def about():
  return render_template('about.html')


if __name__ == '__main__':
  port = int(os.environ.get("PORT", 33507))
  app.run(host='0.0.0.0', port=port)
