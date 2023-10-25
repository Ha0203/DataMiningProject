from utils import *

input_file, output_file, method, columns = set_up_cmd()

df = get_data(input_file)

df = convert_column_types(df)

new_df = impute(df, columns, method)

write_data(new_df, output_file)
