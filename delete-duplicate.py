from utils import *

argParser = argparse.ArgumentParser(description='Delete Duplicate Samples')
argParser.add_argument('in', help='input file name')
argParser.add_argument('-out', '--out', help='output file name')

args = argParser.parse_args()

input_file = sys.argv[1]
output_file = args.out

df = get_data(input_file)

df = convert_column_types(df)

count = 0
for i in range(len(df[list(df.keys())[0]])):
    to_be_remove = []
    for j in range(i + 1, len(df[list(df.keys())[0]])):
        row_i = []
        row_j = []
        for key in df:
            row_i.append(df[key][i])
            row_j.append(df[key][j])
        if(row_i == row_j):
            to_be_remove.append(j)
    count += len(to_be_remove)
    for key in df:
        df[key] = [i for j, i in enumerate(df[key]) if j not in to_be_remove]

print("The number of rows has been remove: ", count)

write_data(df, output_file)