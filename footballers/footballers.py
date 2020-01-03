import sys
import os
import requests
import bs4 as bs
import lxml
import pandas as pd


def script_path():
    current_path = os.path.realpath(os.path.dirname(sys.argv[0]))
    os.chdir(current_path)
    return current_path
    
    
def get_footballers():
    url = 'https://pl.wikipedia.org/wiki/Reprezentanci_Polski_w_piłce_nożnej_mężczyzn'
    res = requests.get(url)
    soup = bs.BeautifulSoup(res.text, 'lxml')
    tables = soup.find_all('table', {'class': 'wikitable sortable'})
    main_table = tables[0]
    tr_list = main_table.find_all('tr')
    
    
    # ************** get header **************
    header = [item.text.strip() for item in tr_list[0].find_all('th')]
    header = header[:-1] + [header[-1] + '01', header[-1] + '02']           # split last element into two
    
    
    # ************** get data **************
    data = [item.find_all('td') for item in tr_list[1:]]
    data = [[value.text.strip() for value in item] for item in data]
    
    
    # ************** create data frame **************
    df = pd.DataFrame(data)
    df.columns = header
    return df
    
    
if __name__ == "__main__":
    script_path()
    df = get_footballers()
    df.to_csv('file.csv', index=False)
