#-------------------------------------------------------------------------------
# Name:        WikiLoc Trail Link Finder
# Purpose:     Find links to trails for various activities on Wikiloc and write links to a CSV file for use with
#               Wikiloc trail scraper.
# Author:      Angie Schirck-Matthews
#
# Created:     23/01/2020
# Copyright:   (c) aschirck 2020

#-------------------------------------------------------------------------------
from bs4 import BeautifulSoup as BS
import re
import config as cfg
import csv
import requests

def get_headers():
    """
    generate headers to use when accessing a url
    :return:
    """
    headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/77.0.3865.120 Safari/537.36'}
    return headers
email = 'youremail'
password = 'yourwikilocpassword'

def get_page(page_url):
    """
    returns an HTML string from page URL
    :param page_url:
    :return: string HTML string
    """
    try:
        page = requests.get(page_url, auth = (email, password), headers=get_headers(), timeout=cfg.PAGE_TIMEOUT)
        page.raise_for_status()
    except Exception:
        raise requests.HTTPError(Exception)

    if page.status_code == 200:
        return page
    else:
        return -1

def main():

    Trail_types = ['mountain-biking', 'hiking', 'cycling', 'walking', 'running', 'kayaking-canoeing']
# at the time of extraction this set how many of each trail type there were in search results, found by manual search
# on the website
    for trail in Trail_types:
        if trail == 'moutain-biking':
            k = 832
        elif trail == 'hiking':
            k = 3340
        elif trail == 'cycling':
            k = 3260
        elif trail == 'walking':
            k = 1020
        elif trail == 'running':
            k= 1700
        else:
            k=2570  #paddle sports

# The loop below reads though all the search results, 20 per page.
        for i in range (0, k, 20):
            j=i+20
            try:
                start = str(i)
                stop = str(j)
                Surl ='https://www.wikiloc.com/trails/'+ trail +'/united-states/florida?act=21&from=' + start +'&to='+ stop
                Search_Page = get_page(Surl)

# Parse the page for links to trails
                soup=BS(Search_Page.content,'html.parser')
                trail_list = soup.find(class_='trail-list')
                trails = trail_list.find_all('h3')

# Extract trail name and link and write to CSV file

                for Trail in trails:
                    name = str(Trail.a.get('title'))
                    link = str(Trail.a.get('href'))
                    trip_id = link.split('-')[-1]

                    with open (r"C:/Users/aschi/Google Drive/Research/Paper2/Parks/Wikiloc/Trail_Links.csv",'a', newline = '', encoding = 'utf-8') as csvfile:
                        writer = csv.writer(csvfile, dialect = 'excel')
                        writer.writerow([trip_id, name, link])

                    csvfile.close()
            except: continue

if __name__ == '__main__':
    main()
