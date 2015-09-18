import rdflib
from rdflib.plugin import register, Parser
import rdflib_jsonld.parser
from rdflib import Graph, plugin
from rdflib.serializer import Serializer
import yaml
import json
import ref_resolver

def printrdf(workflow, wf, ctx, sr):
    g = Graph().parse(data=json.dumps(wf), format='json-ld', location=workflow, context=ctx)
    print(g.serialize(format=sr))

y = yaml.load(open("metaschema.yml"))

printrdf("metaschema.yml", y, json.load(open("context.json")), "turtle")
