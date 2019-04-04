# energy_price_predictor
Downloads data about energy prices and predicts future prices.
Downloader module - downloads data from: https://gaz.tge.pl/pl/rdn/tgebase/?
Predictor module - prerddicts prices, adn drawing plots using matplotlib
## To launch you should write:
python3 datacenter.py
## How it Works:
the main function is run() function:
   def run():
     download_data()
     analyse_data()

## TODO
- Rewrite code in the datacenter
- add modules for functionalities in data_center
- Write some tests
