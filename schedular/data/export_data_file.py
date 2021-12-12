import pandas as pd

data = pd.DataFrame({'Fruits': ['apple', 'pears', 'bannanas', 'tomato']})

datatoexcel = pd.ExcelWriter("fromPython.xlsx", engine='xlsxwriter')

data.to_excel(datatoexcel, sheet_name='Sheet1')

datatoexcel.save()
