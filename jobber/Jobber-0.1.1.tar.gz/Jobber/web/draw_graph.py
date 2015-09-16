import sys
sys.path.append("..")
from Jobber import database
import graphviz as gv
from flask import Flask, render_template, url_for, redirect

g2 = gv.Digraph(format='svg')
db = database.getDB()
for d in db.getMembers(int(sys.argv[1])):
    print d['status'], d['name'], d['is_group_job']
    g2.node(d['name'])

for d in db.getMembers(int(sys.argv[1])):
    for dep in db.getDependentJobs(d['id']):
        g2.edge(d['name'], db.getJobInfo(dep)['name'])

g2.render('img/g2')
