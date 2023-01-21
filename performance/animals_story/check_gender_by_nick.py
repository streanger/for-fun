import urllib
import requests
import bs4 as bs

def check_sex(nick):
    base_url = "https://www.wykop.pl/ludzie/"
    nick_url = urllib.parse.urljoin(base_url, nick)
    res = requests.get(nick_url)
    content = res.text
    status = res.status_code
    if status == 404:
        return "male", False
    soup = bs.BeautifulSoup(content, 'lxml')
    hrefs = soup.find_all('meta', {'property': "profile:gender"})
    if not hrefs:
        return "male", False
    gender = hrefs[0]['content']
    return gender, True


if __name__ == "__main__":
    nick = 'someone'
    gender, _ = check_sex(nick)
    print(gender)