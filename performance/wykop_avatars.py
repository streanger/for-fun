#script for downloading wykop.pl avatars
import os
import sys
import shutil
import requests
import bs4 as bs
import lxml
import urllib.parse

def script_path():
    '''change current path to script one'''
    path = os.path.realpath(os.path.dirname(sys.argv[0]))
    os.chdir(path)  #it seems to be quite important
    return path
    
def get_avatar(nick):
    base_url = "https://www.wykop.pl/ludzie/"
    nick_url = urllib.parse.urljoin(base_url, nick)
    content, status = get_content(nick_url)
    if status == 404:
        return ""
    soup = bs.BeautifulSoup(content, 'lxml')
    hrefs = soup.find_all('img', {'title': nick})       #this is useful
    if hrefs:
        avatar_url = hrefs[0]['src']
    else:
        avatar_url = ""
    return avatar_url

def make_dir(new_dir):
    path = os.path.realpath(os.path.dirname(sys.argv[0]))
    os.chdir(path)
    if not os.path.exists(new_dir):
        os.makedirs(new_dir)
    new_path = os.path.join(path, new_dir)
    return new_path
    
def save_avatars(nick_list, subdir):
    new_path = make_dir(subdir)      #create dir if not exists
    paths = {}
    for nick in nick_list:
        avatar_url = get_avatar(nick)
        file_path = os.path.join(new_path, nick + ".png")
        paths[nick] = file_path
        if download_image(avatar_url, file_path):
            print("avatar saved as: {}".format(file_path))
            pass
        else:
            print("failed to download from: '{}' nick: '{}'".format(avatar_url, nick))
            pass
    return paths

def read_file(file_name, rmnl=False):
    try:
        with open(file_name, "r") as file:
            if rmnl:
                fileContent = file.read().splitlines()
            else:
                fileContent = file.readlines()
    except:
        fileContent = []
    return fileContent
    
def get_content(url):
    res = requests.get(url)
    content = res.text
    status = res.status_code
    return content, status

def convert_nick_str_to_list(nick_str):
    nick_str = nick_str.replace("@", " ")
    nick_str = nick_str.replace(",", " ")
    nick_list = [item.strip() for item in nick_str.split() if item]
    to_call = " ".join(["@" + item for item in nick_list])
    return nick_list, to_call   
    
def download_image(url, file_name):
    '''download image from specified url and save it to specified file_name'''
    try:
        response = requests.get(url, stream=True)
        with open(file_name, 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
        return True
    except:
        return False

def usage():
    print("usage:")
    print("     from console:")
    print("         -run script and put nicknames into console window")
    print("     from file:")
    print("         -run script with .txt file with nicnames as argument. Example:")
    print("         python wykop_avatars.py nicnames.txt")
    print("tip: you can put nicnames separeted with spaces, comas and with '@' in front of. It doesn't matter")
    print("--"*20)
    print()
        
        
if __name__ == "__main__":
    path = script_path()
    args = sys.argv[1:]
    if not args:
        usage()
        nick_str = input("put vikop nicnames here:\n")
    else:
        file = args[0]
        try:
            nick_str = " ".join(read_file(file, rmnl=True))
        except:
            nick_str = ""
    nick_list, to_call = convert_nick_str_to_list(nick_str)
    save_avatars(nick_list, 'avatars')
    