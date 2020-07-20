import tkinter as tk
from tkinter.tix import ScrolledWindow
import tkinter.font as font

# pages
from GUI.pages.HomePage import HomePage
from GUI.pages.ImpactPage import ImpactPage
from GUI.pages.ScanLinePage import ScanLinePage
from GUI.pages.SurfacePage import SurfacePage

# styling
from GUI.constants import *

class GWindow(tk.Tk):
  def __init__(self, *args, **kwargs):
    tk.Tk.__init__(self, *args, **kwargs)

    # adjust window size
    self.update_idletasks()
    xpos = 0 # (self.winfo_screenwidth() // 2) - (WINDOW_WIDTH // 2)
    ypos = 0 # (self.winfo_screenheight() // 2) - (WINDOW_HEIGHT // 2)
    self.geometry(f'{int(3/4 * self.winfo_screenwidth())}x{self.winfo_screenheight()}+{xpos}+{ypos}')

    # max out rows and columns
    self.rowconfigure(0, weight = 1)
    self.columnconfigure(0, weight = 1)

    # set inner container: holds all pages to be raised
    container = tk.Frame(self)
    container.configure(bg = BASE_LIGHT)
    container.grid(row = 0, column = 0, sticky = 'nsew')
    container.rowconfigure(0, weight = 1)
    container.columnconfigure(0, weight = 1)
    self.container = container

    # add all pages to window
    self.pages = {}
    for Page in [HomePage, ScanLinePage, ImpactPage]: # SurfacePage):
      if Page == HomePage:
        page = Page(master = container, controller = self)
      else:
        page = Page(master = container, controller = self, home = self.pages[HomePage])
      self.pages[Page] = page
      page.grid(row = 0, column = 0, sticky = 'nsew')

    # display the start page
    self.show_page(HomePage)

  def show_page(self, page):
    to_display = self.pages[page]
    to_display.tkraise()

  def quit_program(self):
    self.quit()
    self.destroy()