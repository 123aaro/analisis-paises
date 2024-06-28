import requests
import pandas as pd

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

# Verificación de df
print(df.head())
print(df.columns)