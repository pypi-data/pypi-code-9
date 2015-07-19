from __future__ import absolute_import

import os, logging
import shutil, stat
import xml.etree.ElementTree as ET
import six

from marcodeployer import conf

skeldir = '/etc/skel/.'
def configure_tomcat(directory, uid):
    """
    Configures the local instance of Tomcat to work with a set of ports dedicated to the user.

    Tomcat uses the following ports:

    - 8080: The main port where services listen for connections. It is replaced by uid + 10000 
    - 8005: The shutdown port. It is replaced by uid + 20000

    :param str directory: The path of the Tomcat installation

    :param int uid: The uid of the user, which determines the number of the port
    """
    if not isinstance(uid, six.integer_types):
        error = None
        try:
            uid = int(uid, 10)
        except ValueError:
            error = True

        if error:
            raise Exception("Wrong uid value")

    server_xml = os.path.join(directory, 'conf/server.xml')
    logging.debug(server_xml)
    if not os.path.isfile(server_xml):
        raise Exception("Not found!")
    error = None
    
    try:
        tree = ET.parse(server_xml)
    except Exception:
        error = True
    if error:
        raise Exception("Error on parsing")

    root = tree.getroot()

    root.attrib["port"] = str(uid+conf.STOP_PORT_INCREMENT)

    ajp = root.find("./Service[@name='Catalina']/Connector[@protocol='AJP/1.3']")
    http = root.find("./Service[@name='Catalina']/Connector[@protocol='HTTP/1.1']")
    
    if http is None or ajp is None:
        raise Exception("Necessary tags elements not found in XML")
    
    http.attrib["port"] = str(uid)
    ajp.attrib["port"] = str(uid+conf.MAIN_PORT_INCREMENT)

    tree.write(server_xml)


def create_homedir(name, uid, gid):
    """
    Creates the home directory, setting the appropriate permissions
    
    :param str name: The path of the directory

    :param int uid: The uid of the owner

    :param int gid: The gid of the owner's main group
    """
    if os.path.exists(name):
        logging.info("The directory %s already exists.", name)
        return 1

    try:
        shutil.copytree(skeldir, name)
    except OSError as e:
        logging.error("Directory not copied. Error %s" % e)
        return 2

    try:
        for root, dirs, files in os.walk(name):
            for d in dirs: os.chown(os.path.join(root, d), uid, gid)
            for f in files: os.chown(os.path.join(root, f), uid, gid)
    except Exception as e:
        logging.error("Something went wrong during chown. %s" % e)
        return 2

    try:
        os.chown(name, uid, gid)
    except OSError as e:
        logging.error("Ownership could not be set: %s", e)
        return 2

    try:
        os.chmod(name, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH)
    except OSError as e:
        logging.error("Permission could not be set: %s", e)
        return 0

    if os.path.exists(os.path.join(name, 'apache-tomcat-7.0.62')):
        logging.debug("I shall now configure Tomcat")
        try:
            configure_tomcat(os.path.join(name, 'apache-tomcat-7.0.62'), int(uid))
        except Exception as e:
            logging.debug(e)
        
    return 0

