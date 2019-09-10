#This script downloads metadata about specified tickers from Tiingo. You can get an API key on the tiingo website.

from tiingo import TiingoClient

config = {}
API_KEY = "your api key"
config['api_key'] = API_KEY
SMIF_health_tickers = ['BMY','PFE','UNH']

client = TiingoClient(config)

SMIF_health_metadata = {}

for i in range (0,len(SMIF_health_tickers)):
    ticker_metadata = client.get_ticker_metadata(SMIF_health_tickers[i])
    SMIF_health_metadata[str(SMIF_health_tickers[i])] = ticker_metadata
SMIF_health_metadata
