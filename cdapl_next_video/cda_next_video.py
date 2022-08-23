from itertools import count
import lxml
import requests
from rich import print
from bs4 import BeautifulSoup as bs

url = 'https://www.cda.pl/video/91345787'
base_url = 'https://www.cda.pl'
collected_data = []
for x in count(1):
    try:
        print(x)
        response = requests.get(url)
        soup = bs(response.text, "lxml")
        next_video = soup.find('div', {'class': "media-show-body"})
        next_video_href = next_video.a['href']
        next_video_text = next_video.a.text
        next_video_url = base_url + next_video_href
        # print('{} -> {}'.format(next_video_url, next_video_text))
        collected_data.append((next_video_url, next_video_text))
        url = next_video_url
    except KeyboardInterrupt:
        print('[red]\[x] broken by user')
        break
        
    except Exception as err:
        print('[red]\[x] error catched: {}'.format(err))
        break
        
        
collected_data_str = '\n'.join(['{}: {} -> {}'.format(58+index, url, text) for index, (url, text) in enumerate(collected_data)])
print(collected_data_str)
