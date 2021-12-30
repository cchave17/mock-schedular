"""
Helper methods for parsing and cleaning data
"""
import glob
import pandas as pd
import numpy as np
from artificial_intelligence.schedular.config import AUDIT_DEFECT_FILE_PATH, DEFECT_RESULT_FILE_PATH, \
    AUDIT_INSTANCE_FILE_PATH


def read_xlxs(path):
    """
    Get sql alchemy engine and create connection to mysql db
    :param path: string path to file to upload
    :return: dataframe of source excel file
    """
    # Using glob which return a list, use first item in list
    return pd.ExcelFile(glob.glob(path)[0]).parse("Data")


def get_audit_defect():
    """
    Read in audit defect excel and clean
    :return: excel one dataframe
    """

    ad_xl = read_xlxs(AUDIT_DEFECT_FILE_PATH)
    # There are duplicates in here, drop duplicates
    ad_df = ad_xl.drop_duplicates()
    # Need to rename field as currently incorrect name
    ad_df = ad_df.rename(columns={"case Status": "defect_case_status"})
    return ad_df


def get_defect_result():
    """
    Read in defect results excel and clean
    :return: defect results dataframe
    """
    dr_xl = read_xlxs(DEFECT_RESULT_FILE_PATH)

    # want the most recent time occrance per defect handle
    dr_df = dr_xl.sort_values('Create Date/Time').groupby('Defect Handle').first()

    # there are some negative values in this column, take absolute value
    dr_df['Overpayment/Underpayment Amount'] = dr_df['Overpayment/Underpayment Amount'].abs()
    return dr_df


def get_audit_instances():
    """
    Read in audit instances excel and clean
    :return:  file 3 dataframe
    """
    ai_xl = read_xlxs(AUDIT_INSTANCE_FILE_PATH)
    # Need to rename field as currently incorrect name
    ai_xl = ai_xl.rename(columns={"Case Status": "audit_case_status"})

    return ai_xl


def get_claim_history(sql_engine):
    """
    Read in
    :param sql_engine:
    :return:
    """
    return pd.read_sql("SELECT 'requests'.*, 'sample_queries'.'queryname', 'claim_history'.'Claim_Number', "
                       "'claim_history'.'division_number', 'claim_history'.'total_amount_paid', "
                       "'claim_history'.'total_billed_amount'"
                       "FROM requests",
                       "INNER JOIN responses ON 'requests'.'requestId' = 'responses'.'requestId'"
                       "INNER JOIN response_items ON 'responses'.'responseId' = 'response_items'.'responseId'"
                       "INNER JOIN sample_queries ON requests.queryID = sample_queries.queryID"
                       "INNER JOIN claim_history ON"
                       "'response_items'.'Claim_History_ID' = 'claim_history'.'Claim_History_ID';", sql_engine)


def clean_final_df(final_df):
    """
    Clean the dataframe before write out to csv or db
    :param final_df: dataframe to clean
    :return: cleaned dat
    """
    # Clean column names (replace space with '_')
    final_df.columns = final_df.columns.str.replace(' ', '_')
    # Clean column names (replace '/' with '_')
    final_df.columns = final_df.columns.str.replace('/', '_')
    # Clean column names lowercase all characters
    final_df.columns = final_df.columns.str.lower()

    # rename columns
    final_df = final_df.rename(columns={"instance_handle_key_y": "defect_handl_key",
                                        "instance_handle_key_x": "instance_handle_key",
                                        "sample_date_(audit_create_date)": "sample_date"})

    # Get rid of NaNs, and NaTs
    # df1 = final_df.where(final_df.notnull(), None)
    # We have two columns for claim number, remove one of them
    final_df = final_df.drop(columns=['claim_identifier'])
    final_df = final_df.replace({np.nan: None})

    # sort results by date and give each row id
    final_df = final_df.sort_values(by=['sample_date'], ascending=True).reset_index(drop=True)
    final_df.index += 1
    final_df.index(0, 'report_id', final_df.index)

    return final_df
