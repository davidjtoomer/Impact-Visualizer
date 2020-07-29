import numpy as np
import pandas as pd
from scipy import interpolate

from models.ScanLine import ScanLine

class Impact:
  def __init__(self, datafiles, filenames):
    self.num_scanlines = len(filenames)
    scanlines = [ScanLine(data, filename) for data, filename in zip(datafiles, filenames)]
    self.scanlines = sorted(scanlines, key = lambda x: x.ypos) 
    self.xrange = self.scanlines[0].data[:, 0][-1]
    self.reset_ypos()
    self.combine_scanlines()

  def reset_ypos(self):
    min_ypos = min([scanline.ypos for scanline in self.scanlines])
    for scanline in self.scanlines:
      scanline.set_ypos(scanline.ypos - min_ypos)
    self.yrange = max([scanline.ypos for scanline in self.scanlines])

  def combine_scanlines(self):
    density = self.xrange / len(self.scanlines[0].data)
    self.X = np.arange(0, self.xrange, density)
    self.Y = np.array([scanline.ypos for scanline in self.scanlines])
    self.Z = np.array([scanline.data_corrected_smooth[:, 1] for scanline in self.scanlines])