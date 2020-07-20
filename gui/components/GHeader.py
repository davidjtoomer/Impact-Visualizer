import tkinter as tk
from gui.constants import *

class GHeader(tk.Frame):
  def __init__(self, master = None, *args, **kwargs):
    tk.Frame.__init__(self, master, *args, **kwargs)

    self.title = master.title

    self.configure(bg = PRIMARY, padx = HEADER_PADX, pady = HEADER_PADY)

    self.rowconfigure(0, weight = 1, minsize = HEADER_MINSIZE)
    self.columnconfigure(0, weight = 1)

    title = tk.Label(self)
    title.configure(text = self.title, bg = PRIMARY, fg = BASE_LIGHT, font = (FONT_FAMILY, FONTSIZE_H1), anchor = tk.W, justify = tk.LEFT)
    title.grid(row = 0, column = 0, sticky = 'sw')