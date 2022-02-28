import sys
import os
import time
import requests
import bs4 as bs
import lxml
import matplotlib.pyplot as plt
from pathlib import Path
from collections import Counter
from nltk.tokenize import RegexpTokenizer  # word_tokenize, TreebankWordTokenizer
from wordcloud import WordCloud, STOPWORDS
from urllib.parse import urlparse


def script_path():
    '''set current path to script_path'''
    current_path = os.path.realpath(os.path.dirname(sys.argv[0]))
    os.chdir(current_path)
    return current_path
    
    
def write_file(filename, text, mode='w'):
    '''write to file'''
    try:
        with open(filename, mode, encoding='utf-8') as f:
            f.write(text)
    except Exception as err:
        print('[x] failed to write to file: {}, err: {}'.format(filename, err))
    return None
    
    
def read_file(filename, mode='r'):
    '''read from file'''
    content = ''
    try:
        with open(filename, mode, encoding='utf-8') as f:
            content = f.read()
    except Exception as err:
        print('[x] failed to read from file: {}, err: {}'.format(filename, err))
    return content
    
    
def website_tokens(response):
    """response - requests response object"""
    # ******** get strings ********
    soup = bs.BeautifulSoup(response.text, 'lxml')
    span_items = [item.text for item in soup.find_all('span')]
    a_items = [item.text for item in soup.find_all('a')]
    b_items = [item.text for item in soup.find_all('b')]
    p_items = [item.text for item in soup.find_all('p')]
    strings_content = span_items + a_items + b_items + p_items
    strings_content = [part for item in strings_content for part in item.splitlines()]
    strings_content = [item.strip() for item in strings_content if item.strip()]
    
    # ******** tokens ********
    text = ' '.join(strings_content)
    tokenizer = RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(text)
    tokens = [item for item in tokens if len(item) > 1]
    return tokens
    
    
def collect_stopwords():
    stopwords_dir = Path('stopwords')
    files = [stopwords_dir.joinpath(item) for item in os.listdir(stopwords_dir) if item.endswith('.txt')]
    stopwords = []
    for filename in files:
        content = [line.strip() for line in read_file(filename).splitlines() if line.strip()]
        stopwords.extend(content)
    stopwords = tuple(sorted(set(stopwords)))
    return stopwords
    
    
def make_wordcloud(tokens, stopwords):
    words = ' '.join(tokens)
    wordcloud = WordCloud(
                    width = 1920,
                    height = 1080,
                    background_color = 'white',
                    stopwords = stopwords,
                    collocations = False,       # it cause words will not occur twice or more
                    mode = "RGBA",
                    max_words = 1000,
                    min_font_size = 10).generate(words)
    return wordcloud
    
    
def show_wordcloud_plot(wordcloud):
    plt.figure(figsize = (8, 8), facecolor = None)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad = 0)
    plt.show()
    return None
    
    
def timestamp_str():
    return time.strftime("%Y%m%d_%H%M%S")
    
    
def domain_name(url):
    """extract domain name from url"""
    domain = urlparse(url).netloc
    return domain
    
    
if __name__ == "__main__":
    script_path()
    
    # ******** tokens from website ********
    url = 'https://www.telemagazyn.pl/'
    response = requests.get(url)
    tokens = website_tokens(response)
    print('[*] tokens numer: {}'.format(len(tokens)))
    
    # ******** unique ********
    # unique_words = sorted(list(set(tokens)))
    # unique_words_count = Counter(tokens)
    
    
    # ******* wordcloud *******
    # stopwords = set(STOPWORDS)
    stopwords = list(collect_stopwords())
    stopwords.extend([])  # add stopwords here
    
    wordcloud = make_wordcloud(tokens, stopwords)
    wordcloud_file = '{}_{}.png'.format(domain_name(url), timestamp_str())
    wordcloud.to_file(wordcloud_file)
    print('[*] image saved to file: {}'.format(wordcloud_file))
    
    
    # ******* show plot *******
    # show_wordcloud_plot(wordcloud)
    
    
"""
https://stackoverflow.com/questions/44203397/python-requests-get-returns-improperly-decoded-text-instead-of-utf-8
https://www.kite.com/python/answers/how-to-remove-all-punctuation-marks-with-nltk-in-python
https://stackoverflow.com/questions/44113335/extract-domain-from-url-in-python

todo:
    -add time to filename  (+)
    -add domain name to filename  (+)
"""
