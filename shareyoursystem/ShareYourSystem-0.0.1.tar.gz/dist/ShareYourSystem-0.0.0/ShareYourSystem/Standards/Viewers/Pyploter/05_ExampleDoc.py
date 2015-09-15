
#ImportModules
import ShareYourSystem as SYS

#figure
MyPyploter=SYS.PyploterClass(
	).mapSet(
		{
			'-Charts':
			{
				'|a':{
					'-Draws':[
						('|0',{
							'PyplotingDrawVariable':
							[
								(
									'plot',
									{
										'#liarg':[
											[1,2,3],
											[2,6,3]
										],
										'#kwarg':{
											'linestyle':"",
											'marker':'o'
										}
									}
								)
							]
						}),
						('|1',{
							'PyplotingDrawVariable':
							[
								(
									'plot',
									{
										'#liarg':[
											[0,1,2],
											[2,3,4]
										],
										'#kwarg':{
											'linestyle':"--",
											'color':'r'
										}
									}
								)
							],
						})
					],
					'PyplotingChartVariable':
					[
						('set_xlim',[0,5])
					]
				}
			}
		}
	).pyplot(
	)

#print
print('MyPyploter is ')
SYS._print(MyPyploter)

#show
SYS.matplotlib.pyplot.show()
