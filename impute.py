from utils import *

df, output_file, method, columns = set_up_cmd()

new_df = impute(df, columns, method)

write_data(new_df, output_file)
