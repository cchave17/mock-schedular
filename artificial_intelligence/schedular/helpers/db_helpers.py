"""
All things Database related
"""

import os
from dotenv.main import load_dotenv
from sqlalchemy import Table
# from sqlalchemy.engine.base import Engine as sql_engine
from sqlalchemy.dialects.mysql import insert
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine
from artificial_intelligence.schedular.config import DB_CONNECTION_STRING


def upsert_database(list_input, engine, table):
    """
    take a dataframe and upsert it into mysql DB
    :param list_input: dataframe to insert
    :param engine: mysql connection
    :param table: string name of table to insert to
    :return: None
    """
    if len(list_input) == 0:
        # if df is empty return
        return None

    # flattend out rows in databrame, as in put each row in dict
    flattened_input = list_input.to_dict('records')
    with engine.connect() as conn:
        # Create object model of database
        base = automap_base()
        base.prepare(engine, reflect=True)

        # # Get info about table
        target_table = Table(table, base.metadata,
                             autoload=True, autoload_with=engine)

        # print(target_table.columns)
        # #Group together in 1000 for faster inserts
        chunks = [flattened_input[i:i + 1000] for i in range(0, len(flattened_input), 1000)]
        for chunk in chunks:
            # Generate insert statements with values chunked out
            stmt = insert(target_table).values(chunk)

            # If duplicate occurs update fields beside primary key
            conn.execute(stmt.on_duplicate_key_update(
                line_of_business=stmt.inserted.line_of_business,
                claim_platform=stmt.inserted.claim_platform,
                functional_area=stmt.inserted.functional_area,
                audit_program_title=stmt.inserted.audit_program_title,
                audit_type=stmt.inserted.audit_type,
                sample_date=stmt.inserted.sample_date,
                case_id=stmt.inserted.case_id,
                audit_month=stmt.inserted.audit_month,
                claimtype=stmt.inserted.claimtype,
                claim_total=stmt.inserted.claim_total,
                type_of_service=stmt.inserted.type_of_service,
                provider_contract_scope=stmt.inserted.provider_contract_scope,
                provider_contract_oos_reason=stmt.inserted.provider_contract_oos_reason,
                source_of_truth_availability=stmt.inserted.source_of_truth_availability,
                auditor_name=stmt.inserted.auditor_name,
                audit_case_status=stmt.inserted.audit_case_status,
                audit_close_date=stmt.inserted.audit_close_date,
                audit_handle=stmt.inserted.audit_handle,
                defect_case_status=stmt.inserted.defect_case_status,
                defect_handle=stmt.inserted.defect_handle,
                defect_validator=stmt.inserted.defect_validator,
                full_name=stmt.inserted.full_name,
                root_cause_level_1=stmt.inserted.root_cause_level_1,
                root_cause_level_2=stmt.inserted.root_cause_level_2,
                root_cause_level_3=stmt.inserted.root_cause_level_3,
                root_cause_level_4=stmt.inserted.root_cause_level_4,
                root_cause_level_5=stmt.inserted.root_cause_level_5,
                financial_procedural=stmt.inserted.financial_procedural,
                validation_workgroup=stmt.inserted.validation_workgroup,
                responsible_id=stmt.inserted.responsible_id,
                error_description=stmt.inserted.error_description,
                defect_validation_outcome=stmt.inserted.defect_validation_outcome,
                defect_validation_comments=stmt.inserted.defect_validation_comments,
                defect_handle_key=stmt.inserted.defect_handle_key,
                create_date_time=stmt.inserted.create_date_time,
                needs_correction=stmt.inserted.needs_correction,
                overpayment_underpayment_amount=stmt.inserted.overpayment_underpayment_amount,
                overpayment_underpayment=stmt.inserted.overpayment_underpayment,
                requestid=stmt.inserted.requestid,
                requesttimestamp=stmt.inserted.requesttimestamp,
                samplecounttype=stmt.inserted.samplecounttype,
                fixedcount=stmt.inserted.fixedcount,
                queryid=stmt.inserted.queryid,
                queryname=stmt.inserted.queryname,
                claim_number=stmt.inserted.claim_number,
                division_number=stmt.inserted.division_number,
                total_amount_paid=stmt.inserted.total_amount_paid,
                total_billed_amount=stmt.inserted.total_billed_amount,
                status='U'
            ))
        return None


def mysql_connection():
    """
    get sql alchemy engine and create connection to mysql db
    :return: sql connection
    """

    sql_engine = create_engine(DB_CONNECTION_STRING(), POOL_RECYCLE=3600)
    return sql_engine.connect()
