#!/usr/bin/env python
# coding: utf-8

# In[1]:


import dash
from dash import dcc
from dash import dcc
from dash import html
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import folium
import dash_mantine_components as dmc
from dash import Dash, dash_table
import dash_bootstrap_components as dbc
from dash import Dash, Input, Output, callback, dash_table
import numpy as np
import matplotlib.pyplot as plt


# In[2]:


css = 'https://codepen.io/chriddyp/pen/bWLwgP.css'
app = Dash(__name__, external_stylesheets=[css])
server = app.server


# In[5]:


def serve_layout():
    data=pd.read_excel("Ultima_Consulta.xlsx")
    data=data.drop("Unnamed: 0",axis=1)
    
            
    fig_semaforo_general = px.pie(data,names='Semaforo_General',title='Semáforo general 🚦',hole=.3,color='Semaforo_General',color_discrete_map={'Rojo':'red',
                                 'Verde':'green',
                                 'Amarillo':'yellow',
                                 'No es posible calcular':'gray',
                                 'Calculando..':'#C39BD3',
                                 })
    fig_semaforo_general.update_layout({
    'plot_bgcolor': 'rgba(0, 0, 0, 0)',
    'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    },font=dict(
        family="Verdana, Sans-serif",
        size=13,
        color="white"
    ),title_x=0.5)
    
    X = ['En transito a origen','En origen','En transito a destino','En destino']
    Verde=[len(data[(data["Estatus"]=='En tránsito a origen')&(data["Semaforo_General"]=='Verde')]),len(data[(data["Estatus"]=='En origen')&(data["Semaforo_General"]=='Verde')]),len(data[(data["Estatus"]=='En tránsito a destino')&(data["Semaforo_General"]=='Verde')]),len(data[(data["Estatus"]=='En destino')&(data["Semaforo_General"]=='Verde')])]
    Amarillo=[len(data[(data["Estatus"]=='En tránsito a origen')&(data["Semaforo_General"]=='Amarillo')]),len(data[(data["Estatus"]=='En origen')&(data["Semaforo_General"]=='Amarillo')]),len(data[(data["Estatus"]=='En tránsito a destino')&(data["Semaforo_General"]=='Amarillo')]),len(data[(data["Estatus"]=='En destino')&(data["Semaforo_General"]=='Amarillo')])]
    Rojo=[len(data[(data["Estatus"]=='En tránsito a origen')&(data["Semaforo_General"]=='Rojo')]),len(data[(data["Estatus"]=='En origen')&(data["Semaforo_General"]=='Rojo')]),len(data[(data["Estatus"]=='En tránsito a destino')&(data["Semaforo_General"]=='Rojo')]),len(data[(data["Estatus"]=='En destino')&(data["Semaforo_General"]=='Rojo')])]


    fig_semaforo_estatus = go.Figure(data=[
        go.Bar(name='En tiempo', x=X, y=Verde,text=Verde,marker_color=["green"]*4),
        go.Bar(name='En riesgo', x=X, y=Amarillo,text=Amarillo,marker_color=["yellow"]*4),
        go.Bar(name='Urgente', x=X, y=Rojo,text=Rojo,marker_color=["red"]*4)
    ])
    # Change the bar mode
    fig_semaforo_estatus.update_layout({
    'plot_bgcolor': 'rgba(0, 0, 0, 0)',
    'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    },barmode='stack',
    font=dict(
        family="Verdana, Sans-serif",
        size=13,
        color="white"
    ),title='Semáforo por estatus 🚦',title_x=0.5)
    


    estatus_=pd.DataFrame(data.groupby(by=["Estatus"]).size(),columns=["Count"])
    estatus_["Estatus"]=estatus_.index
    
    fig_estatus = px.bar(estatus_,x='Estatus',y='Count',title='Estatus',color='Estatus',text_auto=True)
    fig_estatus.update_layout({
    'plot_bgcolor': 'rgba(0, 0, 0, 0)',
    'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    },font=dict(
        family="Verdana, Sans-serif",
        size=13,
        color="white"
    ),title_x=0.5)

    
    colors={'Verde':'green','Rojo':'red','Amarillo':'yellow','Carga finalizada':'#C39BD3','No es posible calcular':'gray','Calculando..':'blue','Viaje finalizado':'orange'}
    Puntos_I={}
    for j in range(len(data)):
        color=colors[data.loc[j,"Semaforo_General"]]
        Puntos_I[data.loc[j,"Folio"]]=data.loc[j,"Coordenadas"].split(',')
        Puntos_I[data.loc[j,"Folio"]].append(color)
    
    # crear un mapa base centrado en México
    mapObj = folium.Map(location = [22.227205095658114, -100.3189399012432], zoom_start = 5)
    # crear objeto marcador para cada camion, uno por uno para cada coordenada en los datos DataFrame
    for i in Puntos_I:
        # crear un marcador para el lugar
        markerObj = folium.Marker(location = [Puntos_I[i][0],Puntos_I[i][1]], popup = i, tooltip= i,icon=folium.Icon(color=Puntos_I[i][2]))
        # añadir marcador al mapa
        markerObj.add_to(mapObj)
    
    markerObj.save('mapa.html')
    

    
    return html.Div(style={'backgroundColor': '#111111'},
    children=[
        html.H1(children="KLS LOGISTICS",className="hello",
    style={"fontSize": "48px",'color':'#dd191b','text-align':'center','fontWeight': 'bold'
          }),
        html.P(
            children="Monitoreo Viajes Prisma🧊",style={"fontSize": "25px",'color':'#ec8c88','text-align':'center'
          }
        ),
        html.Iframe(srcDoc=open('mapa.html','r').read(),width='100%',height='600'),
        dash_table.DataTable(data.loc[:,['Folio','Coordenadas','Estatus','Subestatus','Semaforo_General']].to_dict('records'), [{"name": i, "id": i} for i in data.loc[:,['Folio','Coordenadas',"Estatus","Subestatus",'Semaforo_General']].columns],style_as_list_view=False,
            style_cell={'padding': '2px','textAlign': 'center'},
                                 style_data={'color': 'black',
            'backgroundColor': '#adadad','whiteSpace': 'normal',
            'height': 'auto'},
            style_header={
                'backgroundColor': '#721717',
                'color':'white',
            },style_data_conditional=[
               {
            "if": {
                'column_id': 'Semaforo_General',
                'filter_query': '{Semaforo_General} eq "Rojo"'
            },
            "backgroundColor": "#FF0000",
            "color": "white"
            },{
            "if": {
                'column_id': 'Semaforo_General',
                'filter_query': '{Semaforo_General} eq "Verde"'
            },
            "backgroundColor": "#00E572",
            "color": "black"
            },
            {
            "if": {
                'column_id': 'Semaforo_General',
                'filter_query': '{Semaforo_General} eq "Amarillo"'
            },
            "backgroundColor": "#FFFB00",
            "color": "black"
            }
            ],),
        dcc.Graph(
            figure=fig_semaforo_general,
            style={'text-align':'center','width': '95vh', 'height': '95vh','display': 'inline-block'},
            
        ),
        dcc.Graph(
            figure=fig_semaforo_estatus,
            style={'text-align':'center','width': '95vh', 'height': '95vh','display': 'inline-block'},
            
        ),


        dcc.Graph(
            figure=fig_estatus,
            style={'text-align':'center','width': '200vh', 'height': '95vh'},
        ),
        
        
        
    ],
)


# In[6]:


app.layout=serve_layout


# In[7]:


if __name__ == '__main__':
    app.run_server(debug=True,use_reloader=False)

