
import numpy as np 
import pandas as pd

# Showing missing, duplicates, shape, dtypes
def df_summary(df, title):
    print(f"Dataframe ({title}) Summary")
    #print data shape and show if there is duplicated data
    print(f"Shape(col,rows): {df.shape}")
    print(f"Number of duplicates: {df.duplicated().sum()}")
    
    #check data type
    print('---'*20)
    print(f'Number of each unique datatypes:\n{df.dtypes.value_counts()}')
    
    #check for missing data
    print('---'*20)
    print("Columns with missing values:")
    _df_ = df_missing(df)
    if _df_.empty:
        print("--No Missing Data--")
    else:
        print(_df_)
        
    #Check data values
    print('---'*20)
    print("Check Quantitative data values:")
    # Check if the DataFrame contains numerical columns
    if df.select_dtypes(include=['number']).columns.empty:
        print("--No Quantitative feature columns--")
    else:
        min_max_df_ = get_min_max_df(df)
        print(min_max_df_)

    # Check if the DataFrame contains string/object columns
    print('---'*20)
    print("Check Qualitative data values:")
    if df.select_dtypes(include=['object']).columns.empty:
        print("--No Qualitative feature columns--")
    else:
        for col in df.select_dtypes(include=['object']).columns:
            print(f"--Column '{col}' has\n {df[col].nunique()} unique values\n")
    print('---'*20)
    print("\nEnd of Dataframe Summary")


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
