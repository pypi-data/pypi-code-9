#!/usr/bin/env python

import os.path
import requests

'''
 * Classe per interagire con l'API REST di Storage31
 *
 * @version 1.0.0
 * @package GCloud-SDK-Python
'''

'''
 * Dipendiamo da requests
 * http://docs.python-requests.org/en/latest/
 * pip install requests
'''

def ifDifferent(f):
    ''' Decoratore che si occupa di evitare di scaricare o uplodare un file gia' presente.'''
    def wrapper(*args, **kwargs):
        # L'argomento zero e' l'istanza della classe
        CS = args[0]
        pr_debug(kwargs)
        pr_debug('sono in ifDifferent')
        '''
        Check = devo verificare se sono diversi?
        isDiff = sono diversi?
        
        Tabella della verita':
        Check isDiff ?
        0     0      Do
        0     1      Do
        1     0      Not Do
        1     1      Do
        '''
        if (CS.CheckIfDifferent and not CS.isDifferent(kwargs['localFile'], kwargs['fileKey'])):
            pr_debug('NON FACCIO')
            return True
        else:
            pr_debug('FACCIO')
            return f(*args, **kwargs)
    return wrapper

def pr_debug(string):
    return string
    #return ''

class Cloud31_Storage31:
    '''
     * Definizione della classe principale
     *
     * @author Ilario Febi <ifebi@schema31.it>
     * @package SC31-Storage31
    '''

    # Attuale versione della libreria
    VERSION = 'Cloud31_Storage31 1.0.1'

    # LastError - l'ultimo errore ricevuto
    LastError = ''

    def __init__(self, RN='', AUTH='', HOST='storage.gcloud.schema31.it'):
        # Repository su cui operare
        self.repositoryName = RN

        # Chiave di autenticazione
        self.Authentication = AUTH
        
        # Host dove inviare e ricevere file
        self.Storage31Host = HOST

        self.headers = {'Authentication': self.Authentication,
                        'repositoryName': self.repositoryName,
                        'User-Agent': self.VERSION,
                        }
        
        # Abilita o meno il decoratore ifDifferent
        self.CheckIfDifferent = False

    # Stampa errori per il debug
    def err(self, r):
        print(r.status_code)
        print(r.headers)
        print(r.content)

            
    @ifDifferent
    def sendFile(self, localFile=False, mime='application/octet-stream',
                 publicName=False, fileKey=False):
        '''
         Carica un documento su Storage31
         *
         * @param string localFile Path del file da inviare su questo filesystem
         * @param string mime Mime part del file da inviare
            (default application/octet-stream)
         * @param string publicName Nome del file da inviare a Storage31
            (di default prende il basename di $localFile)
         * @param string fileKey Riferimento ad una fileKey gia' esistente per
            effettuare la "sovrascrittura" di un file
         * @return boolean|string torna la fileKey ritornata da Storage31 oppure
            FALSE in caso di errore
        '''

        if (localFile is False):
            raise("il parametro localFile e' richiesto!")
        #  Se non ci viene passato un publicName esplicito lo ricaviamo
        #  dal nome del file da inviare

        if (publicName is False):
            publicName = os.path.basename(localFile)
        #  Verifico se c'e' una fileKey preimpostata
        if (fileKey is not False):
            extraUrl = 'fileKey/' + fileKey
        else:
            extraUrl = ''

        #  Creiamo un'istanza dell'oggetto Request2 definendo tutti i parametri
        url = 'http://{0}/api/resource/{1}/'.format(
            self.Storage31Host, extraUrl)

        files = {'file': (publicName, open(localFile, 'rb'), mime)}

        try:
            r = requests.post(url, files=files, headers=self.headers)
            #pr_debug(r.headers)
            
        except requests.exceptions.TooManyRedirects as e:
            print(e)
            return False
        else:
            if (r.status_code == requests.codes.created):
                return r.json()
            else:
                self.err(r)
                return False
    
    # Verifica la presenza del file sullo storage prima di effettuare il send
    def isDifferent(self, localFile=False, fileKey=False):
        if (localFile is False or fileKey is False):
            raise ('Local file e File Key sono obbligatorie')
        
        import hashlib
        import json
        
        if (not os.path.isfile(localFile)):
            pr_debug('il file %s non esiste' % localFile)
            return True
        
        localmd5 = hashlib.md5(open(localFile, 'rb').read()).hexdigest()
        datail_array = self.detailFile(fileKey)
        if (localmd5 == datail_array['fileMD5']):
            pr_debug('Il file %s e la filekey %s sono la stessa cosa' % (localFile, fileKey))
            return False
        else:
            pr_debug('Il file %s e la filekey %s sono diversi' % (localFile, fileKey))
            return True
    
    # Torna le informazioni su un dato file
    def detailFile(self, fileKey, fileVersion=False):
        url = 'http://{0}/api/resource/fileKey/{1}/'.format(
            self.Storage31Host, fileKey)
        if (fileVersion is not False):
            url += '/fileVersion/' + fileVersion

        try:
            r = requests.get(url, headers=self.headers)
        except requests.exceptions.TooManyRedirects as e:
            print(e)
            print(r.history)
            return False
        else:
            if (r.status_code == requests.codes.ok):
                return r.json()
            else:
                self.err(r)
                return False

    def listFiles(self):
        url = 'http://{0}/api/resources/'.format(self.Storage31Host)
        try:
            r = requests.get(url, headers=self.headers)
        except requests.exceptions.TooManyRedirects as e:
            print(e)
            print(r.history)
            return False
        else:
            if (r.status_code == requests.codes.ok):
                return r.json()
            else:
                self.err(r)
                return False

    # Scarica un documento da Storage31
    @ifDifferent
    def getFile(self, fileKey=False, localFile=False, fileVersion=False):
        '''
        Scarica un documento su Storage31
        * @param string fileKey Riferimento alla fileKey da scaricare
        * @param string fileVersion Versione del file da scaricare
        * @param string localFile Path dove salvare il file localmente, 
            se localFile == False il file viene inviato sulla stdout
        * @return boolean|string torna il documento associato alla fileKey su stdout 
            oppure FALSE in caso di errore 
            oppure TRUE nel caso in cui il documento e' stato salvato su file
        '''
        
        response = self.detailFile(fileKey, fileVersion=False)
        if (response is False):
            return False
        else:
            # Creiamo un'istanza dell'oggetto Request2
            # definendo tutti i parametri
            url = response['friendlyUrl']

            try:
                r = requests.get(url, headers=self.headers)

            except requests.exceptions.TooManyRedirects as e:
                print(e)
                return False
            else:
                if (r.status_code == requests.codes.ok):
                    if (localFile is not False):
                        # Se esplicitato il localfile scrive direttamente li senza mostrarlo a video
                        with open(localFile, 'wb') as fd:
                            for chunk in r.iter_content(10):
                                fd.write(chunk)
                        return True
                    else:
                        return r.content
                else:
                    self.err(r)
                    return False

    # Cancella un documento da Storage31
    def deleteFile(self, fileKey, fileVersion=False):
        url = 'http://{0}/api/resource/fileKey/{1}/'.format(
            self.Storage31Host, fileKey)
        if (fileVersion is not False):
            url += '/fileVersion/' + fileVersion

        try:
            r = requests.delete(url, headers=self.headers)
        except requests.exceptions.TooManyRedirects as e:
            print(e)
            return False
        else:
            if (r.status_code == requests.codes.ok):
                return r.json()
            else:
                self.err(r)
                return False

def main():
    import argparse

    # Parser degli argomenti
    parser = argparse.ArgumentParser(
        description='gCloud Info test',
        epilog="La nuova generazione di Storage Virtuale")
    parser.add_argument(
        "-w", "--what",
        choices=['detail', 'send', 'get', 'delete', 'ls', 'version'],
        help="What??",
        required=True)
    parser.add_argument(
        "-r", "--repositoryname", help="Nome del repository", required=True)
    parser.add_argument(
        "-k", "--authkey", help="Authentication key", required=True)
    parser.add_argument(
        "-f", "--filekey", help="FileKey", default=False)
    parser.add_argument(
        "-l", "--local-file", help="File locale da inviare o dove scaricare", default=False)
    parser.add_argument(
        "-p", "--public-name", help="Nome del file sul repository", default=False)
    parser.add_argument(
        "-M", "--mime-type", help="Imposta manualmente il mime type", default='application/octet-stream')
    parser.add_argument(
        "-d", "--is-different", help="verifica se il file locale e remoto sono uguali",
        action='store_true')

    args = parser.parse_args()
    
    #force_to_host='storage.gcloud.schema31.it.phpengine-rm-01.gcloud.schema31.it'
    CS = Cloud31_Storage31(
        args.repositoryname,
        args.authkey,
        #force_to_host,
    )
    
    # Imposta se attivare o meno i decoratori IfDifferent
    CS.CheckIfDifferent = args.is_different
        
    # Execution
    if (args.what == 'detail'):
        print(CS.detailFile(args.filekey))
        
    elif (args.what == 'ls'):
        print(CS.listFiles())
        
    elif (args.what == 'get'):
        print(CS.getFile(fileKey=args.filekey, 
                          localFile=args.local_file))
        
    elif (args.what == 'send'):
        CS.sendFile(fileKey=args.filekey, 
                          localFile=args.local_file, 
                          mime=args.mime_type,
                          publicName=args.public_name,)
        
    elif (args.what == 'delete'):
        print(CS.deleteFile(args.filekey))
        
    elif (args.what == 'version'):
        print(CS.VERSION)


if __name__ == "__main__":
    main()
