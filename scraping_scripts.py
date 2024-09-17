import pandas as pd
import random
import time
import json
import requests

def get_seven_store(lat:float, long:float):
    url = "find from 7-11website"
    payload = {"latitude": lat, "longitude": long}
    headers = {'Accept': 'application/json, text/plain, */*'}
    response = requests.post(url, json=payload, headers=headers) 
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: Received status code {response.status_code}")
        return None

"""Read tambon df and use TA_ID to scrape location based on Thai Tambon"""
selected_province_list = ["กรุงเทพมหานคร"]
tambon_lat_long_df = pd.read_excel('tambon.xlsx')
tambon_lat_long_df = tambon_lat_long_df[tambon_lat_long_df.CHANGWAT_T.isin(selected_province_list)]
tambon_lat_long_df = tambon_lat_long_df[["TA_ID", "TAMBON_T", "LAT", "LONG"]].drop_duplicates(subset='TA_ID', keep="first")
tambon_lat_long_df = tambon_lat_long_df.sort_values(by=['TA_ID']).reset_index()
print(tambon_lat_long_df.head())

RESULT_DIRECTORY = "raw-data"
print("Total api calls:", len(tambon_lat_long_df))
for index, row in tambon_lat_long_df.iterrows():
    print(index, row['TA_ID'], row['TAMBON_T'], row['LAT'], row['LONG'])
    json_data = get_seven_store(row['LAT'], row['LONG'])
    filename = f"{RESULT_DIRECTORY}/by_latlng/{index}_{int(row['TA_ID'])}.json"
    with open(filename, 'w', encoding='utf-8') as outfile: json.dump(json_data, outfile, ensure_ascii=False)
    time.sleep(random.randint(30, 90)) #random sleep time !!! do not flood the API
