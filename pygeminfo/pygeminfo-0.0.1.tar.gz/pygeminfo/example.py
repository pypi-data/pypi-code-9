# from pygeminfo.gems import *
#from pygeminfo.gems import Stats

#! Import pygeminfo
#--> sample = pygeminfo.gems.Stats("ruby")

#Using the gem's Stats class

#Enter Rubygem's name as argument

# sample = Stats("ruby")
# print ("Gem Name: {}".format(sample.name()))
# print ("Overall Gem download: {}".format(sample.total()))
# print ("Latest version download: {}".format(sample.latest()))
# print ("Latest version: {}".format(sample.latestversion()))
# print ("Authors: {}".format(sample.authors()))
# print ("Description: {}".format(sample.info()))
# print ("Licenses : {}".format(sample.licenses()))
# print ("Metadata : {}".format(sample.metadata()))
# print ("Secure Hash Algorithm: {}".format(sample.sha()))
# print ("Gem's URL: {}".format(sample.gemURL()))
# print ("Project URL: {}".format(sample.projectURL()))
# print ("Gem's homepage: {}".format(sample.homepage()))
# print ("Wiki webpage: {}".format(sample.wikiURL()))
# print ("Documentation webpage: {}".format(sample.docURL()))
# print ("Mailing list website: {}".format(sample.mailURL()))
# print ("Source code URL: {}".format(sample.sourceURL()))
# print ("Bug tracker URL: {}".format(sample.bugURL()))


from gems import *
#Using the Gem's other module methods 
#(self-printing. No need to print

# gemversions("geminfo")
downloads()
usergems("tushortz")



