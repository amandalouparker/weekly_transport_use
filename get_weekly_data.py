# script to format opal data into the tsv file weekly format
import pandas as pd
import numpy as np
from sklearn import preprocessing
# Format
# Col 1 = 'day' range 1-7
# Col 2 'hour' range 1-24
# Col 3 'value' 0-100?
df = pd.read_csv('data/time_20160725-31.csv',parse_dates=['date','time'])
# Col 1 = 'day' range 1-7
df_dates = df['date'].copy()
df_dates_1 = df_dates.dt.strftime('%Y-%m-%d')
df_dates_2 = df_dates_1.copy()
df['day'] = df_dates_2.replace(['2016-07-25', '2016-07-26', 
                    '2016-07-27', '2016-07-28', 
                    '2016-07-29', '2016-07-30', 
                    '2016-07-31'],[1, 2, 3, 4, 5, 6, 7]) 
# Col 2 'hour' range 1-24
df['hour'] = df['time'].copy()
 # add numbers for the hour
df_hours = df['time'].copy()
for h in range(0,len(df_hours)):
    df.hour[h] = df_hours[h][0]+df_hours[h][1]
 # Col 3 'value' 0-100?
df = df.fillna(value=0).copy()
min_max_scaler = preprocessing.MinMaxScaler()
val_scaled = min_max_scaler.fit_transform(df['count'])
val_normalized = pd.DataFrame(val_scaled)
df['value'] =  val_normalized*100
# drop hour = 0
df_c = df[df['hour']!='-1']
# Strip data down to day, hour, value and mode
new = df_c[['day', 'hour', 'value', 'mode']].copy()
df_bus = new[new['mode']=='bus'].reindex(index=None).copy()
df_train = new[new['mode']=='train'].reindex(index=None).copy()
df_ferry = new[new['mode']=='ferry'].reindex(index=None).copy()
df_lightrail = new[new['mode']=='lightrail'].reindex(index=None).copy()

bus = df_bus[['day', 'hour', 'value']].copy()
train = df_train[['day', 'hour', 'value']].copy()
ferry = df_ferry[['day', 'hour', 'value']].copy()
lightrail = df_lightrail[['day', 'hour', 'value']].copy()

bus['hour'] = pd.to_numeric(bus['hour'])+1
train['hour'] = pd.to_numeric(train['hour'])+1
ferry['hour'] = pd.to_numeric(ferry['hour'])+1
lightrail['hour'] = pd.to_numeric(lightrail['hour'])+1

new_bus = bus.groupby(['day','hour'], as_index=False).sum()
new_train = train.groupby(['day','hour'], as_index=False).sum()
new_ferry = ferry.groupby(['day','hour'], as_index=False).sum()
new_lightrail = lightrail.groupby(['day','hour'], as_index=False).sum()
# make template from example tsv file
data = pd.read_csv('data/data.tsv', sep='	')
tmpl = data[['day', 'hour']].copy()
# merge template and data
m_bus = pd.merge(tmpl, new_bus, how='left', on=['day', 'hour'])
m_train = pd.merge(tmpl, new_train, how='left', on=['day', 'hour'])
m_ferry = pd.merge(tmpl, new_ferry, how='left', on=['day', 'hour'])
m_lightrail = pd.merge(tmpl, new_lightrail, how='left', on=['day', 'hour'])

f_bus = m_bus.fillna(value=0).copy()
f_train = m_train.fillna(value=0).copy()
f_ferry = m_ferry.fillna(value=0).copy()
f_lightrail = m_lightrail.fillna(value=0).copy()
# save files
f_bus.to_csv('data/opal_bus.tsv',sep='	',index=False)
f_train.to_csv('data/opal_train.tsv',sep='	',index=False)
f_ferry.to_csv('data/opal_ferry.tsv',sep='	',index=False)
f_lightrail.to_csv('data/opal_lightrail.tsv',sep='	',index=False)

