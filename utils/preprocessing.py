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

def extract_ystep(matlab_contents):
  if matlab_contents:
    _, content_string = matlab_contents.split(',')
    decoded = base64.b64decode(content_string)
    matlab_file = io.BytesIO(decoded)
    for line in matlab_file:
      line = line.decode('utf-8')
      if line.startswith('ystep ='):
        return float(line[line.find('=') + 2 : line.find(';')])
  return 0.02

def extract_matlab(contents, filenames):
  matlab_contents, matlab_filename = None, None
  for i, filename in enumerate(filenames):
    if filename.endswith('.m'):
      matlab_filename = filenames.pop(i)
      matlab_contents = contents.pop(i)
  return matlab_contents, matlab_filename