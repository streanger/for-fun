'''script for wykop voting, by nyxesis'''
import time
import re
import lxml
import requests
import bs4 as bs


def main(login, password, url='', manual_mode=True):
    '''
    parameters:
        login       -wykop login
        password    -wykop password
        url         -link to wykop post; if not specified reads from user
        manual_mode -True/False auto or manual vote mode
    '''
    
    login_url = 'https://www.wykop.pl/zaloguj/?fEr[0]=YmVmYmh0dHBzOi8vd3d3Lnd5a29wLnBsLw%3D%3D'
    
    with requests.session() as s:
        # ****** log in into wykop ******
        payload = {
            'user[username]': login,
            'user[password]': password,
            }
        res = s.post(login_url, data=payload)
        
        if res.text.find('Niepoprawne') > -1:
            print('[*] failed to log in')
            return False
            
            
        # ****** get hash value ******
        hash_line = [line for line in res.text.splitlines() if 'hash   :' in line][0]
        hash_val = hash_line.split(':')[1].strip(' ",')
        
        
        # ****** get url for vote loop ******
        while True:
            if url:
                vote_url = url
            else:
                vote_url = input('>>> url for vote: ')      # ask for post id, to be upvoted
                
                if not vote_url.strip():
                    continue
                    
            try:
                id = re.findall(r'\d+', vote_url)[0]    # get id value
            except IndexError:
                print('[*] incorrect url. Put direct url to wykop post')
                continue
                
            vote_up_url = 'https://www.wykop.pl/ajax2/wpis/voteUp/{}/hash/{}/'.format(id, hash_val)
            
            try:
                # ****** vote loop ******
                counter = 0
                while True:
                    try:
                        res = s.post(vote_up_url)
                        
                    except requests.exceptions.SSLError:
                        print('\n[*] too many requests')
                        if not manual_mode:
                            time.sleep(3)
                        continue
                        
                    if res.status_code == 200:
                        soup = bs.BeautifulSoup(res.text, 'lxml')
                        
                        try:
                            votes = [item.strip('\\t \\n') for item in soup.strings][-3]
                        except IndexError:
                            continue
                            
                        counter += 1
                        if manual_mode:
                            input('>>> id: {}, counter: {}, votes: {}, next? '.format(id, counter, votes))
                        else:
                            print('>>> id: {}, counter: {}, votes: {}'.format(id, counter, votes))
                    else:
                        print('\n[*] wrong response from server: {}'.format(res.status_code))
                        
                    if not manual_mode:
                        # time.sleep(0.66)  # OK
                        time.sleep(0.5)  # OK
                        
            except KeyboardInterrupt:
                # when ctrl-c, just ask again
                print()
    return None
    
    
if __name__ == "__main__":
    # INFO: pass url directly -> no input message; empty url -> wait for input message to provide url
    login, password = 'your_login', 'your_password'
    url = ''    # leave empty or put some wykop post url
    main(login, password, url, manual_mode=False)
