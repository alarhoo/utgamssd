import os, requests
import pandas as pd
import traceback, logging

def exer_a(source = os.getcwd()):
    # prints the list of files inside given directory
    
    # Arguments
    # 1. source: the full-path of a directory, assigns current directory if omitted.
    
    try:
        for root, dirs, files in os.walk(source, topdown=True):
            for f in files:
                print(f)
    except Exception as e:
        logging.error(e)

def exer_b(interval = 0.25):
    # modify the lon & lat in below URL with 0.25 interval
    
    # Arguments
    # 1. interval: a number to be added to lon & lat value; default is 0.25.
    # Returns
    # 1. List of URLs with different intervals
    
    lon = -95.3698
    lat = 29.7604
    urls = []
    for x in range(5):
        lon += interval
        lat += interval
        url = 'http://www.7timer.info/bin/api.pl?lon=' + str(lon) + '&lat=' + str(lat) + '&product=astro&output=json'
        urls.append(url)
        print(url)
    return urls
        
def exer_c():
    # get the URL requests response and store it in a list of JSON
    # Returns:
    # A dictionary of data from DataFrame
    
    # get the list of URLs
    urls = exer_b()
    
    response_list = [] # empty list to contain JSON values of weather result-set
    for url in urls:
        res = requests.get(url) # perfrom HTTP GET call on given URL
        response_list.append(res.json()) # convert the HTPP response into JSON & store it in the list
    
    # print timepoint, cloudcover, temperature, wind speed and direction
    
    # collecting data in dataframe structure to create a file out of it
    df_data = {
        'timepoint': [],
        'cloudcover': [],
        'temperature': [],
        'wind direction': [],
        'wind speed': []
    }
    for res in response_list:
        dataseries = res['dataseries']
        for data in dataseries:
            # populating data for DataFrame object
            df_data['timepoint'].append(data['timepoint'])
            df_data['cloudcover'].append(data['cloudcover'])
            df_data['temperature'].append(data['temp2m'])
            df_data['wind direction'].append(data['wind10m']['direction'])
            df_data['wind speed'].append(data['wind10m']['speed'])
            
            print('timepoint: ' + str(data['timepoint']))
            print('cloudcover: ' + str(data['cloudcover']))
            print('temperature: ' + str(data['temp2m']))
            print('wind direction: ' + data['wind10m']['direction'])
            print('wind speed: ' + str(data['wind10m']['speed']))
    return df_data

def exer_d():
    # create an excel file from the data collected in excercise C
    
    try:
        df_data = exer_c()
        df = pd.DataFrame(df_data)
        writer = pd.ExcelWriter('7timer.xlsx', engine='xlsxwriter')
        df.to_excel(writer, sheet_name='7timer', index=False, header=True)
        writer.save()
    except Exception as e:
        logging.error(e)

def exer_e():
    # Read the files to dataframe - family, family_literature_reference
    try:
        family = pd.read_csv('family.csv')
        family_literature_reference = pd.read_csv('family_literature_reference.csv')
        new_df = pd.merge(family, family_literature_reference, on='rfam_acc', how='left')
        filt = new_df['description'].str.contains('oronavirus')
        
        # Display all pmid, description, where description contains "oronavirus"
        print('Display all pmid, description, where description contains "oronavirus"')
        print(new_df.loc[filt, ['pmid', 'description']])
        
        # Display count of pmid (literature references) using aggfunc=len for each description
        print('Display count of pmid (literature references) using aggfunc=len for each description')
        print(pd.pivot_table(new_df, columns='description', aggfunc=len))
    except Exception as e:
        logging.error(e)
    
def main():
    while True:
        print('\n\nWelcome, ' + os.getlogin()) 
        print('Choose an option to perform listed exercises.') 
        print('******************** PYTHON EXERCISES ********************')
        print('A. working with os module')
        print('B. working with loop')
        print('C. working with request module')
        print('D. working with pandas module')
        print('E. working with dataframe operations')
        print('Any other key to End or Exit or Stop')
        print('**********************************************************')
        
        option = input()
        
        if option in ['A', 'a']:
            exer_a()
        elif option in ['B', 'b']:
            exer_b()
        elif option in ['C', 'c']:
            exer_c()
        elif option in ['D', 'd']:
            exer_d()
        elif option in ['E', 'e']:
            exer_e()
        else:
            print('Program Terminated')
            break

if __name__ == "__main__":
    main()