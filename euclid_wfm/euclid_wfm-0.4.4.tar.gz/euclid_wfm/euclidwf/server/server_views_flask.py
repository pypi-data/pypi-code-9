'''
Defines the views provided by the pipeline run server.

Created on May 29, 2015

@author: martin.melchior
'''
import datetime
import json
import os
from flask import Flask
from flask import request
from flask.templating import render_template
from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import get_lexer_by_name

from euclidwf.framework.runner import ExecStatus, PipelineExecution, REPORT,\
    PIPELINE, RUNID, STATUS, SUBMITTED
from euclidwf.server import server_model, server_config
from euclidwf.utilities import visualizer
import traceback


app = Flask(__name__)

registry = server_model.registry
history=server_model.history

@app.context_processor
def now():
    def formated_date():        
        return datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M%p")
    return dict(now=formated_date)

@app.route('/submit', methods=['POST'])
def submit():
    payload = request.data
    data=server_model.load_submit_data(payload, app.config)
    response=_submit(data)
    return json.dumps(response)

@app.route('/status/<runid>', methods=['GET'])
def status(runid):
    response=_status(runid)
    return json.dumps(response)

@app.route('/runs/<runid>/status', methods=['GET'])
def run_status(runid):
    response=_status(runid)
    return json.dumps(response)

@app.route('/runs', methods=['GET'])
def runs():
    if request.headers['Content-Type']=='application/json':
        runs=_runs()
        return json.dumps({ 'runids' : runs })
    else:
        runs=_runs()
        table={'cols': RUNS_COLS, 'rows':runs}
        context={'table':table}
        return render_template("runids.html", **context)
        

@app.route('/runs/<runid>', methods=['GET'])
def run_details(runid):
    if not registry.has_run(runid):
        return {'success' : False,
                'message' : "Runid %s does not exist"%runid }
    
    run=registry.get_run(runid)
    context=run.todict()
    tasks_cols=({'name':'tick'}, {'name':'model path'}, {'name':'pid'}, 
                {'name':'status'}, {'name':'duration'}, {'name':'output dir'})
    tasks_rows=context[REPORT]
    context['tasks']={'cols':tasks_cols, 'rows':tasks_rows}
    
    if request.headers['Content-Type']=='application/json':
        return json.dumps(context)
    else:
        # create pygraph, the map file is also created, but does not work yet (--> tooltips,etc)
        graph=run.traverser.get_graph()
        pygraph=visualizer.create_pygraph(graph)
        pngname='%s_%s.png'%(context[PIPELINE]['name'],runid)
        mapname='%s_%s.html'%(context[PIPELINE]['name'],runid)
        _draw_pygraph(pygraph, pngname, mapname)
        context['graph_png']='%s/%s'%(app.config[server_config.IMG_DIR],pngname)
        context['graph_map']='%s/%s'%(app.config[server_config.IMG_DIR],mapname)        
        return render_template("run_details.html", **context)


def _submit(data):
    try:
        runid=data[RUNID]
    except Exception as e:
        return {STATUS : str(ExecStatus.FAILED),
                'reason' : '%s\n%s'%(str(e),'\n'.join(traceback.format_stack())), 
                RUNID  : None }

    if registry.has_run(runid):
        return {'success' : False,
                'message' : "Runid %s does already exist"%runid }

    try:
        pipeline_exec=PipelineExecution.fromdict(data)
    except Exception as e:
        return {STATUS : str(ExecStatus.FAILED),
                'reason' : '%s\n%s'%(str(e),'\n'.join(traceback.format_stack())), 
                RUNID  : runid }
        
    try:
        pipeline_exec.initialize()
    except Exception as e:
        return {STATUS : str(ExecStatus.FAILED),
                'reason' : '%s\n%s'%(str(e),'\n'.join(traceback.format_stack())), 
                RUNID  : runid }
    
    registry.add_run(runid, pipeline_exec)
    _ = pipeline_exec.start()
    history.add_entry("Runid %s submitted to the system"%runid, datetime.datetime.now())
    return {STATUS : str(ExecStatus.EXECUTING),
            RUNID  : pipeline_exec.runid }


def _status(runid):
    if not registry.has_run(runid):
        return {'success' : False,
                'message' : "Runid %s does not exist"%runid }

    run=registry.get_run(runid)
    if run.get_status()==ExecStatus.EXECUTING:
        return { STATUS : str(ExecStatus.EXECUTING),
                 RUNID  : runid }
    else:
        return run.todict()




RUNS_COLS=[{'name':'run (ID)'}, {'name':'status'}, { 'name' : 'pipeline'}, { 'name' : 'version' }, {'name' : 'submitted'}]
def _runs():
    return [{RUNID : runid, 
             STATUS : str(registry.get_run(runid).status), 
             PIPELINE : registry.get_run(runid).pipeline.func_name,
             'version' : 'n/a',
             SUBMITTED : registry.get_run(runid).created.strftime("%A, %d. %B %Y %I:%M%p")
             } for runid in registry.get_all_runids()]


def _draw_pygraph(pygraph, pngname, mapname):
    pngpath=os.path.join(app.config[server_config.STATIC_FILES], app.config[server_config.IMG_DIR], pngname) 
    if os.path.exists(pngpath):
        os.remove(pngpath)   
    mappath=os.path.join(app.config[server_config.STATIC_FILES], app.config[server_config.IMG_DIR], mapname)
    if os.path.exists(mappath):
        os.remove(mappath)       
    pygraph.draw(path=pngpath,format='png')
    pygraph.draw(path=mappath, format="cmapx")


@app.route('/runs/<runid>/script', methods=['GET'])
def run_script(runid):
    if not registry.has_run(runid):
        return {'success' : False,
                'message' : "Runid %s does not exist"%runid }
    
    run=registry.get_run(runid)
    pipeline=run.todict()['pipeline']


    # load file and convert it into html - with code highlighting:
    with open (pipeline['file'], "r") as srcfile:
        code=srcfile.read()    
    lexer = get_lexer_by_name("python", stripall=True)
    formatter = HtmlFormatter(linenos=True, cssclass="source")
    outfilepath=os.path.join(app.config['CODE_DIR'],pipeline['name']+".html")
    with open(outfilepath,'w') as outfile: 
        _ = highlight(code, lexer, formatter, outfile=outfile)
    context={RUNID:runid, 'script':'generated/%s.html'%pipeline['name'], 'pipeline':pipeline['name']}
    return render_template("script.html",**context)


@app.route('/runs/<runid>/reset', methods=['PUT'])
def reset(runid):
    response=_reset(runid)
    return json.dumps(response)        

def _reset(runid):
    if not registry.has_run(runid):
        return {'success' : False,
                'message' : "Runid %s does not exist"%runid }

    try:
        pipeline_exec = registry.get_run(runid)
    except Exception as e:
        return {STATUS : str(ExecStatus.FAILED),
                'reason' : '%s\n%s'%(str(e),'\n'.join(traceback.format_stack()))}
                    
    pipeline_exec.reset()
    history.add_entry("Runid %s reset."%runid, datetime.datetime.now())
    return {STATUS : str(ExecStatus.EXECUTING),
            RUNID  : runid }


@app.route('/runs/<runid>/cancel', methods=['DELETE'])
def cancel(runid):
    response=_cancel(runid)
    return json.dumps(response)        

def _cancel(runid):
    if not registry.has_run(runid):
        return {'success' : False,
                'message' : "Runid %s does not exist"%runid }
    try:
        pipeline_exec = registry.get_run(runid)
    except Exception as e: 
        return {STATUS : str(ExecStatus.FAILED),
                'reason' : '%s\n%s'%(str(e),'\n'.join(traceback.format_stack()))}
        
    pipeline_exec.cancel()
    registry.delete_run(runid)
    history.add_entry("Runid %s cancelled."%runid, datetime.datetime.now())
    return {STATUS : str(ExecStatus.CANCELLED),
            RUNID  : runid}


