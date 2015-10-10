import os

def create_folder(folder_path):
	""" Create folder based on folder path given
		Args:
			folder_path (str): full path of folder.
	
	"""
	if not os.path.exists(folder_path): os.makedirs(folder_path)