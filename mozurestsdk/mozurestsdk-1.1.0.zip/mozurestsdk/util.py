import logging
from mozurestsdk.headers import Headers;
from mozurestsdk.apiexception import ApiException;
from mozurestsdk.version import __apiversion__
import json;
import requests;
import datetime;
import platform;
import configparser;

def readConfigFile(configFile):
	if (configFile is None):
		return None;
	config = configparser.ConfigParser();
	config.optionxform=str
	config.read(configFile);
	logging.info("Getting values from configFile : %s" % configFile);
	return configSectionToDict(config, "MozuConfig");

def merge_dict(data, *override):
    result = {}
    for current_dict in (data,) + override:
        result.update(current_dict)
    return result

def configSectionToDict(config, section):
	options = config.options(section);
	configDict = {};
	for option in options:
		try:
			value = config.get(section, option);
			configDict[option] = value;
		except:
			configDict[option] = None
	return configDict;

def validateResponse(response):
	status = response.status_code;
	correlationId = response.headers.get(Headers.X_VOL_CORRELATION);
	if ( (200 <= status <= 299) ):
		return response;

	if (status == 404 and correlationId is not None):
		return None;
	
	
	apiException = ApiException();
	apiException.correlationId = correlationId;
	apiException.statusCode = status;

	if (response.text is not ''):
		content =  response.json();
		apiException.message = content["message"];
		apiException.errorCode = content["errorCode"];
		apiException.items = content["items"];
		apiException.AdditionalErrorData = content["additionalErrorData"];
	else:
		apiException.message = response.reason;
	raise apiException;

def getUserAgent():
	library_details = "requests %s; python %s" % (requests.__version__, platform.python_version());
	return "MozuRestSDK (%s)" %  library_details;

def http_call(url, method, **args):
	"""Makes a http call. Logs response information."""
	logging.info('Request[%s]: %s' % (method, url))
	start_time = datetime.datetime.now()
	
	args["headers"]["User-Agent"] = getUserAgent();	
	args["headers"][Headers.X_VOL_VERSION] = __apiversion__;
	args["stream"] = False;
	if (args["verify"]):
		del args["verify"];
	response = requests.request(method, url, **args)

	duration = datetime.datetime.now() - start_time
	logging.info('Request[%s], Url[%s], Response[%s]: %s, Duration: %s.%ss.' % (method, url, response.status_code, response.reason, duration.seconds, duration.microseconds))
	correlationId = response.headers.get(Headers.X_VOL_CORRELATION);
	if correlationId:
		logging.debug('Request[%s], Url[%s],correlationId: %s' % (method, url, correlationId));
	return validateResponse(response);

def mergeProperties(obj1, obj2):
	for property in obj1.__dict__:
		if (not callable(obj1.__dict__[property])):
			value = getattr(obj1,property);
			if (value is not None):
				setattr(obj2, property, value);
	return obj2;