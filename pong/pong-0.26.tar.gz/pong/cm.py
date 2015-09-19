from itertools import combinations
from dist_metrics import cluster_dist
from objects import Match

def clumpp(pong, dist_metric, sim_threshold, dif_threshold):
	all_kgroups = pong.all_kgroups
	runs = pong.runs
	cluster_matches = pong.cluster_matches
	'''
	Here, the boolean passed into match_clusters represents fixed_K, 
		meaning we're comparing runs with the same number of clusters.
	
	Note: In the base case, we entered the while loop with 2 unique runs left.
		Then, either they were identical and we combined them and now 
		len(unique_runs) = 0, OR they weren't and there's still one left.
		The other base case is that there was only 1 run to begin with.
		In this case, we would never have entered the while loop, and we
		likewise need to add the one entry of unique_runs to rep_runs.
	'''
	for kgroup in pong.all_kgroups:

		unique_runs = list(kgroup.all_runs)
		kgroup.primary_run = unique_runs[0]

		modes = {}
		while len(unique_runs) > 1:
			modes[unique_runs[0]] = [unique_runs[0]]
			# compare all other qmatrices to the first one
			for run in unique_runs[1:]:
				match = match_clusters(pong, pong.runs[unique_runs[0]].data, 
					pong.runs[run].data, kgroup.K, dist_metric, True )

				# add_cluster_match(pong, unique_runs[0], run, match )

				# if it's very similar, it can be represented by the first one
				# if they are very similar, remove this run because it is represented by the 1st
				if match.sim > sim_threshold and match.dif > dif_threshold:
					unique_runs.remove(run)
					modes[unique_runs[0]].append(run)
					# pong.runs[unique_runs[0]].sim_runs.append(run)
					# pong.runs[run].represented_by = unique_runs[0]

			# add to rep runs and remove from unique runs
			# kgroup.rep_runs.append(unique_runs.pop(0)) 
			unique_runs.pop(0)

		# if len(unique_runs) == 1: kgroup.rep_runs.append(unique_runs[0])
		if len(unique_runs) == 1: modes[unique_runs[0]] = [unique_runs[0]]

		# print(modes)
		major_mode = max(modes, key=lambda r: len(modes[r]))
		# print(major_mode)

		kgroup.primary_run = major_mode
		kgroup.all_runs.remove(major_mode)
		kgroup.all_runs.insert(0,major_mode)

	
		for reps in modes:
			
			# compare all other qmatrices to the first one
			for run in kgroup.all_runs:
				if run != reps:
					if major_mode != run:
						match = match_clusters(pong, pong.runs[major_mode].data, 
							pong.runs[run].data, kgroup.K, dist_metric, True )

						add_cluster_match(pong, major_mode, run, match )
					if run == major_mode or run not in modes[major_mode]:
						match = match_clusters(pong, pong.runs[reps].data,
							pong.runs[run].data, kgroup.K, dist_metric, True )

						add_cluster_match(pong, reps, run, match )
					# if it's very similar, it can be represented by the first one
					# if they are very similar, remove this run because it is represented by the 1st
					if run in modes[reps]:
						pong.runs[reps].sim_runs.append(run)
						pong.runs[run].represented_by = reps


			# add to rep runs and remove from unique runs
			kgroup.rep_runs.append(reps)

		pl = ""
		if len(kgroup.all_runs) > 1:
			pl = "s"
		# print number of unique clustering solutions
		if len(kgroup.rep_runs) == 1:
			print 'For K=%d, there is 1 mode across %d run%s.' % (kgroup.K, len(kgroup.all_runs),pl)
		else:
			data = (kgroup.K, len(kgroup.rep_runs), len(kgroup.all_runs),pl)
			print 'For K=%d, there are %d modes across %d run%s.' % data

	pong.sort_by = max(kgroup.rep_runs, key=lambda r: len(runs[r].sim_runs))



def multicluster_match(pong, dist_metric):
	runs, all_kgroups = pong.runs, pong.all_kgroups
	'''
	Here, the boolean passed into match_clusters represents fixed_K, meaning
	we're comparing runs with different values of K (i.e. K is not fixed).
	'''
	# for each K except K_max
	for i in range(len(all_kgroups)-1):
		for run1 in all_kgroups[i].rep_runs:
			for run2 in all_kgroups[i+1].rep_runs:
				match = match_clusters(pong, runs[run1].data, runs[run2].data, 
					all_kgroups[i].K, dist_metric, False)
				
				add_cluster_match(pong, run1, run2, match)










def match_clusters(pong, run1, run2, K, dist_metric, fixed_K):
	'''
	nodes are either cluster vecs or conglomerates of multiple cluster vecs.

	edges[i] corresponds with the (i+1)th cluster in run1, and is itself a set 
	of edges between the (i+1)th cluster in run1 and nodes (=clusters or 
	conglomerates of clusters) in run2. It is implemented as a list of tuples,
	each of which having the form (edge_weight, node_id).

	node_id is itself a tuple, either containing one number (the run2 cluster 
	number) or two (the two clusters in run2 constituting the node)

	e.g. edges = [ [ (0.99,(1,)), (0.87,(2,3)), ...], [ (0.98,(2,)),...],...]

	FIGURE OUT OVERALL Q-MATRIX SIMILARITY: assuming you pick the best cluster 
	match in run2 for each cluster in run1, how similar are the two matrices?
	This information is used by clumpp() to determine multimodality and
	condense the dataset.
	'''
	match = Match()

	# GENERATE NETWORK GRAPH AND EDGE WEIGHTS
	cluster_num = 1
	for n1 in run1:

		for i,n2 in enumerate(run2):
			weight = cluster_dist(pong, n1, n2, K, dist_metric)
			cluster_id = (i+1,) # must include comma so we know it's a tuple
			match.edges[(cluster_num,cluster_id)] = weight
			match.to_nodes.add(cluster_id)


		# INCLUDE HYBRID NODES FOR MATCHING RUNS ACROSS K
		if not fixed_K:
			# combs = []
			# for i in range(2,(len(run2)+1 if all_cluster_mixtures else 3)):
			# 	combs += [x for x in combinations(range(len(run2)),i)]
			# combs = [x for x in combinations(range(len(run2)), 2)]

			for c1,c2 in combinations(range(len(run2)), 2):
				n2 = run2[c1]+run2[c2]
				weight = cluster_dist(pong, n1, n2, K, dist_metric)
				cluster_id = (c1+1, c2+1)
				match.edges[(cluster_num,cluster_id)] = weight
				match.to_nodes.add(cluster_id)

		match.from_nodes.add(cluster_num)
		cluster_num += 1


	''' TODO: POTENTIAL PROBLEM = what if there's only 1 match (K=1 or 
	something) then there won't be a n1[1][0]
	'''
	match.compute_sim_and_dif()

	return match






def add_cluster_match(pong, id1, id2, data):
	'''
	Adds cluster matching details (network graph) between 2 runs
	to the cluster_matches dictionary.

	"data" is of the form (edges, sim, dif)
	'''
	try:
		pong.cluster_matches[id1][id2] = data
	except KeyError:
		pong.cluster_matches[id1] = {id2: data}






