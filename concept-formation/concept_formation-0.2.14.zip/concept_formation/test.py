from concept_formation.action_planner import ActionPlanner

state = {'correct': 'Correct',
 ('_', ('_name', '?723a1110-8310-44b3-adc2-9f6ec9083984')): 'CheckPoint',
 ('_', ('_name', '?9c912225-080d-496b-961f-a1b6cce7d256')): 'CheckPoint',
 ('_', ('_name', '?CheckPoint')): 'CheckPoint',
 ('_', ('_name', '?GoalTrigger')): 'GoalTrigger',
 ('_', ('_name', '?UFO')): 'UFO',
 ('_', ('_name', '?plate01')): 'plate01',
 ('_', ('_name', '?plate02')): 'plate02',
 ('_', ('_name', '?plate03')): 'plate03',
 ('active', '?723a1110-8310-44b3-adc2-9f6ec9083984'): False,
 ('active', '?9c912225-080d-496b-961f-a1b6cce7d256'): False,
 ('active', '?CheckPoint'): False,
 ('height', '?723a1110-8310-44b3-adc2-9f6ec9083984'): 0.6,
 ('height', '?9c912225-080d-496b-961f-a1b6cce7d256'): 0.6,
 ('height', '?CheckPoint'): 0.6,
 ('height', '?GoalTrigger'): 1.0,
 ('height', '?UFO'): 4.82157564,
 ('height', '?plate01'): 1.74429369,
 ('height', '?plate02'): 1.74429369,
 ('height', '?plate03'): 1.74429369,
 ('type', '?723a1110-8310-44b3-adc2-9f6ec9083984'): 'chec',
 ('type', '?9c912225-080d-496b-961f-a1b6cce7d256'): 'chec',
 ('type', '?CheckPoint'): 'chec',
 ('type', '?GoalTrigger'): 'goal',
 ('type', '?UFO'): 'ufo',
 ('type', '?plate01'): 'plat',
 ('type', '?plate02'): 'plat',
 ('type', '?plate03'): 'plat',
 ('width', '?723a1110-8310-44b3-adc2-9f6ec9083984'): 0.6,
 ('width', '?9c912225-080d-496b-961f-a1b6cce7d256'): 0.6,
 ('width', '?CheckPoint'): 0.6,
 ('width', '?GoalTrigger'): 1.89410138,
 ('width', '?UFO'): 5.250356,
 ('width', '?plate01'): 5.30891228,
 ('width', '?plate02'): 5.30891228,
 ('width', '?plate03'): 5.30891228,
 ('x', '?723a1110-8310-44b3-adc2-9f6ec9083984'): -1.03054357,
 ('x', '?9c912225-080d-496b-961f-a1b6cce7d256'): 0.5932205,
 ('x', '?CheckPoint'): 2.06925225,
 ('x', '?GoalTrigger'): 0.773903847,
 ('x', '?UFO'): -9.736836,
 ('x', '?plate01'): -9.0,
 ('x', '?plate02'): -9.0,
 ('x', '?plate03'): -9.0,
 ('y', '?723a1110-8310-44b3-adc2-9f6ec9083984'): -7.11232,
 ('y', '?9c912225-080d-496b-961f-a1b6cce7d256'): -1.746882,
 ('y', '?CheckPoint'): -7.11232,
 ('y', '?GoalTrigger'): 0.176572323,
 ('y', '?UFO'): -6.78876829,
 ('y', '?plate01'): 8.0,
 ('y', '?plate02'): 8.0,
 ('y', '?plate03'): 8.0}

def add(x,y):
	if isinstance(x,Number) and isinstance(y,Number):
		return x+y
	raise TypeError("Not Numbers")

def sub(x,y):
	if isinstance(x,Number) and isinstance(y,Number):
		return x-y
	raise TypeError("Not Numbers")

def mult(x,y):
	if isinstance(x,Number) and isinstance(y,Number):
		return x*y
	raise TypeError("Not Numbers")

def div(x,y):
	if isinstance(x,Number) and isinstance(y,Number):
		return x/y
	raise TypeError("Not Numbers")

def half(x):
	if isinstance(x,Number):
		return x/2
	raise TypeError("Not Numbers")

actions = {
	"add":add,
	"sub":sub,
	"mult":mult,
	"div":div,
	"half":half
}

sai = ('place', 'plate01', '-1.030323', '-5.346702', '1.744374', '5.308938')


act_plan = ActionPlanner(actions,epsilon=.875)

for i in range(2,6):
	plan = act_plan.explain_value(state,sai[i])
	print(plan)


