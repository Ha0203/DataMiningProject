from utils import *

argParser = argparse.ArgumentParser(description='Performing addition, subtraction, multiplication, and division between two numerical attributes.')
argParser.add_argument('in', help='input file name')
argParser.add_argument('-a1', '--att1', help='attribute 1')
argParser.add_argument('-cal', '--calculation', help='one out of 4 calculation methods: +, -, *, /')
argParser.add_argument('-a2', '--att2', help='attribute 2')
argParser.add_argument('-out', '--out', help='output file name')

cal = ['+', '-', '*', '/']


args = argParser.parse_args()

if(args.calculation not in cal):
    print("Fail! You have inputted an invalid calculation, try: '+', '-', '*', '/'")
    sys.exit()

input_file = sys.argv[1]
output_file = args.out

df = get_data(input_file)

df = convert_column_types(df)

new_att = args.att1 + ' ' + args.calculation + ' ' + args.att2

df[new_att] = []

if (isinstance(df[args.att1][0], (int, float)) and isinstance(df[args.att2][0], (int, float))):
    for i in range(len(df[list(df.keys())[0]])):
        try:
            string = str(df[args.att1][i]) + ' ' + args.calculation + ' ' + str(df[args.att2][i])
            res = eval(string)
            df[new_att].append(res)
        except:
            df[new_att].append(0)
else:
    print("Fail! You have to input 2 numerical attributes")
    sys.exit()

print("Calculate successfully")

write_data(df, output_file)