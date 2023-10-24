import sys
import pandas as pd # used for testing 
import numpy as np # used for testing
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


# ------------------------------------------- All the functions below are for TESTING PURPOSE -------------------------------------------------------------

# check if a column has no value in it
def column_with_no_value(df, i):
  n, m = get_shape(df)

  for j in range(0, n):
    if not isNaN(df.iloc[j][i]):
      return False
  
  return True


def get_column_type(df, i):
  return df.iloc[:,i].dtype

def missing_value(df, i):
  """
    check if column i in df have missing value or not
  """

  n, m = get_shape(df)

  for n in range(0, n):
    if isNaN(df.iloc[n][i]):
      return True
  return False

def print_numerical_columns(df):
  res = df.select_dtypes(include=NUMERICS).columns
  print("There are", len(res), "numerical columns")
  print(res)

def print_object_columns(df):
  res = df.select_dtypes(include=['object']).columns
  print("There are", len(res), "object columns")
  print(res)

def print_missing_value_of_all_columns(df): 
  print(df.isna().sum())

def print_column(df, name):
  print(df[name])

def print_missing_value_of_a_column(df, name):
  print(df[name].isna().sum())

def get_index_of_a_column(df, name):
  return df.columns.get_loc(name)

def print_columns_has_missing_value(df):
  n, m = get_shape(df)

  indexes = [i for i in range(0, m) if missing_value(df, i)]

  names = get_column_names(df)

  res = [names[i] for i in indexes]

  for i in res:
    print(i, ' ',end='')

def fillna(df, method, output_file):
  """
  Used for testing in function: "impute missing value using mean, median and mode with appropriate attributes
  """
  names = get_column_names(df)

  for name in names:
    if column_with_no_value(df, df.columns.get_loc(name)):
      continue

    if df[name].dtype == 'object' or df[name].dtype == 'category':
      df[name].fillna(df[name].mode()[0], inplace=True)
    else:
      if method == 'mean':
        df[name].fillna(df[name].mean(), inplace=True)
      else:
        df[name].fillna(df[name].median(), inplace=True)

  df.to_csv(output_file, index=False)