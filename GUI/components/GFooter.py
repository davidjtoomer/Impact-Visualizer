import tkinter as tk

from GUI.components.GWidgetButton import GWidgetButton
from GUI.constants import *

class GFooter(tk.Frame):
  def __init__(self, master = None, controller = None, *args, **kwargs):
    tk.Frame.__init__(self, master, *args, **kwargs)

    self.configure(bg = PRIMARY_LIGHT, padx = FOOTER_PADX, pady = FOOTER_PADY)

    self.rowconfigure(0, weight = 1)
    self.columnconfigure(0, weight = 1)

    exit_button = tk.Button(self, text = 'Exit Program', font = (FONT_FAMILY, FONTSIZE_P), command = lambda: controller.quit_program())
    exit_button.grid(row = 0, column = 0, sticky = 'nsew')