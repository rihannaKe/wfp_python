import csv
import requests    
import json   
import pandas as pd


populaton_url = "https://api.hungermapdata.org/swe-notifications/population.csv" 

def getCountry(region_id):
    response = requests.get("https://api.hungermapdata.org/swe-notifications/region/" +str(region_id)+ "/country")
    countries = json.loads(response.text)
    return countries

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