import tkinter as tk
from tkinter.filedialog import askopenfilename

import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

from models.ScanLine import ScanLine

from gui.components.GPage import GPage
from gui.components.GSection import GSection
from gui.components.GMainButton import GMainButton
from gui.components.GWidgetButton import GWidgetButton

from gui.constants import *

class ScanLinePage(GPage):
  def __init__(self, master = None, controller = None, home = None, *args, **kwargs):
    GPage.__init__(self, master = master, controller = controller, title = 'ScanLine\nPlotter', *args, **kwargs)

    self.home = home
    self.regression = True
    self.plot_configs = {
      's': 0.5,
      'c': PRIMARY_LIGHT
    }
    self.display_type = 'RAW'

    self.rowconfigure(1, weight = 1)

    main_section = GSection(master = self)
    main_section.grid(row = 1, column = 0, sticky = 'nsew')
    main_section.rowconfigure(0, weight = 1)
    main_section.columnconfigure(0, weight = 1)
    self.main_section = main_section

    self.display_navigation()

  def display_navigation(self):
    navigation = tk.Frame(self.main_section)
    navigation.rowconfigure(0, weight = 1)
    navigation.columnconfigure(0, weight = 3)
    navigation.columnconfigure(1, weight = 1)
    navigation.grid(row = 0, column = 0, sticky = 'nsew')

    nav_button_select = GMainButton(master = navigation, text = 'Select\nScanline\nFile', command = lambda: self.load_scanline())
    nav_button_select.grid(row = 0, column = 0, sticky = 'nsew')

    nav_button_home = GMainButton(master = navigation, text = 'Back\nto\nHome', command = lambda: self.return_home())
    nav_button_home.grid(row = 0, column = 1, sticky = 'nsew')

  def display_scanline(self, display_type, **kwargs):
    self.display_type = display_type

    # adjust display settings
    display = tk.Frame(self.main_section)
    display.rowconfigure(0, weight = 1) # graph and widgets
    display.columnconfigure(0, weight = 1)
    display.grid(row = 0, column = 0, sticky = 'nsew')

    # DISPLAYS BOTH THE FIGURE AND THE WIDGETS ON THE SIDE
    figure_widget_display = tk.Frame(display)
    figure_widget_display.rowconfigure(0, weight = 1)
    figure_widget_display.columnconfigure(0, weight = 3)
    figure_widget_display.columnconfigure(1, weight = 1)
    figure_widget_display.grid(row = 0, column = 0, sticky = 'nsew')

    # ONLY DISPLAYS THE FIGURE
    figure_display = tk.Frame(figure_widget_display)
    figure_display.grid(row = 0, column = 0)

    self.get_configs(**kwargs)
    figure = Figure()
    if self.display_type == 'RAW':
      plot = figure.add_subplot(111)
      plot.scatter(self.scanline.data[:, 0], self.scanline.data[:, 1], **self.plot_configs)
      if self.regression:
        plot.plot(self.scanline.data[:, 0], self.scanline.regression, c = PRIMARY_DARK)
    elif self.display_type == 'CORRECTED':
      plot = figure.add_subplot(111)
      plot.scatter(self.scanline.data_corrected[:, 0], self.scanline.data_corrected[:, 1], **self.plot_configs)
      if self.regression:
        plot.plot(self.scanline.data[:, 0], np.zeros((len(self.scanline.data_corrected),)), c = PRIMARY_DARK)
    elif self.display_type == 'SMOOTHED':
      plot = figure.add_subplot(111)
      plot.scatter(self.scanline.data_corrected_smooth[:, 0], self.scanline.data_corrected_smooth[:, 1], **self.plot_configs)
      if self.regression:
        plot.plot(self.scanline.data[:, 0], np.zeros((len(self.scanline.data_corrected),)), c = PRIMARY_DARK)

    figure_canvas = FigureCanvasTkAgg(figure, figure_display)
    figure_canvas.draw()
    toolbar = NavigationToolbar2Tk(figure_canvas, figure_display)
    toolbar.update()
    figure_canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=1)

    # ONLY DISPLAYS THE WIDGETS
    widget_display = tk.Frame(figure_widget_display)
    widget_display.grid(row = 0, column = 1, sticky = 'nsew')
    widget_display.columnconfigure(0, weight = 1)

    # file information
    file_frame = tk.Frame(widget_display)
    file_frame.grid(row = 0, column = 0, sticky = 'nsew')
    file_frame.columnconfigure(0, weight = 1)
    file_frame.columnconfigure(1, weight = 1)

    file_header_frame = tk.Frame(file_frame, pady = WIDGET_BUTTON_SPACING)
    file_header_frame.grid(row = 0, column = 0, columnspan = 2, sticky = 'nsew')
    file_header_frame.rowconfigure(0, weight = 1)
    file_header_frame.columnconfigure(0, weight = 1)

    filename_label = tk.Label(file_header_frame, text = f'Filename: {self.scanline.filename_short}', anchor = tk.W, justify = tk.LEFT, font = (FONT_FAMILY, FONTSIZE_H4), padx = WIDGET_BUTTON_PADX, bg = PRIMARY_LIGHT, fg = BASE_DARK)
    filename_label.grid(row = 0, column = 0, columnspan = 2, sticky = 'nsew')

    ypos_label = tk.Label(file_frame, text = 'ypos: ', font = (FONT_FAMILY, FONTSIZE_P), anchor = tk.W, justify = tk.LEFT)
    ypos_label.grid(row = 1, column = 0, sticky = 'nsew')
    ypos_value = tk.StringVar()
    ypos_entry = tk.Entry(file_frame, textvariable = ypos_value)
    ypos_entry.grid(row = 1, column = 1, sticky = 'nsew')
    ypos_value.set(f'{self.scanline.ypos}')

    update_ypos_button = GWidgetButton(master = file_frame, text = 'UPDATE YPOS', font = (FONT_FAMILY, FONTSIZE_P), command = lambda: self.update_ypos(ypos_entry.get()))
    update_ypos_button.grid(row = 2, column = 1, sticky = 'nsew')

    # graph options buttons
    graph_options_frame = tk.Frame(widget_display, pady = WIDGET_BUTTON_SPACING)
    graph_options_frame.grid(row = 1, column = 0, sticky = 'nsew')
    graph_options_frame.rowconfigure(0, weight = 1)
    graph_options_frame.columnconfigure(0, weight = 1)

    graph_label = tk.Label(graph_options_frame, text = 'Graph Options', anchor = tk.W, justify = tk.LEFT, font = (FONT_FAMILY, FONTSIZE_H4), padx = WIDGET_BUTTON_PADX, bg = PRIMARY_LIGHT, fg = BASE_DARK)
    graph_label.grid(row = 1, column = 0, sticky = 'nsew')

    button_raw_data = GWidgetButton(master = widget_display, text = 'Raw Data', command = lambda: self.display_scanline('RAW'))
    button_raw_data.grid(row = 2, column = 0, sticky = 'nsew')

    button_slope_correct = GWidgetButton(master = widget_display, text = 'Slope Correction', command = lambda: self.display_scanline('CORRECTED'))
    button_slope_correct.grid(row = 3, column = 0, sticky = 'nsew')

    button_smooth = GWidgetButton(master = widget_display, text = 'Smoothen + Correction', command = lambda: self.display_scanline('SMOOTHED'))
    button_smooth.grid(row = 4, column = 0, sticky = 'nsew')

    button_regress = GWidgetButton(master = widget_display, command = lambda: self.toggle_regression())
    button_regress.configure(text = f'Regression: {"ON" if self.regression else "OFF"}')
    button_regress.grid(row = 5, column = 0, sticky = 'nsew')

    # edit parameter values
    parameter_frame = tk.Frame(widget_display)
    parameter_frame.grid(row = 6, column = 0, sticky = 'nsew')
    parameter_frame.rowconfigure(0, weight = 1)
    parameter_frame.rowconfigure(1, weight = 1)
    parameter_frame.columnconfigure(0, weight = 1)
    parameter_frame.columnconfigure(1, weight = 1)

    slope_label = tk.Label(parameter_frame, text = 'Slope: ', anchor = tk.W, justify = tk.LEFT, font = (FONT_FAMILY, FONTSIZE_P))
    slope_label.grid(row = 0, column = 0, sticky = 'nsew')
    slope_value = tk.StringVar()
    slope_entry = tk.Entry(parameter_frame, textvariable = slope_value)
    slope_entry.grid(row = 0, column = 1, sticky = 'nsew')
    slope_value.set(f'{self.scanline.slope}')

    intercept_label = tk.Label(parameter_frame, text = 'Intercept: ', anchor = tk.W, justify = tk.LEFT, font = (FONT_FAMILY, FONTSIZE_P))
    intercept_label.grid(row = 1, column = 0, sticky = 'nsew')
    intercept_value = tk.StringVar()
    intercept_entry = tk.Entry(parameter_frame, textvariable = intercept_value)
    intercept_entry.grid(row = 1, column = 1, sticky = 'nsew')
    intercept_value.set(f'{self.scanline.intercept}')

    update_regression_button = GWidgetButton(master = parameter_frame, text = 'UPDATE REGRESSION', command = lambda: self.update_parameters(float(slope_entry.get()), float(intercept_entry.get())))
    update_regression_button.grid(row = 2, column = 1, sticky = 'nsew')

    reset_frame = tk.Frame(widget_display, pady = WIDGET_BUTTON_SPACING)
    reset_frame.grid(row = 7, column = 0, sticky = 'nsew')
    reset_frame.rowconfigure(0, weight = 1)
    reset_frame.columnconfigure(0, weight = 1)
    newfile_label = tk.Label(reset_frame, text = 'Reset Information', anchor = tk.W, justify = tk.LEFT, font = (FONT_FAMILY, FONTSIZE_H4), padx = WIDGET_BUTTON_PADX, bg = PRIMARY_LIGHT, fg = BASE_DARK)
    newfile_label.grid(row = 0, column = 0, sticky = 'nsew')

    pick_new_button = GWidgetButton(master = widget_display, text='Choose New Scanline', command = lambda: self.load_scanline())
    pick_new_button.grid(row = 8, column = 0, sticky = 'nsew')

    return_home_button = GWidgetButton(master = widget_display, text='Back to Home', command = lambda: self.return_home())
    return_home_button.grid(row = 9, column = 0, sticky = 'nsew')

  def load_scanline(self):
    self.get_scanline()
    self.display_scanline('RAW') if self.scanline else self.display_navigation()

  def get_scanline(self):
    filename = askopenfilename(initialdir = '/', title = 'Select File', filetypes = [('Excel files','*.xls *.xlsx')])
    self.scanline = ScanLine(filename) if filename else None

  def toggle_regression(self):
    self.regression = not self.regression
    self.display_scanline(self.display_type)

  def get_configs(self, **kwargs):
    for kwarg in kwargs:
      self.plot_configs[kwarg] = kwargs[kwarg]
  
  def update_parameters(self, slope, intercept):
    self.scanline.update_regression(slope, intercept)
    self.display_scanline(self.display_type)

  def update_ypos(self, ypos):
    self.scanline.set_ypos(ypos)

  def return_home(self):
    self.home.tkraise()