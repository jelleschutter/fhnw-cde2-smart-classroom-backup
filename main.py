import pandas as pd
import getopt
import sys
from helper import get_all_items, get_opts, ensure_dir

opts = get_opts()

ensure_dir('./data/measurements')

print('Loading sensors...')

sensors = get_all_items(opts['endpoint'] + '/sensors', auth=(opts['username'], opts['password']))

print('Finished loading sensors.')

print('Saving sensors to CSV...')

sensors_df = pd.DataFrame(sensors)
sensors_df.to_csv('./data/sensors.csv', index=False)

print('Sensors saved to CSV.')

print('Loading measurements...')

measurements = get_all_items(opts['endpoint'] + '/measurements', auth=(opts['username'], opts['password']))

print('Finished loading measurements.')

print('Saving measurements to CSV...')

data_df = pd.DataFrame(measurements)
data_df['day'] = pd.to_datetime(data_df['insert_timestamp']).dt.floor('d')

for name, group in data_df.groupby('day'):
    date = name.date()
    group.drop('day',axis=1).to_csv('./data/measurements/{}.csv'.format(date), index=False)
    print('Saved measurements for {} to CSV.'.format(date))

print('All measurements saved to CSV.')