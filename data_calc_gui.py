#!/usr/bin/python 

from Tkinter import *
import Tkinter as tk
import json
from collections import OrderedDict
from data_calc2 import Data_calculator
from PIL import Image, ImageTk
#from data_tools_gui import Data_tools_gui





VERSION = 1.07

units = {"kb":1024, "kiB":8192, "kB":8000, "Mb":1048576, "MiB":8388608, "MB":8000000, "Gb":1073741824, "GiB":8589934592, "GB":8000000000, "Tb":1099511627776, "TiB":8796093022208, "TB":8000000000000, "PB":8000000000000000}

unit_list = ""
for i in units:
	unit_list += i + ", "

arri_cams = json.load(open('arri_cams.json', 'r'), object_pairs_hook=OrderedDict)


#_______________________________________________________


class Data_calc_gui():
	def __init__(self, arri_cams):
		self.arri_cams = arri_cams
		self.units = units
		self.error = None

		self.about_text = "Camera Data Calculator v" + str(VERSION) + " - Ben Coxon 2018\n" + '''
Instructions:

1. Select Camera from radio buttons on left.
2. Select Resolution from the dropdown in top-right
3. Set FPS - default is 24

4. Tools:

- Data Rate:  

With the Camera, Resolution and FPS set, click 'Data Rate' to display the Data Rate in MB/s.

- Duration:  

With the Camera, Resolution and FPS set, enter a data size in the 'Data Size (for Duration)' box.  
The syntax is the value (integer or float number) followed a space, and the a data unit.  
For example:  '1.5 TB', '10 Gb', '23456 MB' etc. 

Units Support: ''' + unit_list + '''

Click 'Duration' and the duration for that camera format in hours, minutes, seconds and frames will be 
displayed.

- Data Size:

With the Camera, Resolution and FPS set, enter a duration in the 'Duration (for Data Size)' box.
The syntax is in hours, minutes, seconds and frames, although not all of these units are required.
For example:

1h 2s 3s 4f

25m 13f

10s

25000f

- FPS:

With the Camera and Resolution set, enter a duration in the 'Duration (for Data Size)' box
and enter a data size in the 'Data Size (for Duration)' box.  Click FPS to display the FPS.
This can be useful to getting an FPS readout from timing a data copy.


- Other Uses:

Calculate the data rate from a specific fps, such as the Generate readout from drserver log by 
setting the Camera and Resolution, setting the FPS to the log readout and clicking the 'Data Rate' button.

		'''

	#__________________________________________________________
	## Grab Info from Camera Json dict
	#__________________________________________________________
	

	def get_cam_list(self):
		self.camlist = []
		for i in self.arri_cams:
			self.camlist.append(i)

	def get_rez_list(self, cam):
		self.rez_list = []
		for i in self.arri_cams[cam]["ARRIRAW"]:
			self.rez_list.append(i)
		return self.rez_list
		

	def get_mode_list(self):
		self.modelist = []
		for i in self.arri_cams:
			for m in self.arri_cams[i]:
				if not m in self.modelist:
					self.modelist.append(m)
		
	#__________________________________________________________
	##  GUI WIDGETS
	#__________________________________________________________
	
	def rez_select(self):
		Label(self.root, text="				", bg="grey", fg="white").grid(row=(len(self.arri_cams) + 2), column=1, sticky=(N,W,E,S))
		Label(self.root, text="				", bg="grey", fg="white").grid(row=(len(self.arri_cams) + 3), column=1, sticky=(N,W,E,S))
		for cam in self.camlist:
			if str(self.cam_var.get()) == cam:
				self.rez_choice.set('Select')
				self.get_rez_list(cam)
				row_count = 1 
				self.popupMenu = OptionMenu(self.mainframe, self.rez_choice, *self.rez_list)
				Label(self.mainframe, text="Resolution", bg="gray", fg="white").grid(row = 1, column = 1)
				self.popupMenu.grid(row = 2, column =1)	
				self.popupMenu.configure(background="gray")


	def start_gui(self):
		self.get_cam_list() # Create Cam list from arricams dictionary
		self.root = Tk()
		self.root.configure(background='grey')
		self.root.title("Camera Data Calculator v" + str(VERSION))
		self.cam_var = StringVar()
		self.cam_var.set(self.camlist[0])

		self.get_rez_list("Alexa 65") # set default Alexa65 rez list

		#canvas = Canvas(root, width = 300, height = 300)  
		# canvas = tkinter.Canvas(self.root, width = width, height = height)
		# canvas.grid()
		# img = PIL.ImageTk.PhotoImage(image ="Codex Ring 2018.png")    
		# canvas.create_image(20,20, anchor=NW, image=img)
		self.gui_elements()

	def gui_elements(self):

		# SET Data Rate and Duration Info 
		Label(self.root, text="				", bg="gray", fg="white").grid(row=(len(self.arri_cams) + 2), column=1, sticky=(N,W,E,S))
		Label(self.root, text="				", bg="gray", fg="white").grid(row=(len(self.arri_cams) + 3), column=1, sticky=(N,W,E,S))
		self.clear_fps() # set dummy value so it can be removed when switching views

		
		# Create Camera Radiobuttons
		Label(self.root, text="Camera:", bg="grey", fg="white").grid(row=0, column=0, sticky=W)
		row_count = 1
		for item in self.camlist:
		    button = Radiobutton(self.root, text=item, variable=self.cam_var, value=item, command=self.rez_select, bg="gray", fg="white")
		    button.grid(row=row_count, sticky=W)
		    button.configure(foreground = "white")
		    row_count += 1

		# Create Resolution Dropdown    
		## Add a grid
		self.mainframe = Frame(self.root)
		self.mainframe.grid(column=2,row=0, sticky=(N,W,E,S) )
		self.mainframe.columnconfigure(0, weight = 1)
		self.mainframe.rowconfigure(0, weight = 1)
		self.mainframe.configure(background="gray")
		
		## Create a Tkinter variable
		self.rez_choice = StringVar(self.root)
		 
		## Dictionary with options
		self.rez_choice.set('Select') # set the default option
		 
		self.popupMenu = OptionMenu(self.mainframe, self.rez_choice, *self.rez_list)
		Label(self.mainframe, text="Resolution", bg="gray", fg="white").grid(row = 1, column = 1)
		self.popupMenu.grid(row = 2, column =1)
		self.popupMenu.configure(background="gray")
		 
		## on change dropdown value
		def change_dropdown(*args):
		    print( self.rez_choice.get() )
		 
		## link function to change dropdown
		self.rez_choice.trace('w', change_dropdown)

		## FPS Dialog
		self.fps_label = Label(self.root, text="FPS:", bg="gray", fg="white")
		self.fps_label.grid(row=1, column=1, sticky=(N,W,E,S))
		self.fps = StringVar()
		self.fps_box = Entry(textvariable=self.fps, width = 1)
		self.fps_box.grid(column=1, row=2, sticky=(N,W,E,S))
		self.fps_box.insert(0, "24")

		## Data Size Dialog
		self.dsize_label = Label(self.root, text="Data Size (for Duration)", bg="gray", fg="white")
		self.dsize_label.grid(row=3, column=1, sticky=(N,W,E,S))
		self.dsize = StringVar()
		self.dsize_box = Entry(textvariable=self.dsize, width = 1)
		self.dsize_box.grid(column=1, row=4, sticky=(N,W,E,S))
		self.dsize_box.insert(0, "0")

		## Duration Dialog
		self.dur_box_label = Label(self.root, text="Duration (for Data Size)", bg="gray", fg="white")
		self.dur_box_label.grid(row=5, column=1, sticky=(N,W,E,S))
		self.dur = StringVar()
		self.dur_box = Entry(textvariable=self.dur, width = 1)
		self.dur_box.grid(column=1, row=6, sticky=(N,W,E,S))
		self.dur_box.insert(0, "0")

		#__________________________________________________________
		## BUTTONS

		### Data Rate Button
		drate_but_row = len(self.arri_cams) + 3
		self.a = Button(self.root, text="Data Rate", command=self.data_rate, bg="gray")
		#a.grid(row=drate_but_row, column=0)
		self.a.grid(row=2, column=2)
		self.a.configure(background="gray")

		# Label for result
		drate_but_row = len(self.arri_cams) + 3
		self.drate_label = Label(self.root, text="Date Rate:", bg="gray")
		self.drate_label.grid(row=drate_but_row, column=0)


		### Duration Button
		dur_but_row = len(self.arri_cams) + 4
		self.b = Button(self.root, text=" Duration ", command=self.duration, bg="gray")
		#b.grid(row=dur_but_row, column=0)
		self.b.grid(row=4, column=2)
		self.b.configure(background="gray")

		# Label for result
		dur_but_row = len(self.arri_cams) + 4
		self.dur_but_label = Label(self.root, text="Duration:", bg="gray")
		self.dur_but_label.grid(row=dur_but_row, column=0)


		### Data Size Button
		data_but_row = len(self.arri_cams) + 5
		self.c = Button(self.root, text="Data Size ", command=self.data_size, bg="gray")
		#c.grid(row=data_but_row, column=0)
		self.c.grid(row=6, column=2)
		self.c.configure(background="gray")

		# Label for result
		data_but_row = len(self.arri_cams) + 5
		self.data_size_label = Label(self.root, text="Data Size:", bg="gray")
		self.data_size_label.grid(row=data_but_row, column=0)


		## FPS Button
		self.d = Button(self.root, text="FPS", command=self.fps_from_data_dur, bg="gray")
		self.d.grid(row=8, column=2)
		self.d.configure(background="gray")


		## ABOUT BUTTON
		self.about_button = Button(self.root, text="About", command=self.about, bg="gray")
		self.about_button.grid(row=0, column = 1, sticky=W)
		self.about_button.configure(background="gray")


		## DATA TOOLS BUTTON
		self.dt_button = Button(self.root, text="Data Tools", command=self.data_tools, bg="gray")
		self.dt_button.grid(row=0, column = 1, sticky="E")
		self.dt_button.configure(background="gray")	



		#__________________________________________________________
		## STATUS 
		self.status_update()


		# Codex Logo
		logo = PhotoImage(data=open('Codex Ring 2018.gif').read(), format='gif')
		Label(self.root, image=logo, bg="grey", fg="red").grid(row=0, column=0, sticky=("N,S,E,W"))



		self.root.mainloop()

	##_____________________________________________________________________________	

	def data_tools(self):
		## CLEAR UI
		Label(self.root, text="                    ", bg="gray").grid(row=1, column=0, sticky=W)
		Label(self.root, text="                    ", bg="gray").grid(row=8, column=0, sticky=W)
		self.about_button.grid_remove()
		self.a.grid_remove()
		self.b.grid_remove()
		self.c.grid_remove()
		self.d.grid_remove()
		self.fps_box.grid_remove()
		self.fps_label.grid_remove()
		self.dsize_box.grid_remove()
		self.dsize_label.grid_remove()
		self.dur_box.grid_remove()
		self.dur_box_label.grid_remove()
		self.mainframe.grid_remove()
		self.dur_but_label.grid_remove()
		self.drate_label.grid_remove()
		self.data_size_label.grid_remove()
		self.status_label.grid_remove()
		self.dt_button.grid_remove()
		self.fps_result_label.grid_remove()
		try:
			self.calc_dur_label.grid_remove()
		except:
			pass
		try:
			self.data_size_label.grid_remove()
		except:
			pass
		try:
			self.calc_dur_label.grid_remove()
		except:
			pass
		try:
			self.data_rate_label.grid_remove()
		except:
			pass
		try:
			self.fps_result_label.grid
		except:
			pass


		self.start_dt_gui()


	#__________________________________________________________
	##	Status and Error Functions
	#__________________________________________________________

	# Print Status in Status Bar
	def status_update(self):
		status_row = len(self.arri_cams) + 6
		if self.error == None:
			status_message = "Ready"
			self.status_label = Label(self.root, text=status_message, bg="grey", fg="white")
			self.status_label.grid(row=status_row, column=1, sticky=(N,W,E,S))
		else:
			status_message = self.error
			self.status_label = Label(self.root, text=status_message, bg="grey", fg="red")
			self.status_label.grid(row=status_row, column=1, sticky=(N,W,E,S))

	# Check Resolution is set.  Error in Status bar if not!
	def rez_error(self):   
		if self.rez_choice.get() == "Select":
		 	self.error = "No Resolution Selected"
		 	self.status_update() 


	#__________________________________________________________
	## ABOUT BUTTON FUNCTION
	#__________________________________________________________
	def about(self):
		print "About"
		self.about_root = Tk()
		self.about_root.configure(background='grey')
		self.about_root.title("About Camera Data Calculator v" + str(VERSION))
		Label(self.about_root, text=self.about_text, bg="grey", fg="black", justify=tk.LEFT).grid(row=0, column=0, sticky=W)
		self.about_root.mainloop()



	#__________________________________________________________
	## Data Rate Function
	#__________________________________________________________
 
	def data_rate(self):
		self.error = None
		self.status_update()
		drate_but_row = len(self.arri_cams) + 3
		cam = self.cam_var.get()
		self.rez_error()  # check resolution is set 
		rez = self.rez_choice.get()
		mode = "ARRIRAW"
		c_fps = self.fps.get()
		frame_size = self.arri_cams[cam][mode][rez]["file_size"]
		res = round((float(c_fps) * float(frame_size) / 1.0), 2)
		result = "Data Rate is " + str(res) + " MB/s"
		self.data_rate_label = Label(self.root, text=result, bg="grey")
		self.data_rate_label.grid(row=drate_but_row, column=1, sticky=(N,W,E,S))

	#__________________________________________________________
	## Duration Functions

	def duration(self):
		self.error = None
		self.status_update()
		## Clear FPS Readout
		self.clear_fps()
		self.rez_error()  # check resolution is set

		cam = self.cam_var.get()
		rez = self.rez_choice.get()
		mode = "ARRIRAW"
		c_fps = self.fps.get()
		d_size = self.dsize.get()
		frame_size = self.arri_cams[cam][mode][rez]["file_size"]
		bandwidth = float(frame_size) * float(c_fps)

		### Set Split point
		fs_split = d_size.find(" ")

		### Test if first part of split is a number
		try:
			float(d_size[:fs_split])
		except:
			self.error = "Invalid entry for 'Data Size'"
			self.status_update()
			return

		### Split Digits from Units
		f_size = float(d_size[:fs_split])
		f_units = d_size[fs_split + 1:]


		### Validate Digits and Units
		data_calc2 = Data_calculator()
		if not data_calc2.valid_digit(f_size):
			self.error = "Invalid entry for 'Data Size'"
			self.status_update()
			return
		if not data_calc2.valid_unit(f_units):
			self.error = "Invalid unit for 'Data Size'"
			self.status_update()
			return

		# Make Calculations
		file_size = f_size * self.units[f_units]
	 	secs = file_size / (bandwidth * self.units["MB"])
		dur_but_row = len(self.arri_cams) + 4
		res, frac= data_calc2.convert_seconds(secs)
		result = str(res) + " " + str(int(float(frac) * float(self.fps.get()))) + " fr"
		self.calc_dur_label = Label(self.root, text=result, bg="grey")
		self.calc_dur_label.grid(row=dur_but_row, column=1, sticky=(N,W,E,S))


	def split_input(self, d_size):
		fs_split = d_size.find(" ")

		### Test if first part of split is a number
		try:
			float(d_size[:fs_split])
		except:
			self.error = "Invalid entry for 'Data Size'"
			self.status_update()
			return

		### Split Digits from Units
		f_size = float(d_size[:fs_split])
		f_units = d_size[fs_split + 1:]


		### Validate Digits and Units
		data_calc2 = Data_calculator()
		if not data_calc2.valid_digit(f_size):
			self.error = "Invalid entry for 'Data Size'"
			self.status_update()
			return
		if not data_calc2.valid_unit(f_units):
			self.error = "Invalid unit for 'Data Size'"
			self.status_update()
			return

		return f_size, f_units



	# # Calculate Duration in secs based on Data Size 
	# def dur_secs(self):
	# 	cam = self.cam_var.get()
	# 	rez = self.rez_choice.get()
	# 	mode = "ARRIRAW"
	# 	c_fps = self.fps.get()
	# 	d_size = self.dsize.get()
	# 	frame_size = self.arri_cams[cam][mode][rez]["file_size"]
	# 	bandwidth = float(frame_size) * float(c_fps)

	# 	if self.split_input(d_size):
	# 		f_size, unit, error = self.split_input(d_size)
	# 	else:
	# 		return False

	# 	if error:
	# 		self.error = error
	# 		self.status_update()

	# 	else:
	# 		file_size = f_size * self.units[unit]
	# 		secs = file_size / (bandwidth * self.units["MB"])
	# 		return secs

	# # and display result next to Duration box
	# def duration(self):
	# 	self.error = None
	# 	self.status_update()
	# 	## Clear FPS Readout
	# 	self.clear_fps()

	# 	self.rez_error()  # check resolution is set

	# 	secs = self.dur_secs()
	# 	dur_but_row = len(self.arri_cams) + 4
	# 	data_calc2 = Data_calculator()
	# 	res, frac= data_calc2.convert_seconds(secs)
	# 	result = str(res) + " " + str(int(float(frac) * float(self.fps.get()))) + " fr"
	# 	Label(self.root, text=result, bg="grey").grid(row=dur_but_row, column=1, sticky=(N,W,E,S))

	def clear_dur(self):
		dur_but_row = len(self.arri_cams) + 4
		Label(self.root, text="                              ", bg="grey").grid(row=dur_but_row, column=1, sticky=(N,W,E,S))

	# # Split the Data Size input in value and unit	
	# def split_input(self, fs):
	# 	data_calc2 = Data_calculator()
	# 	fs_split = fs.find(" ")
	# 	error = False
	# 	try:
	# 		float(fs[:fs_split])
	# 	except:
	# 		self.error = "Invalid entry for 'Data Size'"
	# 		self.status_update()
	# 		error = True
	# 		return False
	# 	file_size = float(fs[:fs_split])
	# 	f_units = fs[fs_split + 1:]
	# 	if not data_calc2.valid_digit(file_size):
	# 		self.error = "Invalid entry for 'Data Size'"
	# 		self.status_update()
	# 		error = True
	# 		return False
	# 	if not data_calc2.valid_unit(f_units):
	# 		self.error = "Invalid unit for 'Data Size'"
	# 		self.status_update()
	# 		error = True
	# 		return False
	# 	return file_size, f_units, error




	#_________________________________________________________
	## SPLIT DATA TOOLS

	# Split the Data Size input in value and unit	
	def split_input_dt(self, fs):
		data_calc2 = Data_calculator()
		fs_split = fs.find(" ")
		try:
			float(fs[:fs_split])
		except:
			self.error = "Invalid entry for 'Data Size'"
			self.cam_tools_status_update()
		file_size = float(fs[:fs_split])
		f_units = fs[fs_split + 1:]
		if not data_calc2.valid_digit(file_size):
			self.error = "Invalid entry for 'Data Size'"
			self.status_update()
		if not data_calc2.valid_unit(f_units):
			self.error = "Invalid unit for 'Data Size'"
			self.status_update()
		return file_size, f_units



	#__________________________________________________________
	##  Data Size Functions

	def data_size(self):
		## Reset Error status to None
		self.error = None
		self.status_update()

		## Clear FPS Readout
		self.clear_fps()

		## Validate Duration Input 
		if not self.validate_dur_string(self.dur.get()):  # Validate Duration Input 
			self.data_size_error()
			return

		cam = self.cam_var.get()  # Which Camera has been chosen with Radio Buttons?
		self.rez_error()  # check resolution is set
		rez = self.rez_choice.get() # Set Resolution
		mode = "ARRIRAW"  # Set Mode
		c_fps = self.fps.get() # Get FPS from FPS Input Box
		frame_size = self.arri_cams[cam][mode][rez]["file_size"]  # Get Frame Size from Camera Dict

		secs, frames = self.convert_time()  # Convery Duration Input into Seconds and Frames

		res = (float(frame_size) * float(c_fps) * secs) + (float(frame_size) * float(frames))  # Calculate result in MBs

		## Set which unit to display result, dependant on size.
		if res > 999999.99:
			data_calc2 = Data_calculator()
			res = data_calc2.conv_datarate_per_sec(res, "MB", "TB")
			result = str(res) + " TBs"
		elif res > 999.99:
			data_calc2 = Data_calculator()
			res = data_calc2.conv_datarate_per_sec(res, "MB", "GB")
			result = str(res) + " GBs"
		else:
			result = str(res) + " MBs"

		## Display result next to "Data Size" button	
		data_but_row = len(self.arri_cams) + 5
		self.data_size_label = Label(self.root, text=result, bg="grey")
		self.data_size_label.grid(row=data_but_row, column=1, sticky=(N,W,E,S))

	def clear_dsize(self):
		data_but_row = len(self.arri_cams) + 5
		Label(self.root, text="                   ", bg="grey").grid(row=data_but_row, column=1, sticky=(N,W,E,S))



	# Validate Duration Input
	def validate_dur_string(self, dur_string): # REady TO IMPLEMENT!!!	
		hmsf_list = ["h", "m", "s", "f"]
		if not any(hmsf in dur_string for hmsf in hmsf_list):
			print "not found"
			return False
		if not any(hmsf in dur_string[-1:] for hmsf in hmsf_list):
			print "Last entry did not contain h, m, s or f"
			return False
		else:
			return True

	# If Duration Input validate unsuccessful, print error.
	def data_size_error(self):
		self.error = "Define Duration: e.g. '1h 2m 3s 4f'"
		self.status_update()
		result = "Incorrect values entered!"
		data_but_row = len(self.arri_cams) + 5
		Label(self.root, text="Invalid Duration Syntax!", bg="grey").grid(row=data_but_row, column=1, sticky=(N,W,E,S))


	# Convert Duration Input into Seconds and Frames for data_size() function to calulate
	def convert_time(self):
		dur_string = self.dur.get()
		hours, mins, secs, frames = self.convert_hmsf(dur_string)
		data_calc2 = Data_calculator()
		return data_calc2.how_many_seconds(hours, mins, secs), frames

	def convert_hmsf(self, dur_string):
		hours = 0
		mins = 0
		secs = 0
		frames = 0
		for i in str(dur_string):
			if i == "h":
				hours = dur_string[:dur_string.find("h")]
				dur_string = dur_string[dur_string.find("h")+2:]
				print dur_string
		for i in str(dur_string):	
			if i == "m":
				mins = dur_string[:dur_string.find("m")]
				dur_string = dur_string[dur_string.find("m")+2:]
		for i in str(dur_string):	
			if i == "s":
				secs = dur_string[:dur_string.find("s")]
				dur_string = dur_string[dur_string.find("s")+2:]
		if dur_string:	
		 	frames = dur_string[:-1]
		return hours, mins, secs, frames



	#__________________________________________________________
	## FPS from Data Size & Duration Function
	#__________________________________________________________
 	def calc_fps(self):
 		self.error = None # Reset error
		self.status_update()
		self.rez_error()  # check resolution is set
	




 	def fps_from_data_dur(self):
 		self.error = None
		self.status_update()
		self.clear_dur() # Clear Duration readout
		self.clear_dsize() # Clear Data Size readout
		self.rez_error()  # check resolution is set

		## Validate Duration
		if not self.validate_dur_string(self.dur.get()):
			self.error = "Invalid Duration!"
			self.status_update()
			return 
		
		secs, frames = self.convert_time()	

		## Validtae Data Size
		if not self.split_input(self.dsize.get()):
			return

		## Calculate FPS
		file_size, unit = self.split_input(self.dsize.get())
		frame_size = self.arri_cams[self.cam_var.get()]["ARRIRAW"][self.rez_choice.get()]["file_size"]  # Get Frame Size from Camera Dict
		data_calc2 = Data_calculator()
		fs_in_mb = data_calc2.convert_unit(file_size, unit, "MB") + (float(frame_size) * float(frames))
		mb_per_sec = fs_in_mb / secs
		num_frames = fs_in_mb / frame_size
		fps, mb_per_sec = (num_frames / secs), mb_per_sec
		if len(str(fps)) >= 5:  # Round FPS to 2 decimal places
			fps = round(fps,2)
		fps = str(fps)
		result = fps + " FPS (" + str(round(mb_per_sec, 2)) + " MB/s)"

		self.fps_result_label = Label(self.root, text=result, bg="grey", fg="black")
		self.fps_result_label.grid(row=8, column=1, sticky=(N,W,E,S))


	## Clear FPS Function	
	def clear_fps(self):
		self.fps_result_label = Label(self.root, text="         ", bg="grey", fg="black")
		self.fps_result_label.grid(row=8, column=1, sticky=(N,W,E,S))



##################################################################################################
# DATA TOOLS CLASS
##################################################################################################


# class Data_tools_gui():
# 	def __init__(self, root):
# 		self.root = root
# 		self.arri_cams = json.load(open('arri_cams.json', 'r'), object_pairs_hook=OrderedDict)


	#______________________________________________________________________
	# Data Tools Status Update

	def cam_tools_status_update(self):
		status_row = 14
		if self.error == None:
			status_message = "Ready"
			self.cam_status_label = Label(self.root, text=status_message, bg="grey", fg="white")
			self.cam_status_label.grid(row=status_row, column=1, sticky=(N,W,E,S))
		else:
			status_message = self.error
			self.cam_status_label = Label(self.root, text=status_message, bg="grey", fg="red")
			self.cam_status_label.grid(row=status_row, column=1, sticky=(N,W,E,S))

	def reset_cam_tools_status(self):
		self.error = None
		self.cam_tools_status_update()


	#______________________________________________________________________
	# Data Tools GUI

	def start_dt_gui(self):

		# Remove Cam Tools Status and reset Data Tools status to "Ready"
		self.error = "                               "
		self.status_update()
		self.reset_cam_tools_status()


		
		## Title
		self.gen_title_label = Label(self.root, text="GENERAL DATA TOOLS", bg="gray", fg="black")
		self.gen_title_label.grid(row=0, column=1, sticky=W)

		

		## Calc Data Copy time
		self.copy_time_label = Label(self.root, text="Calculate Copy Time:", bg="gray", fg="black")
		self.copy_time_label.grid(row=2, column=0, sticky=W)


		self.ct_data_label = Label(self.root, text="File Size", bg="gray", fg="white")
		self.ct_data_label.grid(row=2, column=0, sticky=E)
		self.ct_bw_label = Label(self.root, text="Bandwidth i.e. 10 Gb", bg="gray", fg="white")
		self.ct_bw_label.grid(row=2, column=1, sticky=E)


		self.copy_file_size = StringVar()
		
		self.copy_fs_box = Entry(textvariable=self.copy_file_size, width = 1)
		self.copy_fs_box.grid(column=0, row=3, sticky=(N,W,E,S))
		self.copy_fs_box.insert(0, "1 TB")

		self.copy_rate = StringVar()
		self.copy_rate_box = Entry(textvariable=self.copy_rate, width = 1)
		self.copy_rate_box.grid(column=1, row=3, sticky=(N,W,E,S))
		self.copy_rate_box.insert(0, "250 MB")




		## Calc Data Rate

		### File Size box
		self.dr_label = Label(self.root, text="Calculate Data Rate: ", bg="gray", fg="black")
		self.dr_label.grid(row=4, column=0, sticky=W)
		self.dr_file_size = StringVar()

		self.dr_data_label = Label(self.root, text="File Size", bg="gray", fg="white")
		self.dr_data_label.grid(row=4, column=0, sticky=E)

		self.dr_secs_label = Label(self.root, text="Seconds", bg="gray", fg="white")
		self.dr_secs_label.grid(row=4, column=1, sticky=W)

		self.unit_for_dr_label = Label(self.root, text="Unit", bg="gray", fg="white")
		self.unit_for_dr_label.grid(row=4, column=1, sticky=E)

		self.dr_fs_box = Entry(textvariable=self.dr_file_size, width = 1)
		self.dr_fs_box.grid(column=0, row=5, sticky=(N,W,E,S))
		self.dr_fs_box.insert(0, "")

		### Seconds box
		self.secs_to_copy = StringVar()
		self.secs_to_copy_box = Entry(textvariable=self.secs_to_copy, width = 16)
		self.secs_to_copy_box.grid(column=1, row=5, sticky=W)
		self.secs_to_copy_box.insert(0, "")


		### Unit for Data Rate Conversion
		self.unit_for_dr = StringVar()
		self.unit_for_dr_box = Entry(textvariable=self.unit_for_dr, width = 3)
		self.unit_for_dr_box.grid(column=1, row=5, sticky=E)
		self.unit_for_dr_box.insert(0, "")




		## Convert Data Rate

		### Original Data Rate
		self.og_rate_label = Label(self.root, text="Convert Data Rate: ", bg="gray", fg="black")
		self.og_rate_label.grid(row=6, column=0, sticky=W)
		self.og_rate = StringVar()


		self.cr_data_label = Label(self.root, text="DataRate", bg="gray", fg="white")
		self.cr_data_label.grid(row=6, column=0, sticky=E)
		self.cr_units_label = Label(self.root, text="Unit per sec to Convert e.g 'MB'", bg="gray", fg="white")
		self.cr_units_label.grid(row=6, column=1, sticky=E)



		self.og_rate = Entry(textvariable=self.og_rate, width = 1)
		self.og_rate.grid(column=0, row=7, sticky=(N,W,E,S))
		self.og_rate.insert(0, "")

		### Unit to Convert to
		self.conv_unit = StringVar()
		self.conv_unit_box = Entry(textvariable=self.conv_unit, width = 3)
		self.conv_unit_box.grid(column=1, row=7, sticky=E)
		self.conv_unit_box.insert(0, "")



		## Convert Seconds
		self.secs_label = Label(self.root, text="Convert Seconds", bg="gray", fg="black")
		self.secs_label.grid(row=8, column=0, sticky=(N,W,E,S))
		self.secs_to_conv = StringVar()
		self.secs_box = Entry(textvariable=self.secs_to_conv, width = 1)
		self.secs_box.grid(column=0, row=9, sticky=(N,W,E,S))
		self.secs_box.insert(0, "0")


		## Convert Hours, Mins & Seconds
		self.hms_label = Label(self.root, text="Convert Hours, Minutes and Seconds", bg="gray", fg="black")
		self.hms_label.grid(row=10, column=0, sticky=(N,W,E,S))
		self.hms = StringVar()
		self.hms_box = Entry(textvariable=self.hms, width = 1)
		self.hms_box.grid(column=0, row=11, sticky=(N,W,E,S))
		self.hms_box.insert(0, "0")



		## DATA TOOLS BUTTON
		self.dc_button = Button(self.root, text="Cam Tools", command=self.cam_tools, bg="gray")
		self.dc_button.grid(row=0, column = 2, sticky=E)
		self.dc_button.configure(background="gray")	

		## DATA COPY BUTTON
		self.data_copy_button = Button(self.root, text="Do It!", command=self.calc_data_copy_time, bg="gray")
		self.data_copy_button.grid(row=3, column = 2, sticky=E)
		self.data_copy_button.configure(background="gray")	

		## CALCULATE DATA RATE BUTTON
		self.data_rate_button = Button(self.root, text="Do It!", command=self.calc_datarate, bg="gray")
		self.data_rate_button.grid(row=5, column = 2, sticky=E)
		self.data_rate_button.configure(background="gray")	


		## CALCULATE DATA RATE BUTTON
		self.conv_rate_button = Button(self.root, text="Do It!", command=self.conv_datarate, bg="gray")
		self.conv_rate_button.grid(row=7, column = 2, sticky=E)
		self.conv_rate_button.configure(background="gray")	

		## CONVERT SECONDS
		self.conv_secs_button = Button(self.root, text="Do It!", command=self.conv_secs, bg="gray")
		self.conv_secs_button.grid(row=9, column = 2, sticky=E)
		self.conv_secs_button.configure(background="gray")	

		## CONVERT HOURS, MINS, SECS BUTTON
		self.hms_button = Button(self.root, text="Do It!", command=self.conv_hms, bg="gray")
		self.hms_button.grid(row=11, column = 2, sticky=E)
		self.hms_button.configure(background="gray")	


		## RESULTS LABEL

		self.spacer = Label(self.root, text="_______________ ", bg="gray", fg="white")
		self.spacer.grid(row=12, column=0, sticky=W)

		self.results_heading = Label(self.root, text="RESULTS: ", bg="gray", fg="black")
		self.results_heading.grid(row=13, column=0, sticky=W)

		# Empty results label
		self.results = Label(self.root, text="" , bg="gray", fg="black")


		self.cam_tools_status_update()

		# self.root.mainloop()



	## DATA TOOLS FUNCTIONS

	def calc_data_copy_time(self):
		self.clear_results()
		self.reset_cam_tools_status()
		data_calc2 = Data_calculator()
		
		# Split File Size and Unit and check for errors
		file_size, f_units, error = data_calc2.split_input(self.copy_file_size.get()) 
		if error:
			self.error = error
			self.cam_tools_status_update()
			return

		# Split Bandwidth value and Unit and check for errors
		bandwidth, b_units, error = data_calc2.split_input(self.copy_rate.get())
		if error:
			self.error = error
			self.cam_tools_status_update()
			return
		
		res, frames = data_calc2.download_time(file_size, f_units, bandwidth, b_units)
		if not res:
			print "no res"
		self.update_results(res)


	def calc_datarate(self):
		self.clear_results()
		self.reset_cam_tools_status()
		data_calc2 = Data_calculator()

		# Split File Size and Unit and check for errors
		file_size, f_units, error = data_calc2.split_input(self.dr_file_size.get()) 
		if error:
			self.error = error
			self.cam_tools_status_update()
			return

		secs = self.secs_to_copy.get()
		if not data_calc2.valid_digit(secs):
			self.error = "Invalid digit for Seconds"
			self.cam_tools_status_update()
			return

		b_units = self.unit_for_dr.get()
		print b_units
		if not data_calc2.valid_unit(b_units):
			self.error = "Invalid Unit entered!"
			self.cam_tools_status_update()
			return

		res = data_calc2.data_rate(file_size, f_units, b_units, secs)

		self.update_results(res)


	def conv_datarate(self):
		self.clear_results()
		self.reset_cam_tools_status()
		data_calc2 = Data_calculator()

		data_rate, unit, error = data_calc2.split_input(self.og_rate.get()) 
		if error:
			self.error = error
			self.cam_tools_status_update()
			return

		return_unit = self.conv_unit.get()
		if not data_calc2.valid_unit(return_unit):
			self.error = "Invalid Unit to Convert to!"
			self.cam_tools_status_update()
			return

		result = data_calc2.convert_unit(data_rate, unit, return_unit)
		res = str(result) + " " + return_unit + "/s"
		self.update_results(res)


	def conv_secs(self):
		self.clear_results()
		self.reset_cam_tools_status()
		data_calc2 = Data_calculator()
		res, frac = data_calc2.convert_seconds(float(self.secs_to_conv.get()))	
		self.update_results(res)
		
	def conv_hms(self):
		self.clear_results()
		self.reset_cam_tools_status()
		if not self.validate_dur_string(self.hms.get()):  # Validate Duration Input 
			self.error = "Define Duration e.g. '1h 2m 3s"
			self.cam_tools_status_update()
			return
		hours, mins, secs, frames = self.convert_hmsf(self.hms.get())
		data_calc2 = Data_calculator()
		res = str(data_calc2.how_many_seconds(hours, mins, secs)) + " seconds"
		self.update_results(res)

	
	## FUNCTION TO PRINT RESULTS FOR ALL DATA TOOLS 
	def update_results(self, result):
		self.results = Label(self.root, text=result , bg="gray", fg="black")
		self.results.grid(row=13, column=1, sticky=W)

	## CLEAR DATA TOOLS RESULTS
	def clear_results(self):
		self.results.grid_remove()
		data_calc2 = Data_calculator()


	## SWITCH BACK TO CAMERA TOOLS PAGE
	def cam_tools(self):
		self.copy_time_label.grid_remove()
		self.copy_fs_box.grid_remove()
		self.dr_label.grid_remove()
		self.dr_fs_box.grid_remove()
		self.secs_label.grid_remove()
		self.secs_box.grid_remove()
		self.hms_label.grid_remove()
		self.hms_box.grid_remove()
		self.og_rate_label.grid_remove()
		self.og_rate.grid_remove()
		self.conv_unit_box.grid_remove()
		self.status_label.grid_remove()
		self.dc_button.grid_remove()
		self.data_copy_button.grid_remove()
		self.data_rate_button.grid_remove()
		self.conv_rate_button.grid_remove()
		self.spacer.grid_remove()
		self.results_heading.grid_remove()
		self.conv_rate_button.grid_remove()
		self.conv_secs_button.grid_remove()
		self.hms_button.grid_remove()
		self.gen_title_label.grid_remove()
		self.ct_bw_label.grid_remove()
		self.dr_data_label.grid_remove()
		self.ct_data_label.grid_remove()
		self.secs_to_copy_box.grid_remove()
		self.unit_for_dr_label.grid_remove()
		self.cam_status_label.grid_remove()

		self.error = "                               "
		self.cam_tools_status_update()

		self.gui_elements()



