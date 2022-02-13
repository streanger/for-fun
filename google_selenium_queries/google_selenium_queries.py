import sys
import os
import time
import json
import codecs
import selenium
import pandas as pd
import numpy as np
import cv2
from pathlib import Path
from termcolor import colored

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


def script_path():
    '''set current path, to script path'''
    current_path = os.path.realpath(os.path.dirname(sys.argv[0]))
    os.chdir(current_path)
    return current_path
    
    
def write_json(filename, data):
    '''write to json file'''
    with open(filename, 'w') as fp:
        # ensure_ascii -> False/True -> characters/u'type'
        json.dump(data, fp, sort_keys=True, indent=4, ensure_ascii=False)
    return True
    
    
def read_json(filename):
    '''read json file to dict'''
    data = {}
    try:
        with open(filename) as f:
            data = json.load(f)
    except FileNotFoundError:
        pass
    return data
    
    
def create_driver(driver_path, headless):
    '''create driver object with config'''
    
    # ********* driver setup *********
    service = Service(driver_path)
    options = selenium.webdriver.ChromeOptions()
    if headless:
        options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--log-level=3')
    options.add_argument('--start-maximized')
    
    
    # ********* prevent detection *********
    options.add_argument('--disable-blink-features')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option('excludeSwitches', ['enable-logging', 'enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)
    # options.add_argument("window-size=1280,800")
    # options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36")
    driver = selenium.webdriver.Chrome(service=service, options=options)
    print(colored('[+] driver created', 'green'))
    return driver
    
    
def click_agree_button(driver):
    '''click google agree popup'''
    # HACK
    agree_button = driver.find_element(by='xpath', value='//*[@id="L2AGLb"]/div')
    agree_button.click()
    return None
    
    
def show_image(title, image):
    '''
    WINDOW_AUTOSIZE
    WINDOW_FREERATIO
    WINDOW_FULLSCREEN
    WINDOW_GUI_EXPANDED
    WINDOW_GUI_NORMAL
    WINDOW_KEEPRATIO
    WINDOW_NORMAL
    WINDOW_OPENGL
    '''
    cv2.namedWindow(title, cv2.WINDOW_NORMAL)
    cv2.imshow(title, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return True
    
    
def img_from_bytes(bytes_string):
    np_array = np.frombuffer(bytes_string, np.uint8)
    img_np = cv2.imdecode(np_array, cv2.IMREAD_UNCHANGED)
    return img_np
    
    
def bunch_of_not_used_code():
    """
    # ********* find divs by attribute *********
    all_divs = driver.find_elements(by='tag name', value='div')
    presentation_div = [item.get_attribute('role') for item in all_divs]
    
    # ********* screenshot of full window *********
    input('[*] press enter ')
    image_bytes = driver.get_screenshot_as_png()
    full_window_image = img_from_bytes(image_bytes)
    show_image('full_window_image', full_window_image)
    
    # ********* image operations *********
    # query_and_hints_img = np.concatenate([query_entry_img, hints_img], axis=0)
    
    # hints
    hints = hints_view.text.splitlines()    # faster, but wont work with multiline hint
    """
    return None
    
    
if __name__ == "__main__":
    script_path()
    os.system('color')
    input(colored('[*] press enter to start ', 'green'))
    
    # ********* driver setup *********
    driver = create_driver(driver_path=r'chromedriver.exe', headless=False)
    
    # ********* get url & click popup window *********
    url = 'https://www.google.pl/'
    driver.get(url)
    click_agree_button(driver)  # google
    
    # ********* find query entry *********
    query_entry = driver.find_element(by='name', value='q')
    
    # ********* json data *********
    filename = 'google_queries.json'
    data = read_json(filename)
    
    # ********* images directory *********
    images_dir = Path('images')
    images_dir.mkdir(exist_ok=True)
    
    # ********* queries *********
    queries = ['cats are', 'dogs are', 'animals are', 'people are', 'programmers are']
    
    # ********* iteration *********
    print(colored('[*] iteration starts', 'green'))
    for index, query in enumerate(queries):
        try:
            print('{:02}) [*] query: {}'.format(index+1, colored(query, 'cyan')))
            
            # ********* check if data exists *********
            if query in data:
                print(colored('    [*] data exists', 'cyan'))
                continue
                
            # ********* queries & screenshots *********
            query_entry.send_keys(query)
            time.sleep(0.1)
            
            # ********* screenshot of query entry *********
            query_entry_div = driver.find_element(by='class name', value='RNNXgb')
            image_bytes = query_entry_div.screenshot_as_png
            query_entry_img = img_from_bytes(image_bytes)
            # show_image('query_entry_img', query_entry_img)
            
            # ********* hints *********
            hints_view = driver.find_element(by='tag name', value='ul')
            
            # ********* hints text *********
            hints_rows = hints_view.find_elements(by='tag name', value='li')
            hints = [row.text for row in hints_rows]
            print('    [*] hints: {}'.format(colored(hints, 'cyan')))
            
            if hints:
                # ********* screenshot of hints *********
                image_bytes = hints_view.screenshot_as_png
                hints_img = img_from_bytes(image_bytes)
                # show_image('hints_img', hints_img)
                
                # ********* images concatenation *********
                full_image = cv2.vconcat([query_entry_img, hints_img])
            else:
                full_image = query_entry_img
                
            # ********* saving images *********
            img_file = '{}.png'.format(query)
            img_path = str(images_dir.joinpath(img_file))
            cv2.imwrite(img_path, full_image)
            # show_image('full_image', full_image)
            print('    [*] img saved: {}'.format(colored(img_path, 'cyan')))
            
            # ********* update data *********
            subdata = {
                'hints': hints,
                'img_path': img_path,
                }
            data[query] = subdata
            
        except KeyboardInterrupt:
            print(colored('    [x] broken by user', 'yellow'))
            break
            
        except Exception as err:
            print(colored('    [x] error catched: {}'.format(err), 'yellow'))
            break
            
        finally:
            # ********* cleanup *********
            # input('    [*] press enter, to clean query ')
            query_entry.clear()
            print()
            
            
    # ********* update json *********
    write_json(filename, data)
    print('[*] file updated: {}'.format(colored(filename, 'cyan')))
    
    
    # ********* driver cleanup *********
    driver.close()
    driver.quit()
    print(colored('[*] driver closed', 'cyan'))
    
    
"""
https://www.tutorialspoint.com/google-search-automation-with-python-selenium
https://stackoverflow.com/questions/64717302/deprecationwarning-executable-path-has-been-deprecated-selenium-python
https://stackoverflow.com/questions/47392423/python-selenium-devtools-listening-on-ws-127-0-0-1
https://stackoverflow.com/questions/43143014/chrome-is-being-controlled-by-automated-test-software
https://stackoverflow.com/questions/28426645/is-there-a-way-to-find-an-element-by-attributes-in-python-selenium
https://stackoverflow.com/questions/44330084/opencv-imwrite-doesnt-work-because-of-special-character-in-file-path
"""
