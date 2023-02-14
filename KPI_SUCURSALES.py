#!/usr/bin/env python
# coding: utf-8

# In[22]:


import pandas as pd
from pylab import rcParams
import matplotlib.pyplot as plt
import dash_auth

import plotly.graph_objects as go
from datetime import datetime

import dash
import dash_core_components as dcc 
import dash_html_components as html
import plotly.express as px
from dash.dependencies import Input, Output


# In[23]:


ALL_DATA=pd.read_csv('DATOS_1.csv', encoding='latin-1')
ALL_DATA['FECHA_ven']=pd.to_datetime(ALL_DATA.Fecha_ven)


# In[24]:


grades=ALL_DATA.TOTAL_VENTA.tolist()
ALL_DATA['TOTAL_VENTA']=[float(g) for g in grades]
ALL_DATA=ALL_DATA[ALL_DATA['TOTAL_VENTA']>=10]


# In[25]:


grades=ALL_DATA.CODIGO_BARRAS.tolist()
ALL_DATA['BARRAS']=[str(g) for g in grades]
ALL_DATA['BARRAS']=ALL_DATA.BARRAS.str.split(".", expand = True)[0]

grades=ALL_DATA.MES.tolist()
ALL_DATA['MES']=[str(g) for g in grades]
ALL_DATA['MES']=ALL_DATA.MES.str.split(".", expand = True)[0]

grades=ALL_DATA.PERIODO.tolist()
ALL_DATA['PERIODO']=[str(g) for g in grades]
ALL_DATA['PERIODO']=ALL_DATA.PERIODO.str.split(".", expand = True)[0]


# In[26]:


#fecha de un dia anterior a hoy
dia='31'
mes='01'
mess='Ene'
FECHA0=mess+'-'+'01'
FECHA1=mess+'-'+dia


# In[27]:


#### DEL MES
TEXT_19_1=ALL_DATA[(ALL_DATA['FECHA_ven']>='2019-'+mes+'-01')&(ALL_DATA['FECHA_ven']<='2019'+'-'+mes+'-'+dia)]
TEXT_20_1=ALL_DATA[(ALL_DATA['FECHA_ven']>='2020-'+mes+'-01')&(ALL_DATA['FECHA_ven']<='2020'+'-'+mes+'-'+dia)]
TEXT_21_1=ALL_DATA[(ALL_DATA['FECHA_ven']>='2021-'+mes+'-01')&(ALL_DATA['FECHA_ven']<='2021'+'-'+mes+'-'+dia)]
TEXT_22_1=ALL_DATA[(ALL_DATA['FECHA_ven']>='2022-'+mes+'-01')&(ALL_DATA['FECHA_ven']<='2022'+'-'+mes+'-'+dia)]
TEXT_23_1=ALL_DATA[(ALL_DATA['FECHA_ven']>='2023-'+mes+'-01')&(ALL_DATA['FECHA_ven']<='2023'+'-'+mes+'-'+dia)]

ALL_DATA_mes=pd.concat([TEXT_19_1,TEXT_20_1,TEXT_21_1,TEXT_22_1,TEXT_23_1])

#### DEL DIA
TEXT_19_2=ALL_DATA_mes[(ALL_DATA_mes['FECHA_ven']=='2019'+'-'+mes+'-'+dia)]
TEXT_20_2=ALL_DATA_mes[(ALL_DATA_mes['FECHA_ven']=='2020'+'-'+mes+'-'+dia)]
TEXT_21_2=ALL_DATA_mes[(ALL_DATA_mes['FECHA_ven']=='2021'+'-'+mes+'-'+dia)]
TEXT_22_2=ALL_DATA_mes[(ALL_DATA_mes['FECHA_ven']=='2022'+'-'+mes+'-'+dia)]
TEXT_23_2=ALL_DATA_mes[(ALL_DATA_mes['FECHA_ven']=='2023'+'-'+mes+'-'+dia)]

ALL_DATA_dia=pd.concat([TEXT_19_2,TEXT_20_2,TEXT_21_2,TEXT_22_2,TEXT_23_2])


# In[28]:


# grafica financiera total y de texto
dff_tot=ALL_DATA.groupby(pd.Grouper(key='FECHA_ven',freq='1d')).sum()[['TOTAL_VENTA','CANTIDAD_VENTA']]
##--------------------------------
dff_tot=dff_tot.reset_index()
dff_tot['Año'] = dff_tot['FECHA_ven'].dt.year 
dff_tot['Mes'] = dff_tot['FECHA_ven'].dt.month 
dff_tot['Dia'] = dff_tot['FECHA_ven'].dt.day 


lista1=dff_tot.TOTAL_VENTA.tolist()[:-1]
DATOOO=dff_tot[(dff_tot['Mes']==1)&(dff_tot['Año']>=2019)]  #para venta acumulada


# In[29]:


look_up = {1: 'Ene', 2: 'Feb', 3: 'Mar', 4: 'Abr', 5: 'May',6: 'Jun', 7: 'Jul', 8: 'Ago', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dic'}

TOTAL_REF=dff_tot[(dff_tot['FECHA_ven']>='2019-01-01')&(dff_tot['FECHA_ven']<='2019'+'-'+mes+'-'+dia)
        |(dff_tot['FECHA_ven']>='2020-01-01')&(dff_tot['FECHA_ven']<='2020'+'-'+mes+'-'+dia)
        |(dff_tot['FECHA_ven']>='2021-01-01')&(dff_tot['FECHA_ven']<='2021'+'-'+mes+'-'+dia)
        |(dff_tot['FECHA_ven']>='2022-01-01')&(dff_tot['FECHA_ven']<='2022'+'-'+mes+'-'+dia)
        |(dff_tot['FECHA_ven']>='2023-01-01')&(dff_tot['FECHA_ven']<='2023'+'-'+mes+'-'+dia)]

TOTAL_REF['MES'] = TOTAL_REF['Mes'].apply(lambda x: look_up[x])
TOTAL_REF['AÑO']=[str(g) for g in TOTAL_REF.Año.tolist()]
anual=TOTAL_REF.groupby(['AÑO']).sum().round().reset_index()
mensual=TOTAL_REF[TOTAL_REF['MES']==mess].groupby(['AÑO']).sum().round().reset_index()


# In[30]:


VENTA_DEL_MES=ALL_DATA_mes.groupby(by=['SUCURSAL','PERIODO']).sum()[['TOTAL_VENTA']].reset_index().sort_values(by='PERIODO',ascending=True)

VENTA_DEL_DIA=ALL_DATA_dia.groupby(by=['SUCURSAL','PERIODO']).sum()[['TOTAL_VENTA']].reset_index().sort_values(by='PERIODO',ascending=True)


# In[31]:


lista=VENTA_DEL_MES.groupby('SUCURSAL').sum().sort_values(by='TOTAL_VENTA',ascending=False).reset_index().SUCURSAL.tolist()
MES=pd.DataFrame()
for i in lista:
    MES2=VENTA_DEL_MES[VENTA_DEL_MES['SUCURSAL']==i]
    MES=pd.concat([MES,MES2])
VENTA_DEL_MES=MES


# In[32]:


MES=pd.DataFrame()
for i in lista:
    MES2=VENTA_DEL_DIA[VENTA_DEL_DIA['SUCURSAL']==i]
    MES=pd.concat([MES,MES2])
VENTA_DEL_DIA=MES


# In[33]:


PRODUCTO_MES=ALL_DATA_mes.groupby(by=['PERIODO','TITULO']).sum()[['TOTAL_VENTA']].reset_index().sort_values(by='TOTAL_VENTA',ascending=False)
PRODUCTO_DIA=ALL_DATA_dia.groupby(by=['PERIODO','TITULO']).sum()[['TOTAL_VENTA']].reset_index().sort_values(by='TOTAL_VENTA',ascending=False)
periodo=['2019', '2020','2021', '2022','2023']
TOP_mes=pd.DataFrame()
TOP_dia=pd.DataFrame()
for i in periodo:
    PROD1=PRODUCTO_MES[PRODUCTO_MES['PERIODO']==i].sort_values(by='TOTAL_VENTA',ascending=False).head(10)
    PROD2=PRODUCTO_DIA[PRODUCTO_DIA['PERIODO']==i].sort_values(by='TOTAL_VENTA',ascending=False).head(10)
    TOP_mes=pd.concat([TOP_mes,PROD1])
    TOP_dia=pd.concat([TOP_dia,PROD2])


# In[ ]:





# In[34]:


PRODUCTO_MES=ALL_DATA_mes[(ALL_DATA_mes['TIPO_PRODUCTO']=='Producto 1')&(ALL_DATA_mes['LINEA_NEGOCIO']!='TEXTO')&(ALL_DATA_mes['TIPO_VENTA']!='MAYORISTAS')&(ALL_DATA_mes['TIPO_VENTA']!='CREDITO')].groupby(by=['PERIODO','BARRAS','TITULO']).sum()[['TOTAL_VENTA']].reset_index().sort_values(by='TOTAL_VENTA',ascending=False)
PRODUCTO_DIA=ALL_DATA_dia[(ALL_DATA_mes['TIPO_PRODUCTO']=='Producto 1')&(ALL_DATA_dia['LINEA_NEGOCIO']!='TEXTO')&(ALL_DATA_dia['TIPO_VENTA']!='MAYORISTAS')&(ALL_DATA_dia['TIPO_VENTA']!='CREDITO')].groupby(by=['PERIODO','BARRAS','TITULO']).sum()[['TOTAL_VENTA']].reset_index().sort_values(by='TOTAL_VENTA',ascending=False)
periodo=['2019', '2020','2021', '2022','2023']
TOP_mes_notext=pd.DataFrame()
TOP_dia_notext=pd.DataFrame()
for i in periodo:
    PROD1=PRODUCTO_MES[PRODUCTO_MES['PERIODO']==i].sort_values(by='TOTAL_VENTA',ascending=False).head(10)
    PROD2=PRODUCTO_DIA[PRODUCTO_DIA['PERIODO']==i].sort_values(by='TOTAL_VENTA',ascending=False).head(10)
    TOP_mes_notext=pd.concat([TOP_mes_notext,PROD1])
    TOP_dia_notext=pd.concat([TOP_dia_notext,PROD2])


# In[35]:


num=VENTA_DEL_DIA[VENTA_DEL_DIA['PERIODO']=='2023'].TOTAL_VENTA.sum()
ventadeldia = "${:,.2f}".format(num)

num=VENTA_DEL_MES[VENTA_DEL_MES['PERIODO']=='2023'].TOTAL_VENTA.sum()
ventadelmes = "${:,.2f}".format(num)


# In[36]:


ACCESORIOS=ALL_DATA_mes[(ALL_DATA_mes['TIPO_PRODUCTO']=='Producto 2')].groupby(['SUCURSAL','PERIODO','MES']).sum()[['TOTAL_VENTA']].reset_index()
ACCESORIOS=ACCESORIOS.sort_values(by='TOTAL_VENTA',ascending=False)
num=ACCESORIOS[ACCESORIOS['PERIODO']=='2023'].TOTAL_VENTA.sum()
accesorios = "${:,.2f}".format(num)

LIBRO=ALL_DATA_mes[(ALL_DATA_mes['TIPO_PRODUCTO']=='Producto 1')].groupby(['SUCURSAL','PERIODO','MES']).sum()[['TOTAL_VENTA']].reset_index()
LIBRO=LIBRO.sort_values(by='TOTAL_VENTA',ascending=False)
num=LIBRO[LIBRO['PERIODO']=='2023'].TOTAL_VENTA.sum()
libros = "${:,.2f}".format(num)


# In[37]:


ALL_DATA_mes['SUCURSAL'].unique()


# In[38]:


TEXTO=ALL_DATA_mes[(ALL_DATA_mes['LINEA_NEGOCIO']=='Línea 2')&(ALL_DATA_mes['TIPO_PRODUCTO']=='Producto 1')].groupby(['SUCURSAL','PERIODO','MES']).sum()[['TOTAL_VENTA']].reset_index()
TEXTO=TEXTO.sort_values(by='TOTAL_VENTA',ascending=False)
num=TEXTO[TEXTO['PERIODO']=='2023'].TOTAL_VENTA.sum()
texto = "${:,.2f}".format(num)


FONDO=ALL_DATA_mes[(ALL_DATA_mes['LINEA_NEGOCIO']=='Línea 1')&(ALL_DATA_mes['TIPO_PRODUCTO']=='Producto 1')].groupby(['SUCURSAL','PERIODO','MES']).sum()[['TOTAL_VENTA']].reset_index()
FONDO=FONDO.sort_values(by='TOTAL_VENTA',ascending=False)
num=FONDO[FONDO['PERIODO']=='2023'].TOTAL_VENTA.sum()
fondo = "${:,.2f}".format(num)


NOVEDAD=ALL_DATA_mes[(ALL_DATA_mes['LINEA_NEGOCIO']=='Línea 3')&(ALL_DATA_mes['TIPO_PRODUCTO']=='Producto 1')].groupby(['SUCURSAL','PERIODO','MES']).sum()[['TOTAL_VENTA']].reset_index()
NOVEDAD=NOVEDAD.sort_values(by='TOTAL_VENTA',ascending=False)
num=NOVEDAD[NOVEDAD['PERIODO']=='2023'].TOTAL_VENTA.sum()
novedad = "${:,.2f}".format(num)

IMPORTACION=ALL_DATA_mes[(ALL_DATA_mes['LINEA_NEGOCIO']=='Línea 4')&(ALL_DATA_mes['TIPO_PRODUCTO']=='Producto 1')].groupby(['SUCURSAL','PERIODO','MES']).sum()[['TOTAL_VENTA']].reset_index()
IMPORTACION=IMPORTACION.sort_values(by='TOTAL_VENTA',ascending=False)
num=IMPORTACION[IMPORTACION['PERIODO']=='2023'].TOTAL_VENTA.sum()
importacion = "${:,.2f}".format(num)


# In[39]:


POSICIONES=["1er", "2do", "3er", "4to",'5to','6to','7to','8to','9to','10to','11to','12to','13to','14to','15to','16to','17to','18to','19to','20to']


# In[42]:


#VALID_USERNAME_PASSWORD_PAIRS = {
 #   'Fernando': 'Fernando','CARLOS': 'CARLOS'
#}
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
#auth = dash_auth.BasicAuth(app,VALID_USERNAME_PASSWORD_PAIRS)
app.layout = html.Div([
    
    html.Div([
        html.H1('Indicadores de venta - prueba', style={'fontSize': 30,'font-family':'sans-serif'}),
        html.Img(src='assets/ALIMENTO.png')
    ],style = {}, className = 'banner'),

    html.Div([
        html.Div([
            html.P('Selecciona la Sucursal', className = 'fix_label', style={'color':'black', 'margin-top': '4px'}),
            dcc.RadioItems(id = 'items', 
                            labelStyle = {'display': 'inline-block'},
                            options = [
                                {'label' : 'CADENA', 'value' : 'CADENA'},
                            ], value = 'CADENA',
                            style = {'text-aling':'center', 'color':'navy'}, className = 'dcc_compon'),
        ], className = 'create_container2 thirteen columns', style = {'margin-bottom': '10px'}),
    ], className = 'row flex-display'),

##################################################################------------------------------

    html.Div([
        html.Div([
            dcc.Graph(id = 'my_graph1_1', figure = {})
        ], className = 'create_container1 six columns'),
        html.Div([
            dcc.Graph(id = 'index_graph1_1', figure = {})
        ], className = 'create_container1 four columns'),
        html.Div([
            dcc.Graph(id = 'my_graph1_2', figure = {})
        ], className = 'create_container1 four columns'),
    ], className = 'row flex-display'),
    
##################################################################------------------------------

    html.Div([
        html.H1('Comportamiento de ventas', style={'fontSize': 25,'font-family':'sans-serif'})
    ],style = {}, className = 'banner3'),
    
##################################################################------------------------------    
    html.Div([
        html.Div([
            dcc.Graph(id = 'bar_graph2_1', figure = {})
        ], className = 'create_container1 seven columns'),        
        html.Div([
            dcc.Graph(id = 'bar_graph2_2', figure = {})
        ], className = 'create_container1 seven columns'),

    ], className = 'row flex-display'),
##################################################################------------------------------
    
##################################################################------------------------------

    html.Div([
        html.H1('Venta segmentada', style={'fontSize': 25,'font-family':'sans-serif'})
    ],style = {}, className = 'banner2'),
##################################################################------------------------------
    html.Div([
        html.Div([
            dcc.Graph(id = 'bar_graph3_3', figure = {})
        ], className = 'create_container1 four columns'),
        html.Div([
            dcc.Graph(id = 'bar_graph3_2', figure = {})
        ], className = 'create_container1 four columns'),
        html.Div([
            dcc.Graph(id = 'bar_graph3_1', figure = {})
        ], className = 'create_container1 seven columns'),

    ], className = 'row flex-display'),
##################################################################------------------------------
    html.Div([
        html.Div([
            dcc.Graph(id = 'bar_graph4_3', figure = {})
        ], className = 'create_container1 four columns'),
        html.Div([
            dcc.Graph(id = 'bar_graph4_2', figure = {})
        ], className = 'create_container1 four columns'),
        html.Div([
            dcc.Graph(id = 'bar_graph4_1', figure = {})
        ], className = 'create_container1 seven columns'),

    ], className = 'row flex-display'),    
##################################################################------------------------------

    html.Div([
        html.H1('Indicadores por línea de negocio', style={'fontSize': 25,'font-family':'sans-serif'})
    ],style = {}, className = 'banner2'),
    
##################################################################------------------------------
    html.Div([
        html.Div([
            dcc.Graph(id = 'bar_graph8_1', figure = {})
        ], className = 'create_container1 seven columns'),
        html.Div([
            dcc.Graph(id = 'bar_graph8_2', figure = {})
        ], className = 'create_container1 four columns'),
        html.Div([
            dcc.Graph(id = 'bar_graph8_3', figure = {})
        ], className = 'create_container1 four columns'),

    ], className = 'row flex-display'),    
    
##################################################################------------------------------
    html.Div([
        html.Div([
            dcc.Graph(id = 'bar_graph9_1', figure = {})
        ], className = 'create_container1 seven columns'),
        html.Div([
            dcc.Graph(id = 'bar_graph9_2', figure = {})
        ], className = 'create_container1 four columns'),
        html.Div([
            dcc.Graph(id = 'bar_graph9_3', figure = {})
        ], className = 'create_container1 four columns'),

    ], className = 'row flex-display'),    
    
    
##################################################################------------------------------
    html.Div([
        html.Div([
            dcc.Graph(id = 'bar_graph11_1', figure = {})
        ], className = 'create_container1 seven columns'),
        html.Div([
            dcc.Graph(id = 'bar_graph11_2', figure = {})
        ], className = 'create_container1 four columns'),
        html.Div([
            dcc.Graph(id = 'bar_graph11_3', figure = {})
        ], className = 'create_container1 four columns'),

    ], className = 'row flex-display'),    
##################################################################------------------------------
##################################################################------------------------------    
    
    
    html.Div([
        html.H1('TOP 10 del mes y dia', style={'fontSize': 25,'font-family':'sans-serif'})
    ],style = {}, className = 'banner3'),
    
##################################################################------------------------------    
    html.Div([
        html.Div([
            dcc.Graph(id = 'bar_graph5_1', figure = {})
        ], className = 'create_container1 seven columns'),        
        html.Div([
            dcc.Graph(id = 'bar_graph5_2', figure = {})
        ], className = 'create_container1 seven columns'),

    ], className = 'row flex-display'),

    
], id='mainContainer', style={'display':'flex', 'flex-direction':'column'})


# In[ ]:


##################################################################------------------------------

@app.callback(
    Output('my_graph1_1', component_property='figure'),
    [Input('items', component_property='value')])


def update_graph_pie(value):
    if value == 'CADENA':
        fig5 = go.Figure()
        fig5.add_trace(go.Histogram(histfunc="sum", y=DATOOO[DATOOO['Año']==2019].TOTAL_VENTA, x=DATOOO[DATOOO['Año']==2019].Dia, name="2019",nbinsx=31))
        fig5.add_trace(go.Histogram(histfunc="sum", y=DATOOO[DATOOO['Año']==2020].TOTAL_VENTA, x=DATOOO[DATOOO['Año']==2020].Dia, name="2020",nbinsx=31))
        fig5.add_trace(go.Histogram(histfunc="sum", y=DATOOO[DATOOO['Año']==2021].TOTAL_VENTA, x=DATOOO[DATOOO['Año']==2021].Dia, name="2021",nbinsx=31))
        fig5.add_trace(go.Histogram(histfunc="sum", y=DATOOO[DATOOO['Año']==2022].TOTAL_VENTA, x=DATOOO[DATOOO['Año']==2022].Dia, name="2022",nbinsx=31))
        fig5.add_trace(go.Histogram(histfunc="sum", y=DATOOO[DATOOO['Año']==2023].TOTAL_VENTA, x=DATOOO[DATOOO['Año']==2023].Dia, name="2023",nbinsx=31))
        fig5.update_layout(title='Comparativo de venta diaria - ENERO',yaxis_title='Pesos $',showlegend=True, height=350)
    return (fig5)



@app.callback(
    Output('index_graph1_1', component_property='figure'),
    [Input('items', component_property='value')])

def update_graph_pie(value):
    if value == 'CADENA':
        fig2 = go.Figure()

        fig2.add_trace(go.Indicator(mode = "number+delta",value = anual[anual['AÑO']=='2023'].TOTAL_VENTA.sum(),
        title = {"text": "Alcance anual<br><span style='font-size:0.8em;color:gray'>2023 vs 2022</span><br><span style='font-size:0.6em;color:gray'>Ene-01 a "+FECHA1+" (2023)"+"</span>"},
        delta = {'reference': anual[anual['AÑO']=='2022'].TOTAL_VENTA.sum(), 'relative': False},
        domain = {'x': [.05, .32], 'y':  [0.2, .8]}))
        fig2.add_trace(go.Indicator(mode = "delta",value = anual[anual['AÑO']=='2023'].TOTAL_VENTA.sum(),
        delta = {'reference': anual[anual['AÑO']=='2022'].TOTAL_VENTA.sum(), 'relative': True},
        domain = {'x': [.05, .32], 'y': [0.15, .35]}))        

        fig2.add_trace(go.Indicator(mode = "number+delta",value = mensual[mensual['AÑO']=='2023'].TOTAL_VENTA.sum(),
        title = {"text": "Alcance mensual<br><span style='font-size:0.8em;color:gray'>2023 vs 2022</span><br><span style='font-size:0.6em;color:gray'>Ene-01 a "+FECHA1+" (2023)"+"</span>"},
        delta = {'reference': mensual[mensual['AÑO']=='2022'].TOTAL_VENTA.sum(), 'relative': False},
        domain = {'x': [.68, .95], 'y': [0.2, .8]}))
        fig2.add_trace(go.Indicator(mode = "delta",value = mensual[mensual['AÑO']=='2023'].TOTAL_VENTA.sum(),
        delta = {'reference': mensual[mensual['AÑO']=='2022'].TOTAL_VENTA.sum(), 'relative': True},
        domain = {'x': [.68, .95], 'y': [0.15, .35]}))
        
        fig2.update_layout(title='Alcance de venta',showlegend=True,height=350)
    return (fig2)

@app.callback(
    Output('my_graph1_2', component_property='figure'),
    [Input('items', component_property='value')])

def update_graph_pie(value):
    if value == 'CADENA':
        df=TOTAL_REF
        fig3 = px.histogram(df, x="AÑO", y="TOTAL_VENTA", color="MES")
        fig3.update_layout(title='Venta acumulada, de Enero-01 a '+FECHA1, yaxis_title='Pesos $',showlegend=True, height=350)
    return (fig3)


##################################################################------------------------------
##################################################################------------------------------
@app.callback(
    Output('bar_graph2_1', component_property='figure'),
    [Input('items', component_property='value')])

def update_graph(value):

    if value == 'CADENA':

        fig5 = go.Figure()
        fig5.add_trace(go.Histogram(histfunc="sum", y=VENTA_DEL_MES[VENTA_DEL_MES['PERIODO']=='2019'].TOTAL_VENTA, x=VENTA_DEL_MES[VENTA_DEL_MES['PERIODO']=='2019'].SUCURSAL, name="2019",nbinsx=31))
        fig5.add_trace(go.Histogram(histfunc="sum", y=VENTA_DEL_MES[VENTA_DEL_MES['PERIODO']=='2020'].TOTAL_VENTA, x=VENTA_DEL_MES[VENTA_DEL_MES['PERIODO']=='2020'].SUCURSAL, name="2020",nbinsx=31))
        fig5.add_trace(go.Histogram(histfunc="sum", y=VENTA_DEL_MES[VENTA_DEL_MES['PERIODO']=='2021'].TOTAL_VENTA, x=VENTA_DEL_MES[VENTA_DEL_MES['PERIODO']=='2021'].SUCURSAL, name="2021",nbinsx=31))
        fig5.add_trace(go.Histogram(histfunc="sum", y=VENTA_DEL_MES[VENTA_DEL_MES['PERIODO']=='2022'].TOTAL_VENTA, x=VENTA_DEL_MES[VENTA_DEL_MES['PERIODO']=='2022'].SUCURSAL, name="2022",nbinsx=31))
        fig5.add_trace(go.Histogram(histfunc="sum", y=VENTA_DEL_MES[VENTA_DEL_MES['PERIODO']=='2023'].TOTAL_VENTA, x=VENTA_DEL_MES[VENTA_DEL_MES['PERIODO']=='2023'].SUCURSAL, name="2023",nbinsx=31))
        fig5.update_layout(title='Venta mensual, de Ene-01 a '+FECHA1+'- '+ventadelmes,yaxis_title='Pesos $',showlegend=True, height=420,xaxis = go.layout.XAxis(
        tickangle = 90))
    return (fig5)


@app.callback(
    Output('bar_graph2_2', component_property='figure'),
    [Input('items', component_property='value')])

def update_graph_pie(value):
    if value == 'CADENA':
        fig5 = go.Figure()
        fig5.add_trace(go.Histogram(histfunc="sum", y=VENTA_DEL_DIA[VENTA_DEL_DIA['PERIODO']=='2019'].TOTAL_VENTA, x=VENTA_DEL_DIA[VENTA_DEL_DIA['PERIODO']=='2019'].SUCURSAL, name="2019",nbinsx=31))
        fig5.add_trace(go.Histogram(histfunc="sum", y=VENTA_DEL_DIA[VENTA_DEL_DIA['PERIODO']=='2020'].TOTAL_VENTA, x=VENTA_DEL_DIA[VENTA_DEL_DIA['PERIODO']=='2020'].SUCURSAL, name="2020",nbinsx=31))
        fig5.add_trace(go.Histogram(histfunc="sum", y=VENTA_DEL_DIA[VENTA_DEL_DIA['PERIODO']=='2021'].TOTAL_VENTA, x=VENTA_DEL_DIA[VENTA_DEL_DIA['PERIODO']=='2021'].SUCURSAL, name="2021",nbinsx=31))
        fig5.add_trace(go.Histogram(histfunc="sum", y=VENTA_DEL_DIA[VENTA_DEL_DIA['PERIODO']=='2022'].TOTAL_VENTA, x=VENTA_DEL_DIA[VENTA_DEL_DIA['PERIODO']=='2022'].SUCURSAL, name="2022",nbinsx=31))
        fig5.add_trace(go.Histogram(histfunc="sum", y=VENTA_DEL_DIA[VENTA_DEL_DIA['PERIODO']=='2023'].TOTAL_VENTA, x=VENTA_DEL_DIA[VENTA_DEL_DIA['PERIODO']=='2023'].SUCURSAL, name="2023",nbinsx=31))
        fig5.update_layout(title='Venta de '+FECHA1+'- '+ventadeldia,yaxis_title='Pesos $',showlegend=True, height=420,xaxis = go.layout.XAxis(
        tickangle = 90))
    return (fig5)
        
##################################################################------------------------------
##################################################################------------------------------
@app.callback(
    Output('bar_graph3_1', component_property='figure'),
    [Input('items', component_property='value')])

def update_graph(value):
    if value == 'CADENA':
        fig5 = go.Figure()
        fig5.add_trace(go.Histogram(histfunc="sum", y=LIBRO[LIBRO['PERIODO']=='2019'].TOTAL_VENTA, x=LIBRO[LIBRO['PERIODO']=='2019'].SUCURSAL, name="2019",nbinsx=31))
        fig5.add_trace(go.Histogram(histfunc="sum", y=LIBRO[LIBRO['PERIODO']=='2020'].TOTAL_VENTA, x=LIBRO[LIBRO['PERIODO']=='2020'].SUCURSAL, name="2020",nbinsx=31))
        fig5.add_trace(go.Histogram(histfunc="sum", y=LIBRO[LIBRO['PERIODO']=='2021'].TOTAL_VENTA, x=LIBRO[LIBRO['PERIODO']=='2021'].SUCURSAL, name="2021",nbinsx=31))
        fig5.add_trace(go.Histogram(histfunc="sum", y=LIBRO[LIBRO['PERIODO']=='2022'].TOTAL_VENTA, x=LIBRO[LIBRO['PERIODO']=='2022'].SUCURSAL, name="2022",nbinsx=31))
        fig5.add_trace(go.Histogram(histfunc="sum", y=LIBRO[LIBRO['PERIODO']=='2023'].TOTAL_VENTA, x=LIBRO[LIBRO['PERIODO']=='2023'].SUCURSAL, name="2023",nbinsx=31))
        fig5.update_layout(title='Comparativo de venta mensual-Producto 1, de Ene-01 a '+FECHA1+'- '+libros,yaxis_title='Pesos $',showlegend=True, height=350,xaxis = go.layout.XAxis(
        tickangle = 90))
    return (fig5)


@app.callback(
    Output('bar_graph3_2', component_property='figure'),
    [Input('items', component_property='value')])

def update_graph_pie(value):
    if value == 'CADENA':
        fig5 = go.Figure()
        fig5 = px.histogram(LIBRO.sort_values(by='PERIODO'), x="PERIODO", y="TOTAL_VENTA", color="MES")
        fig5.update_layout(title='Venta acumulada, de Enero-01 a '+FECHA1, yaxis_title='Pesos $',showlegend=True, height=350)
    return (fig5)

@app.callback(
    Output('bar_graph3_3', component_property='figure'),
    [Input('items', component_property='value')])

def update_graph_pie(value):
    if value == 'CADENA':
        fig5 = go.Figure() 
        fig5.add_trace(go.Indicator(mode = "number+delta",value = ALL_DATA_mes[(ALL_DATA_mes['TIPO_PRODUCTO']=='Producto 1')&(ALL_DATA_mes['PERIODO']=='2023')].TOTAL_VENTA.sum(),
        title = {"text": "Alcance mensual<br><span style='font-size:0.8em;color:gray'>2023 vs 2022</span><br><span style='font-size:0.6em;color:gray'>Ene-01 a "+FECHA1+" (2023)"+"</span>"},
        delta = {'reference': ALL_DATA_mes[(ALL_DATA_mes['TIPO_PRODUCTO']=='Producto 1')&(ALL_DATA_mes['PERIODO']=='2022')].TOTAL_VENTA.sum(), 'relative': False},
        domain = {'x': [.1, .85], 'y': [0.2, .8]}))
        fig5.add_trace(go.Indicator(mode = "delta",value = ALL_DATA_mes[(ALL_DATA_mes['TIPO_PRODUCTO']=='Producto 1')&(ALL_DATA_mes['PERIODO']=='2023')].TOTAL_VENTA.sum(),
        delta = {'reference': ALL_DATA_mes[(ALL_DATA_mes['TIPO_PRODUCTO']=='Producto 1')&(ALL_DATA_mes['PERIODO']=='2022')].TOTAL_VENTA.sum(), 'relative': True},
        domain = {'x': [.1, .85], 'y': [0.01, .25]}))
        fig5.update_layout(title='Alcance de venta - Producto 1',showlegend=True,height=350)
    return (fig5)        
##################################################################------------------------------
##################################################################------------------------------
@app.callback(
    Output('bar_graph4_1', component_property='figure'),
    [Input('items', component_property='value')])

def update_graph(value):
    if value == 'CADENA':
        fig5 = go.Figure()
        fig5.add_trace(go.Histogram(histfunc="sum", y=ACCESORIOS[ACCESORIOS['PERIODO']=='2019'].TOTAL_VENTA, x=ACCESORIOS[ACCESORIOS['PERIODO']=='2019'].SUCURSAL, name="2019",nbinsx=31))
        fig5.add_trace(go.Histogram(histfunc="sum", y=ACCESORIOS[ACCESORIOS['PERIODO']=='2020'].TOTAL_VENTA, x=ACCESORIOS[ACCESORIOS['PERIODO']=='2020'].SUCURSAL, name="2020",nbinsx=31))
        fig5.add_trace(go.Histogram(histfunc="sum", y=ACCESORIOS[ACCESORIOS['PERIODO']=='2021'].TOTAL_VENTA, x=ACCESORIOS[ACCESORIOS['PERIODO']=='2021'].SUCURSAL, name="2021",nbinsx=31))
        fig5.add_trace(go.Histogram(histfunc="sum", y=ACCESORIOS[ACCESORIOS['PERIODO']=='2022'].TOTAL_VENTA, x=ACCESORIOS[ACCESORIOS['PERIODO']=='2022'].SUCURSAL, name="2022",nbinsx=31))
        fig5.add_trace(go.Histogram(histfunc="sum", y=ACCESORIOS[ACCESORIOS['PERIODO']=='2023'].TOTAL_VENTA, x=ACCESORIOS[ACCESORIOS['PERIODO']=='2023'].SUCURSAL, name="2023",nbinsx=31))
        fig5.update_layout(title='Comparativo de venta mensual-Producto 2, de Ene-01 a '+FECHA1+'- '+accesorios,yaxis_title='Pesos $',showlegend=True, height=350,xaxis = go.layout.XAxis(
        tickangle = 90))
    return (fig5)


@app.callback(
    Output('bar_graph4_2', component_property='figure'),
    [Input('items', component_property='value')])

def update_graph_pie(value):
    if value == 'CADENA':
        fig5 = go.Figure()
        fig5 = px.histogram(ACCESORIOS.sort_values(by='PERIODO'), x="PERIODO", y="TOTAL_VENTA", color="MES")
        fig5.update_layout(title='Venta acumulada, de Enero-01 a '+FECHA1, yaxis_title='Pesos $',showlegend=True, height=350)
    return (fig5)

@app.callback(
    Output('bar_graph4_3', component_property='figure'),
    [Input('items', component_property='value')])

def update_graph_pie(value):
    if value == 'CADENA':
        fig5 = go.Figure() 
        fig5.add_trace(go.Indicator(mode = "number+delta",value = ALL_DATA_mes[(ALL_DATA_mes['TIPO_PRODUCTO']=='Producto 2')&(ALL_DATA_mes['PERIODO']=='2023')].TOTAL_VENTA.sum(),
        title = {"text": "Alcance mensual<br><span style='font-size:0.8em;color:gray'>2023 vs 2022</span><br><span style='font-size:0.6em;color:gray'>Ene-01 a "+FECHA1+" (2023)"+"</span>"},
        delta = {'reference': ALL_DATA_mes[(ALL_DATA_mes['TIPO_PRODUCTO']=='Producto 2')&(ALL_DATA_mes['PERIODO']=='2022')].TOTAL_VENTA.sum(), 'relative': False},
        domain = {'x': [.1, .75], 'y': [0.2, .8]}))
        fig5.add_trace(go.Indicator(mode = "delta",value = ALL_DATA_mes[(ALL_DATA_mes['TIPO_PRODUCTO']=='Producto 2')&(ALL_DATA_mes['PERIODO']=='2023')].TOTAL_VENTA.sum(),
        delta = {'reference': ALL_DATA_mes[(ALL_DATA_mes['TIPO_PRODUCTO']=='Producto 2')&(ALL_DATA_mes['PERIODO']=='2022')].TOTAL_VENTA.sum(), 'relative': True},
        domain = {'x': [.1, .75], 'y': [0.01, .25]}))
        fig5.update_layout(title='Alcance de venta - Producto 2',showlegend=True,height=350)
    return (fig5)
##################################################################------------------------------
##################################################################------------------------------
@app.callback(
    Output('bar_graph8_1', component_property='figure'),
    [Input('items', component_property='value')])

def update_graph(value):
    if value == 'CADENA':
        fig5 = go.Figure()
        fig5.add_trace(go.Histogram(histfunc="sum", y=FONDO[FONDO['PERIODO']=='2019'].TOTAL_VENTA, x=FONDO[FONDO['PERIODO']=='2019'].SUCURSAL, name="2019",nbinsx=31))
        fig5.add_trace(go.Histogram(histfunc="sum", y=FONDO[FONDO['PERIODO']=='2020'].TOTAL_VENTA, x=FONDO[FONDO['PERIODO']=='2020'].SUCURSAL, name="2020",nbinsx=31))
        fig5.add_trace(go.Histogram(histfunc="sum", y=FONDO[FONDO['PERIODO']=='2021'].TOTAL_VENTA, x=FONDO[FONDO['PERIODO']=='2021'].SUCURSAL, name="2021",nbinsx=31))
        fig5.add_trace(go.Histogram(histfunc="sum", y=FONDO[FONDO['PERIODO']=='2022'].TOTAL_VENTA, x=FONDO[FONDO['PERIODO']=='2022'].SUCURSAL, name="2022",nbinsx=31))
        fig5.add_trace(go.Histogram(histfunc="sum", y=FONDO[FONDO['PERIODO']=='2023'].TOTAL_VENTA, x=FONDO[FONDO['PERIODO']=='2023'].SUCURSAL, name="2023",nbinsx=31))
        fig5.update_layout(title='Comparativo de venta mensual - LÍNEA 2, de Ene-01 a '+FECHA1+'- '+fondo,yaxis_title='Pesos $',showlegend=True, height=350,xaxis = go.layout.XAxis(
        tickangle = 90))
    return (fig5)

@app.callback(
    Output('bar_graph8_2', component_property='figure'),
    [Input('items', component_property='value')])

def update_graph_pie(value):
    if value == 'CADENA':
        fig5 = go.Figure()
        fig5 = px.histogram(FONDO.sort_values(by='PERIODO'), x="PERIODO", y="TOTAL_VENTA", color="MES")
        fig5.update_layout(title='Venta acumulada, de Enero-01 a '+FECHA1, yaxis_title='Pesos $',showlegend=True, height=350)
    return (fig5)

@app.callback(
    Output('bar_graph8_3', component_property='figure'),
    [Input('items', component_property='value')])

def update_graph_pie(value):
    if value == 'CADENA':
        fig5 = go.Figure() 
        fig5.add_trace(go.Indicator(mode = "number+delta",value = ALL_DATA_mes[(ALL_DATA_mes['LINEA_NEGOCIO']=='Línea 2')&(ALL_DATA_mes['TIPO_PRODUCTO']=='Producto 1')&(ALL_DATA_mes['PERIODO']=='2023')].TOTAL_VENTA.sum(),
        title = {"text": "Alcance mensual<br><span style='font-size:0.8em;color:gray'>2023 vs 2022</span><br><span style='font-size:0.6em;color:gray'>Ene-01 a "+FECHA1+" (2023)"+"</span>"},
        delta = {'reference': ALL_DATA_mes[(ALL_DATA_mes['LINEA_NEGOCIO']=='Línea 2')&(ALL_DATA_mes['TIPO_PRODUCTO']=='Producto 1')&(ALL_DATA_mes['PERIODO']=='2022')].TOTAL_VENTA.sum(), 'relative': False},
        domain = {'x': [.1, .75], 'y': [0.2, .8]}))
        fig5.add_trace(go.Indicator(mode = "delta",value = ALL_DATA_mes[(ALL_DATA_mes['LINEA_NEGOCIO']=='Línea 2')&(ALL_DATA_mes['TIPO_PRODUCTO']=='Producto 1')&(ALL_DATA_mes['PERIODO']=='2023')].TOTAL_VENTA.sum(),
        delta = {'reference': ALL_DATA_mes[(ALL_DATA_mes['LINEA_NEGOCIO']=='Línea 2')&(ALL_DATA_mes['TIPO_PRODUCTO']=='Producto 1')&(ALL_DATA_mes['PERIODO']=='2022')].TOTAL_VENTA.sum(), 'relative': True},
        domain = {'x': [.1, .75], 'y': [0.01, .25]}))
        fig5.update_layout(title='Alcance de venta - LÍNEA 2',showlegend=True,height=350)
    return (fig5)
##################################################################------------------------------
##################################################################------------------------------
@app.callback(
    Output('bar_graph9_1', component_property='figure'),
    [Input('items', component_property='value')])

def update_graph(value):
    if value == 'CADENA':
        fig5 = go.Figure()
        fig5.add_trace(go.Histogram(histfunc="sum", y=NOVEDAD[NOVEDAD['PERIODO']=='2019'].TOTAL_VENTA, x=NOVEDAD[NOVEDAD['PERIODO']=='2019'].SUCURSAL, name="2019",nbinsx=31))
        fig5.add_trace(go.Histogram(histfunc="sum", y=NOVEDAD[NOVEDAD['PERIODO']=='2020'].TOTAL_VENTA, x=NOVEDAD[NOVEDAD['PERIODO']=='2020'].SUCURSAL, name="2020",nbinsx=31))
        fig5.add_trace(go.Histogram(histfunc="sum", y=NOVEDAD[NOVEDAD['PERIODO']=='2021'].TOTAL_VENTA, x=NOVEDAD[NOVEDAD['PERIODO']=='2021'].SUCURSAL, name="2021",nbinsx=31))
        fig5.add_trace(go.Histogram(histfunc="sum", y=NOVEDAD[NOVEDAD['PERIODO']=='2022'].TOTAL_VENTA, x=NOVEDAD[NOVEDAD['PERIODO']=='2022'].SUCURSAL, name="2022",nbinsx=31))
        fig5.add_trace(go.Histogram(histfunc="sum", y=NOVEDAD[NOVEDAD['PERIODO']=='2023'].TOTAL_VENTA, x=NOVEDAD[NOVEDAD['PERIODO']=='2023'].SUCURSAL, name="2023",nbinsx=31))
        fig5.update_layout(title='Comparativo de venta mensual - LÍNEA 3, de Ene-01 a '+FECHA1+'- '+novedad,yaxis_title='Pesos $',showlegend=True, height=350,xaxis = go.layout.XAxis(
        tickangle = 90))
    return (fig5)


@app.callback(
    Output('bar_graph9_2', component_property='figure'),
    [Input('items', component_property='value')])

def update_graph_pie(value):
    if value == 'CADENA':
        fig5 = go.Figure()
        fig5 = px.histogram(NOVEDAD.sort_values(by='PERIODO'), x="PERIODO", y="TOTAL_VENTA", color="MES")
        fig5.update_layout(title='Venta acumulada, de Enero-01 a '+FECHA1, yaxis_title='Pesos $',showlegend=True, height=350)
    return (fig5)

@app.callback(
    Output('bar_graph9_3', component_property='figure'),
    [Input('items', component_property='value')])

def update_graph_pie(value):
    if value == 'CADENA':
        fig5 = go.Figure() 
        fig5.add_trace(go.Indicator(mode = "number+delta",value = ALL_DATA_mes[(ALL_DATA_mes['LINEA_NEGOCIO']=='Línea 3')&(ALL_DATA_mes['TIPO_PRODUCTO']=='Producto 1')&(ALL_DATA_mes['PERIODO']=='2023')].TOTAL_VENTA.sum(),
        title = {"text": "Alcance mensual<br><span style='font-size:0.8em;color:gray'>2023 vs 2022</span><br><span style='font-size:0.6em;color:gray'>Ene-01 a "+FECHA1+" (2023)"+"</span>"},
        delta = {'reference': ALL_DATA_mes[(ALL_DATA_mes['LINEA_NEGOCIO']=='Línea 3')&(ALL_DATA_mes['TIPO_PRODUCTO']=='Producto 1')&(ALL_DATA_mes['PERIODO']=='2022')].TOTAL_VENTA.sum(), 'relative': False},
        domain = {'x': [.1, .75], 'y': [0.2, .8]}))
        fig5.add_trace(go.Indicator(mode = "delta",value = ALL_DATA_mes[(ALL_DATA_mes['LINEA_NEGOCIO']=='Línea 3')&(ALL_DATA_mes['TIPO_PRODUCTO']=='Producto 1')&(ALL_DATA_mes['PERIODO']=='2023')].TOTAL_VENTA.sum(),
        delta = {'reference': ALL_DATA_mes[(ALL_DATA_mes['LINEA_NEGOCIO']=='Línea 3')&(ALL_DATA_mes['TIPO_PRODUCTO']=='Producto 1')&(ALL_DATA_mes['PERIODO']=='2022')].TOTAL_VENTA.sum(), 'relative': True},
        domain = {'x': [.1, .75], 'y': [0.01, .25]}))
        fig5.update_layout(title='Alcance de venta - LÍNEA 3',showlegend=True,height=350)
    return (fig5)

##################################################################------------------------------
##################################################################------------------------------
@app.callback(
    Output('bar_graph11_1', component_property='figure'),
    [Input('items', component_property='value')])

def update_graph(value):
    if value == 'CADENA':
        fig5 = go.Figure()
        fig5.add_trace(go.Histogram(histfunc="sum", y=IMPORTACION[IMPORTACION['PERIODO']=='2019'].TOTAL_VENTA, x=IMPORTACION[IMPORTACION['PERIODO']=='2019'].SUCURSAL, name="2019",nbinsx=31))
        fig5.add_trace(go.Histogram(histfunc="sum", y=IMPORTACION[IMPORTACION['PERIODO']=='2020'].TOTAL_VENTA, x=IMPORTACION[IMPORTACION['PERIODO']=='2020'].SUCURSAL, name="2020",nbinsx=31))
        fig5.add_trace(go.Histogram(histfunc="sum", y=IMPORTACION[IMPORTACION['PERIODO']=='2021'].TOTAL_VENTA, x=IMPORTACION[IMPORTACION['PERIODO']=='2021'].SUCURSAL, name="2021",nbinsx=31))
        fig5.add_trace(go.Histogram(histfunc="sum", y=IMPORTACION[IMPORTACION['PERIODO']=='2022'].TOTAL_VENTA, x=IMPORTACION[IMPORTACION['PERIODO']=='2022'].SUCURSAL, name="2022",nbinsx=31))
        fig5.add_trace(go.Histogram(histfunc="sum", y=IMPORTACION[IMPORTACION['PERIODO']=='2023'].TOTAL_VENTA, x=IMPORTACION[IMPORTACION['PERIODO']=='2023'].SUCURSAL, name="2023",nbinsx=31))
        fig5.update_layout(title='Comparativo de venta mensual - LÍNEA 4, de Ene-01 a '+FECHA1+'- '+importacion,yaxis_title='Pesos $',showlegend=True, height=350,xaxis = go.layout.XAxis(
        tickangle = 90))
    return (fig5)


@app.callback(
    Output('bar_graph11_2', component_property='figure'),
    [Input('items', component_property='value')])

def update_graph_pie(value):
    if value == 'CADENA':
        fig5 = go.Figure()
        fig5 = px.histogram(IMPORTACION.sort_values(by='PERIODO'), x="PERIODO", y="TOTAL_VENTA", color="MES")
        fig5.update_layout(title='Venta acumulada, de Enero-01 a '+FECHA1, yaxis_title='Pesos $',showlegend=True, height=350)
    return (fig5)

@app.callback(
    Output('bar_graph11_3', component_property='figure'),
    [Input('items', component_property='value')])

def update_graph_pie(value):
    if value == 'CADENA':
        fig5 = go.Figure() 
        fig5.add_trace(go.Indicator(mode = "number+delta",value = ALL_DATA_mes[(ALL_DATA_mes['LINEA_NEGOCIO']=='Línea 4')&(ALL_DATA_mes['TIPO_PRODUCTO']=='Producto 1')&(ALL_DATA_mes['PERIODO']=='2023')].TOTAL_VENTA.sum(),
        title = {"text": "Alcance mensual<br><span style='font-size:0.8em;color:gray'>2023 vs 2022</span><br><span style='font-size:0.6em;color:gray'>Ene-01 a "+FECHA1+" (2023)"+"</span>"},
        delta = {'reference': ALL_DATA_mes[(ALL_DATA_mes['LINEA_NEGOCIO']=='Línea 4')&(ALL_DATA_mes['TIPO_PRODUCTO']=='Producto 1')&(ALL_DATA_mes['PERIODO']=='2022')].TOTAL_VENTA.sum(), 'relative': False},
        domain = {'x': [.1, .75], 'y': [0.2, .8]}))
        fig5.add_trace(go.Indicator(mode = "delta",value = ALL_DATA_mes[(ALL_DATA_mes['LINEA_NEGOCIO']=='Línea 4')&(ALL_DATA_mes['TIPO_PRODUCTO']=='Producto 1')&(ALL_DATA_mes['PERIODO']=='2023')].TOTAL_VENTA.sum(),
        delta = {'reference': ALL_DATA_mes[(ALL_DATA_mes['LINEA_NEGOCIO']=='Línea 4')&(ALL_DATA_mes['TIPO_PRODUCTO']=='Producto 1')&(ALL_DATA_mes['PERIODO']=='2022')].TOTAL_VENTA.sum(), 'relative': True},
        domain = {'x': [.1, .75], 'y': [0.01, .25]}))
        fig5.update_layout(title='Alcance de venta - LÍNEA 4',showlegend=True,height=350)
    return (fig5)
##################################################################------------------------------
##################################################################------------------------------

@app.callback(
    Output('bar_graph5_1', component_property='figure'),
    [Input('items', component_property='value')])

def update_graph(value):

    if value == 'CADENA':
        fig15 = go.Figure()
        fig15.add_trace(go.Funnel(name = '2019',orientation = "h",
            y = POSICIONES,
            x = TOP_mes[TOP_mes['PERIODO']=='2019'].TOTAL_VENTA.tolist(),textposition = "inside",text=TOP_mes[TOP_mes['PERIODO']=='2019'].TITULO.tolist(),textinfo = "text"))
        fig15.add_trace(go.Funnel(name = '2020',orientation = "h",
            y = POSICIONES, x = TOP_mes[TOP_mes['PERIODO']=='2020'].TOTAL_VENTA.tolist(),textposition = "inside",text=TOP_mes[TOP_mes['PERIODO']=='2020'].TITULO.tolist(),textinfo = "text"))
        fig15.add_trace(go.Funnel(name = '2021',orientation = "h",
            y = POSICIONES, x = TOP_mes[TOP_mes['PERIODO']=='2021'].TOTAL_VENTA.tolist(),textposition = "inside",text=TOP_mes[TOP_mes['PERIODO']=='2021'].TITULO.tolist(),textinfo = "text"))
        fig15.add_trace(go.Funnel(name = '2022',orientation = "h",
            y = POSICIONES, x = TOP_mes[TOP_mes['PERIODO']=='2022'].TOTAL_VENTA.tolist(),textposition = "inside",text=TOP_mes[TOP_mes['PERIODO']=='2022'].TITULO.tolist(),textinfo = "text"))
        fig15.add_trace(go.Funnel(name = '2023',orientation = "h",
            y = POSICIONES, x = TOP_mes[TOP_mes['PERIODO']=='2023'].TOTAL_VENTA.tolist(),textposition = "inside",text=TOP_mes[TOP_mes['PERIODO']=='2023'].TITULO.tolist(),textinfo = "text"))
        fig15.update_layout(title='TOP 10 mensual, de Ene-01 a '+FECHA1 ,height=600)
        fig15.update_traces(textfont_size=20, textangle=0, cliponaxis=False)
    return (fig15)


@app.callback(
    Output('bar_graph5_2', component_property='figure'),
    [Input('items', component_property='value')])

def update_graph_pie(value):
    if value == 'CADENA':
        fig16 = go.Figure()
        fig16.add_trace(go.Funnel(name = '2019',orientation = "h",
            y = POSICIONES, x = TOP_dia[TOP_dia['PERIODO']=='2019'].TOTAL_VENTA.tolist(),textposition = "inside",text=TOP_dia[TOP_dia['PERIODO']=='2019'].TITULO.tolist(),textinfo = "text"))
        fig16.add_trace(go.Funnel(name = '2020',orientation = "h",
            y = POSICIONES, x = TOP_dia[TOP_dia['PERIODO']=='2020'].TOTAL_VENTA.tolist(),textposition = "inside",text=TOP_dia[TOP_dia['PERIODO']=='2020'].TITULO.tolist(),textinfo = "text"))
        fig16.add_trace(go.Funnel(name = '2021',orientation = "h",
            y = POSICIONES, x = TOP_dia[TOP_dia['PERIODO']=='2021'].TOTAL_VENTA.tolist(),textposition = "inside",text=TOP_dia[TOP_dia['PERIODO']=='2021'].TITULO.tolist(),textinfo = "text"))
        fig16.add_trace(go.Funnel(name = '2022',orientation = "h",
            y = POSICIONES, x = TOP_dia[TOP_dia['PERIODO']=='2022'].TOTAL_VENTA.tolist(),textposition = "inside",text=TOP_dia[TOP_dia['PERIODO']=='2022'].TITULO.tolist(),textinfo = "text"))
        fig16.add_trace(go.Funnel(name = '2023',orientation = "h",
            y = POSICIONES, x = TOP_dia[TOP_dia['PERIODO']=='2023'].TOTAL_VENTA.tolist(),textposition = "inside",text=TOP_dia[TOP_dia['PERIODO']=='2023'].TITULO.tolist(),textinfo = "text"))

        fig16.update_layout( title='TOP 10 del dia, '+FECHA1,height=600)
        fig16.update_traces(textfont_size=20, textangle=0, cliponaxis=False)

    return (fig16)



##################################################################------------------------------
##################################################################------------------------------

if __name__ == ('__main__'):
    app.run_server()
#    app.run_server()


# In[ ]:




