"""script for downloading github avatars"""
import sys
import os
import requests
from pathlib import Path
from termcolor import colored


def save_img(url, path):
    '''save image from specified url, to specified local path'''
    response = requests.get(url)
    if response.status_code != 200:
        return False
    with open(path, 'wb') as f:
        f.write(response.content)
    return True
    
    
if __name__ == "__main__":
    os.system('color')
    os.chdir(str(Path(sys.argv[0]).parent))
    
    # ********* directory & catched *********
    images_directory = Path('images')
    images_directory.mkdir(exist_ok=True)
    already_catched = [item for item in os.listdir(images_directory) if item.endswith('.png')]
    
    # ********* get new *********
    counter = 0
    base_url = 'https://avatars.githubusercontent.com/u/{:09}?v=4'
    while True:
        try:
            counter += 1
            filename = '{:09}.png'.format(counter)
            print('{:09}) {}'.format(counter, filename))
            if filename in already_catched:
                print(colored('    [+] already catched', 'green'))
                continue
            url = base_url.format(counter)
            path = images_directory.joinpath(filename)
            save_img(url, path)
            print(colored('    [+] saved to: {}'.format(path), 'cyan'))
            
        except KeyboardInterrupt:
            print(colored('    [x] broken by user', 'yellow'))
            break
            
        except Exception as err:
            print(colored('    [x] error catched: {}'.format(err), 'yellow'))
            break
            
            