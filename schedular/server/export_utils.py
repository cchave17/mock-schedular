import pandas as pd

ExcelRead = pd.read_excel("D:\Personal-Projects\mock-schedular\schedular\data\studyplanexcel.xlsx")

data = pd.DataFrame({'Fruits': ['apple', 'pears', 'bannanas', 'tomato']})

datatoexcel = pd.ExcelWriter("../../fromPython.xlsx", engine='xlsxwriter')

data.to_excel(datatoexcel, sheet_name='Sheet1')

datatoexcel.save()


for (columnName, columnData) in ExcelRead.iteritems():
#   for data in columnData.values:
    ExcelRead.dropna(inplace=True)
    print('Column Name : ', columnName)
    print('Column Contents : ', columnData.values)