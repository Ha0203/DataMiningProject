from utils import *

argParser = argparse.ArgumentParser(description='Delete Rows Processing')
argParser.add_argument('in', help='input file name')
argParser.add_argument('-p', '--percent', type = float, help='the proportion of missing attribute to all the attributes')
argParser.add_argument('-out', '--out', help='output file name')

args = argParser.parse_args()

input_file = sys.argv[1]
output_file = args.out

df = get_data(input_file)

df = convert_column_types(df)

to_be_remove = []
for i in range(len(df[list(df.keys())[0]])):
    count = 0
    for key in df:
        if df[key][i] is None or df[key][i] == '':
            count += 1
    if ((count/len(df)*100) > args.percent):
        to_be_remove.append(i)

for key in df:
    df[key] = [i for j, i in enumerate(df[key]) if j not in to_be_remove]
    
print("The number of rows has been remove: ", len(to_be_remove))

write_data(df, output_file)

