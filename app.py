import os
from   flask import Flask, render_template, request, redirect, Response
from   bokeh.embed import components

import plot_stock_module

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
  return render_template('index.html')

@app.route('/make_plot', methods=['POST'])
def make_plot():
  plot = plot_stock_module.plot_stock(stock=request.form['stock'],
                                   year=request.form['year'],
                                   month=request.form['month'])
  if isinstance(plot, str):
    return plot
  else:
    script, div = components(plot)
    return render_template('Stock_plot.html', script=script, div=div)

@app.route('/about')
def about():
  return render_template('about.html')


if __name__ == '__main__':
  port = int(os.environ.get("PORT", 33507))
  app.run(host='0.0.0.0', port=port)
