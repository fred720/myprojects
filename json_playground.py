import json
import requests


country = 'India'

url = f'https://restcountries.com/v3.1/name/{country}'

# print(url)

r = requests.get(url)
# print(type(r))
# print(response.status_code)
json_response = r.json()
# print(type(json_response)) # <class 'list'>
# print(json_response)
# for country in json_response:
#     print(country)
    
# print(type(country))

# for country in json_response:
#     print(country['name']['common'])
#     print(country['name']['official'])
#     print(country['capital'][0])
#     print(*country['languages'])
#     print(country['region'])
#     print(country['population'])
#     print(*country['currencies'])

def get_country_details(country):
    url = f'https://restcountries.com/v3.1/name/{country}'
    r = requests.get(url)
    json_response = r.json()
    for country in json_response:
        print(f'Common Name: {country['name']['common']}')
        print(f'Official Name: {country['name']['official']}')
        print(f'Capital: {country['capital'][0]}')
        print(f'Official Languages: {country['languages']}')
        print(f'Region: {country['region']}')
        print(f'Population: {country['population']}')
        print(f'Currencies: {country['currencies']}')
        
        
get_country_details('Chad')

    
    












# {'numFound': 0, 'start': 0, 'numFoundExact': True, 'docs': [], 'num_found': 0, 'q': '', 'offset': None}
# payload = {'q':'Science and math','offset':0,'limit':50,'sort':'new','order':'desc','lang':'en'}
# r =  requests.get('https://openlibrary.org/search.json',params=payload) # get the latest events from github
# # print(type(r))
# # print(dir(r))

# json_response = r.json()
# # print(type(json_response))


# docs = json_response['docs']
# print(type(docs))
# print(docs[0])

# for doc in docs:
#     print(doc)

# # print(type(doc))

# title = doc['title']

# author_name = doc['author_name']
# print(author_name)

# for author in author_name:
    # print(author)
    

# def get_title():
#     json_response = r.json()
#     docs = json_response['docs']
#     for doc in docs:
#         print(doc['title'])
        
        
# def get_author():
#     json_response = r.json()
#     docs = json_response['docs']
#     for doc in docs:
#         author_name = doc['author_name']
#         for author in author_name:
#             print(author)
    


        
# get_title()
# get_author()

   