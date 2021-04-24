from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
import time
import requests
from bs4 import BeautifulSoup as bs
import csv
import re

# Login to AllTrails
def login (driver, user_email, user_password):
    driver.get(f'https://www.alltrails.com/login')
    # Enter email and password
    email = driver.find_element_by_name('userEmail')
    email.send_keys(user_email)
    password = driver.find_element_by_name('userPassword')
    password.send_keys(user_password)
    password.send_keys(Keys.RETURN)
    time.sleep(5)

#get page for use with beautiful soup
def get_search_page(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}
    try:
        page = requests.get(url, headers = headers)
        page.raise_for_status()
    except Exception:
        raise requests.HTTPError(Exception)
    if page.status_code == 200:
        return page
    else:
        return -1

# Get links to Florida State Parks (uses selenium)
def get_trail_links (driver, trails_url, n):
    time.sleep(1)
    driver.get(trails_url)
    wait = WebDriverWait(driver, 5000)
    wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class,'row trail-row')]/div/div[3]")))
    driver.find_element_by_xpath("//div[contains(@class,'row trail-row')]/div/div[3]").click()
    wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='tracks']/div[1]/div[1]/div[2]/div[1]/div[1]/h4/a[2]")))

# Load all recordings
    page_count = 0
    while page_count < n:
        wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@title='Show more recordings']")))
        time.sleep(10)
        driver.find_element_by_xpath("//button[@title='Show more recordings']").click()
        page_count += 1

    recordings = driver.find_elements_by_xpath("//*[@id='tracks']/div/div/div/div/div/h4/a[2]")
    urls = []
    for record in recordings:
        url = record.get_attribute('href')
        urls.append(url)
        with open (r'C:\Users\aschi\Google Drive\Research\Paper2\Parks\AllTrails\SPlinks1.csv','a') as f:
            f.writelines(url)
    return urls

def get_trail_info(url, trail_no):
    # Get basic stats from page using beautiful soup
    try:
        results = get_search_page(url)
    except:
        print('Failed to get page ' + url + ' retrying...')
        results = get_search_page(url)
    soup = bs(results.content,'html.parser')
    trip_id = trail_no
    trail_name = soup.find('h1').text.strip()
    park_name = soup.find(class_='styles-module__content___1eARw').a.text
    user = soup.find(class_='clickable').get('title')
    try:
        sport = soup.find(class_='styles-module__tag___2s-oD').text
    except:
        sport = 'Unspecified'
    date = soup.find(class_='styles-module__date___1DvYf').text
    dist = soup.find(class_='total-distance').text.split('e')[1].split()[0]
    elevGain = soup.find(class_='elevation-gain').text.split('n')[2].split()[0]
    moving_time = soup.find(class_='moving-time').text.split('e')[1]
    avg_pace = soup.find(class_='avg-speed').text.split('e')[1]
    calories = soup.find(class_='calories').text.split('s')[1]
    total_time = soup.find(class_='total-time').text.split('e')[1]
    start_lat = soup.find(property = 'place:location:latitude').get('content')
    start_lon = soup.find(property = 'place:location:longitude').get('content')
    link = soup.find(property = 'og:url').get('content')

    trail_stats = [trip_id, trail_name, park_name, user, sport, date, dist, elevGain, moving_time, avg_pace, calories, total_time, start_lat,start_lon, link]

    with open(r"C:/Users/aschi/Google Drive/Research/Paper2/Parks/AllTrails/AllTrailsStats1.csv", 'a', encoding="utf-8", newline='') as csvfile:
        writer = csv.writer(csvfile, dialect='excel')
        writer.writerow(trail_stats)
    csvfile.close()

def main():
    pass
    driver = webdriver.Chrome()
    trails_url = 'https://www.alltrails.com/us/florida/state-parks'
    number_of_pages = 2  #Enter here the number of search result pages (at 30 pp)
    urls = get_trail_links(driver, trails_url, number_of_pages)
    driver.close()
   #for url in urls:
        # get_trail_info(url)
 #   url = 'https://www.alltrails.com/explore/recording/little-manatee-river-green-and-red-trails-loop-closed-07bb5fd'
    with open (r'C:\Users\aschi\Google Drive\Research\Paper2\Parks\AllTrails\SPlinks1.csv','r') as r:
        reader = csv.DictReader(r)
        trail_no = 0
        for row in reader:
            url = row['url']
            trail_no += 1
            get_trail_info(url, trail_no)
            print('Processed trail ' + str(trail_no))

if __name__ == '__main__':
    main()