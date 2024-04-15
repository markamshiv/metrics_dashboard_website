import pandas as pd
import datetime
# from datetime import datetime
snp_file = r"C:/Users/markp/OneDrive/Documents/Projects/github/metrics_dashboard_website/data/snp_kaggle/sp500_index.csv"
company_file = r"C:\Users\markp\OneDrive\Documents\Projects\github\metrics_dashboard_website\data\snp_kaggle\sp500_stocks.csv"

company_info_file = r"C:\Users\markp\OneDrive\Documents\Projects\github\metrics_dashboard_website\data\snp_kaggle\sp500_companies.csv"


# p0 s&p 500 chart
df_snp = pd.read_csv(snp_file)
df_company = pd.read_csv(company_file)
df_company_info = pd.read_csv(company_info_file)


def snp_daily_data(start, end):
    """
    Retrieves the daily data for the S&P500 index within the specified date range.

    Parameters:
    start (str): The start date in the format 'YYYY-MM-DD'.
    end (str): The end date in the format 'YYYY-MM-DD'.

    Returns:
    pandas.DataFrame: A DataFrame containing the daily data for the S&P500 index within the specified date range.
    """

    df_temp = df_snp[(df_snp.Date>=start) & (df_snp.Date<=end)].copy()
    df_temp['Price'] = df_temp['S&P500']
    df_temp = df_temp.drop(columns=['S&P500'])
    return df_temp
 
def company_daily_data(company, start, end):
    """
    Retrieves the daily data for a specific company within a given date range.

    Parameters:
    company (str): The symbol of the company.
    start (str): The start date in the format 'YYYY-MM-DD'.
    end (str): The end date in the format 'YYYY-MM-DD'.

    Returns:
    pandas.DataFrame: A DataFrame containing the daily data for the specified company within the given date range.
    """

    df_temp = df_company[(df_company.Symbol==company) & (df_company.Date>=start) & (df_company.Date<=end)]
    df_temp['Price'] = df_temp['Close']
    return df_temp

def all_company_daily_data(start, end):
    """
    Retrieves the daily data for all companies within a specified date range.

    Parameters:
    start (str): The start date in the format 'YYYY-MM-DD'.
    end (str): The end date in the format 'YYYY-MM-DD'.

    Returns:
    pandas.DataFrame: A DataFrame containing the daily data for all companies within the specified date range.
    """
    df_temp = df_company[(df_company.Date>=start) & (df_company.Date<=end)]
    df_temp['Price'] = df_temp['Close']
    return df_temp

def get_company_information(company_list):
    """
    Retrieves information about a company or a list of companies from the df_company_info DataFrame.

    Parameters:
    - company_list (str or list): A string representing a single company symbol or a list of company symbols.

    Returns:
    - DataFrame: A DataFrame containing the information of the specified company or companies.

    Raises:
    - ValueError: If the company_list variable has an invalid value.
    """

    if (type(company_list) == str) and company_list=='All':
        return df_company_info
    
    if (type(company_list) == str) and (company_list in df_company_info.Symbol):
        return df_company_info[df_company_info.Symbol==company_list]
    
    if type(company_list) == list:
        return df_company_info[df_company_info.Symbol.isin(company_list)]

    raise ValueError('company_list variable has wrong value')

# snp_daily_data('2024-04-08', '2024-04-15')

# p1 #and magnificent 7 data pull

# p2 #realtime data
# from finazon_grpc_python.time_series_service import TimeSeriesService, GetTimeSeriesRequest
# from finazon_grpc_python.common.errors import FinazonGrpcRequestError


# service = TimeSeriesService('your_api_key')
