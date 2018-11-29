#!/usr/bin/python

## Data Rate and Bandwidth Calculator Class

import os


class Data_calculator:
	def __init__(self):
		self.secs = "Undefined"	
		self.secs_answer = "Undefined"	
		self.units = {"kb":1024, "kiB":8192, "kB":8000, "Mb":1048576, "MiB":8388608, "MB":8000000, "Gb":1073741824, "GiB":8589934592, "GB":8000000000, "Tb":1099511627776, "TiB":8796093022208, "TB":8000000000000, "PB":8000000000000000}
		self.units_supported = "Units supported:  kb, kiB, kB, Mb, MiB, MB, Gb, GiB, GB, Tb, TiB, and TB"


	## CONVERT SECONDS TO HOURS, MINUTES AND SECONDS.	
	def convert_seconds(self, secs):
	    frac = secs % 1
	    frac = float(frac)
	    secs = int(secs)
	    hours = secs / 3600
	    if hours:
	        secs = secs - (hours * 3600)
	    mins = secs / 60
	    if mins:
	        secs = secs - (mins * 60)
	    # if frac != 0:    
	    #     secs = secs + frac

	    # if hours:
	    # 	secs = int(secs)
	    # if mins:
	    # 	secs = int(secs)	
	    if hours == 1:
	        h_string = str(hours) + " hr, "
	    else:
	        h_string = str(hours) + " hrs, "
	    if mins == 1:
	        m_string = str(mins) + " min, "
	    else:
	        m_string = str(mins) + " mins, "
	    if secs == 1:
	        s_string = str(secs) + " sec"
	    else:
	        s_string = str(secs) + " secs" 

	    if hours: 
	    	ans = h_string + m_string + s_string
	    	return ans, frac
	    if mins:
	    	ans = (m_string + s_string)
	    	return ans, frac
	    else:
			ans = (s_string)
			return ans, frac


	def valid_unit(self, unit):
		if unit in self.units:
			return unit
		else:
			return False


	## Validate if a string can be converted into an into float
	def valid_digit(self, num):
		try:
			if int(num):
				return int(num)
		except:
			pass
		try:
			if float(num):
				return float(num)
		except:
			return False


	def split_input(self, fs):
		error = None
		fs_split = fs.find(" ")
		file_size = fs[:fs_split]
		f_units = fs[fs_split + 1:]
		if not self.valid_digit(file_size):
			error = "Invalid Digits"
			return 1, "MB", error    #default returns
		if not self.valid_unit(f_units):
			error = "Invalid Unit"
			return 1, "MB", error    #default returns
		return float(file_size), f_units, error


	## Calculate donwload time based on file size and bandwidth
	def download_time(self, file_size, f_units, bandwidth, b_units):
	    file_size = (file_size + 0.0) * self.units[f_units]
	    bandwidth = (bandwidth + 0.0) * self.units[b_units]
	    secs = file_size / bandwidth
	    return self.convert_seconds(secs)



	## Calculate data_rate based on filesize and time.
	def data_rate(self, file_size, f_units, b_units, secs):
		file_size = (file_size + 0.0) * self.units[f_units]
		bandwidth = (file_size / float(secs)) / self.units[b_units]
		return str(bandwidth) + " " + b_units + " per second."


	def conv_datarate_per_sec(self, rate, f_units, b_units):
		return float((rate * self.units[f_units]) / self.units[b_units])


	## Fuction to convert hours, secs and mins into seconds
	def how_many_seconds(self, hours, mins, secs):
		hours = float(hours)
		mins = float(mins)
		secs = float(secs)
		return (hours * 3600) + (mins * 60) + secs


	def convert_unit(self, file_size, unit, return_unit):
		file_size = (file_size + 0.0) * self.units[unit]
		return file_size / self.units[return_unit]











		


    	
