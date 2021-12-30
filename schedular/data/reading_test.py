import pandas as pd

ExcelRead = pd.read_excel("D:\Personal-Projects\mock-schedular\schedular\data\studyplanexcel.xlsx")

for (columnName, columnData) in ExcelRead.iteritems():
#   for data in columnData.values:
    ExcelRead.dropna(inplace=True)
    print('Column Name : ', columnName)
    print('Column Contents : ', columnData.values)