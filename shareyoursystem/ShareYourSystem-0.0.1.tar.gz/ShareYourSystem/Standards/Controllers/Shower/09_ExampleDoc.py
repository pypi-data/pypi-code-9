#ImportModules
import ShareYourSystem as SYS

#Define
MyShower=SYS.ShowerClass(
	).mapSet(
		{
			'-Views':
			{
				'|Example':{
					'ParentingTriggerVariable':
					{

						'#plot':{
							'#liarg':[
								[1,2,3],
								[2,6,3]
							],
							'#kwarg':{
								'linestyle':"",
								'marker':'o'
							}
						}
					}
				}
			}
		}
	).show(
	)

#print
print('MyShower is ')
SYS._print(MyShower)