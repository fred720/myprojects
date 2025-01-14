# Description: This script uses the restcountries API to get information about a country. 
import requests


def get_country_details(country: str)-> None:
    url = f'https://restcountries.com/v3.1/name/{country}'
    r = requests.get(url)
    json_response = r.json()
    for country in json_response:
        print(f'Common Name: {country['name']['common']}')
        print(f'Official Name: {country['name']['official']}')
        print(f'Capital: {country['capital'][0]}')
        print(f'Region: {country['region']}')
        print(f"Official Languages: {', '.join(list(country['languages'].values()))}")
        print(f'Population: {country['population']:,}')
        print(f"Area: {country['area']} km²")
        currencies = [f"{curr['name']} ({curr['symbol']})" for curr in country['currencies'].values()]
        print(f"Currencies: {', '.join(currencies)}")
        print(f'Car Driving: {country['car']['signs'][0]} : {country['car']['side']}')
        print(f"Latitude and logitude: {country['latlng'][0], country['latlng'][1]}")
        print(f"Timezones: {', '.join(country['timezones'])}")
        
        
        
get_country_details('russia')
