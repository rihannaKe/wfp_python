### To start the app
    - clone this repo
    - run app.py file
!!Note: it is scheduled to run once per day, to quickly check the app set the time at line 93 of app.py
## Below the main files and their content of what is done

### app.py
Contians all the necessary functions in order to accomplish the task that are schedualed to run on daily bases.

### helper_script.py 
Contains helper scripts to call once in while in order facilitate data ritrival and avoid network calls of the same data that over and over again and in particular calls to rest apis to get the parent-child relationship between countries and regions and the population data. Population data is update once a year, instead on fetching it eveytime we can fetch the copy of it enriched with coutry_id column to better organize the data and facilitate the functions called on daily routine.

### email_utility.py
Contains email utility function to use to send the notifications. 

### assets directory    
Contains the following assets:
    message.txt - a text file that contains the messge to send via email 
    contacts.json - a json file that contains the contacts per each country saved using the country_id as key 

### Want to do  
 - Better customized notification message with details of country and decrease values
 - Save fetched contact list to avoid calling multiple time
 - Add descriptive logs 
 - Add unit testing to the code
 
 