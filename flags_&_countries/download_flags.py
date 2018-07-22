#!/usr/bin/python3
import os
import sys
import shutil   #download_image
import requests #download_image
import re

def download_flags():
    flagsUrl = "https://www.nationsonline.org/flags/"
    urls = ["https://www.nationsonline.org/oneworld/flags_of_africa.htm",
            "https://www.nationsonline.org/oneworld/flags_of_the_americas.htm",
            "https://www.nationsonline.org/oneworld/flags_of_asia.htm",
            "https://www.nationsonline.org/oneworld/flags_of_australia_oceania.htm",
            "https://www.nationsonline.org/oneworld/flags_of_europe.htm"]
    gifs = []
    for url in urls:
        res = requests.get(url)
        content = res.text
        gifs.extend(re.findall(r'[\w]+flag.gif', content))
        #status = res.status_code
    gifs = list(set(gifs))
    countries = [item[:-9].lower() for item in gifs]
    countries.sort()        #in place

    #write countries to .txt
    path = script_path()
    simple_write("countries.txt", "\n".join(countries))
    
    #write gifs to flags dir
    gifsDir = "flags"
    if not os.path.exists(gifsDir):
        os.makedirs(gifsDir)
    path = os.path.join(path, gifsDir)
    for gif in gifs:
        gifUrl = flagsUrl + gif
        gifPath = os.path.join(path, gif)
        print(gifUrl)
        download_image(gifUrl, gifPath)
    return gifs, countries

def download_image(url, fileName="image.png"):
    try:
        response = requests.get(url, stream=True)
        with open(fileName, 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
    except:
        pass
    del response
    return True

def simple_write(file, strContent):
    with open(file, "w") as f:
        f.write(strContent + "\n")
        f.close()
    return True  
    
def script_path(fileName=''):
    path = os.path.realpath(os.path.dirname(sys.argv[0]))
    os.chdir(path)  #it seems to be quite important
    if fileName:
        fullPath = os.path.join(path, fileName)
        return fullPath
    return path
    
if __name__ == "__main__":
    download_flags()