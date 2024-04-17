import pandas as pd
import datetime

import dataUtilities

def get_default_start_date():
    start = datetime.date.today() - datetime.timedelta(days=7)
    start = start.strftime( '%Y-%m-%d')
    return start

def get_n_previos_date(n,end_date=None):
    if end_date is None:
        start = datetime.date.today() - datetime.timedelta(days=n)
    else:
        end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
        start = end_date - datetime.timedelta(days=n)
        
    start = start.strftime( '%Y-%m-%d')
    return start

def get_default_end_date():
    end = datetime.date.today()
    end = end.strftime( '%Y-%m-%d')
    return end


def get_snp_daily_data(start, end):
    """
    Retrieves the daily data for SNP (Standard & Poor's 500) index within the specified date range.

    Parameters:
    start (str): Start date in the format 'YYYY-MM-DD'.
    end (str): End date in the format 'YYYY-MM-DD'.

    Returns:
    pandas.DataFrame: DataFrame containing the SNP daily data within the specified date range.
    """
    # Retrieve the daily data for SNP (Standard & Poor's 500) index within the specified date range
    df = dataUtilities.snp_daily_data(start, end)
    df = df.sort_values('Date', ascending=False)

    # Get the minimum and maximum dates in the DataFrame
    start_date = df.Date.min()
    end_date = df.Date.max()

    # Get the price on the start date and end date
    start_date_price = df[df.Date == start_date].Price.values[0]
    end_date_price = df[df.Date == end_date].Price.values[0]

    # Calculate the percentage change in price
    percentage_change = 100 * (end_date_price - start_date_price) / start_date_price

    # Add a column for normalized price
    df['normalized_price'] = 100 * (df['Price'] - start_date_price) / start_date_price

    df['percentage_change'] = percentage_change

    return df



def get_biggest_movers(start, num_companys=3, type='gainers'):
    
    """
    Retrieves the biggest movers in terms of percentage change between the start and end dates.

    Parameters:
    - start (str): The start date in the format 'YYYY-MM-DD'.
    - num_companys (int): The number of companies to retrieve. Default is 3.
    - type (str): The type of movers to retrieve. Options are 'gainers' (default) or 'losers'.

    Returns:
    - DataFrame: A DataFrame containing the symbol, start price, end price, change, and percentage change
      for the biggest movers.

    Example usage:
    >>> get_biggest_movers('2022-01-01', num_companys=5, type='losers')
    """

    end = datetime.date.today()
    end = end.strftime('%Y-%m-%d')

    if start > end:
        raise ValueError('The start date cannot be greater than the end date.')

    df_company = dataUtilities.all_company_daily_data(start, end)
    
    #from the data we have to get the start and end date of the company
    start_date = df_company.Date.min()
    end_date = df_company.Date.max()

    #calculate the percentage change
    df_company_start_end_data = df_company[df_company.Date.isin([start_date,end_date])]
    df_company_start_end_data = df_company_start_end_data.pivot(index='Symbol', columns='Date', values='Price')
    df_company_start_end_data = df_company_start_end_data.reset_index()
    df_company_start_end_data['Change'] = df_company_start_end_data[end_date] - df_company_start_end_data[start_date]
    df_company_start_end_data['percentage_change'] = 100*df_company_start_end_data['Change'] / df_company_start_end_data[start_date]

    if type == 'losers':
        df_company_start_end_data = df_company_start_end_data.sort_values('percentage_change', ascending=True)
    else:
        df_company_start_end_data = df_company_start_end_data.sort_values('percentage_change', ascending=False)
    
    #take the top n companies
    df_company_start_end_data = df_company_start_end_data.head(num_companys)
    
    #get percentage change into the main dataframe
    df_company_start_end_data = df_company_start_end_data[["Symbol", start_date, 'percentage_change']]
    df_company_start_end_data = df_company_start_end_data.drop_duplicates(subset=['Symbol'])
    df_company = df_company.merge(df_company_start_end_data, on='Symbol')
    
    #calculate the normalized price using the start date price
    df_company['normallized_price'] = 100*(df_company['Price'] - df_company[start_date]) / df_company[start_date]

    #add company name
    df_company_info = dataUtilities.get_company_information('All')
    df_company_info['company'] = df_company_info["Longname"]
    df_company = df_company.merge(df_company_info[['Symbol', 'company']], on='Symbol')

    return df_company


