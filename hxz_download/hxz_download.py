import polars as pl
from polars import col as c
import pandas as pd
import requests
import re
from bs4 import BeautifulSoup
import tempfile
from zipfile import ZipFile
from io import StringIO


base_url = 'https://global-q.org/uploads/1/2/2/6/122679606'

def list_factor_versions():
    return [i for i in range(2019, 2026)]

def list_port_versions():
    return [i for i in range(2021, 2026)]

def list_freq():
    return ['daily', 'weekly', 'weekly_w2w', 'monthly', 'quarterly', 'annual']

def list_themes():
    return ['mom', 'vvg', 'inv', 'prof', 'intan', 'fric']

def doc_dl():
    url = 'https://global-q.org/testingportfolios.html'
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    response = requests.get(url, headers=headers)
    res = []
    if response.status_code == 200:
        source = response.text
        soup = BeautifulSoup(source, 'html.parser')
        for i in soup.find_all('br'):
            i.replace_with('\n')

        text = soup.get_text()
        pattern = r'(\d+)\.\s*(.*?)\s*\("(.+?)"\),\s*(.*?);?(?=\n)'
        matches = re.findall(pattern, text)
        for i in matches:
            res.append((i[1], i[2], i[3].replace('\xa0', ' ')))

    df = pl.DataFrame(res, schema=['short_name', 'signalname', 'full_name'], orient='row')
    return df

def factor_dl(freq, version):
    url = f'{base_url}/q5_factors_{freq}_{version}.csv'
    return pl.read_csv(url)

def port_dl(theme, freq, version):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    url = f'{base_url}/{theme}_{freq}_{version}.zip'
    response = requests.get(url, headers=headers)
    df = pl.DataFrame()
    if response.status_code == 200:
        with tempfile.TemporaryFile() as temp:
            temp.write(response.content)
            with ZipFile(temp) as tempzip:
                file_list = tempzip.namelist()[1:]
                for i in file_list:
                    source = tempzip.open(i).read().decode()
                    data = pd.read_csv(StringIO(source)).pipe(lambda x: pl.from_pandas(x))
                    col_name = data.columns
                    name = [i.replace('rank_', '').lower() for i in col_name if 'rank' in i]
                    col_name = ['port' if 'rank' in i else i for i in col_name]
                    data.columns = col_name
                    data = data.with_columns(pl.lit(name[0]).alias('signalname'))
                    df = pl.concat([df, data])

    return df.select('signalname', pl.exclude('signalname'))

