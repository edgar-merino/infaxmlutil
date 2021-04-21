#!/usr/bin/env python3
# standard libraries
import sys
import os

def basename(path):
	return os.path.basename(os.path.normpath(path))

def get_exec_path():
	if getattr(sys, 'frozen', False):
		# If the application is run as a bundle, the PyInstaller bootloader
		# extends the sys module by a flag frozen=True and sets the app 
		# path into variable _MEIPASS'.
		return sys._MEIPASS
	else:
		return os.path.dirname(os.path.abspath(__file__))

def get_local_path():
	'''returns the path where the application is executed'''
	return get_exec_path()

