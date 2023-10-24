from utils import *

def extract_columns_with_missing_value(df):
  n, m = get_shape(df) # n: number of rows, m: number of columns

  column_names = get_column_names(df)

  missing_columns = [] # name of each columns which has missing value

  for i in range(0, m):
    for j in range(0, n):
      if isNaN(df.iloc[j][i]):
        missing_columns.append(column_names[i])
        break


  return missing_columns

data_file_name = sys.argv[1]

df = get_data(data_file_name) 

res = extract_columns_with_missing_value(df)

print("Number of Columns with missing value:", len(res))

print(res)
