import tkinter as tk
from GUI.constants import *

class GWidgetButton(tk.Frame):
  def __init__(self, master = None, *args, **kwargs):
    tk.Button.__init__(self, master, *args, **kwargs)

    self.configure(font = (FONT_FAMILY, FONTSIZE_P))