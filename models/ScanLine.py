import numpy as np
import pandas as pd
from sklearn import linear_model

class ScanLine:
  def __init__(self, filename):
    try:
      startpos = filename.rfind('/') + 1
      ypos_digits = 8
      self.ypos = float(filename[startpos : startpos + ypos_digits])
    except:
      self.ypos = None

    self.filename = filename
    self.filename_short = filename[filename.rfind('/') + 1:]
    self.data = pd.read_excel(filename, sheet_name='DATA', header=None, nrows=6000, usecols='E:F', keep_default_na=False).to_numpy()
    self.data[:, 1] /= 1000 # convert microns to mm
    self.slope_correction()
    self.smooth_width = 100
    self.smooth()

  def slope_correction(self):
    x = self.data[:, 0].reshape(-1, 1)
    y = self.data[:, 1].reshape(-1, 1)

    # linear regression
    lr = linear_model.LinearRegression()
    lr.fit(x, y.ravel())
    regression = lr.predict(x)
    self.regression = regression

    self.slope = lr.coef_[0]
    self.intercept = lr.intercept_

    self.data_corrected = np.copy(self.data)
    self.data_corrected[:, 1] -= regression 

  def smooth(self):
    smoothed = np.convolve(self.data_corrected[:, 1], np.ones((self.smooth_width,)) / self.smooth_width, mode='same')
    double_smoothed = np.convolve(smoothed, np.ones((self.smooth_width,)) / self.smooth_width, mode='same')
    self.data_corrected_smooth = np.copy(self.data_corrected)
    self.data_corrected_smooth[:, 1] = double_smoothed

  def update_regression(self, slope, intercept):
    self.slope = slope
    self.intercept = intercept
    self.regression = (slope * self.data[:, 0] + intercept).reshape(len(self.data), -1)
    self.data_corrected[:, 1] = self.data[:, 1] - self.regression.ravel()
    self.smooth()

  def set_ypos(self, ypos):
    self.ypos = ypos