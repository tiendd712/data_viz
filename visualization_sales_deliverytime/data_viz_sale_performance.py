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
order_items = pd.read_csv(os.path.join(root, 'data/order_items.csv'))

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


## join table

join_df = (customers[['account_code', 'territory', 'account_type', 'account_name', 'account_manager']]
           .merge(orders[['order_id', 'customer_id', 'cart_price_incp', 'order_date', 'delivery_date', 'order_year']], how='left', left_on = 'account_code', right_on='customer_id')
           .merge(regions[['territory', 'area']], how='left', left_on = 'territory', right_on='territory')
           .merge(order_items, how = 'left', left_on = 'order_id', right_on = 'order_id')
           .merge(products[['product_code', 'product_name', 'business_unit', 'type', 'brand_name']], how = 'left', left_on = 'product_id', right_on = 'product_code'))


join_df['product_name_id'] = join_df['product_name'] + '_' + join_df['product_id'].astype(str)

join_df['order_month'] = pd.to_datetime(join_df['order_date'].dt.strftime('%m-%Y'))

## Deploy the graph

app.layout = html.Div([
    html.Div([

        html.Div([
            dcc.Dropdown(
                options = join_df['account_type'].unique(),
                value = join_df['account_type'].unique(),
                id='filter-acccount-type',
                multi=True
            ),
            dcc.Dropdown(
                options=join_df['area'].unique(),
                value=join_df['area'].unique(),
                id='filter-area',
                multi=True
            )
        ],
        style={'width': '49%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                options = join_df['brand_name'].unique(),
                value=join_df['brand_name'].unique(),
                id='filter-brand-name',
                multi=True
            ),
            dcc.Dropdown(
                options =join_df['business_unit'].unique(),
                value=join_df['business_unit'].unique(),
                id='filter-business-unit',
                multi=True
            )
        ], style={'width': '49%', 'float': 'right', 'display': 'inline-block'})
    ], style={
        'padding': '10px 5px'
    }),

    html.Div([
        dcc.Graph(
            id='crossfilter-indicator-scatter',
            hoverData={'points': [{'customdata': 'product_id'}]}
        )
    ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}),
    html.Div([
        dcc.Graph(id='x-time-series'),
        dcc.Graph(id='y-time-series'),
    ], style={'display': 'inline-block', 'width': '49%'}),

    
])


@callback(
    Output('crossfilter-indicator-scatter', 'figure'),
    Input('filter-acccount-type', 'value'),
    Input('filter-area', 'value'),
    Input('filter-brand-name', 'value'),
    Input('filter-business-unit', 'value'),
    )
def update_graph(account_type_value, area_value,
                 brand_name_value, business_unit_value):
    
    if type(account_type_value) == str:
        account_type_value = [account_type_value]

    if type(area_value) == str:
        area_value = [area_value]

    if type(brand_name_value) == str:
        brand_name_value = [brand_name_value]

    if type(business_unit_value) == str:
        business_unit_value = [business_unit_value]

    
    dff = join_df[
                  (join_df['account_type'].isin(account_type_value)) &
                  (join_df['area'].isin(area_value)) & 
                  (join_df['brand_name'].isin(brand_name_value)) &
                  (join_df['business_unit'].isin(business_unit_value))]
    
    group_df = (dff
                .groupby(['order_year', 'type', 'product_name_id', 'product_name', 'brand_name', 'business_unit'])
                .agg({'quantities': 'sum', 'product_price_incp':'sum'})
                .reset_index())
    
    group_df['avg_price'] = round(group_df['product_price_incp']/group_df['quantities'],3)
    
    group_df.columns = ['order_year', 'type', 'product_name_id', 'product_name','brand_name', 'business_unit',
                        'num_orders', 'revenues', 'avg_price']

    fig = px.scatter(
            group_df,
            x='num_orders',
            y='revenues',
            hover_name='product_name_id',
            size="avg_price",
            ##color = 'type',
            animation_frame="order_year",
            animation_group="product_name_id",
            size_max = 30
            )


    fig.update_traces(customdata=group_df['product_name_id'])

    fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 20}, hovermode='closest')

    fig.update_xaxes(title_text = 'Total orders')

    fig.update_yaxes(title_text = 'Total revenues')


    return fig


def create_time_series(df, yaxis, ytitle, title=None):

    fig = px.scatter(df, x='order_month', y=yaxis)

    fig.update_traces(mode='lines+markers')

    fig.update_xaxes(showgrid=False, title_text = 'Month')

    fig.update_yaxes(title_text = ytitle)

    fig.add_annotation(x=0, y=0.85, xanchor='left', yanchor='bottom',
                       xref='paper', yref='paper', showarrow=False, align='left',
                       text=title)

    fig.update_layout(height=225, margin={'l': 20, 'b': 30, 'r': 10, 't': 10})

    return fig


@callback(
    Output('x-time-series', 'figure'),
    Input('crossfilter-indicator-scatter', 'hoverData')
)
def update_x_timeseries(hoverData):
    product_name_id = hoverData['points'][0]['customdata']
    dff = join_df[join_df['product_name_id'] == product_name_id]
    group_df = (dff
                .groupby(['order_month', 'product_name_id', 'product_name'])
                .agg({'quantities': 'sum'})
                .reset_index())
    
    title = '<b>{}</b><br>{}'.format(product_name_id, '')
    return create_time_series(group_df, 'quantities' ,'Monthly total orders',title)


@callback(
    Output('y-time-series', 'figure'),
    Input('crossfilter-indicator-scatter', 'hoverData')
)
def update_y_timeseries(hoverData):
    product_name_id = hoverData['points'][0]['customdata']
    dff = join_df[join_df['product_name_id'] == product_name_id]
    group_df = (dff
                .groupby(['order_month', 'product_name_id', 'product_name'])
                .agg({'product_price_incp': 'sum'})
                .reset_index())
    title = '<b>{}</b><br>{}'.format(product_name_id, '')
    return create_time_series(group_df, 'product_price_incp', 'Monthly total revenues',title)


if __name__ == '__main__':
    app.run(debug=True)
