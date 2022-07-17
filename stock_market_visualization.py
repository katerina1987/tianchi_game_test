'''
Author: katerina
Date: 2022-07-07 19:47:37
LastEditTime: 2022-07-08 18:42:28
LastEditors: katerina
Description: 数据可视化
FilePath: /tianchi_game/test123.py
katerina编写
'''
from doctest import OutputChecker
from colorama import Style
import pandas as pd
import matplotlib as mpl
from matplotlib import pyplot as plt
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from dash.dependencies import Input, Output

#导入数据
df_sh_index = pd.read_csv("/Users/mac/Desktop/tianchi_game/data/sh_index.csv")
df_sz_index = pd.read_csv("/Users/mac/Desktop/tianchi_game/data/sz_index.csv")
df_sh_margin_trade = pd.read_csv("/Users/mac/Desktop/tianchi_game/data/sh_margin_trade.csv")
df_sz_margin_trade = pd.read_csv("/Users/mac/Desktop/tianchi_game/data/sz_margin_trade.csv")

app = dash.Dash()

date = [str(x) for x in df_sh_index["date"].to_list()]
vol = df_sh_index["vol"].to_list()
date_index_new = pd.to_datetime(date, format="%Y-%m-%d")
df_index = pd.DataFrame({"date":date_index_new, "vol":vol})
fig = px.scatter(df_index, x ="date", y = "vol", title = "沪深股市趋势", labels={"date":"日期", "vol":"成交量"})


date = [str(x) for x in df_sh_margin_trade["date"].to_list()]
balance = df_sh_margin_trade["margin_balance"].to_list()
date_new = pd.to_datetime(date, format="%Y-%m-%d")
df_balance = pd.DataFrame({"date":date_new, "balance":balance})
fig_trend = px.bar(df_balance, x ="date", y = "balance", title = "趋势图", labels={"date":"日期", "balance":"余额"})

app.layout = html.Div([
    html.H1("沪深股市数据可视化"),
    
    html.Div([
       dcc.Dropdown(
            id = "stock_index",
            options = [{"label" : "sh_index", "value" : "sh_index" },
                       {"label" : "sz_index", "value" : "sz_index" }],
            value= "sh_index",
            multi= True
        ),
        dcc.Graph(id = "stock_index_graph", figure = fig), 
    ]),
    
    html.Div([
        dcc.RadioItems(
            id = "margin_balance",
            options = [{"label":"margin_balance","value":"margin_balance"}, 
                       {"label":"financing_balance","value":"financing_balance"},
                       {"label":"securities_lending_balance","value":"securities_lending_balance"}],
            value= "margin_balance"
        ),
    dcc.Graph(id = "margin_balance_graph", figure= fig_trend),
    ])
])


@app.callback(
    Output("stock_index_graph", "figure"),
    Input("stock_index", "value"))

def update_graph(selected_dropdown_value):
    if selected_dropdown_value == "sh_index":
        date = [str(x) for x in df_sh_index["date"].to_list()]
        date_new = pd.to_datetime(date, format="%Y-%m-%d")
        vol = df_sh_index["vol"].to_list()
        df = pd.DataFrame({"date":date_new, "vol":vol})
    elif selected_dropdown_value == "sz_index":
        date = [str(x) for x in df_sz_index["date"].to_list()]
        date_new = pd.to_datetime(date, format="%Y-%m-%d")
        vol = df_sz_index["vol"].to_list()
        df = pd.DataFrame({"date":date_new, "vol":vol})
    fig = px.scatter(df, x = "date", y = "vol" , title = "沪深股市指数", labels={"date":"日期", "vol":"成交量"})
    return fig

@app.callback(
    Output("margin_balance_graph", "figure"),
    Input("margin_balance", "value"))

def update_graph(margin_balance):
    if margin_balance == "margin_balance":
        date = [str(x) for x in df_sh_margin_trade["date"].to_list()]
        date_new = pd.to_datetime(date, format="%Y-%m-%d")
        balance = df_sh_margin_trade["margin_balance"].to_list()
        df_balance = pd.DataFrame({"date":date_new, "balance":balance})
    elif margin_balance == "financing_balance":
        date = [str(x) for x in df_sh_margin_trade["date"].to_list()]
        date_new = pd.to_datetime(date, format="%Y-%m-%d")
        balance = df_sh_margin_trade["financing_balance"].to_list()
        df_balance = pd.DataFrame({"date":date_new, "balance":balance})
    elif margin_balance == "securities_lending_balance":
        date = [str(x) for x in df_sh_margin_trade["date"].to_list()]
        date_new = pd.to_datetime(date, format="%Y-%m-%d")
        balance = df_sh_margin_trade["securities_lending_balance"].to_list()
        df_balance = pd.DataFrame({"date":date_new, "balance":balance}) 
    fig = px.bar(df_balance, x = "date", y = "balance" , title = "趋势图", labels={"date":"日期", "balance":"余额"})
    return fig


app.css.append_css({'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'})

if __name__ == '__main__':
    app.run_server(debug=True)