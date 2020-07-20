import tkinter as tk

from gui.components.GPage import GPage
from gui.components.GSection import GSection
from gui.components.GMainButton import GMainButton
from gui.components.GWidgetButton import GWidgetButton
from gui.pages.ImpactPage import ImpactPage
from gui.pages.ScanLinePage import ScanLinePage

from gui.constants import *

class HomePage(GPage):
  def __init__(self, master = None, controller = None, *args, **kwargs):
    GPage.__init__(self, master = master, controller = controller, title = 'Impact\nVisualizer', *args, **kwargs)

    self.rowconfigure(1, weight = 1)

    navigation = GSection(master = self)

    navigation.rowconfigure(0, weight = 1)
    navigation.rowconfigure(1, weight = 0)
    navigation.columnconfigure(0, weight = 1)
    navigation.columnconfigure(1, weight = 1)
    navigation.grid(row = 1, column = 0, sticky = 'nsew')

    nav_button_scanline = GMainButton(master = navigation, text = 'View\nIndividual\nScanlines', command = lambda: controller.show_page(ScanLinePage))
    nav_button_scanline.grid(row = 0, column = 0, sticky = 'nsew')

    nav_button_impact = GMainButton(master = navigation, text = 'View\nWhole\nImpacts', command = lambda: controller.show_page(ImpactPage))
    nav_button_impact.grid(row = 0, column = 1, sticky = 'nsew')