from utils import *

df, _, _, columns, _ = set_up_cmd(output_file=False, method=False)

res = extract_columns_with_missing_value(df)

print("Number of Columns with missing value:", len(res))

print(res)
