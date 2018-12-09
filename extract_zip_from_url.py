''' 
-reading zip file from url, and extracting it to current dir 
-just the modyfication of someones script
-could be useful
'''
import os
import sys
import urllib.request
import zipfile
import io


if __name__ == "__main__":
    path = os.path.realpath(os.path.dirname(sys.argv[0]))
    os.chdir(path)

    rok = ['2017', '2018']
    miesiac = ['01', '02', '03', '04', '05']

    for i in rok:
        for j in miesiac:
            resp = urllib.request.urlopen('https://dane.imgw.pl/data/dane_pomiarowo_obserwacyjne/dane_meteorologiczne/dobowe/klimat/'+i+'/'+i+'_'+j+'_k.zip')
            file = zipfile.ZipFile(io.BytesIO(resp.read()))
            file.extractall('.')
