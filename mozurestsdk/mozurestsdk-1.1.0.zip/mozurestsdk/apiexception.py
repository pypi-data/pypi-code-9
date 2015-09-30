class ApiException(BaseException):
	correlationId = None;
	message = None;
	errorCode = None;
	exceptionDetail = None;
	items = None;
	AdditionalErrorData = None;
	statusCode = None;
	