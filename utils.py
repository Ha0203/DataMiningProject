import sys
import argparse
import csv


NUMERICS = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']

def column_with_all_missing_values(df, name):
  if type(df[name][0]) == str:
    for value in df[name]:
      if value != '':
        return False
  else:
     for value in df[name]:
      if value != None:
        return False
  return True

def is_float(string):
    try:
        float(string)
        return True
    except ValueError:
        return False
    
def get_data(url):
  """
  get data from file 
  """
  file = open(url, 'r')

  cols = {}

  first_line_vals = file.readline().rstrip().split(',')

  for val in first_line_vals:
    cols[val] = [] 

  for line in file:
    line_vals = line.rstrip().split(',')
    
    for i in range(len(line_vals)):
      cols[first_line_vals[i]].append(line_vals[i])

  file.close()
  
  return cols

def write_data(df, url):
  """
  Write data to csv
  """
  
  with open(url, 'w', newline='') as file:
    csvwriter = csv.writer(file)

    csvwriter.writerow(get_column_names(df))
    
    rows = []
    for col_name, col_data in df.items():
      new_row = []
      for value in col_data:
        new_row.append(value)
      
      rows.append(new_row)

    rows = list(map(list, zip(*rows)))

    csvwriter.writerows(rows)

def isNaN(value):
  """
  Check if a value is NaN
  """
  return value != value

def get_shape(df):
  """
  return the shape of df(columns, rows)
  """
  return len(df), len(df['Id'])

def get_column_names(df):
  return list(df.keys())

def get_all_column_types(df):
  for key, value in df.items():
    print(f'{key} {type(value[0])}')

def convert_column_types(df):
  new_df = {}

  for col_name, col_data in df.items():
    for value in col_data:
      if isNaN(value):
        continue 

      if value.isdigit():
        new_col = []

        for value in col_data:
          new_col.append(int(value))
          
        new_df[col_name] = new_col
        break
      elif is_float(value):
          new_col = []

          for value in col_data:
            if value == '':
              new_col.append(None)
            else:
              new_col.append(float(value))

          new_df[col_name] = new_col
          break
      else:
        new_df[col_name] = col_data
  
  return new_df
      


def get_mode_of_a_column(df, name):
  res = {}

  for value in df[name]:
    if value == '':
      continue

    if value in res:
      res[value] += 1
    else:
      res[value] = 1
  
  max_frequency = 0
  max_value = 0
  for key, value in res.items():
    if value > max_frequency:
      max_frequency = value   
      max_value = key
    
  return max_value

def get_mean_of_a_column(df, name):
  sum = 0
  n = 0
  for value in df[name]:
    if not value is None:
      sum += value
      n += 1

  return sum / n

def get_median_of_a_column(df, name):
  n, m = get_shape(df)

  arr = [value for value in df[name] if not value is None] # remove NaN values

  arr = sort(arr)

  median_pos = int(len(arr) / 2)

  if len(arr) % 2 == 0:
    return (arr[median_pos] + arr[median_pos - 1]) / 2.0
  
  return arr[median_pos]

def sort(arr): 
  for i in range(0, len(arr) - 1):
    for j in range(i + 1, len(arr)):
      if arr[i] > arr[j]:
        t = arr[i]
        arr[i] = arr[j]
        arr[j] = t
  return arr

def extract_columns_with_missing_value(df):

  missing_columns = [] # name of each columns which has missing value

  for col_name, col_data in df.items():
    if None in col_data or '' in col_data:
      missing_columns.append(col_name)
      continue

  return missing_columns

def get_number_of_missing_values(col_data):
  sum = 0
  for value in col_data:
    if value is None or value == '':
      sum += 1
  return sum

def delete_cols(df, columns):
  """
  Delete column which has the total of missing value greater than half of the total rows in dataset
  return: a list of name of delete cols, and a dataset after deleting some columns
  """
  del_cols = []
  new_df = df.copy()

  for col_name in columns:
    col_data = df[col_name]
    num_missing_value = get_number_of_missing_values(col_data)

    if num_missing_value > len(col_data) / 2:
      del new_df[col_name]
      del_cols.append(col_name)
  
  return del_cols, new_df

def impute(df, column_names, method):
  missing_col_names = extract_columns_with_missing_value(df) 

  for name in column_names:
    new_cols = []
    impute_value = 0

    if column_with_all_missing_values(df, name):
      df[name] = [''] * len(df[name]) 
      continue
    
    if not type(df[name][0]) == str:
      if method == 'mean':
        impute_value = get_mean_of_a_column(df, name)
      else:
        impute_value = get_median_of_a_column(df, name) 
   
    else:
      impute_value = get_mode_of_a_column(df, name)

    for value in df[name]:
      if value is None or value == '':
        value = impute_value
      new_cols.append(value)

    df[name] = new_cols

  return df

def get_variance(df, col_name):
  mean = get_mean_of_a_column(df, col_name)
  
  return sum([(value - mean) ** 2 for value in df[col_name]]) / len(df[col_name])

def get_standard_deviation(df, col_name):
  variance = get_variance(df, col_name)
  return variance ** 0.5

def column_value_all_zeroes(col_data):
  for value in col_data:
    if value != 0:
      return False

  return True

def normalize(df, method, col_names):
  # Before imputing, we need to remove the columns which has too many missing values
  del_cols, deleted_df = delete_cols(df, col_names)

  cols_remain = [name for name in col_names if name not in del_cols]

  # before normalizing, we need to impute the value first

  imputed_df = impute(deleted_df, cols_remain, 'mean')
  
  for col_name in cols_remain:
    col_data = imputed_df[col_name]
    
    if column_value_all_zeroes(col_data):
      continue

    if type(col_data[0]) != str:
      new_col = []
      if method == 'min-max':
        max_value = max(col_data)
        min_value = min(col_data)
        for value in col_data:
          new_col.append((value - min_value) / (max_value - min_value))
      else:
        for value in col_data:
          new_col.append(float(value - get_mean_of_a_column(imputed_df, col_name)) / get_standard_deviation(imputed_df, col_name))
      df[col_name] = new_col
    else:
      df[col_name] = col_data
  
  return df

def set_up_cmd(output_file = True, method=True):
  argParser = argparse.ArgumentParser(description="Normalizing Numerical Attribute Processing")

  argParser.add_argument('in', help='Input file name')

  argParser.add_argument('-columns', '--columns', help='columns you want to normalize, leave it empty to normalize ALL the columns', default=[], nargs='*')
  
  if output_file:
    argParser.add_argument('-out', '--out', help='Output file name')
  
  if method:
    argParser.add_argument('-method', '--method', help='method(min-max or z-score)')

  args = argParser.parse_args()

  input_file = sys.argv[1]
  
  if output_file: 
    output_file = args.out
  
  if method:
    method = args.method
  
  columns = []

  df = get_data(input_file)

  df = convert_column_types(df)

  if args.columns == []:
    columns = get_column_names(df)
  else:
    columns = args.columns

  return df, output_file, method, columns

