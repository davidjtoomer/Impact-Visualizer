import io
import base64
import pandas as pd

def parse_impact(contents):
  datafiles = []
  for content in contents:
    _, content_string = content.split(',')
    decoded = base64.b64decode(content_string)
    datafiles.append(pd.read_excel(io.BytesIO(decoded), sheet_name = 'DATA', header = None, nrows = 6000, usecols = 'E:F', keep_default_na = False))
  return datafiles

def extract_ypos(file):
  # get the file
  # find the ypos from the file
  # get the number that follows the ypos
  return