from utils import *

# ---------  Command line processing --------
argParser = argparse.ArgumentParser(description='Delete Columns Processing')
argParser.add_argument('in', help='input file name')
argParser.add_argument('-columns', '--columns', help='columns you want to check, or leave it empty for checking All the columns', default=[], nargs='*')
argParser.add_argument('-out', '--out', help='output file name')

args = argParser.parse_args()

input_file = sys.argv[1]
output_file = args.out

df = get_data('house-prices.csv')

df = convert_column_types(df)

columns = []
if args.columns == []:
  columns = get_column_names(df)
else: 
  columns = args.columns

del_cols, new_df = delete_cols(df, columns)

print("The columns have been remove: ", del_cols)

write_data(new_df, output_file)

