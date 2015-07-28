from gurl import Gurl

options = {'url': "http://google.com",
               'file': "/Users/scraig/Desktop/temp.download",
               'follow_redirects': False,
               'can_resume': False,
               'additional_headers': {},
               'download_only_if_changed': False,
               'cache_data': None,
               'logging_function': None}
    #munkicommon.display_debug2('Options: %s' % options)

connection = Gurl.alloc().initWithOptions_(options)
stored_percent_complete = -1
stored_bytes_received = 0
connection.start()
try:
    while True:
        # if we did `while not connection.isDone()` we'd miss printing
        # messages and displaying percentages if we exit the loop first
        connection_done = connection.isDone()
        if message and connection.status and connection.status != 304:
            # log always, display if verbose is 1 or more
            # also display in MunkiStatus detail field
            #munkicommon.display_status_minor(message)
            print message
            # now clear message so we don't display it again
            message = None
        if (str(connection.status).startswith('2')
            and connection.percentComplete != -1):
            if connection.percentComplete != stored_percent_complete:
                # display percent done if it has changed
                stored_percent_complete = connection.percentComplete
                #munkicommon.display_percent_done(
                #                            stored_percent_complete, 100)
                print stored_percent_complete
        elif connection.bytesReceived != stored_bytes_received:
            # if we don't have percent done info, log bytes received
            stored_bytes_received = connection.bytesReceived
            #munkicommon.display_detail(
            #    'Bytes received: %s', stored_bytes_received)
        if connection_done:
            break
except (KeyboardInterrupt, SystemExit):
    # safely kill the connection then re-raise
    connection.cancel()
    raise
except Exception, err: # too general, I know
    # Let us out! ... Safely! Unexpectedly quit dialogs are annoying...
    connection.cancel()
    # Re-raise the error as a GurlError
    #raise GurlError(-1, str(err))
    #raise Exception(-1, str(err))
    print "Exception"