"""
Driver method to join all source data and upsert to db or write out to csv
"""
from dotenv import load_dotenv
from artificial_intelligence.schedular.helpers.db_helpers import mysql_connection, upsert_database
from artificial_intelligence.schedular.helpers.parse_helpers import get_audit_defect, get_defect_result, \
    get_audit_instances, get_claim_history, clean_final_df
from artificial_intelligence.schedular.config import OUTPUT_TYPE, SOURCE_DIRECTORY_PATH, TABLE_NAME


def update():
    """
    Driver method to join all source data and upsert to db or write out to csv
    """

    # AUDIT DEFECT
    print("AD")
    ad_df = get_audit_defect()

    # Defect Results
    print("DR")
    dr_df = get_defect_result()

    # Join first two tables
    print("1st JOIN.....")
    join_df = ad_df.merge(dr_df, on=['Defect Handle'], how='inner')

    print("AI")
    # Audit Instance
    ai_df = get_audit_instances()

    all_cvs_df = ai_df.merge(join_df, left_on=['Instance Handle Key'], right_on=['Audit Handle'], \
                             how='left')

    # Create SQL connection
    sql_engine = mysql_connection()

    print("CH")
    # GET CLAIM_HISTORY
    mysql_df = get_claim_history(sql_engine)

    print("2nd JOIN.....")
    final_df = all_cvs_df.merge(mysql_df, left_on=['Claim identifier'], right_on=['Claim_number'], \
                                how='left')
    # Clean column names
    final_df = clean_final_df(final_df)

    # Write to CSV
    if OUTPUT_TYPE == 'csv':
        print("Writing CSV to" + f"{SOURCE_DIRECTORY_PATH}/claim_status_report.csv")
        final_df.to_csv(f"{SOURCE_DIRECTORY_PATH}/claim_status_report.csv", index=False)
    elif OUTPUT_TYPE == 'db':
        print("UPSERTING TO DB....")
        upsert_database(final_df, sql_engine, TABLE_NAME)
    elif OUTPUT_TYPE == 'all' or OUTPUT_TYPE == 'both':
        print("Writing CSV to" + f"{SOURCE_DIRECTORY_PATH}/claim_status_report.csv")
        final_df.to_csv(f"{SOURCE_DIRECTORY_PATH}/claim_status_report.csv", index=False)
        print("UPSERTING TO DB....")
        upsert_database(final_df, sql_engine, TABLE_NAME)
    else:
        print("Output Nothing. csv or db was not included as argument in run command")
    print("DONE")
