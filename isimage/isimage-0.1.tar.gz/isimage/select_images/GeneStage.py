""" Utility module for command line script select_images
"""
# Author: Ilya Patrushev ilya.patrushev@gmail.com

# License: GPL v2.0

import matplotlib.pyplot as plt

from isimage import Image

from check_cleared import check_cleared
from score_images import score_images

import numpy as np

import os

class ImageGroup(object):
	""" Class doc """
	
	def __init__ (self, images):
		""" Class initialiser """
		self.images = images
		if len(self.images) == 0:
			return
			
	def best (self):
		""" Function doc """
		assert( all([hasattr(img, "score") for img in self.images]))
		
		return self.images[np.argmax([img.score for img in self.images])]
			
	def __getitem__ (self, index):
		""" Function doc """
		return self.images[index]
		
	def __setitem__(self, index, value):
		""" Function doc """
		self.images[index] = value
		
	def __len__(self):
		""" Function doc """
		return len(self.images)
		
	def dry (self):
		""" Function doc """
		for img in self.images:
			if hasattr(img, "img"):
				del img.img
			if hasattr(img, "mask"):
				del img.mask
			if hasattr(img, "outline"):
				del img.outline
			if hasattr(img, "pattern"):
				del img.pattern	
			if hasattr(img, "pigment"):
				del img.pigment
				
	def save(self, path, append=[]):
		""" Function doc """
			
		for i, img  in enumerate(sorted(self.images, key=lambda x: -x.score)):
			
			l, r, t, b = img.rect
			name = os.path.split(img.name)[-1].split('.')
			app = append + [str(i), str(l), str(t), str(r-l), str(b-t)]
			name = '.'.join(name[:-1] + ['_'.join(app)] + name[-1:])
			
			assert(hasattr(img, "img"))
			img.saved_name = os.path.join(path, name)
			plt.imsave(img.saved_name, img.img)
			
				
class GeneStage(object):
	""" Class doc """
	
	def __init__ (self, gene, stage, names, model=None, compute=None, cluster=False, verbose=False):
		""" Class initialiser """
		self.names = names
		self.verbose = verbose
		self.path = os.path.split(names[0])[0]
		self.gene = gene
		self.stage = stage
			
		images = [Image(name, verbose=verbose) for name in names]
		images = [image for image in images if not hasattr(image, 'valid') or image.valid]
		
		cleared = check_cleared([img.img for img in images], model)
		
		self.cleared = score_images(
			ImageGroup([img for img, c in zip(images, cleared) if c])
			, cluster = cluster
			, max_comp=3
			, compute=compute, verbose=verbose)
			
			
		self.uncleared = score_images(
			ImageGroup([img for img, c in zip(images, cleared) if not c])
			, cluster = cluster
			, compute=compute, verbose=verbose)

		if verbose:
			print "Cleared"
			for i, img in [(i, img) for i, ig in enumerate(self.cleared) for img in ig]:
				print i, img.name, img.score

			print "Uncleared"
			for i, img in [(i, img)for i, ig in enumerate(self.uncleared) for img in ig]:
				print i, img.name, img.score
		
		
	def save(self, path):
		""" Function doc """
		self.selected_path = os.path.join(os.path.join(path, 'selected'), os.path.split(self.path)[-1])
		if not os.path.exists(self.selected_path):
			os.makedirs(self.selected_path)
			
		self.cleared_path = os.path.join(os.path.join(path, 'cleared'), os.path.split(self.path)[-1])
		if not os.path.exists(self.cleared_path):
			os.makedirs(self.cleared_path)
		
		for i, ig in enumerate(self.cleared):
			ig.save(self.cleared_path, append=[str(i)])
			ImageGroup([ig.best()]).save(self.selected_path, append=[str(i)])

		self.uncleared_path = os.path.join(os.path.join(path, 'uncleared'), os.path.split(self.path)[-1])
		if not os.path.exists(self.uncleared_path):
			os.makedirs(self.uncleared_path)

		for i, ig in enumerate(self.uncleared):
			ig.save(self.uncleared_path, append=[str(i)])
			ImageGroup([ig.best()]).save(self.selected_path, append=[str(i)])
		
		
	def dry(self):
		""" Function doc """
		for ig in self.cleared:
			ig.dry()
		for ig in self.uncleared:
			ig.dry()
			
		return self
		
	def find_images(self, name):
		""" Function doc """
		
		ret = [img for cls in self.cleared for img in cls if img.name == name]
		ret += [img for cls in self.uncleared for img in cls if img.name == name]
		
		return ret		

