import requests
import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

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
    dcc.Graph(id='population-area-scatter'),
    dcc.Graph(id='region-population-bar'),
    dcc.Graph(id='region-area-bar')
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

# Ejecutar la app
if __name__ == '__main__':
    app.run_server(debug=True)