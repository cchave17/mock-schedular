import sys
import os

ENV_PATH = "../.env"

SOURCE_DIRECTORY_PATH = sys.argv[1]

OUTPUT_TYPE = sys.argv[2] if len(sys.argv) >= 3 else 'test'

# Locations of excel files to read in
AUDIT_DEFECT_FILE_PATH = f"{SOURCE_DIRECTORY_PATH}/PreCheckAuditDefect*.xlsx"
DEFECT_RESULT_FILE_PATH = f"{SOURCE_DIRECTORY_PATH}/PreCheckDefectRev*.xlsx"
AUDIT_INSTANCE_FILE_PATH = f"{SOURCE_DIRECTORY_PATH}/Audit_Instances*.xlsx"

TABLE_NAME = 'claim_audit_reports'


def DB_CONNECTION_STRING():
    return f'mysql+pymysql://{os.getenv("DB_USERNAME")}:{os.getenv("DB_USERNAME")}@{os.getenv("DB_HOST")}/{os.getenv("DB_ACTUAL_NAME")}'
