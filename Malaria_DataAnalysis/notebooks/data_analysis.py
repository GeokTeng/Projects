
import numpy as np 
import pandas as pd

# Showing missing, duplicates, shape, dtypes
def df_summary(df, title):
    print('---'*5 + f"DATAFRAME SUMMARY OF: {title}" + '---'*5)
    #print data shape and show if there is duplicated data  
    print(f"SHAPE(col,rows): {df.shape}\n")
    print('DUPLICATES')
    print(f"Number of duplicates: {df.duplicated().sum()}")
    
    #check data type
    print('\nDATA TYPE')
    print(df.dtypes)
    
    #check for missing data
    print('\nMISSING DATA')
    print("Columns with missing values:")
    _df_ = df_missing(df)
    if _df_.empty:
        print("--No Missing Data--")
    else:
        print(_df_)

    #check for Data Values
        print('\nDATA VALUES: Quantitative data')
    # Check if the DataFrame contains numerical columns
    if df.select_dtypes(include=['number']).columns.empty:
        print("--No Quantitative feature columns--")
    else:
        min_max_df_ = get_min_max_df(df)
        print(min_max_df_)

    # Check if the DataFrame contains string/object columns
    print('\nDATA VALUES: Qualitative data')
    if df.select_dtypes(include=['object']).columns.empty:
        print("--No Qualitative feature columns--")
    else:
        for col in df.select_dtypes(include=['object']).columns:
            print(f"--Column '{col}' has\n {df[col].nunique()} unique values\n")
    print('---'*5 + f"END OF DATA SUMMARY OF {title}" + '---'*5)


# Showing min and max values of each column
def get_min_max_df(df):
    if isinstance(df, pd.Series):
        df = pd.DataFrame(df)
    
    min_max_list = []
    _df = df.select_dtypes(exclude=['object'])
    for col in _df.columns:
        min_val = df[col].min()
        max_val = df[col].max()
        min_max_list.append([col, min_val, max_val])
    min_max_df = pd.DataFrame(min_max_list, columns=['Column Name', 'Minimum Value', 'Maximum Value'])
    return min_max_df

# Gives a dataframe showing summary of the columns with missing values
def df_missing(df):
    if isinstance(df, pd.Series):
        df = pd.DataFrame(df)
    
    isnull_df = pd.DataFrame(df.isnull().sum()).reset_index()
    isnull_df.columns = ['col','num_nulls']
    isnull_df['perc_null'] = ((isnull_df['num_nulls'])/(len(df))).round(2)
    isnull_df = isnull_df[isnull_df['num_nulls']>0]
    isnull_df.reset_index(drop=True, inplace=True)
    
    return isnull_df
