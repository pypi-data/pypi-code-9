import xml.etree.ElementTree as XML
import logging

logger = logging.getLogger(__name__)


def set_build_result(parser, xml_parent, data):
    t = XML.SubElement(
            xml_parent,
            'org.jenkins_ci.plugins.fail_the_build.FixResultBuilder')
    XML.SubElement(t, 'defaultResultName').text = data.upper()
