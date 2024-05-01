import mysql.connector
import argparse
import json
import os
import pandas
import requests
import urllib
import uszipcode
import csv
import os
import requests
import json

# Define the API Key, Endpoint, and Header
API_KEY = ''
ENDPOINT = "https://api.yelp.com/v3/businesses/search?"
HEADERS = {'Authorization': 'bearer %s' % API_KEY}

# Define the parameters for the 'black-owned' search
PARAMETERS_BLACK_OWNED = {
    'term': 'black-owned', 
    'limit': 50,
    'radius': 1000, 
    'location': 'Baltimore'
}

# Define the parameters for the 'african' search
PARAMETERS_AFRICAN = {
    'term': 'african', 
    'limit': 50,
    'radius': 1000, 
    'location': 'Baltimore'
}

# Define the parameters for the 'haitian' search
PARAMETERS_HAITIAN = {
    'term': 'haitian', 
    'limit': 50,
    'radius': 1000, 
    'location': 'Baltimore'
}

def search_businesses(params):
    offset = 0
    total_results = float('inf')
    results_per_page = 50
    all_businesses = []

    while offset < total_results:
        params['offset'] = offset
        response = requests.get(url=ENDPOINT, params=params, headers=HEADERS)
        business_data = response.json()

        if 'businesses' in business_data:
            all_businesses.extend(business_data['businesses'])
            total_results = business_data['total']
            offset += results_per_page
        else:
            print("Error: Unable to find 'businesses' in the response data.")
            print("Response from Yelp API:")
            print(business_data)
            break

    return all_businesses

# Perform separate searches for 'black-owned' and 'african' businesses and 'haitian' businesses
black_owned_businesses = search_businesses(PARAMETERS_BLACK_OWNED)
african_businesses = search_businesses(PARAMETERS_AFRICAN)
haitian_businesses = search_businesses(PARAMETERS_HAITIAN)

# Combine the results
all_businesses = black_owned_businesses + african_businesses + haitian_businesses

# Write response to a txt file
filename1 = 'black_results.txt'
with open(filename1, 'w') as f:
    f.write(json.dumps(all_businesses, indent=3))
print(f'Data has been written to {filename1}')

# Write data to a csv file
filename2 = 'black_results.csv'
with open(filename2, 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)

    if all_businesses:
        # Write the header row
        csvwriter.writerow(all_businesses[0].keys())
        # Write the data rows
        for business in all_businesses:
            csvwriter.writerow(business.values())
        print(f'Data has been written to {filename2}')
    else:
        print("No businesses found in the response data.")
