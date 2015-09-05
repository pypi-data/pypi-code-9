#working_dir='/home/user/dev/tao1/sites/daoerp'
#python='/usr/bin/python3.4'
#pythonpath=/usr/local/lib/python3.4/dist-packages

worker_class ='aiohttp.worker.GunicornWebWorker'
bind='127.0.0.1:6677'
workers=8
reload=True
user = "nobody"

#        'app.app',    