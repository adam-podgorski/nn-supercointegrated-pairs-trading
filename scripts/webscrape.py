from bs4 import BeautifulSoup
import pandas as pd
import requests

def ftse_download_symbols(exchange='ftse', number=250):
    exchange = exchange.upper()
    exchange_number = str(number)
    url = 'https://en.wikipedia.org/wiki/{}_{}_Index'.format(
        exchange,
        exchange_number
    )

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    tickers = []
    for row in soup.find('table', {'id': 'constituents'}).tbody.findAll('tr'):
        i = 0
        for col in row.findAll('td'):
            i += 1
            if i % 2 == 0:
                tickers.append(col.text.strip())

    if exchange == 'ftse':
        tickers = [ticker + '.L' for ticker in tickers]
    return tickers

def snp500_download_symbols():
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    tickers = []
    for row in soup.find('table', {'id': 'constituents'}).tbody.findAll('tr'):
        text = row.find('a').get_text()
        tickers.append(text)
    del tickers[0]
    df = pd.DataFrame(index=range(len(tickers)))
    df['Symbols'] = tickers
    df.to_csv(open('data/snp500.csv', 'w'), index=False)

def snp100_download_symbols():
    url = 'https://en.wikipedia.org/wiki/S%26P_100'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    tickers = []
    for row in soup.find('table', {'class': 'wikitable sortable'}).tbody.findAll('tr'):
        for col in row.findAll('td'):
            text = col.get_text().strip()
            tickers.append(text)
            break
    df = pd.DataFrame(index=range(len(tickers)))
    df['Symbols'] = tickers
    df.to_csv(open('data/snp100.csv', 'w'), index=False)

snp100_download_symbols()