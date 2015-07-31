#!/usr/bin/env python
#Once upon a time...

import random
from numpy import mean,std
import time
import sys
from  multiprocessing import Pool
from functools import partial

######################################################################
##
##      Given the ratio of F1 (complete) reads to F2 (boundary) reads
##		simulate to find the average TL that gave the ratio 
##
##      Author: jhrf
##
######################################################################

class LengthEstimator(object):
	def __init__(self,insert_mu,insert_sigma,complete,boundary,read_len=100):
		self._insert_mu = insert_mu
		self._insert_sigma = insert_sigma
		self._complete = complete 
		self._boundary = boundary 
		self._read_len = read_len

		print boundary,complete

		self._read_sim = self.__simulate_reads__

	def start(self):
		if self._boundary <= 0 or self._complete <= 0:
			return 0
		else:
			return self.__run_sim__()

	def __run_sim__(self):
		found = False
		tel_len = int(self._insert_mu+((float(self._complete)/self._boundary) * 100))
		max_its = 300
		its = 0

		best_result = float("inf")
		best_tel_len  = tel_len

		read_simulator = self._read_sim
		get_factor = self.__get_factor__

		while(not found and its < max_its):
			sim_comp,sim_boun = read_simulator(tel_len)
			#	result can be positive or negative thus 
			#	influencing elongation and shortening
			#	A negative diference (overestimate) results 
			#	in a shorter telomere length next iteration
			result = self.is_same_ratio(sim_comp,sim_boun)
			abs_result = abs(result)

			if abs_result < best_result:
				best_result = abs_result
				best_tel_len = tel_len

			if result == 0: 
				found = True
			else:
				mult = -1 if result < 0 else 1
				factor = get_factor(abs_result)
				tel_len += factor * mult
			its += 1

		return best_tel_len

	def __get_factor__(self,abs_result):
		if abs_result > 1000:
			return 200
		elif abs_result < 1000:
			return random.sample([1,2,5], 1)[0]
		elif results < 50:
			return 0

	def is_same_ratio(self,comp,boun):
		if comp == self._complete and boun == self._boundary:
			return 0
		else:
			return self._complete - comp

	def __simulate_reads__(self,tel_len):
		cur_complete = 0
		cur_boundary = 0
		total = 0

		#speedup
		is_complete = self.is_complete
		is_boundary = self.is_boundary

		if tel_len < self._insert_mu:
			return ( int(self._complete * .50),self._boundary)

		while total < (self._complete + self._boundary):
			insert_size = int(random.gauss(self._insert_mu,self._insert_sigma))
			location = random.randint(0,tel_len)
			if is_complete(location,insert_size):
				cur_complete += 1
				total += 1
			elif is_boundary(location,insert_size):
				cur_boundary += 1
				total += 1
		return (cur_complete,cur_boundary)

	def is_complete(self,location,insert_size):
		return (location - insert_size) > 0

	def is_boundary(self,location,insert_size):
		return (location - self._read_len) > 0

def check_results(sim_results):
	if 0 in sim_results:
		sys.stderr.write("[WARNING] Telomere length reported zero. This means telomercat\n"+
						"\tfailed to identify enough complete or boundary reads.\n"+
						"\tThis  may mean your original sample was preprocessed to remove \n"+
						"\ttelomere reads. Alternatively this sample could have \n"+
						"\tvery short average TL.\n")

def run_simulator(insert_mu,insert_sigma,complete,boundary,proc,read_len,N=10):
	simmer = LengthEstimator(insert_mu,insert_sigma,complete,boundary,read_len)
	res = []
	for i in range(N):
		res.append(simmer.start())
	check_results(res)
	return (mean(res),std(res))

def estimator_process(job,insert_mu,insert_sigma,complete,boundary,read_len):
	length_estimator = LengthEstimator(insert_mu,insert_sigma,complete,boundary,read_len)
	results = length_estimator.start()
	return results

def run_simulator_par(insert_mu,insert_sigma,complete,boundary,proc,read_len,N=10):
	p = Pool(proc)
	sim_partial = partial(estimator_process,insert_mu=insert_mu,
						  insert_sigma=insert_sigma,complete=complete,
						  boundary=boundary,read_len=read_len)
	results = p.map(sim_partial,range(N))
	p.close()
	check_results(results)
	return (mean(results),std(results))

if __name__ == "__main__":
	print "Type telomerecat into your terminal for more details"