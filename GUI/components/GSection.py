import tkinter as tk
from GUI.constants import *

class GSection(tk.Frame):
  def __init__(self, master = None, *args, **kwargs):
    tk.Frame.__init__(self, master, *args, **kwargs)

    self.configure(padx = PAGE_PADX, pady = PAGE_PADY)