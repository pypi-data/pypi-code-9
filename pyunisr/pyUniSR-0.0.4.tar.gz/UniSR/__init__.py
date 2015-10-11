import requests
from lxml import html
import re
from collections import OrderedDict
from sys import exit

class User:
    def __init__(self, notification_helper = False):
        self.url = "http://intranet.unisr.it/esse3/"
        self.dati_url = "http://datistudenti.unisr.it/"
        self.bacheca_url = "http://studenti.unisr.it/messaggi/view2.asp?Id_messaggio="
        self.elencoBachecha = "default2.asp"
        self.f_url = {
            "login": "auth/Logon.do",
            "home": "Home.do",
            "sceltaPiano": "auth/studente/SceltaCarrieraStudente.do",
            "libretto": "auth/studente/Libretto/LibrettoHome.do",
            "redirect": "Redirect.do",
            "servizi": self.dati_url + "default.asp",
            "datiDocenti": self.dati_url + "verify.asp",
            "prenotazioni": "auth/studente/Appelli/BachecaPrenotazioni.do",
            "orarioLezioni": "http://intranet.unisr.it/aule/default.asp",
        }
        self.servizi = {
            "datiDocenti": {"SESSIONE_AS": "SESSIONIDGUEST"}
        }
        self.redirect = {
            "bachecaOnline": {"parconfurl": "ALTRI_SERVIZI_STU_1"},
            "datiDocenti": {"parconfurl": "ALTRI_SERVIZI_STU_4"},
            "frequenze": {"parconfurl": "ALTRI_SERVIZI_STU_8"},
            "orarioLezioni": {"parconfurl": "ALTRI_SERVIZI_STU_9"},
        }
        self.virtual_base = ["DocentiStudenti"]
        self.currentPath = []
        self.corsi = []
        self.session = requests.Session()
        self.message_con_opened = False
        if notification_helper:
            self.notification_helper = notification_helper
        else:
            self.notification_helper = False
        self.plane_choosen = False
        self.corso = ""

    def cd(self, folderName = ".."):
        if folderName == "..":
            try:
                self.currentPath.pop()
            except:
                print("Sei gia al livello piu alto!")
            command = "LevelUp"
            path = "undefined"
        else:
            self.currentPath.append(folderName)
            command = "OpenFolder"
            path = '\\'.join(self.currentPath[:-1])
            path += "\\"
        virtual = list(self.virtual_base)
        virtual = "/".join(virtual)

        post_data = {
            "command": command,
            "parameter": str(folderName),
            "virtual": "/" + virtual + "/",
            "folder": path,
            "popup": "false",
            "username":"",
            "password":""
        }

        self.lastPageContent = self.session.post(self.f_url['servizi'], data = post_data, auth=self.auth).content

    def req_get(self, url, auth = "auth", params = "params"):
        auth = self.auth if auth == "auth" else ()
        params = () if params == "params" else params
        return self.session.get(url, params=params, auth=auth)

    def getParams(self, others = {}):
        params = OrderedDict([('jsessionid', self.jsessionid)])
        if others != {}:
            for key, value in list(others.items()): #others.iteritems()
                params[key] = value
        url_params = ""
        first = 1
        for key, value in list(params.items()): #params.iteritems()
            prepend = ";" if first else "?"
            first = 0
            url_params += prepend+key+"="+value
        return url_params

    def login(self, username, password, matricola = "auto"):
        self.auth = (username, password)
        self.session.get(self.url + self.f_url['home'])
        self.jsessionid = self.session.cookies['JSESSIONID']
        url = self.url + self.f_url['login'] + self.getParams()
        self.req_get(url, "noauth")
        login = self.req_get(url)
        if login.status_code == 200:
            self.lastPageContent = login.content
            login_html = html.fromstring(login.content)
            print("Logged in as %s successfully" % (username))
            if login_html.xpath('//div[@class="titolopagina"]/text()')[0] == "Scegli carriera":
                if matricola == "auto":
                    table = [ box for box in login_html.xpath('//table[@class="detail_table"]//text()') if box.strip() ]
                    piani_disponibili = int(len(table) / 4) - 1
                    for i in range(piani_disponibili):
                        if table[ (i+1) * 4 + 3] == "Attivo":
                            matricola = table[ (i+1) * 4]
                            self.corso = table[ (i+1) * 4 + 2 ]
                    if matricola == "auto":
                        exit("Impossibile ottenere numero di matricola")
                self.matricola = matricola
                self.sceltapiano(self.matricola)
        else:
            exit("Error %s" % login.status_code)

    def sceltapiano(self, matricola): #Devo farla automaticamente su quello attivo
        if not self.plane_choosen:
            student_id = {"stu_id":str(matricola)}
            url = self.url + self.f_url['sceltaPiano'] + self.getParams(student_id)
            for i in range(2):
                self.req_get(url)
            self.plane_choosen = True

    def media(self):
        url = self.url + self.f_url['libretto'] + self.getParams()
        libretto = self.req_get(url).content
        libretto_html = html.fromstring(libretto)
        media = {}
        media['aritmetica'], media['pesata'] = libretto_html.xpath('//td[@class="tplMaster"]//text()')
        media['aritmetica'], media['pesata'] =\
        [ m.group(0) for m in [ re.search("([\d.]{5})", mean) for mean in media.itervalues() ] ]
        return media

    def ls(self):
        dati_html = html.fromstring(self.lastPageContent)
        folders = dati_html.xpath('//td/a[@title="Apri cartella"]/font/text()')
        files = dati_html.xpath('//td/a[@title="Download File"]/text()')
        return folders, files

    def getFile(self, fileName):
        file = list(self.virtual_base)
        file.extend(self.currentPath)
        file.append(fileName)
        url = self.dati_url + "/".join(file)
        print("Downloading %s" % fileName)
        file_content = self.session.get(url, auth=self.auth)
        return file_content

    def datiDocenti(self):
        post_data = {"username": self.auth[0], "password": self.auth[1]}
        self.lastPageContent = self.session.post(self.f_url['datiDocenti'], data=post_data).content
        return self.ls()

    def saveFile(self, fileName, requests_response):
        with open(fileName, 'wb') as fd:
            for chunk in requests_response.iter_content(1024):
                fd.write(chunk)

    def messageLink(self): #Use it the first time you call self.c in a func
        if self.message_con_opened == False:
            import sqlite3
            self.conn = sqlite3.connect(self.db_file)
            self.c = self.conn.cursor()
            return self.c
        else:
            return self.c

    def messaggiBacheca(self, database):
        self.db_file = database
        url = self.url + self.f_url["redirect"]
        self.lastPageContent = self.req_get(url, auth="auth", params=self.redirect["bachecaOnline"]).content
        bacheca_html = html.fromstring(self.lastPageContent)
        bacheca = bacheca_html.xpath('//blockquote/a/@href')
        self.messageLink().execute("SELECT id FROM messages")
        present_id = [ str(i[0]) for i in self.c.fetchall() ]
        to_download = []
        for link in bacheca:
            add = False
            message_id = ""
            for char in link:
                if char == "=":
                    add = True
                if add and char != "=":
                    message_id += char
            if message_id not in present_id:
                to_download.append(message_id)
                print(message_id)
        if not to_download:
            print("All messages has already been downloaded")
        else:
            self.openMessages(to_download)

    def openMessage(self, m_id):
        self.lastPageContent = self.req_get(self.bacheca_url + m_id, auth="auth").content
        message_html = html.fromstring(self.lastPageContent)
        title = message_html.xpath('//font[@size="3"]/b/text()')[0].strip()
        sent_from = message_html.xpath('//font[@size="2"]/b/text()')[0].strip()
        valid_from = message_html.xpath('//font[@size="2"]/text()')[1].strip()
        valid_through = message_html.xpath('//font[@size="2"]/text()')[2].strip()
        message_content = " ".join(\
        [i.strip() for i in message_html.xpath('//tr//td[@bgcolor="#FFFFFF"][@colspan="2"]//text()')])

        self.messageLink().execute("INSERT INTO messages VALUES (?, ?, ?, ?, ?, ?)", (m_id, valid_from, valid_through, sent_from, title, message_content))

        notification_content = "Hai ricevuto un messaggio in bacheca da %s, intitolato %s, il contenuto e' il seguente:\n\n%s"\
        % (sent_from, title, message_content)

        self.notification_send(notification_content)

        self.conn.commit()

    def openMessages(self, ids):
        for i in ids:
            self.openMessage(i)

    def bacheca(self, database): #alias
        self.messaggiBacheca(database)

    def prenotazioni(self):
        url = self.url + self.f_url['prenotazioni']
        self.lastPageContent = self.req_get(url, auth="auth").content
        prenotazioni_html = html.fromstring(self.lastPageContent)
        exams = prenotazioni_html.xpath('//th[@class="detail_table"]//text()')
        if exams:
            print(exams)
        else:
            print("Non hai prenotazioni!")

    def calendario(self, day_only = False):
        if day_only:
            if day_only in ["oggi", "today"]:
                import datetime
                today = datetime.datetime.now()
                day_only = "%s/%s/%s" % (today.day, today.month, today.year)
#            elif day_only in ["domani", "tomorrow"]: ##There should be an import that does this

            print("Printing only date: %s" % day_only)
        url = self.url + self.f_url["redirect"]
        self.lastPageContent = self.req_get(url, auth="auth", params=self.redirect["orarioLezioni"]).content
        orari_html = html.fromstring(self.lastPageContent)
        if not self.corsi:
            self.getCorsi()
        orari_tmp_list = [ i for i in orari_html.xpath('//table[not(contains(@bgcolor, "#ffffff"))]//tbody/tr[@class="nero"]//td[1]//text()') if i.strip() ]
        dates = {}
        orari_list = []
        c = 0
        for i in orari_tmp_list:
            if "/" in i:
                dates[c] = i
                c -= 1 #update index! those that are removed.. are not in the list!
            else:
                orari_list.append(i)
            c += 1

        aule_list = [ i.strip() for i in orari_html.xpath('//table[not(contains(@bgcolor, "#ffffff"))]//td[2]//text()') if i.strip() ]
        lezioni_list = [ i.strip() for i in orari_html.xpath('//table[not(contains(@bgcolor, "#ffffff"))]//td[3]//text()') if i.strip() ]

        counter = 0
        for lezione in lezioni_list:
            if counter in dates:
                date = dates[counter]
            if lezione in self.corsi:
                index = counter * 2
                to_print = "%s %s %s %s %s" % (date, orari_list[counter], lezione, aule_list[index], aule_list[index + 1])
                if day_only == date or not day_only:
                    print(to_print)

            counter += 1

    def getCorsi(self):
        url = self.url + self.f_url["redirect"]
        self.lastPageContent = self.req_get(url, auth="auth", params = self.redirect["frequenze"]).content
        corsi_html = html.fromstring(self.lastPageContent)
        corsi = corsi_html.xpath('//select/option')
        self.corsi = [ i.text.strip() for i in corsi ]

    def notification_send(self, content):
        '''
            Needs a helper, defined in the config file. return that message to him
        '''
        if self.notification_helper:
            self.notification_helper(content)
        else:
            print("I should send %s but don't know how" % (content))
