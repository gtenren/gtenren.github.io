import pandas as pd
import seaborn as sns

def heatmap(df,value, start_date, end_date):
    '''Create heatmap from a timeseries dataframe'''
    
    #create split time into hours and Day of weeks
    df['weekday'] = df.index.weekday
    #weekday_encrypt = pd.Series(['Mon','Tue','Wed','Thu','Fri','Sat','Sun'],index=list(range(0,7)))
    df['hour'] = df.index.hour
    
    #convert dataframe into input of heatmap
    hm_input = pd.pivot_table(df.loc[start_date:end_date],index = 'hour', columns = 'weekday', values = value)
    hm_input.columns = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
    
    #create the heatmap
    sns.heatmap(hm_input)
