from utils import *

data_file_name = sys.argv[1]

df = get_data(data_file_name) 

df = convert_column_types(df)

res = extract_columns_with_missing_value(df)

print("Number of Columns with missing value:", len(res))

print(res)
