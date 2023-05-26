import pandas as pd

def individual_analysis(data):
    df = pd.DataFrame.from_records(data)
    without_time = df[['consumer_style__style', 'amount', 'minus_money', 'placename', 'placewhere']].copy()
    without_time['all_amount'] = without_time['amount'] * without_time['minus_money']
    grouped_df = without_time.groupby('consumer_style__style').sum()
    grouped_df['count'] = without_time.groupby('consumer_style__style').size()
    grouped_df = grouped_df.reset_index()
    grouped_df['ratio'] = round(grouped_df['all_amount'] / grouped_df['all_amount'].sum() * 100, 2)
    analysis_dict = grouped_df.to_dict(orient='list')
    return analysis_dict

def people_analysis(data):
    df = pd.DataFrame.from_records(data)
    without_time = df[['consumer_style__style', 'amount', 'minus_money', 'placename', 'placewhere']].copy()
    without_time['all_amount'] = without_time['amount'] * without_time['minus_money']
    grouped_df = without_time.groupby('consumer_style__style').sum()
    grouped_df['count'] = without_time.groupby('consumer_style__style').size()
    grouped_df = grouped_df.reset_index()
    grouped_df['ratio'] = round(grouped_df['all_amount'] / grouped_df['all_amount'].sum() * 100, 2)
    analysis_dict = grouped_df.to_dict(orient='list')
    return analysis_dict

def report(data):
    df = pd.DataFrame.from_records(data)
    without_time = df[['consumer_style__style', 'amount', 'minus_money', 'placename', 'placewhere']].copy()
    without_time['all_amount'] = without_time['amount'] * without_time['minus_money']
    grouped_df = without_time.groupby('consumer_style__style').sum()
    grouped_df['count'] = without_time.groupby('consumer_style__style').size()
    grouped_df['ratio'] = round(grouped_df['all_amount'] / grouped_df['all_amount'].sum() * 100, 2)
    grouped_df = grouped_df.sort_values('all_amount', ascending=False).head(3)
    grouped_df = grouped_df.reset_index()
    analysis_dict = grouped_df.to_dict(orient='list')
    return analysis_dict