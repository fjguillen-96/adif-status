# Adif Status
This Python module allows you to obtain the arrival times of trains at different stations in Spain using the Adif website. The module uses web scraping techniques to extract the relevant information from the website.

## Prerequisites
To use this module, you will need to have the following Python packages installed:

* requests
* BeautifulSoup
* pandas

## Usage
To use this module, you need to create an instance of the AdifStatus class. Once you have created an instance, you can call the get_df method to obtain a DataFrame with the arrival times of trains at a specific station. If the station is not found in the database, you can add it using the add_station method.

```python
from AdifStatus import AdifStatus

# Create an instance of the AdifStatus class
adif = AdifStatus()

# Get the DataFrame with the arrival times for a specific station
df = adif.get_df('Barcelona Sants')

# Print the DataFrame
print(df)

```

## Methods
### `AdifStatus()`

This is the constructor method for the AdifStatus class. It initializes the `list_names` and `list_url` attributes by reading the `station_db.txt` file. If the file is empty, the method returns `None`.

### `get_df(name)`
This method takes a station name as an argument and returns a DataFrame with the arrival times of trains at that station.

### `add_station(name, url)`
This method allows you to add a new station to the `station_db.txt` file. It takes a station name and URL as arguments. If the station is already in the database, the method returns 0. If the URL is not a valid Adif website URL, the method returns 1. If the station is added successfully, the method returns 2.

### `update_db()`
This method updates the `list_names` and `list_url` attributes by reading the `station_db.txt` file.



## Example

```python
from AdifStatus import AdifStatus

# Create an instance of the AdifStatus class
adif = AdifStatus()

# Get the DataFrame with the arrival times for a specific station
station_name = input('Enter the name of the station: ')
df = adif.get_df(station_name)

# If the station is not found in the database, ask the user if they want to add it
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

```