import glob
import pandas as pd
import json

data_list = []

for file_name in glob.iglob('raw-data/trimmed_latlng/*.json', recursive=True):
    with open(file_name, 'r', encoding='utf-8') as f:
        data = json.loads(f.read())
    data_list += data

df = pd.DataFrame(data_list)
df = df.drop_duplicates(subset=['id'], keep='first')
selected_province_list = ['กรุงเทพมหานคร']
df = df[df.province.isin(selected_province_list)]
df.to_csv('7-11bangkok_data.csv', index=False)