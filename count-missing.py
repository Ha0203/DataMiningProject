from utils import *

argParser = argparse.ArgumentParser(description="Count the number of lines with missing data")

argParser.add_argument('in', help='input file name')
argParser.add_argument('-c', '--col_name', help='The column name on which to count line with missing data')

args = argParser.parse_args()
input_file = sys.argv[1]
df = get_data(input_file) 

df = convert_column_types(df)

res = get_number_of_missing_values(df[args.col_name])

print(f'The number of lines with missing data in {args.col_name}: {res}')