# -*- coding: utf-8 -*-


""" Modulo para requisiçoes HTTP """


import requests
import logging
import datetime

from retrying import retry


logging.basicConfig(filename='logs_de_rede.log', level=logging.ERROR)


def retry_se_timeout(exception):
    return exception == "Timeout!"


@retry(retry_on_result=retry_se_timeout, stop_max_attempt_number=2, wait_fixed=2000)
def requisicao(url):
    try:
        pagina = requests.get(url, timeout=5)
        pagina.raise_for_status()
        pagina_texto = pagina.text
        return pagina_texto
    
    except requests.exceptions.ConnectionError as e:
        logging.error("Connection Error exception com o link: {0} - {1} ".format(url, datetime.datetime.now()))
        
    except requests.exceptions.Timeout as e:
        logging.error("Timeout exception com o link: {0} - {1} ".format(url, datetime.datetime.now()))
        return "Timeout!"
        
    except requests.exceptions.HTTPError as e:
        logging.error("HTTPError: {0}, URL: {1} - {2}".format(e.message, url, datetime.datetime.now()))


