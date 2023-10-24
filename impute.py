from utils import *

def impute(df, column_names, method, output_file):
  n, m = df.shape 

  for name in column_names:
    i = df.columns.get_loc(name)
    # for i in range(0, m):
    type = get_column_type(df, i)

    if not missing_value(df, i) or column_with_no_value(df, i):
      continue

    if type == 'object':
      mode = get_mode_of_a_column(df, i)
      df.iloc[:,i] = df.iloc[:,i].replace(np.nan, mode)
    else:
      impute_value = 0
      if method == 'mean':
        impute_value = get_mean_of_a_column(df, i) 
      else:
        impute_value = get_median_of_a_column(df, i)
      
      df.iloc[:,i] = df.iloc[:,i].replace(np.nan, impute_value)

  df.to_csv(output_file)

# Command line Processing
input_file = sys.argv[1]

df = get_data(input_file)

argParser = argparse.ArgumentParser(description='Impute process')
argParser.add_argument('in', help='input')
argParser.add_argument("-method", "--method", help="method")
argParser.add_argument("-columns", "--columns", default=[], nargs='*', help="columns")
argParser.add_argument("-out", "--out", help="out")

args = argParser.parse_args()

method = args.method
columns = args.columns
output_file = args.out 
input_file = sys.argv[1]

impute(df, columns, method, output_file)


