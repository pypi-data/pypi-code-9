from flask import Flask
from flask.ext import restful
from flask import request
from flask.ext.cors import CORS
import pandas as pd
import sqlite3    
 
conn = sqlite3.connect('example.db')
 
app = Flask(__name__)
api = restful.Api(app)
cors = CORS(app)
 
class pandarequest(restful.Resource):
    def get(self):
        query = request.args.get('query')
        print query
        result = pd.read_sql_query(query,conn)
        header = result.columns
        return {'result': [result.columns.tolist()]+result.values.tolist()}
    
    def post(self):
        query = request.form['content']
        print query
        result = pd.read_sql_query(query,conn)
        header = result.columns
        return {'result': [result.columns.tolist()]+result.values.tolist()}
 
api.add_resource(pandarequest, '/api/db')
 
if __name__ == '__main__':
    app.run(host="0.0.0.0",port=8090)
