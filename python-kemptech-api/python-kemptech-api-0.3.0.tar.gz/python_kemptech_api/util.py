import xmltodict


class ApiXmlHelper(object):
    """Encapsulate the awful XML response and provide helpful functions."""
    @classmethod
    def get_success_msg(cls, xml):
        return cls._get_xml_field(xml, "Success")

    @classmethod
    def get_error_msg(cls, xml):
        return cls._get_xml_field(xml, "Error")

    @classmethod
    def is_successful(cls, xml):
        """Return True if xml response contains a success, else false."""
        if ApiXmlHelper.get_success_msg(xml):
            return True
        else:
            return False

    @classmethod
    def get_data_field(cls, xml, field):
        return cls._get_xml_field(xml, "Data", data_field=field)

    @classmethod
    def parse_to_dict(cls, xml):
        """Return the XML as an OrderedDict."""
        return xmltodict.parse(xml)

    @classmethod
    def _get_xml_field(cls, xml, field, data_field=None):
        xml_dict = xmltodict.parse(xml)
        try:
            if data_field is None:
                msg = xml_dict.get("Response").get(field)
            else:
                data = xml_dict.get("Response").get("Success").get(field)
                msg = data.get(data_field)
        except KeyError:
            return False
        return msg
