from utils import *

argParser = argparse.ArgumentParser(description="Count the number of lines with missing data")

argParser.add_argument('in', help='input file name')
argParser.add_argument('-c', '--col_name', help='The column name on which to count line with missing data or leave it empty to check missing data for all the columns', default=[], nargs='*')

args = argParser.parse_args()
input_file = sys.argv[1]
df = get_data(input_file) 

df = convert_column_types(df)

cols = []
if args.col_name == []:
  cols = get_column_names(df)
  args.col_name = "All the columns"
else: 
  cols = args.col_name

ress = []

for col in cols:
    ress.append(get_number_of_missing_values(df[col]))
res = max(ress)

print(f'The number of lines with missing data in {args.col_name}: {res}')