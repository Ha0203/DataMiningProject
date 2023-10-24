import sys
import pandas as pd
import numpy as np
import argparse

NUMERICS = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']

def get_data(url):
  """
  get data from file
  """
  df = pd.read_csv(url)
  return df

def isNaN(value):
  """
  Check if a value is NaN
  """
  return value != value

def get_shape(df):
  """
  return the shape of df(rows, columns)
  """
  return len(df), len(df.iloc[0])

def get_column_names(df):
  return list(df.keys())

def get_all_column_types(df):
  n, m = get_shape(df)
  return [df.iloc[:,i].dtype for i in range(0, m)]

def get_column_type(df, i):
  return df.iloc[:,i].dtype

def get_mode_of_a_column(df, i):
  res = {}
  n, m = get_shape(df)
  for j in range(0, n):
    value = df.iloc[j][i]
    if isNaN(value):
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
    
  # return [key for key, value in res.items() if value == max_frequency]
  return max_value
  

def missing_value(df, i):
  """
    check if column i in df have missing value or not
  """

  n, m = get_shape(df)

  for n in range(0, n):
    if isNaN(df.iloc[n][i]):
      return True
  return False

def get_mean_of_a_column(df, i):
  n, m = get_shape(df)

  sum = 0

  elements = 0

  for j in range(0, n):
    if isNaN(df.iloc[j][i]):
      continue
    
    sum += df.iloc[j][i]
    elements += 1

  return sum / elements

def get_median_of_a_column(df, i):
  n, m = get_shape(df)

  # print(df.iloc[:, i].tolist())
  arr = df.iloc[:, i].tolist()

  arr = [i for i in arr if not isNaN(i)] # remove NaN values

  arr = sort(arr)

  median_pos = int(len(arr) / 2)

  # print(sorted_arr[median_pos], sorted_arr[median_pos-1])
  if n % 2 == 0:
    return (arr[median_pos] + arr[median_pos - 1]) / 2
  
  return arr[median_pos]

# check if a column has no value in it
def column_with_no_value(df, i):
  n, m = get_shape(df)

  for j in range(0, n):
    if not isNaN(df.iloc[j][i]):
      return False
  
  return True

def sort(arr): 
  for i in range(0, len(arr) - 1):
    for j in range(i + 1, len(arr)):
      if arr[i] > arr[j]:
        t = arr[i]
        arr[i] = arr[j]
        arr[j] = t
  return arr

# All the functions below are for TESTING PURPOSE

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

  df.to_csv(output_file)