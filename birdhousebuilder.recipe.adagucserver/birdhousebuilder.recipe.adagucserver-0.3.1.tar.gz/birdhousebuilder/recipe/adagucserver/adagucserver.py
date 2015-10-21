import os

def parse_output(output):
    lines = output.split('\n')
    content_type = "text/xml"
    data = '\n'.join(lines)
    for i,line in enumerate(lines):
        if 'Content-Type' in line:
            content_type = line.split(':')[1]
            content_type = content_type.strip()
            start_line = i+1
            break
    for i,line in enumerate(lines):
        if line.startswith('<?xml'):
            data = '\n'.join(lines[i:-1])
    return content_type,data

def app(environ, start_response):
    from subprocess import check_output, STDOUT
    data = None
    try:
        # fake cgi parameters
        """
        QUERY_STRING       
        REQUEST_METHOD     
        CONTENT_TYPE       
        CONTENT_LENGTH     

        SCRIPT_FILENAME 
        SCRIPT_NAME     
        REQUEST_URI        
        DOCUMENT_URI       
        DOCUMENT_ROOT      
        SERVER_PROTOCOL    

        GATEWAY_INTERFACE  CGI/1.1;
        SERVER_SOFTWARE    

        REMOTE_ADDR        
        REMOTE_PORT        
        SERVER_ADDR        
        SERVER_PORT        
        SERVER_NAME        
        """
        params = [
            'QUERY_STRING',
            'REQUEST_METHOD',
            'SERVER_PROTOCOL',
            'SERVER_SOFTWARE',
            'REMOTE_ADDR',
            'SERVER_PORT',
            'SERVER_NAME'
            ]
        
        for param in params:
            os.environ[param] = environ[param]
        os.environ['GATEWAY_INTERFACE'] = 'CGI/1.1'

        # adaguc parameters
        output = check_output(['adagucserver'], stderr=STDOUT)
        content_type, data = parse_output(output)
        #raise Exception(str(data))
        start_response("200 OK", [
            ("Content-Type", content_type),
            #("Content-Length", str(len(data)))
            ])
    except Exception as e:
        data = "Message:<br/>"
        data += e.message

        # TODO: returncode 143 = application was killed
            
        start_response("200 OK", [
            ("Content-Type", "text/html"),
            ("Content-Length", str(len(data)))
            ])
    return iter([data])
