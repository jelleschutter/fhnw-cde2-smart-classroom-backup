import getopt
import sys
import pandas as pd
from helper import get_opts, ensure_dir
import cx_Oracle

opts = get_opts()

ensure_dir('./data/measurements')

print('Connecting to DB...')

connection = cx_Oracle.connect(opts['username'], opts['password'], f"tcps://{opts['hostname']}:{opts['port']}/{opts['service']}?wallet_location=./secrets/Oracle_Wallet&retry_count=20&retry_delay=3")

print('Connected to DB.')

print('Loading sensors...')

sensors = pd.read_sql('SELECT * FROM sensor_meta_infos', connection)

print('Finished loading sensors.')

print('Saving sensors to CSV...')

sensors.to_csv('./data/sensors.csv', index=False)

print('Sensors saved to CSV.')

print('Loading measurements...')

measurements = pd.read_sql('SELECT * FROM sensor_measurements', connection)

print('Finished loading measurements.')

print('Saving measurements to CSV...')

measurements['day'] = pd.to_datetime(measurements['INSERT_TIMESTAMP']).dt.floor('d')

for name, group in measurements.groupby('day'):
    date = name.date()
    group.drop('day', axis=1).to_csv('./data/measurements/{}.csv'.format(date), index=False)
    print('Saved measurements for {} to CSV.'.format(date))

print('All measurements saved to CSV.')