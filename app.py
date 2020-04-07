   #!/usr/bin/python
import smtplib #par inviare email
import schedule  #per schedulare
import time       #per schedulare
import requests     #per fare la chiamata rest
import json         #per leggere json
import pandas as pd


def getFoodSecurityHistory():
    response = requests.get("https://api.hungermapdata.org/swe-notifications/foodsecurity?days_ago="+str(30))
    fd_sec_data_days_ago = json.loads(response.text)
    return fd_sec_data_days_ago
    
def getFoodSecurity():
    response = requests.get("https://api.hungermapdata.org/swe-notifications/foodsecurity")
    fd_sec_data = json.loads(response.text)
    return fd_sec_data

def sendGmailEmail():
    TO = 'rihanna.ke@gmail.com'
    SUBJECT = 'TEST MAIL'
    TEXT = 'Here is a message from python.'
    # Gmail Sign In
    gmail_sender = 'yourmail@gmail.com'
    gmail_passwd = 'youpwd'

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(gmail_sender, gmail_passwd)

    BODY = '\r\n'.join(['To: %s' % TO,
                        'From: %s' % gmail_sender,
                        'Subject: %s' % SUBJECT,
                        '', TEXT])
    try:
        server.sendmail(gmail_sender, [TO], BODY)
        print ('email sent')
    except:
        print ('error sending mail')
    server.quit()

def job():
    print("I am doing this job!")
    sendGmailEmail()

def checkDecrese():
    print("check decrease")


# schedule.every().day.at("16:38").do(job)
# #schedule.every(20).minutes.do(job)
# while True:
#     schedule.run_pending()
#     time.sleep(1)

# food security decreases significantly in a country 
# (that is, if the percentage of food
# insecure people in a country increases of >= 5% compared to 30 days ago
def check_fd_decrease(population, fd_sec, fd_sec_30):
    fd_decreased = False
    percent_fd_today = 100 * float(fd_sec)/float(population)
    percent_fd_30_days_ago = 100 * float(fd_sec_30)/float(population)
    if( (percent_fd_today - percent_fd_30_days_ago) >=  5 ):
        fd_decreased = True
    return fd_decreased


def the_day_job():
    fd_today =  getFoodSecurity()
    fd_days_ago = getFoodSecurityHistory()
    df1 = pd.json_normalize(fd_today)
    df2 = pd.json_normalize(fd_days_ago)
    res1 = pd.merge(df1, df2, on='region_id', how='outer')
    pop_data = pd.read_csv("population_wt_country.csv") 
    result = pd.merge(res1, pop_data, on='region_id', how='inner')
    # print(result) # fino a qui stampa region, fd_today, fd_days_ago
    df_all = result.groupby(['country_id']).agg({'food_insecure_people_x':'sum','food_insecure_people_y':'sum','population':'sum'})
    # print(df_all) 
    for i,row in df_all.iterrows():
       if(check_fd_decrease(row['population'], row['food_insecure_people_x'],row['food_insecure_people_y'])):
            print( check_fd_decrease(row['population'], row['food_insecure_people_x'],row['food_insecure_people_y']))
            sendGmailEmail()
       

    

the_day_job()
