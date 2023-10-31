from utils import *

df, output_file, method, columns, _ = set_up_cmd()

new_df = normalize(df, method, columns)

write_data(new_df, output_file)



