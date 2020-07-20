import tkinter as tk
from GUI.constants import *

class GMainButton(tk.Frame):
  def __init__(self, master = None, text = None, command = None, *args, **kwargs):
    tk.Frame.__init__(self, master, *args, **kwargs)

    self.configure(bg = BASE_LIGHT, padx = 10, pady = 10)
    self.rowconfigure(0, weight = 1)
    self.columnconfigure(0, weight = 1)

    # container for colored border 
    border_frame = tk.Frame(self)
    border_frame.configure(bg = PRIMARY_LIGHT, bd = BUTTON_BORDERWIDTH)
    
    border_frame.rowconfigure(0, weight = 1)
    border_frame.columnconfigure(0, weight = 1)
    border_frame.grid(row = 0, column = 0, sticky = 'nsew')

    # actual button
    button = tk.Button(border_frame, command = command)
    button.configure(bg = BASE_LIGHT, text = text, font = (FONT_FAMILY, FONTSIZE_H2))
    button.grid(row = 0, column = 0, sticky = 'nsew')