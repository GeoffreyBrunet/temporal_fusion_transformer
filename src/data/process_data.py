import numpy as np
import pandas as pd


def sort_data(path: str) -> pd.DataFrame:
    data = pd.read_csv(path, index_col=0, sep=';', decimal=',')
    data.index = pd.to_datetime(data.index)
    data.sort_index(inplace=True)
    return data


def aggregate_hourly_data(df: pd.DataFrame) -> pd.DataFrame:
    data = data.resample('1h').mean().replace(0., np.nan)
    earliest_time = data.index.min()
    df = data[['MT_002', 'MT_004', 'MT_005', 'MT_006', 'MT_008']]
    return df, earliest_time


def create_new_features(df, earliest_time) -> pd.DataFrame:
    df_list = []
    for label in df:
        ts = df[label]
        start_date = min(ts.fillna(method='ffill').dropna().index)
        end_date = max(ts.fillna(method='bfill').dropna().index)
        active_range = (ts.index >= start_date) & (ts.index <= end_date)
        ts = ts[active_range].fillna(0.)
        tmp = pd.DataFrame({'power_usage': ts})
        date = tmp.index
        tmp['hours_from_start'] = (
            date - earliest_time).seconds / 60 / 60 + (date - earliest_time).days * 24
        tmp['hours_from_start'] = tmp['hours_from_start'].astype('int')
        tmp['days_from_start'] = (date - earliest_time).days
        tmp['date'] = date
        tmp['consumer_id'] = label
        tmp['hour'] = date.hour
        tmp['day'] = date.day
        tmp['day_of_week'] = date.dayofweek
        tmp['month'] = date.month
        # stack all time series vertically
        df_list.append(tmp)

    time_df = pd.concat(df_list).reset_index(drop=True)

    # match results in the original paper
    time_df = time_df[(time_df['days_from_start'] >= 1096)
                      & (time_df['days_from_start'] < 1346)].copy()
    
    return time_df


def generate_data(path: str) -> pd.DataFrame:
    df = sort_data(path)
    df, earliest_time = aggregate_hourly_data(df)
    df = create_new_features(df, earliest_time)
    return df
