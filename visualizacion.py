import requests
import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_table

# Conexión a la API REST Countries
url = 'https://restcountries.com/v3.1/all'
response = requests.get(url)

# Verificar si la solicitud fue exitosa
if response.status_code == 200:
    countries_data = response.json()
else:
    print('Error al conectarse a la API')
    countries_data = []

# Extracción de información relevante
relevant_data = []
for country in countries_data:
    name = country.get('name', {}).get('common', 'N/A')
    capital = country.get('capital', ['N/A'])[0]
    region = country.get('region', 'N/A')
    subregion = country.get('subregion', 'N/A')
    population = country.get('population', 'N/A')
    area = country.get('area', 'N/A')
    languages = ', '.join(country.get('languages', {}).values())
    currencies = ', '.join([currency['name'] for currency in country.get('currencies', {}).values()])
    
    relevant_data.append({
        'Name': name,
        'Capital': capital,
        'Region': region,
        'Subregion': subregion,
        'Population': population,
        'Area': area,
        'Languages': languages,
        'Currencies': currencies
    })

# Crear DataFrame con los datos relevantes
df = pd.DataFrame(relevant_data)

# Inicializar la app Dash
app = dash.Dash(__name__)

# Layout de la app
app.layout = html.Div([
    html.H1("Análisis de Datos de Países"),
    
    # Tabla con la información relevante
    dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
        page_size=10,
        style_table={'overflowX': 'auto'},
        style_cell={
            'height': 'auto',
            'minWidth': '100px', 'width': '150px', 'maxWidth': '200px',
            'whiteSpace': 'normal'
        },
        style_header={
            'backgroundColor': 'rgb(230, 230, 230)',
            'fontWeight': 'bold'
        }
    ),
    
    dcc.Graph(id='population-area-scatter'),
    dcc.Graph(id='region-population-bar'),
    dcc.Graph(id='region-area-bar'),
    dcc.Graph(id='languages-bar'),
    dcc.Graph(id='currencies-bar')
])

# Callback para actualizar el gráfico de dispersión
@app.callback(
    Output('population-area-scatter', 'figure'),
    Input('population-area-scatter', 'id')
)
def update_scatter(id):
    fig = px.scatter(df, x='Area', y='Population', hover_name='Name', log_x=True, log_y=True,
                     title='Relación entre Población y Área')
    return fig

# Callback para actualizar el gráfico de barras de población por región
@app.callback(
    Output('region-population-bar', 'figure'),
    Input('region-population-bar', 'id')
)
def update_population_bar(id):
    region_population = df.groupby('Region')['Population'].sum().reset_index()
    fig = px.bar(region_population, x='Region', y='Population', title='Población Total por Región')
    return fig

# Callback para actualizar el gráfico de barras de área por región
@app.callback(
    Output('region-area-bar', 'figure'),
    Input('region-area-bar', 'id')
)
def update_area_bar(id):
    region_area = df.groupby('Region')['Area'].sum().reset_index()
    fig = px.bar(region_area, x='Region', y='Area', title='Área Total por Región')
    return fig

# Callback para actualizar el gráfico de barras de idiomas
@app.callback(
    Output('languages-bar', 'figure'),
    Input('languages-bar', 'id')
)
def update_languages_bar(id):
    language_counts = df['Languages'].str.split(', ').explode().value_counts().reset_index()
    language_counts.columns = ['Language', 'Count']
    fig = px.bar(language_counts, x='Language', y='Count', title='Distribución de Idiomas')
    return fig

# Callback para actualizar el gráfico de barras de monedas
@app.callback(
    Output('currencies-bar', 'figure'),
    Input('currencies-bar', 'id')
)
def update_currencies_bar(id):
    currency_counts = df['Currencies'].str.split(', ').explode().value_counts().reset_index()
    currency_counts.columns = ['Currency', 'Count']
    fig = px.bar(currency_counts, x='Currency', y='Count', title='Distribución de Monedas')
    return fig

# Ejecutar la app
if __name__ == '__main__':
    app.run_server(debug=True)