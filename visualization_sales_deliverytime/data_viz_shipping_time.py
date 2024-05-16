from dash import Dash, html, dcc, Input, Output, callback
import pandas as pd
import numpy as np
import plotly.express as px
import os



external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)

# Data processing

root = os.getcwd()


## import the data

customers = pd.read_csv(os.path.join(root,  'data/customers.csv'))
orders = pd.read_csv(os.path.join(root, 'data/orders.csv'))
products = pd.read_csv(os.path.join(root, 'data/products.csv'))
regions = pd.read_csv(os.path.join(root, 'data/regions.csv'))

## change columns name

customers.columns = ['account_code', 'territory', 'account_type', 
                     'key_account', 'key_account_manager', 'account_name', 'account_manager']


products.columns = ['product_code', 'business_unit', 'type', 'products_business_line_leader',
                    'subtype', 'product_name', 'brand_name', 'brand_manager']

regions.columns = ['territory', 'nation', 'region', 'regional_manager', 'area', 'area_manager']


orders.columns = ['order_id', 'order_date', 'delivery_date', 'customer_id',
                  'territory', 'products', 'product_id', 'quantities', 'cart_price_incp', 
                  'cart_price', 'product_price_incp']


## change data type 

orders['order_date'] = pd.to_datetime(orders['order_date'])
orders['delivery_date'] = pd.to_datetime(orders['delivery_date'])

## create more columns

orders['order_year'] = orders['order_date'].dt.year
orders['delivery_day'] = (orders['delivery_date'] - orders['order_date']).dt.days


## join table

join_df = (customers[['account_code', 'territory', 'account_type', 'account_name', 'account_manager']]
           .merge(orders[['order_id', 'customer_id', 'cart_price_incp', 'order_date', 'delivery_date', 'order_year', 'delivery_day', 'quantities', 'product_price_incp']], how='left', left_on = 'account_code', right_on='customer_id')
           .merge(regions[['territory', 'area', 'region']], how='left', left_on = 'territory', right_on='territory'))


join_df['order_month'] = pd.to_datetime(join_df['order_date'].dt.strftime('%m-%Y'))
join_df['num_items'] = orders['quantities'].str.split(', ').apply(len)



## deploy the graph
app.layout = html.Div([

    html.H4('Animated GDP and population over decades'),

    dcc.Dropdown(
                join_df['area'].unique(),
                'Underdark',
                id='filter-area'
            ),

    html.P("Select a figure:"),

    dcc.RadioItems(
        id='selection',
        options=["sales-growth", "order-growth", 'total-order', 'num-items'],
        value='sales-growth',
    ),
    dcc.Loading(dcc.Graph(id="graph"), type="cube")
])


@callback(
    Output("graph", "figure"), 
    Input("selection", "value"),
    Input("filter-area", "value"))

def display_animated_graph(selection, area):

    join_df_filter = join_df[(join_df.area == area)]

    group_df = (join_df_filter
                .groupby(['order_month'])
                .agg({'order_id': 'nunique', 'cart_price_incp':'sum', 'delivery_day':'mean'})
                .reset_index())
    
    group_df['order_growth'] = group_df['order_id'].pct_change()
    group_df['revenue_growth'] = group_df['cart_price_incp'].pct_change()

    figure_dev = {
        'sales-growth': px.scatter(
            group_df[group_df.delivery_day <=10].dropna(), x='delivery_day', y="revenue_growth",
            hover_name="order_month", size_max=30, 
            trendline='ols',                 
            trendline_color_override='red'),

        'order-growth': px.scatter(
            group_df[group_df.delivery_day <=10].dropna(), x='delivery_day', y="order_growth",
            hover_name="order_month", size_max=30, 
            trendline='ols',                 
            trendline_color_override='red'),

        'total-order': px.scatter(
            group_df[group_df.delivery_day <=10], x='delivery_day', y="order_id",
            hover_name="order_month", size_max=30, 
            trendline='ols', trendline_color_override='red'),

        'num-items': px.scatter(
            join_df_filter, x='delivery_day', y="num_items",
            hover_name="order_id", size_max=30, 
            trendline='ols',                 
            trendline_color_override='red')
    }
    return figure_dev[selection]

if __name__ == '__main__':
    app.run(debug=True)