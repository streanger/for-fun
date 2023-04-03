import os
import re
import time
from itertools import count
from collections import namedtuple

import chime
import selenium
from rich import print
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

Result = namedtuple('Result', ('distance', 'location_name', 'location', 'is_open', 'name', 'info'))

"""
info:
    https://chromedriver.chromium.org/downloads

requirements:
    pip install selenium rich chime

"""

def script_path():
    """set current path, to script path"""
    current_path = os.path.realpath(os.path.dirname(__file__))
    os.chdir(current_path)
    return current_path


def create_driver(driver_path, headless):
    """create driver object with config"""
    
    # ****** driver setup ******
    service = Service(driver_path)
    options = selenium.webdriver.ChromeOptions()
    if headless:
        options.add_argument('--headless')
    options.add_argument("--incognito")
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--log-level=3')
    options.add_argument('--start-maximized')
    
    # ****** prevent detection ******
    options.add_argument('--disable-blink-features')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option('excludeSwitches', ['enable-logging', 'enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)
    driver = selenium.webdriver.Chrome(service=service, options=options)
    return driver


def parse_distance(full_text):
    text = full_text.splitlines()[0]
    distance = re.findall("(\d+(?:\.\d+)?)", text)
    if not distance:
        print('    [yellow]\[x] distance not found')
        return False
    
    if text.endswith('km'):
        distance = float(distance[0])
    elif text.endswith(' m'):
        distance = float(distance[0])/1000
    else:
        print('    [yellow]\[x] unknown distance: {}'.format(text))
        return False
    return distance


def check_medicine_presence(address_query, medicine_query, max_distance, headless=False):
    # driver setup
    driver = create_driver(driver_path=r'chromedriver.exe', headless=headless)
    driver.delete_all_cookies()

    # get url & click popup window
    url = 'https://ktomalek.pl/#0'
    driver.get(url)

    # accept cookies
    accept_cookies_button = driver.find_element(by='id', value='btnCookiesAll')
    accept_cookies_button.click()

    # address entry
    search_address_entry = driver.find_element(by='id', value='searchAdresu')
    search_address_entry.send_keys(address_query)
    search_address_entry.send_keys(Keys.RETURN)

    # medicine entry
    medicine_entry = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.ID, "search")))
    medicine_entry.send_keys(medicine_query)
    medicine_entry.send_keys(Keys.RETURN)

    # find distance
    try:
        distance_container = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CLASS_NAME, 'odlegloscDiv')))
    except selenium.common.exceptions.TimeoutException:
        print('    [yellow]\[x] distance not found')
        return False

    not_found_pattern = 'nie znaleźliśmy w okolicy 50 km'
    if distance_container.text == not_found_pattern:
        print('    [yellow]{}'.format(not_found_pattern))
        return False

    # parse distance text
    full_text = distance_container.text
    distance = parse_distance(full_text)

    # set status
    if not distance:
        return False
    print('    distance: {} \[km]'.format(distance))
    if distance <= max_distance:
        return True
    return False


def check_medicine_presence_results(address_query, medicine_query, max_distance, headless=False):
    # driver setup
    driver = create_driver(driver_path=r'chromedriver.exe', headless=headless)
    driver.delete_all_cookies()

    # get url & click popup window
    url = 'https://ktomalek.pl/#0'
    driver.get(url)

    # accept cookies
    accept_cookies_button = driver.find_element(by='id', value='btnCookiesAll')
    accept_cookies_button.click()

    # address entry
    search_address_entry = driver.find_element(by='id', value='searchAdresu')
    search_address_entry.send_keys(address_query)
    search_address_entry.send_keys(Keys.RETURN)

    # medicine entry
    medicine_entry = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.ID, "search")))
    medicine_entry.send_keys(medicine_query)
    medicine_entry.send_keys(Keys.RETURN)

    # find distance
    try:
        distance_container = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CLASS_NAME, 'odlegloscDiv')))
    except selenium.common.exceptions.TimeoutException:
        print('    [yellow]\[x] distance not found')
        return False

    not_found_pattern = 'nie znaleźliśmy w okolicy 50 km'
    if distance_container.text == not_found_pattern:
        print('    [yellow]{}'.format(not_found_pattern))
        return False

    # choose button
    choose_button = driver.find_element(by='class name', value='przechodzenieDoOfert')
    choose_button.click()
    time.sleep(7)

    # get results (locations and distances)
    results_items = driver.find_elements(by='class name', value='results-item')
    results = []
    for item in results_items:
        if not item.text.strip():
            continue
        strings = item.text.splitlines()
        *distance_text, location_name = strings[0].split(None, 2)
        distance_text = ' '.join(distance_text).replace(',', '.')
        distance = parse_distance(distance_text)
        if distance > max_distance:
            # skip this result
            continue
        location = strings[1]
        is_open = strings[3]
        name = strings[4]
        info = strings[5]
        result = Result(distance, location_name, location, is_open, name, info)
        results.append(result)
    return results


def notify():
    """make some notification"""
    print('    [magenta]FOUND!')
    print('    go to: {}'.format('https://ktomalek.pl/#0'))
    chime.theme('material')
    chime.success()


if __name__ == "__main__":
    script_path()
    print('[cyan]\[*] press enter to start', end='')
    input(' ')

    # ****** setup ******
    address_query = 'Białystok, Słowackiego'
    medicine_query = 'Paracetamol Accord'
    exact_location = 'Mickiewicza'
    max_distance = 15  # km
    wait_between = 60  # [s]
    headless = True
    print('[*] looking for:')
    print('    medicine: [cyan]{}'.format(medicine_query))
    print('    address: [cyan]{}'.format(address_query))
    print('    in range: [cyan]{} \[km]'.format(max_distance))
    print()

    # ****** queries ******
    for index in count(1):
        try:
            now = time.strftime('%d.%m %H:%M:%S')
            print('{}) {}'.format(index, now))
            # status = check_medicine_presence(address_query, medicine_query, max_distance, headless)
            results = check_medicine_presence_results(address_query, medicine_query, max_distance, headless)
            status = False
            for result in results:
                if exact_location in result.location:
                    status = True
                    print(result)
                    break
            print('    status: {}'.format(status))
            if status:
                notify()
            time.sleep(wait_between)
            print()
        except KeyboardInterrupt:
            print('    [yellow]\[x] broken by user')
            break
