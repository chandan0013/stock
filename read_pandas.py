import os
import pandas as pd
from   bokeh.plotting import figure, output_file, show
import quandl
quandl.ApiConfig.api_key = "miwt4s4UiJH7JgU1PA1p"




def read_pandas(stock='AAPL', year='2017', month='01'):

    stock = stock.upper()
    
        
    # Request the data
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


## Execute only if run as a script
if __name__ == "__main__":
    main()
