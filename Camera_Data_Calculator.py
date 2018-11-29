#!/usr/bin/python 

from Tkinter import *
import json
from collections import OrderedDict
from data_calc_gui import Data_calc_gui

#_______________________________________________________


units = {"kb":1024, "kiB":8192, "kB":8000, "Mb":1048576, "MiB":8388608, "MB":8000000, "Gb":1073741824, "GiB":8589934592, "GB":8000000000, "Tb":1099511627776, "TiB":8796093022208, "TB":8000000000000}

arri_cams = json.load(open('arri_cams.json', 'r'), object_pairs_hook=OrderedDict)

#_______________________________________________________



data_calc_gui = Data_calc_gui(arri_cams)
data_calc_gui.start_gui()
