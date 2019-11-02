'''script for downloading youtube avatars by draxter'''
import sys
import os
import shutil
import requests
import bs4 as bs
import lxml


def simple_download_avatar(url, new_dir):
    try:
        if not os.path.exists(new_dir):
            os.makedirs(new_dir)
        new_path = os.path.join(os.path.realpath(os.path.dirname(sys.argv[0])), new_dir)
        res = requests.get(url)
        content = res.text
        soup = bs.BeautifulSoup(content, 'lxml')
        hrefs = soup.find_all('img', {'class': "channel-header-profile-image"})
        avatar_url = hrefs[0]['src']
        true_nick = hrefs[0]['alt']
        avatar_url = avatar_url.replace('s100', 's288')
        file_path = os.path.join(new_dir, true_nick + ".jpg")
        response = requests.get(avatar_url, stream=True)
        with open(file_path, 'wb') as out:
            shutil.copyfileobj(response.raw, out)
        return True
    except:
        return False
        
        
if __name__ == "__main__":
    os.chdir(os.path.realpath(os.path.dirname(sys.argv[0])))
    urls_list = ['https://www.youtube.com/channel/UCLA_DiR1FfKNvjuUpBHmylQ',
                 'https://www.youtube.com/channel/UCSxl6dMdu9pIDkFU6RMSFpg',
                 ]
                 
    for url in urls_list:
        status = simple_download_avatar(url, 'avatars')
        print('{}: {}'.format(url, status))
