
#ImportModules
import ShareYourSystem as SYS
from ShareYourSystem.Standards.Itemizers import Pointer

#Explicit expression
MyParenter=SYS.ParenterClass(
		)['#map@set'](
			{
				'-Lovers':{
					'|Claire':{},
					'|Erwan':{
						'ParentingTriggerVariable':[
							(
								'->/^/|Claire',
								'/-Outlets/|ToClaire/'
							),

							#{
							#	'#key':'/-Outlets/|ToClaire',
							#	'#map@set':{
							#		'PointToVariable':'#get:/^/^/^/|Claire'
							#	}
							#}
						],
						#'PointMapVariable':{
						#
						#
						#}
					}
				}
			}
		)['?v']

#print
print("MyParenter is")
SYS._print(MyParenter)
