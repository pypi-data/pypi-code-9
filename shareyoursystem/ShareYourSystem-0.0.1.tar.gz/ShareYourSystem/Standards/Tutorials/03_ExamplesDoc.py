"""
import pymongo
MyClient=pymongo.MongoClient('mongodb://localhost:27017/')

print(MyClient.MyDatabase)
print(MyClient.MyDatabase.MyCollection)

MyClient.MyDatabase.MyCollection.insert(
	[
		{
			'MyInt':0,
			'MyStr':"hello"
		},
		{
			'MyInt':5,
			'MyStr':"hello"
		},
		{
			'MyInt':5,
			'MyStr':"bonjour"
		}
	]
)

print(

	list(
		MyClient.MyDatabase.MyCollection.find(
			{
				'MyInt':{'$gt':3},
				'MyStr':{}
			}
		)
	)
)

import operator


print(operator.gt(5,6))

if 4>5:
if operator.gt(4,5)



#MyClient.MyDatabase.MyCollection.find()
"""