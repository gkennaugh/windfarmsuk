from dash import Input, Output, Dash, dcc, html, State, dash_table
import pandas as pd
#import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import plotly.express as px
#import json
#import requests
#from bs4 import BeautifulSoup
#import lxml.html as html2
#import time
from dash_bootstrap_templates import load_figure_template, template_from_url
#import geopandas as gpd
import datetime
import dash_daq as daq
#from random import randrange
import numpy as np

load_figure_template('darkly')
#dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
external_stylesheets = [dbc.themes.DARKLY]

mapbox_access_token = 'pk.eyJ1IjoiYWxpc2hvYmVpcmkiLCJhIjoiY2ozYnM3YTUxMDAxeDMzcGNjbmZyMmplZiJ9.ZjmQ0C2MNs1AzEBC_Syadg'
px.set_mapbox_access_token(mapbox_access_token)

shape25m2 = pd.read_csv('shape25m2.csv')
gov_wind = pd.read_csv('gov_wind.csv')
live_offshore = pd.read_csv('live_offshore_dash.csv')
live_offshore_new = pd.read_csv('live_offshore_new2.csv')
substations = pd.read_csv('substations.csv')
reftotal = pd.read_csv('reftotal.csv')
reftotal['Accreditation'] = pd.to_datetime(reftotal['Accreditation'])
sub33g = pd.read_csv('sub33gm.csv')
ukpower = pd.read_csv('grid-and-primary-sites.csv')
ukpower['lat'] = ukpower['Spatial Coordinates'].str.split(',', expand=True)[0].astype('float')
ukpower['lon'] = ukpower['Spatial Coordinates'].str.split(',', expand=True)[1].astype('float')
ssen = pd.read_csv('ssen.csv')
roc = pd.read_csv('roc2010-22(2).csv')
roc['Date'] = pd.to_datetime(roc['Date'])
matches3 = pd.read_csv('matches3.csv')
megamerge = pd.read_csv('megamerge.csv')
megamerge['Site Name'] = megamerge['Site Name'].str[:20]

megcol = ['Site Name', 'Country', 'IC (kW)',
       'RLF', 'ALF', 'Latest MWh pa', 'Latest ROCs pa', 'years',
       'Operational', 'Turbine (MW)', 'No.', 'Height (m)']
megamerge_temp = megamerge[:10][megcol]

color_discrete_map2 = {'Under 5.5': '#fce9da','5.5 - 6': '#9ed560','6 - 6.5': '#95b3d7','6.5 - 7': '#538ed4','7 - 7.5': '#ffb600','7.5 - 8': '#f79647','8 - 9': '#fe0000','9 - 10': '#c00000','Over 10': '#974806'}

PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"

app = Dash(__name__, external_stylesheets=external_stylesheets)

content = dbc.Col(id="page-content-mobile", xs=12, sm=12, md=12, lg=9)

sidebar = dbc.Navbar(
        dbc.Container(
            [
                html.A(
                    # Use row and col to control vertical alignment of logo / brand
                    dbc.Col(
                        [
                            dbc.Button("Menu", id="open-offcanvas", n_clicks=0),
                            dbc.NavItem(dbc.NavLink("Page 1", href="/")),
                            dbc.DropdownMenu(
                                children=[
                                    dbc.DropdownMenuItem("More pages", header=True),
                                    dbc.DropdownMenuItem("Page 2", href="page2"),
                                    dbc.DropdownMenuItem("Page 3", href="page3"),
                                    dbc.DropdownMenuItem("Page 4", href="page4"),
                                ],
                                nav=True,
                                in_navbar=True,
                                label="More",
                            ),

                        ],
                        style={'display':'flex'},
                        align="center",
                        className="g-0",
                    ),
                    style={"textDecoration": "none"},
                ),
                dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
                dbc.Collapse(
                    #search_bar,
                    id="navbar-collapse",
                    is_open=False,
                    navbar=True,
                ),
            ]
        ),
        color="dark",
        dark=True,
        className='bg-primary'
    )

offcanvas = html.Div(
    [
        #dbc.Button("Open Offcanvas", id="open-offcanvas", n_clicks=0),
        dbc.Offcanvas([
            dbc.NavItem(dbc.NavLink("Maps", href='/')),
            dbc.NavItem(dbc.NavLink("Exploration", href='page2')),
            dbc.NavItem(dbc.NavLink("Generation", href='page3')),
            dbc.NavItem(dbc.NavLink("Characteristics", href='page4')),
            html.P(
                "Wind Farms in the United Kingdom "
                "Currently only showing onshore wind farms."
            )],
            id="offcanvas",
            title="Wind Farms",
            is_open=False,
        ),
    ]
)

controls = dbc.Col([
            html.Div([
                html.Div([
                    html.Div(dbc.Alert("Select a wind farm below to see more information.", color="success", dismissable=True)),
                    html.H4('Wind Farm'),
                    'Site Name',
                    dcc.Dropdown(id='drop_mobile', value='Kype Muir Wind Farm', options=[{'label':i,'value':i} for i in matches3['Site Name']], style={'color':'black', 'width':300}),
                    #daq.BooleanSwitch(id='toggle_wind', on=True, label="Hide Farms Under 1MW?", labelPosition="bottom", style={'padding':'5px'}),
                    html.Br(),
                    'Site Name Alt.',
                    dcc.Dropdown(id='drop2_mobile', options=[{'label':i,'value':i} for i in reftotal['Generator Name']], style={'color':'black', 'width':300}, value='Kype Muir Wind Farm'),
                ], style={'padding':'10px', 'margin':'10px', 'backgroundColor':'#303030'}),
                html.Div([
                    html.H4(id='wind_farm_name'),
                    html.Div(id='wind_farm_details'),
                    html.Hr(),
                    html.Div(id='predicted_windspeed'),
                ], style={'padding':'10px', 'margin':'10px', 'backgroundColor':'#303030'}),
                html.Div(id='card3'),
                html.Div([
                    html.H4('Filters'),
                    html.Div([
                        html.P('Best Performing'),
                        dcc.RadioItems(options=[{'label':i, 'value':i} for i in ['High', 'Low', 'All']], value='All', id='radio10_mobile'),
                    ], style={'display':'flex'}),
                    html.Div([
                        html.P('Highest Production'),
                        dcc.RadioItems(options=[{'label':i, 'value':i} for i in ['High', 'Low', 'All']], value='All', id='radio11_mobile'),
                    ], style={'display':'flex'}),
                    html.Hr(),
                    html.H5('Table Filter'),
                    html.Div([
                        html.P('Top 20 by...'),
                        dcc.Dropdown(id='top20_drop', options=[{'label':i, 'value':i} for i in megcol[2:]], value=megcol[2], style={'color':'black', 'width':250}),
                    ], style={'display':'flex', 'width':'100%'}),
                    html.P('Year'),
                    dcc.Slider(id='slider_year',min=roc.Date.dt.year.min(),max=roc.Date.dt.year.max(),step=1,value=2020, tooltip={"placement": "bottom", "always_visible": True}), 
                ], style={'padding':'10px', 'margin':'10px', 'backgroundColor':'#303030'}),
                html.Div(dbc.ButtonGroup([
                    dbc.Button('Average', id='btn_general_mobile', n_clicks_timestamp='0', className='btn btn-primary btn-lg'),
                    dbc.Button('Prediction', id='btn_predict_mobile', n_clicks_timestamp='0', className='btn btn-success btn-lg'),
                    dbc.Button('Total', id='btn_news_mobile', n_clicks_timestamp='0', className='btn btn-light btn-lg'),
                ], vertical=True)
                        , className='d-grid gap-2', style={'padding':'10px', 'margin':'10px', 'backgroundColor':'#303030'}),

            ]),
    dbc.Tooltip("Select a wind farm", target='drop_mobile'),
    dbc.Tooltip("Alternate wind farm names (inactive)", target='drop2_mobile'),
    dbc.Tooltip("Inactive", target='btn_general_mobile'),
    dbc.Tooltip("Inactive", target='btn_predict_mobile'),
    dbc.Tooltip("Inactive", target='btn_news_mobile'),
        ], xs=12, sm=12, md=12, lg=3)

app.layout = html.Div([
    dcc.Location(id="url-mobile"),
    sidebar,
    offcanvas,
    dbc.Row([
        content,
        controls
    ])
], className="dbc")



page1 = dbc.Row([
        dbc.Col([
            html.Div(dbc.Alert([
                html.H4("Wind Farms in the United Kingdom", className="alert-heading"),
                html.P("Explore our content on UK wind farms (onshore at the moment). See how individual wind farms are performing directly from the raw electricity generation data."),
                html.P("Do wind farms decline over the years? Look at our page on individual wind farm generation to see if they do."),
                html.Hr(),
                html.P("This page looks at the location of wind farms. Select a wind farm from the dropdown box."),
            ], color="primary", dismissable=True), style={'margin':'10px'}),
            html.Div([
                html.H4('Predicted wind speed'),
                html.P('Across the UK a predicted wind speed has been estimated based on topology'),
                dcc.Graph(id='graph1_mobile')
            ], style={'padding':'10px', 'margin':'10px', 'backgroundColor':'#303030'})], width=12),
        dbc.Col(
            html.Div([
                html.H4('Current Status'),
                html.P('Wind farms current planning application or live status'),
                dcc.Graph(id='graph2_mobile')
            ], style={'padding':'10px', 'margin':'10px', 'backgroundColor':'#303030'}), xs=12, sm=12, md=12, lg=6),
        dbc.Col(
            html.Div([
                html.H4('Satellite View'),
                html.P('Satellite view of selected wind farm'),
                html.Iframe(id='iframe', width='100%', height='450px')
            ], style={'padding':'10px', 'margin':'10px', 'backgroundColor':'#303030'}), xs=12, sm=12, md=12, lg=6)
    ])


page2 = dbc.Row([
        dbc.Col([
            html.Div(dbc.Alert([
                html.H4("Wind Farms in the United Kingdom", className="alert-heading"),
                html.P(
                    "Explore our content on UK wind farms (onshore at the moment). See how individual wind farms are performing directly from the raw electricity generation data."
                ),
                html.P("Do wind farms decline over the years? Look at our page on individual wind farm generation to see if they do."),
                html.Hr(),
                html.P("This page explores the data on all the wind farms."),
            ], color="primary", dismissable=True), style={'margin':'10px'}),
            dcc.Graph(id='graph5_mobile', style={'height':'45vh', 'margin':'10px'})], xs=12, sm=12, md=12, lg=9),
        dbc.Col([dbc.Row([
            dbc.Col(dcc.Graph(id='graph5_pie1', style={'height':'22vh', 'margin':'10px 0px 0px 0px'}), sm=4, md=4, lg=12),
            dbc.Col(dcc.Graph(id='graph5_pie2', style={'height':'22vh', 'margin':'10px 0px 0px 0px'}), sm=4, md=4, lg=12),
            dbc.Col(dcc.Graph(id='line_month', style={'height':'22vh', 'margin':'10px 0px 0px 0px'}), sm=4, md=4, lg=12),
        ])], xs=12, sm=12, md=12, lg=3),
        dbc.Col(dcc.Graph(id='graph6_mobile', style={'height':'45vh', 'margin':'10px'}), xs=12, sm=12, md=12, lg=6),
        dbc.Col(dcc.Graph(id='graph7_mobile', style={'height':'45vh', 'margin':'10px'}), xs=12, sm=12, md=12, lg=6),
        dbc.Col(html.Div(html.H6('Load Factor by Country'), style={'margin':'10px', 'width':'100%'}), width=6),
        dbc.Col(html.Div(html.H6('Rolling (all time) vs Average (last year) Load Factor'), style={'margin':'10px', 'width':'100%'}), width=6),
        dbc.Col(html.Div(id='gauge2', style={'margin':'10px', 'width':'100%'}), width=6),
        dbc.Col(html.Div(id='gauge3', style={'margin':'10px', 'width':'100%'}), width=6),
        dbc.Col(dcc.Graph(id='graph8_mobile', style={'height':'45vh', 'margin':'10px'}), xs=12, sm=12, md=12, lg=6),
        dbc.Col(dcc.Graph(id='graph9_mobile', style={'height':'45vh', 'margin':'10px'}), xs=12, sm=12, md=12, lg=6),
    ])

page3 = dbc.Row([
    dbc.Col([
        html.Div(dbc.Alert([
                html.H4("Wind Farms in the United Kingdom", className="alert-heading"),
                html.P(
                    "Explore our content on UK wind farms (showing onshore only at the moment). See how individual wind farms are performing directly from the raw electricity generation data."
                ),
                html.P("Do wind farms decline over the years? Look at our page on individual wind farm generation to see if they do."),
                html.Hr(),
                html.P("Select a wind farm from the dropdown box to see its electricity generation data."),
            ], color="primary", dismissable=True), style={'margin':'10px'}),
        html.Div([
            html.H4('Electricity Generated'),
            html.P('Choose a wind farm from the drop down box'),
            dcc.Graph(id='graph4_mobile', className="dbc")
        ], className="dbc", style={'padding':'10px', 'margin':'10px', 'backgroundColor':'#303030'})], width=12),
    dbc.Col(
        html.Div([
            html.H4('Load Factor'),
            html.P('Load Factor Annually for selected wind farm'),
            html.Div(id='gauge')
        ], style={'padding':'10px', 'margin':'10px', 'backgroundColor':'#303030'}), width=12)
])

page4 = dbc.Row([
    dbc.Col([
        html.Div(dbc.Alert([
                html.H4("Wind Farms in the United Kingdom", className="alert-heading"),
                html.P(
                    "Explore our content on UK wind farms (onshore only). See how individual wind farms are performing directly from the raw electricity generation data."
                ),
                html.P("Do wind farms decline over the years? Look at our page on individual wind farm generation to see if they do."),
                html.Hr(),
                html.P("This page explores the characteristics of wind farms based on your filters. Play around with the controls."),
            ], color="primary", dismissable=True), style={'margin':'10px'})], width=12),
    dbc.Col([
        html.Div([
            html.H4('Best Performing'),
            html.P('Load Factor describes how efficient a wind farm is in producing electricity. It is a measure of the percentage of total maximum possible electricity production (if the wind was blowing hard all day every day). The average in the UK is around 28% onshore, and 35% offshore.'),
            dcc.Graph(id='graph10_mobile')
        ], style={'padding':'10px', 'margin':'10px', 'backgroundColor':'#303030'})], sm=12, md=12, lg=6),
    dbc.Col([
        html.Div([
            html.H4('Highest Production'),
            html.P('Highest producing wind farms in the UK'),
            dcc.Graph(id='graph11_mobile')
        ], style={'padding':'10px', 'margin':'10px', 'backgroundColor':'#303030'})], sm=12, md=12, lg=6),
    dbc.Col([
        html.Div([
            dash_table.DataTable(
                data=megamerge_temp.to_dict('records'), 
                columns=[{"name": i, "id": i} for i in megamerge_temp.columns],
                style_header={'color':'white', 'backgroundColor':'#adb5bd'},
                style_data={
                    'color': 'white',
                    'backgroundColor': '#00a077',
                    'whiteSpace': 'normal',
                    'height': 'auto',
                },
                style_data_conditional=[
                    {
                        'if': {'row_index': 'odd'},
                        'backgroundColor': '#2f4d6c',
                    }
                ],
                id='table_mobile'
            )
        ], style={'padding':'10px', 'margin':'10px', 'backgroundColor':'#303030'})], width=12),
    dbc.Col([
        html.Div([
            html.H4('Top 20 Producers'),
            html.P('(owners of multiple wind farms)'),
            dcc.Graph(id='graph12_mobile')
        ], style={'padding':'10px', 'margin':'10px', 'backgroundColor':'#303030'})], sm=12, md=12, lg=8),
    dbc.Col([
        html.Div([
            html.H4('Top 20 Producers (for the year)'),
            html.P('(sorted by chosen year)'),
            dcc.Graph(id='graph13_mobile')
        ], style={'padding':'10px', 'margin':'10px', 'backgroundColor':'#303030'})], sm=12, md=12, lg=4),
    ])
        

@app.callback(
    Output("offcanvas", "is_open"),
    Input("open-offcanvas", "n_clicks"),
    [State("offcanvas", "is_open")],
)
def toggle_offcanvas(n1, is_open):
    if n1:
        return not is_open
    return is_open

#@app.callback(
#    Output('drop_mobile', 'options'),
#    Input('toggle_wind', 'on')
#)
#def update_drop_mobile(on):
#    if on:
#        options=[{'label':i,'value':i} for i in matches3['Site Name']]
#    else:
#        options=[{'label':i,'value':i} for i in shape25m2['Site Name'].unique()[1:]]
#    return options

@app.callback(
    [Output('wind_farm_name', 'children'),
     Output('wind_farm_details', 'children')],
    Input('drop_mobile', 'value')
)
def update_wind_farm_details(site_name):
    v = matches3[matches3['Site Name']==site_name]['Generator Name'].item()
    return site_name, html.Ul([html.Li('Age '+str(reftotal[reftotal['Generator Name']==v]['years'].item())+' years'),  html.Li('Capacity '+str(int(reftotal[reftotal['Generator Name']==v]['IC (kW)'].item()/1000))+'MW'),html.Li('Annual Maximum Capacity '+str(int(reftotal[reftotal['Generator Name']==v]['IC (kW)'].item()/1000*24*365))), html.Li('Latest MWH pa '+str(reftotal[reftotal['Generator Name']==v]['Latest MWh pa'].item())), html.Li('Latest ROCs pa '+str(reftotal[reftotal['Generator Name']==v]['Latest ROCs pa'].item())), html.Li('LF Difference '+str(np.round(reftotal[reftotal['Generator Name']==v]['load factor difference'].item(),2))), html.Li('Annual LF '+str(np.round(reftotal[reftotal['Generator Name']==v]['ALF'].item(),2))), html.Li('Rolling LF '+str(np.round(reftotal[reftotal['Generator Name']==v]['RLF'].item(),2)))])

@app.callback(
    Output('graph1_mobile', 'figure'),
    [Input('drop_mobile', 'value')]
)
def update_map1_mobile(site_name):
    lat=shape25m2[shape25m2['Site Name']==site_name]['lat'].item()
    lon=shape25m2[shape25m2['Site Name']==site_name]['lon'].item()
    newshape = shape25m2[(shape25m2['lat']<(lat+0.6))&(shape25m2['lat']>(lat-0.6))&(shape25m2['lon']<(lon+1))&(shape25m2['lon']>(lon-1))]
    fig = px.scatter_mapbox(newshape[newshape['Speed25m']>0], lat='lat', lon='lon', color='bins3', zoom=10, size='bins2', color_discrete_map=color_discrete_map2, opacity=0.3, hover_name='Site Name', center=dict(lat=55,lon=-3), category_orders={'bins3':list(color_discrete_map2.keys())})
    fig.update_traces(hovertemplate=None, hoverinfo='skip')
    fig.add_trace(px.scatter_mapbox(newshape[newshape['bins2']==10], lat='lat', lon='lon', color_discrete_sequence=['#00bc8c'], size='bins2', size_max=10, hover_name='Site Name').data[0])
    fig.update_layout(mapbox=dict(center=dict(lat=newshape[newshape['Site Name']==site_name]['lat'].item(),lon=newshape[newshape['Site Name']==site_name]['lon'].item())), margin=dict(l=0, r=0, t=0, b=0))
    #fig = px.scatter_mapbox(shape25m2[shape25m2['Speed25m']>0], lat='lat', lon='lon', color='bins3', zoom=10, size='bins2', color_discrete_map=color_discrete_map2, opacity=0.3, hover_name='Site Name', center=dict(lat=55,lon=-3))
    #fig.update_traces(hovertemplate=None, hoverinfo='skip')
    #fig.add_trace(px.scatter_mapbox(shape25m2[shape25m2['bins2']==10], lat='lat', lon='lon', color_discrete_sequence=['#00bc8c'], size='bins2', size_max=10, hover_name='Site Name').data[0])
    #fig.add_trace(px.scatter_mapbox(substations[substations['VOLTAGE_HIGH']==400], lat='lat', lon='lon', color_discrete_sequence=['yellow'], size='VOLTAGE_HIGH', size_max=20).data[0])
    #fig.add_trace(px.scatter_mapbox(substations[substations['VOLTAGE_HIGH']==275], lat='lat', lon='lon', color_discrete_sequence=['red'], size='VOLTAGE_HIGH', size_max=15).data[0])
    #fig.add_trace(px.scatter_mapbox(substations[substations['VOLTAGE_HIGH']==132], lat='lat', lon='lon', color_discrete_sequence=['orange'], size='VOLTAGE_HIGH', size_max=10).data[0])
    #fig.add_trace(px.scatter_mapbox(sub33g, lat='lat', lon='lon', color_discrete_sequence=['pink'], size='size', size_max=10).data[0])
    #fig.add_trace(px.scatter_mapbox(ukpower[ukpower['SiteVoltage']==33], lat='lat', lon='lon', color_discrete_sequence=['pink'], hover_name='DateCommissioned').data[0])
    #fig.add_trace(px.scatter_mapbox(ssen, lat='Location Latitude', lon='Location Longitude', color_discrete_sequence=['pink']).data[0])
    #fig.update_layout(mapbox=dict(center=dict(lat=shape25m2[shape25m2['Site Name']==site_name]['lat'].item(),lon=shape25m2[shape25m2['Site Name']==site_name]['lon'].item())), margin=dict(l=20, r=20, t=20, b=20))
    fig.update_layout(legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01))
    return fig

@app.callback(
    Output('graph2_mobile', 'figure'),
    Input('drop_mobile', 'value')
)
def update_map2_mobile(site_name):
    fig2 = px.scatter_mapbox(gov_wind, lat='lat', lon='lon', hover_name='Site Name',
                  zoom=10, mapbox_style='dark', size='Installed Capacity (MWelec)', color='In Use', color_discrete_sequence=['red', 'yellow', 'green', 'blue', 'orange'])
    fig2.update_layout(mapbox=dict(center=dict(lat=shape25m2[shape25m2['Site Name']==site_name]['lat'].item(),lon=shape25m2[shape25m2['Site Name']==site_name]['lon'].item())), margin=dict(l=0, r=0, t=0, b=0))
    fig2.update_layout(legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01))
    return fig2

@app.callback(
    Output('iframe', 'src'),
    Input('drop_mobile', 'value')
)
def update_iframe(site_name):
    lat = str(gov_wind[gov_wind['Site Name']==site_name]['lat'].item())
    lon = str(gov_wind[gov_wind['Site Name']==site_name]['lon'].item())
    return 'https://www.google.com/maps/embed?pb=!1m14!1m12!1m3!1d5236.086865432605!2d'+lon+'!3d'+lat+'!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!5e1!3m2!1sen!2suk!4v1667916191559!5m2!1sen!2suk'

@app.callback(
    Output('graph3_mobile', 'figure'),
    [Input('drop_mobile', 'value')]
)
def update_graph3_mobile(value):
    fig = px.scatter_mapbox(live_offshore, lat='lat', lon='lon', width=600, size=live_offshore_new['1'], color=live_offshore_new['1']/(live_offshore['MW']*1000), hover_name='Generator Name', zoom=4.8, title='Current production compared with potential production', range_color=[0,1], color_continuous_scale=px.colors.sequential.GnBu)
    fig.update_layout(mapbox=dict(center=dict(lat=55, lon=-1)), margin=dict(l=20, r=20, t=30, b=20), coloraxis_showscale=False)
    return fig

@app.callback(
    Output('graph4_mobile', 'figure'),
    #Input('drop2_mobile', 'value')
    Input('drop_mobile', 'value')
)
def update_graph4_mobile(value):
    if len(matches3[matches3['Site Name']==value])>0:
        if matches3[matches3['Site Name']==value]['Generator Name'].item() is np.nan:
            fig = px.bar([0])
        else:
            value2 = matches3[matches3['Site Name']==value]['Generator Name'].item()
            chosenroc = roc[roc['Generating Station / Agent Group'].str.contains(value2, case=False)]
            chosenroc2 = chosenroc.resample('M', on='Date').sum()
            fig = px.bar(chosenroc2, y='No. Of Certificates', template='darkly')
    else:
        fig = px.bar([0])
    fig.update_layout(margin=dict(l=20, r=20, t=40, b=10))
    return fig

@app.callback(
    Output('gauge', 'children'),
    #Input('drop2_mobile', 'value')
    Input('drop_mobile', 'value')
)
def update_value(value):
    if len(matches3[matches3['Site Name']==value])>0:
        if matches3[matches3['Site Name']==value]['Generator Name'].item() is np.nan:
            return html.Div(daq.Gauge(min=0, max=1, value=0))
        else:
            value2 = matches3[matches3['Site Name']==value]['Generator Name'].item()
            chosenroc = roc[roc['Generating Station / Agent Group'].str.contains(value2, case=False)]
            annual_lf = chosenroc.resample('y', on='Date').sum()['No. Of Certificates']/(reftotal[reftotal['Generator Name']==value2]['IC (kW)'].item()/1000*24*365)
            return html.Div([daq.Gauge(min=0, max=1, value=annual_lf[x], label=str(annual_lf.index[x].year), size=100, color='#00bc8c') for x in range(len(annual_lf))], style={'display':'flex', 'overflow':'scroll'})
    else:
        return html.Div(daq.Gauge(min=0, max=1, value=0))

@app.callback(
    [Output('graph5_mobile', 'figure'),
     Output('graph5_pie1', 'figure'),
     Output('graph5_pie2', 'figure'),
     Output('line_month', 'figure'),
     Output('graph6_mobile', 'figure'),
    Output('graph7_mobile', 'figure'),
    Output('gauge2', 'children'),
    Output('gauge3', 'children'),
    Output('graph8_mobile', 'figure'),
    Output('graph9_mobile', 'figure')],
    Input('drop_mobile', 'value')
)
def update_graph5_mobile(site_name):
    fig = px.scatter(reftotal[reftotal['IC (kW)']>999], x='Accreditation', y=np.log(reftotal[reftotal['IC (kW)']>999]['IC (kW)']), color='Country', title='Size (logarithmic) of wind farms vs age')
    fig.update_layout(margin=dict(l=20, r=20, t=40, b=10))
    pie1 = px.pie(reftotal.groupby('Country').count().reset_index(), values='Subsidy', names='Country', title='Number of wind farms')
    pie1.update_layout(margin=dict(l=20, r=20, t=30, b=20))
    pie2 = px.pie(pd.DataFrame(reftotal.groupby('Country').sum()['IC (kW)']/1000).reset_index(), values='IC (kW)', names='Country', title='MWH Capacity')
    pie2.update_layout(margin=dict(l=20, r=20, t=30, b=10))
    roc['Month'] = roc['Date'].dt.month
    linemonth = px.line(roc.groupby('Month').sum()['No. Of Certificates'], title='MWH by month')
    linemonth.update_layout(margin=dict(l=0, r=10, t=30, b=0), showlegend=False)
    roc_annual = roc.resample('y', on='Date').sum().reset_index()
    roc_annual['year'] = roc_annual['Date'].dt.year
    fig2 = px.bar(x=roc_annual['year'], y=roc_annual['No. Of Certificates'], title='Total Generated MWH')
    fig2.update_layout(margin=dict(l=20, r=20, t=40, b=10))
    fig3 = px.bar(reftotal['years'].value_counts(), title='Age of wind farms')
    fig3.update_layout(margin=dict(l=20, r=20, t=40, b=10), showlegend=False)
    rlf_country = [reftotal[reftotal['Country']==reftotal['Country'].unique()[x]]['RLF'].mean() for x in range(4)]
    gauge2 = html.Div([daq.Gauge(min=0, max=1, value=rlf_country[x], label=str(reftotal['Country'].unique()[x]), size=100, color='#00bc8c') for x in range(4)], style={'display':'flex'})
    gauge3 = html.Div([
        daq.Gauge(min=0, max=1, value=reftotal['RLF'].mean(), label='Rolling RLF', size=100, color='#00bc8c'),
        daq.Gauge(min=0, max=1, value=reftotal['ALF'].mean(), label='Average ALF', size=100, color='#00bc8c')
    ], style={'display':'flex'})
    fig4 = px.bar(reftotal.groupby('years').mean()['RLF'], title='Rolling Load Factor by age of wind farms')
    fig4.update_layout(margin=dict(l=20, r=20, t=40, b=10), showlegend=False)
    fig5 = px.bar(reftotal.groupby('years').mean()['ALF'], title='Average Load Factor last year by age of wind farms')
    fig5.update_layout(margin=dict(l=20, r=20, t=40, b=10), showlegend=False)
    return fig, pie1, pie2, linemonth, fig2, fig3, gauge2, gauge3, fig4, fig5

@app.callback(
    Output('graph10_mobile', 'figure'),
    Input('radio10_mobile', 'value')
)
def update_graph10_mobile(v):
    if v == 'High':
        megamerge2 = megamerge[megamerge['RLF']>0.321]
    elif v == 'Low':
        megamerge2 = megamerge[megamerge['RLF']<0.238]
    else:
        megamerge2 = megamerge
    fig = px.scatter_mapbox(megamerge2, lat='lat', lon='lon', color='RLF', hover_name='Site Name', color_continuous_scale=px.colors.sequential.GnBu, zoom=5)
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
    return fig

@app.callback(
    Output('graph11_mobile', 'figure'),
    Input('radio11_mobile', 'value')
)
def update_graph11_mobile(v):
    if v == 'High':
        megamerge2 = megamerge[megamerge['Latest MWh pa']>50000]
    elif v == 'Low':
        megamerge2 = megamerge[megamerge['Latest MWh pa']<8315]
    else:
        megamerge2 = megamerge
    fig = px.scatter_mapbox(megamerge2, lat='lat', lon='lon', color='Latest MWh pa', size='Latest MWh pa', hover_name='Site Name', zoom=5, color_continuous_scale=px.colors.sequential.GnBu)
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
    return fig

@app.callback(
    Output('table_mobile', 'data'),
    Input('top20_drop', 'value')
)
def update_table_mobile(v):
    megamerge_temp2 = megamerge.sort_values(by=v, ascending=False)[:20][['Site Name', 'Country', 'IC (kW)',
       'RLF', 'ALF', 'Latest MWh pa', 'Latest ROCs pa', 'years',
       'Operational', 'Turbine (MW)', 'No.', 'Height (m)']]
    return megamerge_temp2.to_dict('records')

@app.callback(
    [Output('graph12_mobile', 'figure'),
     Output('graph13_mobile', 'figure')],
    Input('slider_year', 'value')
)
def update_graph12_mobile(v):
    topproducers_alltime = roc.groupby('Current Holder Organisation Name').sum().sort_values(by='No. Of Certificates', ascending=False)[:20].reset_index()
    fig = px.bar(topproducers_alltime, y='Current Holder Organisation Name', x='No. Of Certificates', orientation='h')
    fig.update_layout(margin=dict(l=20, r=20, t=20, b=20))
    topproducers_byyear = roc[roc['Date'].dt.year==v].groupby('Current Holder Organisation Name').sum().sort_values(by='No. Of Certificates', ascending=False)[:20].reset_index()
    fig2 = px.bar(topproducers_byyear, y='Current Holder Organisation Name', x='No. Of Certificates', orientation='h')
    fig2.update_layout(margin=dict(l=20, r=20, t=20, b=20))
    return fig, fig2

@app.callback(
    Output('predicted_windspeed', 'children'),
    Input('drop_mobile', 'value')
)
def update_predicted_windspeed(v):
    x = megamerge[megamerge['Site Name']==v]['speedCat'].item()
    return html.Div(html.P('Predicted wind speed: '+x), style={'backgroundColor':color_discrete_map2[x]})

@app.callback(
    Output('page-content-mobile', 'children'),
    Input('url-mobile', 'pathname')
)
def render_page_content_mobile(pathname):
    if pathname == '/':
        return page1
    elif pathname == '/page2':
        return page2
    elif pathname == '/page3':
        return page3
    elif pathname == '/page4':
        return page4
    return '404'

if __name__=='__main__':
    app.run_server(debug=True, port=8061)