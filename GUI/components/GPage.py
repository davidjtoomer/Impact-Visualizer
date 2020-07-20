import tkinter as tk
from GUI.components.GHeader import GHeader
from GUI.components.GFooter import GFooter
from GUI.constants import *

class GPage(tk.Frame):
  def __init__(self, master = None, controller = None, title = '', *args, **kwargs):
    tk.Frame.__init__(self, master, *args, **kwargs)

    self.configure(bg = BASE_LIGHT)
    self.title = title.upper()

    # configure display
    self.rowconfigure(0, weight = 0)
    self.rowconfigure(MAX_ROWS, weight = 0)
    self.columnconfigure(0, weight = 1)

    # add header
    header = GHeader(master = self, *args, **kwargs)
    header.grid(row = 0, column = 0, sticky = 'nsew')

    # add footer
    footer = GFooter(master = self, controller = controller, *args, **kwargs)
    footer.grid(row = MAX_ROWS, column = 0, sticky = 'nsew')