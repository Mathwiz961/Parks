#-------------------------------------------------------------------------------
# Name:        MMF
# Purpose:     Extract route data from MapMyFitness
#
# Author:      A. Schirck-Matthews
#
# Created:     22/02/2020
# Copyright:   (c) aschirck 2020

#-------------------------------------------------------------------------------
import requests
import csv
import json
import os
import time
import psycopg2
# PostgreSQL login info (this can be used to get all trip points for each trip and write to postgreSQL database)
#PG_HOST = os.environ.get('PG_HOST')
#PG_PORT = os.environ.get('PG_PORT')
#PG_DBNAME = 'bike_routing'
#PG_USER = os.environ.get('PG_USER')
#PG_PASS = os.environ.get('PG_PASS')

# MMF key and secret
CLIENT_ID = os.environ.get('MMF_CLIENT_ID')
CLIENT_SECRET = os.environ.get('MMF_CLIENT_SECRET')

def get_Routes(lat, lon, buff):
# Get authentication token from MMF api

    url = 'https://oauth2-api.mapmyapi.com/v7.1/oauth2/access_token/'
    headers = {'Api-Key': CLIENT_ID, 'Content-Type': 'application/x-www-form-urlencoded'}
    data = {'grant_type': 'client_credentials', 'client_id': CLIENT_ID, 'client_secret': CLIENT_SECRET}
    response = requests.post(url, data=data, headers=headers)
    token = response.json()
    Headers = {'api-key': CLIENT_ID, 'authorization': 'Bearer %s' % token['access_token']}

# Find search results

    try:
        page = requests.get('http://api.mapmyfitness.com/v7.1/route/?order_by=-date_created&close_to_location=' + lat +
                            '%2c' + lon + '&search_radius=' + buff + '&minimum_distance=' + str(1000) +
                            '&field_set=detailed&activity_type=11&limit=40', headers = Headers)
        result = json.loads(page.text)
        count = result['total_count']
        print(count)
        url_base ='http://api.mapmyfitness.com'

# Get first page of results

        url= url_base + result['_links']['self'][0]['href']
        search_page = requests.get(url, headers = Headers)
        load = json.loads(search_page.text)
        get_Results(load)

# Get subsequent pages of results
        try:
            while load['_links']['next'][0]['href']!='':
                time.sleep(5)
                url = url_base + load['_links']['next'][0]['href']
                search_page = requests.get(url, headers = Headers)
                load = json.loads(search_page.text)
                get_Results(load)
                print('this worked!')

        except (Exception) as e:
                print(e)
                print(type(e))

    except(Exception) as e:
        print(e)
        print(type(e))


def get_Results (text):
# This function extracts the data from the search page

    try:
        routes= text['_embedded']['routes']

# Go through list of routes and extract the data

        for item in routes:

            item_list = []
            trip_ID = item['_links']['self'][0]['id']
            user_ID = item['_links']['user'][0]['id']
            activity_type = item['_links']['activity_types'][0]['id']
            total_ascent = item['total_ascent']
            total_descent = item['total_descent']
            max_elevation = item['max_elevation']
            min_elevation = item['min_elevation']
            city = item['city']
            state = item['state']
            country = item['country']
            starting_lat = item['starting_location']['coordinates'][1]
            starting_lon = item['starting_location']['coordinates'][0]
            distance = item['distance']
            item_list=[trip_ID, user_ID, activity_type, total_ascent, total_descent, max_elevation, min_elevation, distance, starting_lat, starting_lon, city, state, country]

# Write Route data to CSV file

            with open (r'C:\Users\aschi\Google Drive\Research\Paper2\mmf_stats.csv', 'a', newline = '') as wcsvfile:
                writer = csv.writer(wcsvfile, dialect = 'excel')
                writer.writerow(item_list)
            wcsvfile.close()

# Get trip points for route item and write to postgreSQL database (if needed, was not used for this project)

            # points=item['points']
            #
            # trip_id = trip_ID
            #
            # for point in points:
            #     lat = point['lat']
            #     lon = point['lng']
            #     dist = point['dis']
            #     elev = point['ele']

# Connect to database and insert data
#                 try:
#                     conn = psycopg2.connect(host=PG_HOST, port=PG_PORT, dbname=PG_DBNAME, user=PG_USER, password=PG_PASS)
#                     cur = conn.cursor()
#                     sql ='INSERT INTO mmf_2d (trip_id, dist, elev, geom) values(%s,%s,%s,ST_SetSRID(ST_MakePoint(%s,%s), 4326))'
#                     cur.execute(sql, (str(trip_id), str(dist), str(elev), str(lon), str(lat) ))
#                     conn.commit()
#
#                 except(Exception) as e:
#                     print(e)
#                     print(type(e))
#                     break
#
#     except(Exception) as e:
#         print(e)
#         print(type(e))


def main():
   pass
# Reads the CSV file with the lat/lon of the centroid of each State Park and corresponding buffer to encompass the entire park.
   with open (r'C:/Users/aschi/Google Drive/Research/Paper2/State_Park_Coordinates.csv', 'r') as rcsvfile:
       reader = csv.DictReader(rcsvfile)
       for row in reader:
          try:
              lat = str(row['latitude'])
              lon = str(row['longitude'])
              buff = str(row['buffer'])
          except:
              print 'error reading CSV'

   get_Routes(lat, lon, buff)

if __name__ == '__main__':
    main()