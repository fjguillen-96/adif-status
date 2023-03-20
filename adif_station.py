import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

class AdifStatus:
    
    def __init__(self):
        # Get the path of the current file
        self.current_path = os.path.dirname(os.path.abspath(__file__))
        
        # Open the 'station_db.txt' file in read-write mode
        with open(self.current_path + '\\station_db.txt', 'a+') as f:
            # Move the read pointer to the beginning of the file
            f.seek(0)
            # Read all the lines of the file
            list_station = f.readlines()
            
            # If there are no stations saved in the file, exit the function
            if len(list_station) == 0:
                return None
            
            # If there are stations saved, initialize the lists to store the names and urls of the stations
            self.list_names = []
            self.list_url = []
            
            # Loop through all the lines of the file
            for line in list_station:
                # Split the name and url of the station
                name, url = line.split()
                # Add the name and url to the corresponding lists
                self.list_names.append(name)
                self.list_url.append(url)
                
    def get_df(self, name):
        # Find the position of the station name in the names list
        try:
            idx = self.list_names.index(name)
            url = self.list_url[idx]
        except:
            # If the station name is not found, exit the function
            return None
                
        # Define the headers for the request
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
        }
        # Make the request to the station url
        r = requests.get(url, headers=headers)
        c = r.content
        # Use BeautifulSoup to parse the content of the response
        soup = BeautifulSoup(c, 'lxml')
        # Find all tables with class "adif-table"
        t_arrival = soup.find_all('table', class_="adif-table")

        # Create an empty DataFrame with the necessary columns
        df = pd.DataFrame({
            'Hora': pd.Series(dtype='str'),
            'Destination': pd.Series(dtype='str'),
            'Line': pd.Series(dtype='str'),
            'Via': pd.Series(dtype='str')
        })
        
        # Find all cells in the second table
        table_td = t_arrival[1].find_all('td')

        # Loop through all cells in the table in groups of four
        for i in range(0, len(table_td), 4):
            # Get the information for each column
            sub_tab_1 = table_td[i]
            sub_tab_2 = table_td[i+1]
            sub_tab_3 = table_td[i+2]
            sub_tab_4 = table_td[i+3]
            
            time = sub_tab_1.find_all('span')[0]
            time = time.text
            if len(time) == 0:
                time = '0 min'

            dest = sub_tab_2.text.replace('\n', '')

            line = sub_tab_3.find_all('span')[-1]
            line = line.text

            via = sub_tab_4.find_all('span')[0]
            via = via.text

            cur_dict = {'Hora': time,
                        'Destination': dest,
                        'Line': line,
                        'Via': via}
            df_dictionary = pd.DataFrame([cur_dict])
            df = pd.concat([df, df_dictionary], ignore_index=True)
        return df
    
    def add_station(self, name, url):
        try:
            # Check if this station already exists
            self.list_names.index(name)
            self.list_url.index(url)
            return 0
        except:
            url_2 = url.split('.es')
            try:
                # Check if the url belongs to adif website
                if url_2[0].split('www.')[1] != 'adif':
                    return 1
                with open(self.current_path+'\\station_db.txt', 'a+') as f:
                    # Append the new station to the file
                    f.write(f'{name} {url}\n')
                    f.close()
                return 2
            except:
                return 1

    def update_db(self):
        with open(self.current_path+'\\station_db.txt', 'a+') as f:
            # Move the read pointer to the beginning of the file
            f.seek(0)
            # Read all the lines of the file
            list_station = f.readlines()
            self.list_names = []
            self.list_url = []
            # Loop through all the lines of the file
            for line in list_station:
                # Split the name and url of the station
                name, url = line.split()
                # Add the name and url to the corresponding lists
                self.list_names.append(name)
                self.list_url.append(url)

if __name__ == "__main__":
    adif = AdifStatus()
    station_name = input('Enter the name of the station: ')
    df = adif.get_df(station_name)
    if df is None:
        print('Invalid station name or station not found in database')
        option = input('Do you want to add this station to the database? (y/n)')
        if option.lower() == 'y':
            station_url = input('Enter the url of the station: ')
            res = adif.add_station(station_name, station_url)
            adif.update_db()
        if res == 0:
            print('This station already exists in the database')
        elif res == 1:
            print('Invalid station url')
        elif res == 2:
            print('Station added to database')
    else:
        print(df)
        