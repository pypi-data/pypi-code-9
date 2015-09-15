
#ImportModules
import ShareYourSystem as SYS

#figure
MyPyploter=SYS.PyploterClass(
	).mapSet(
		{
			'PyplotingDrawVariable':
			{
				'plot':{
					'#liarg':[
						[1,2,3],
						[2,6,3]
					],
					'#kwarg':{
						'linestyle':"--"
					}
				}
			}
		}
	).pyplot(
	)

#print
print('MyPyploter is ')
SYS._print(MyPyploter)



SYS.matplotlib.pyplot.show()
