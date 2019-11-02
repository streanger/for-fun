import os
import sys
import shutil
import requests
import bs4 as bs
import lxml
import urllib.parse


def script_path():
    '''change current path to script one'''
    current_path = os.path.realpath(os.path.dirname(sys.argv[0]))
    os.chdir(current_path)
    return current_path
    
    
def read_file(file):
    data = []
    with open(file, 'r') as f:
        data = f.read().splitlines()
    return data
    
    
def get_content(url):
    res = requests.get(url)
    content = res.text
    status = res.status_code
    return content, status
    
    
def get_avatar(nick):
    '''
    info:
        https://www.youtube.com/channel/ + channel
        https://www.youtube.com/user/ + user
    '''
    if nick.startswith('https://www.youtube.com/'):
        nick_url = nick
    else:
        base_url = "https://www.youtube.com/"
        nick_url = urllib.parse.urljoin(base_url, nick)
    content, status = get_content(nick_url)
    if status == 404:
        return '', ''
    soup = bs.BeautifulSoup(content, 'lxml')
    hrefs = soup.find_all('img', {'class': "channel-header-profile-image"})
    if hrefs:
        avatar_url = hrefs[0]['src']
        true_nick = hrefs[0]['alt']
    else:
        avatar_url = ''
        true_nick = nick
    return avatar_url, true_nick
    
    
def make_dir(new_dir):
    path = os.path.realpath(os.path.dirname(sys.argv[0]))
    os.chdir(path)
    if not os.path.exists(new_dir):
        os.makedirs(new_dir)
    new_path = os.path.join(path, new_dir)
    return new_path
    
    
def download_image(url, file_name):
    '''download image from specified url and save it to specified file_name'''
    try:
        response = requests.get(url, stream=True)
        with open(file_name, 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
        return True
    except:
        return False
        
        
def save_avatars(urls_list):
    new_path = make_dir('avatars')
    for url in urls_list:
        avatar_url, nick = get_avatar(url)
        avatar_url = avatar_url.replace('s100', 's288')     # large image
        if not avatar_url:
            print('cant find url for nick: {}'.format(nick))
            continue
        file_path = os.path.join(new_path, nick + ".jpg")
        if download_image(avatar_url, file_path):
            print("avatar of <{}> saved as: {}".format(nick, file_path))
        else:
            print("failed to download from: '{}' nick: '{}'".format(avatar_url, nick))
    return True
    
    
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
    script_path()
    urls_list = ['https://www.youtube.com/channel/UCLA_DiR1FfKNvjuUpBHmylQ',
                 'https://www.youtube.com/channel/UCSxl6dMdu9pIDkFU6RMSFpg',
                 ]
    # save_avatars(urls_list)   # handling some errors
    
    
    for url in urls_list:
        status = simple_download_avatar(url, 'avatars')
        print('{}: {}'.format(url, status))
        
        