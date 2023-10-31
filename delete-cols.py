from utils import *

df, output_file, _, columns, percent = set_up_cmd(method = False, percent=True)

del_cols, new_df = delete_cols(df, columns, percent)

print("The columns have been remove: ", del_cols)
write_data(new_df, output_file)

