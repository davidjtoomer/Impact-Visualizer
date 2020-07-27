import numpy as np
import pandas as pd
from scipy import interpolate

from models.ScanLine import ScanLine

class Impact:
  def __init__(self, datafiles, filenames):
    self.num_scanlines = len(filenames)
    self.scanlines = [ScanLine(data, filename) for data, filename in zip(datafiles, filenames)] 
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

    self.xgrid, self.ygrid = np.meshgrid(self.X, self.Y)
    self.zgrid = np.array([scanline.data_corrected_smooth[:, 1] for scanline in self.scanlines])

    '''
    self.xgrid_dense, self.ygrid_dense = np.mgrid[0 : self.xrange : complex(0, len(self.scanlines[0].data)), 0 : self.yrange : complex(0, 100)]
    tck = interpolate.bisplrep(self.ygrid, self.xgrid, np.transpose(self.zgrid), w = None, task = 0, kx = 3, ky = 3, s = 2) #  np.linspace(0, 3, 12), ty = np.linspace(0, 1, 12), s = 6)
    self.zgrid_dense = interpolate.bisplev(self.ygrid_dense[0, :], self.xgrid_dense[:, 0], tck)
    '''