from utils import *

df, output_file, _, columns = set_up_cmd(method = False)

del_cols, new_df = delete_cols(df, columns)

print("The columns have been remove: ", del_cols)
write_data(new_df, output_file)

