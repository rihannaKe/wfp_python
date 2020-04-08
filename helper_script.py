import csv
import requests    
import json   
import pandas as pd


populaton_url = "https://api.hungermapdata.org/swe-notifications/population.csv" 

def getCountry(region_id):
    """
    Returns country data fetched from the given url
    """
    response = requests.get("https://api.hungermapdata.org/swe-notifications/region/" +str(region_id)+ "/country")
    countries = json.loads(response.text)
    return countries

# writes population_wt_country.csv data adding the country code for each row
with open('population_wt_country.csv', mode='w') as csv_file:
    fieldnames = ['country_id', 'region_id', 'population']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    population_data = pd.read_csv(populaton_url)
    for index, pop_data in population_data.iterrows():
        country_data = getCountry(pop_data['region_id'])
        writer.writerow({'country_id': country_data['country_id'],
                        'region_id': pop_data['region_id'], 
                        'population': pop_data['population']})
    print('Populating is complete')


# populates fake contacts to contacts.json
# with open('assets/contacts.json', 'w') as f:
#     population_data = pd.read_csv('population_wt_country.csv')
#     datas = population_data.groupby(['country_id'])
#     contacts = {}
#     contacts['admins'] = [{"name": "Bob Smith", "email": "bbb@wfp.mail"}]
#     for index,row in datas:
#         contacts[str(index)] = [{"name": "Jane Ola", "email": "ola@wfp.mail"}]
#     json.dump(contacts,f)