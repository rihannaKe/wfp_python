import schedule  
import time       
import requests     
import json         
import pandas as pd
import email_utility 
 
FOOD_SECURITY_URL = "https://api.hungermapdata.org/swe-notifications/foodsecurity"
CONTACT_URL = "assets/contacts.json"


def getFoodSecurity():
    """
    Returns the data fetched from the FOOD_SECURITY_URL
    """
    response = requests.get(FOOD_SECURITY_URL)
    fd_sec_data = json.loads(response.text)
    return fd_sec_data

def getFoodSecurityHistory():
    """
    Returns the data fetched from the FOOD_SECURITY_URL of 30 days ago
    """
    response = requests.get(FOOD_SECURITY_URL+"?days_ago="+str(30))
    fd_sec_data_days_ago = json.loads(response.text)
    return fd_sec_data_days_ago

def getContacts():
    """
    Returns the json data of the contacts list
    """
    with open(CONTACT_URL) as f:
        data = json.load(f) 
    return data

def sendNotification(country_id):
    """
    Sends the notification by calling the the email utiliry send email function
    """
    # get the contacts list
    contacts= getContacts()
    # get recipients of the country
    resps = contacts[str(country_id)]
    # get admins 
    admins = contacts['admins']
    # concatenate admins and recipients
    email_list = admins + resps
    # call notifyByEmail 
    email_utility.notifyByEmail(email_list)
    
def check_fd_decrease(population, fd_sec, fd_sec_30):
    """
    Returns a boolean value based on checking if the percentage of food
    insecure people in a country increased of >= 5% compared to 30 days ago
    """
    fd_decreased = False
    percent_fd_today = 100 * float(fd_sec)/float(population)
    percent_fd_30_days_ago = 100 * float(fd_sec_30)/float(population)
    if( (percent_fd_today - percent_fd_30_days_ago) >=  5 ):
        fd_decreased = True
    return fd_decreased

def the_day_job():
    """
    Gets the data food security data of today and of the 30 days ago and the population
    and uses check_fd_decrease to determine wether to send email notification or not
    """
    # get today's food security data
    fd_today =  getFoodSecurity()
    fd_days_ago = getFoodSecurityHistory()
    # normilize to json
    df1 = pd.json_normalize(fd_today)
    df2 = pd.json_normalize(fd_days_ago)
    # merge dataframse using reuind_id
    res1 = pd.merge(df1, df2, on='region_id', how='outer')
    # get population data 
    pop_data = pd.read_csv("population_wt_country.csv") 
    # merge the food security datas with population
    result = pd.merge(res1, pop_data, on='region_id', how='inner')
   
    # group by datas and aggregate by summing the values
    df_all = result.groupby(['country_id']).agg({'food_insecure_people_x':'sum','food_insecure_people_y':'sum','population':'sum'})

    # iterate to check if food security as decreased and if decresed send email notification
    for i,row in df_all.iterrows():
       if(check_fd_decrease(row['population'], row['food_insecure_people_x'],row['food_insecure_people_y'])):
           # print( check_fd_decrease(row['population'], row['food_insecure_people_x'],row['food_insecure_people_y']))
            sendNotification(i)
   
    
# schedule daily routine and run
schedule.every().day.at("12:54").do(the_day_job)
while True:
    schedule.run_pending()
    time.sleep(1)