# energy_price_predictor
Downloads data about energy prices and predicts future prices.
Downloader module - downloads data from: https://gaz.tge.pl/pl/rdn/tgebase/?
Predictor module - prerddicts prices, adn drawing plots using matplotlib
## To launch you should write:
python3 datacenter.py
## How it Works:
the main function is the run() function:
 
 ```
 def run():
    download_data()
    analyse_data()
```
as you can see it first downloads data from tge and later analyses them.
### Downloading data:
   ```
   def download_data():
    file = open('dane.txt', 'a')
    max_date = get_current_download_date()  # get our current date
    date = get_date()
    if not date:
        date = datetime.datetime.utcnow() - datetime.timedelta(days=60)
    tge = Tge(date)  # creates tge object
    loop(tge, file, max_date)
    file.close()
   ```
 First it opens file to which we are going to save data. 
```get_date()```  -  simply get's the date from the file
```get_current_download_date()``` -  simply gets the date for which it will download
After that we invoke loop method which is going to download data for us:
```
while date >= api.get_date():
        data = api.get_data()
        save_to_file(data, file)
        api.next_day(
```
### Analysing Data:
```def analyse_data():
    analyse = Analysys()  # tworzymy obiekt klasy analysys
    file = open('dane.txt', 'r')
    trans = analyse.get_price_data(file)
    file.close()

    if trans:
        file = open('wyniki.txt', 'w')
        prognose, price_mistake, vol_mistake = analyse.get_prognose(trans)
        save_to_file(prognose, file, price_mistake, vol_mistake, get_current_download_date())
        file.close()
        trans = analyse.get_last_day_trans(trans)
        draw_func(prognose, trans)
    else:
        print("data reading error")
```
First it creates object of ```Analysys``` class , next opens file from which it will get data.
The program counts progonses and possible mistake levels.

## TODO
- Rewrite code in the datacenter
- add modules for functionalities in data_center
- Write some tests
