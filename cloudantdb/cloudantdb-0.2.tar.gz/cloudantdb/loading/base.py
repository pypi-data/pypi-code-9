import sys
import cloudant

class CloudantDBHandler(object):
    
    def __init__(self,databases):
        #Created for get_db method
        self._databases = dict()
        self._accounts = dict()
        self._labels = list()
        for db_label,db_info in databases.iteritems():
            account = cloudant.Account(db_info.get('ACCOUNT_USERNAME')) 
            account.login(db_info.get('USERNAME'),db_info.get('PASSWORD'))
            db = account.database(db_info.get('DATABASE'))
            db.dbname = db_info.get('DATABASE')
            self._databases[db_label] = db
            self._labels.append(db_label)
            self._accounts[db_label] = account
            
    def get_db(self,db_label):
        
        return self._databases.get(db_label)
        